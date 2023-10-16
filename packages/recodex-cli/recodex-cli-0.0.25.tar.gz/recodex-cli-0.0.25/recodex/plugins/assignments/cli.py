import click
import sys
import os
import datetime
import json
from ruamel import yaml

from recodex.api import ApiClient
from recodex.decorators import pass_api_client
from recodex.utils import asciiize_string


def safe_get_solution_points(solution):
    submission = solution["lastSubmission"]
    if submission is None:
        return -1
    evaluation = submission["evaluation"]
    if evaluation is None:
        return -1
    return evaluation["points"] + solution["bonusPoints"]


def getAssignmentName(assignment):
    if "localizedTexts" not in assignment or len(assignment["localizedTexts"]) == 0:
        # There is no "localizedTexts" key or empty array :(
        return "unknown"
    known_languages = ("en", "cs")
    # Try known languages (in given order)
    for lang in known_languages:
        for item in assignment["localizedTexts"]:
            if item["locale"] == lang:
                return item["name"]
    # Something weird happened, return first name we got
    return assignment["localizedTexts"][0]["name"]


@click.group()
def cli():
    """
    Tools for working with assignments (exercise instances)
    """


@cli.command()
@click.option("download_dir", "-d")
@click.argument("assignment_id")
@pass_api_client
def download_best_solutions(api: ApiClient, download_dir, assignment_id):
    """
    Download the best solution of this assignment from each user.
    """
    if download_dir is None:
        download_dir = "."
    if not os.path.exists(download_dir) or not os.path.isdir(download_dir):
        click.echo("Download path '{}' must exist and must be a directory.".format(download_dir))
        return

    # Get assignment metadata and best solution for each student ...
    assignment = api.get_assignment(assignment_id)
    if assignment is None:
        click.echo("Assignment not found.")
        return
    click.echo("Downloading best solutions of '{}' to '{}' ...".format(
        getAssignmentName(assignment), download_dir))
    best_solutions = api.get_assignment_best_solutions(assignment_id)

    # Iterate over students
    for student in api.get_group_students(assignment["groupId"]):
        # Try to find best solution for the student
        best = best_solutions[student["id"]]
        if best:
            # File name comprise user name in plain ASCII and its ID for uniqueness
            file_name = "{}-{}-{}.zip".format(
                asciiize_string(student["name"]["lastName"]),
                asciiize_string(student["name"]["firstName"]), student["id"])
            points = safe_get_solution_points(best)
            created = datetime.datetime.fromtimestamp(best["createdAt"]).strftime('%Y-%m-%d %H:%M:%S')
            click.echo("Saving {} ... {} points, {}".format(file_name, points, created))
            api.download_solution(best['id'], "{}/{}".format(download_dir, file_name))


@cli.command()
@click.argument("assignment_id")
@click.option("--json/--yaml", "useJson", default=None)
@pass_api_client
def get_solutions(api: ApiClient, assignment_id, useJson):
    """
    Get assignment solutions (including points, score, ...) of all users.
    """

    solutions = api.get_assignment_solutions(assignment_id)
    if useJson is True:
        json.dump(solutions, sys.stdout, sort_keys=True, indent=4)
    elif useJson is False:
        yaml.dump(solutions, sys.stdout)
    else:
        for solution in solutions:
            flags = []
            if (solution["accepted"]):
                flags.append("accepted")
            if (solution["isBestSolution"]):
                flags.append("best")
            points = solution["overriddenPoints"] if solution["overriddenPoints"] else solution["actualPoints"]
            click.echo("{} {} {}+{}/{} {}".format(solution["id"], solution["authorId"],
                       points, solution["bonusPoints"], solution["maxPoints"], ", ".join(flags)))
