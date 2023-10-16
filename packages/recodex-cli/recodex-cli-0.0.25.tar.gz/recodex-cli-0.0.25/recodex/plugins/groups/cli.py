import json
from ruamel import yaml
import sys

import click

from recodex.api import ApiClient
from recodex.decorators import pass_api_client
from recodex.utils import get_localized_name


@click.group()
def cli():
    """
    Tools for groups manipulation
    """


@cli.command()
@click.option("--json/--yaml", "useJson", default=False)
@click.option("--archived", is_flag=True)
@pass_api_client
def all(api: ApiClient, useJson, archived):
    """
    Return all groups (visible to the user)
    """

    groups = api.get_all_groups(archived)
    if useJson is True:
        json.dump(groups, sys.stdout, sort_keys=True, indent=4)
    elif useJson is False:
        yaml.dump(groups, sys.stdout)


@cli.command()
@click.argument("group_id")
@click.option("--json/--yaml", "useJson", default=False)
@pass_api_client
def detail(api: ApiClient, group_id, useJson):
    """
    Read detailed data about given group
    """

    group = api.get_group(group_id)
    if useJson is True:
        json.dump(group, sys.stdout, sort_keys=True, indent=4)
    elif useJson is False:
        yaml.dump(group, sys.stdout)


@cli.command()
@click.argument("group_id")
@click.argument("user_id")
@pass_api_client
def join(api: ApiClient, group_id, user_id):
    """
    Add user as a member (student) of a group
    """

    api.group_add_student(group_id, user_id)


@cli.command()
@click.argument("group_id")
@click.argument("user_id")
@pass_api_client
def leave(api: ApiClient, group_id, user_id):
    """
    Remove user (student) from a group
    """

    api.group_remove_student(group_id, user_id)


@cli.command()
@click.argument("group_id")
@click.argument("exercise_id")
@pass_api_client
def attach(api: ApiClient, group_id, exercise_id):
    """
    Attach exercise to a group of residence
    """

    api.group_attach_exercise(group_id, exercise_id)


@cli.command()
@click.argument("group_id")
@click.argument("exercise_id")
@pass_api_client
def detach(api: ApiClient, group_id, exercise_id):
    """
    Detach exercise from a group of residence
    """

    api.group_detach_exercise(group_id, exercise_id)


@cli.command()
@click.argument("group_id")
@click.option("--json/--yaml", "useJson", default=None)
@pass_api_client
def students(api: ApiClient, group_id, useJson):
    """
    List all students of a group.
    """

    students = api.get_group_students(group_id)
    if useJson is True:
        json.dump(students, sys.stdout, sort_keys=True, indent=4)
    elif useJson is False:
        yaml.dump(students, sys.stdout)
    else:
        for student in students:
            click.echo("{} {}".format(student["id"], student["fullName"]))


@cli.command()
@click.argument("group_id")
@click.option("--json/--yaml", "useJson", default=None)
@pass_api_client
def assignments(api: ApiClient, group_id, useJson):
    """
    List all (regular) assignments of a group.
    """

    assignments = api.get_group_assignments(group_id)
    if useJson is True:
        json.dump(assignments, sys.stdout, sort_keys=True, indent=4)
    elif useJson is False:
        yaml.dump(assignments, sys.stdout)
    else:
        for assignment in assignments:
            click.echo("{} {}".format(assignment["id"], get_localized_name(assignment["localizedTexts"])))
