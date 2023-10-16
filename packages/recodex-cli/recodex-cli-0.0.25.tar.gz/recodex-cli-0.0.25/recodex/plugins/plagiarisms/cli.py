import sys
import click
import json
from ruamel import yaml

from recodex.api import ApiClient
from recodex.decorators import pass_api_client


@click.group()
def cli():
    """
    API related to plagiarism detection and suspected solution similarities
    """


@cli.command()
@click.argument("tool")
@click.argument("tool_params")
@pass_api_client
def create_batch(api: ApiClient, tool, tool_params):
    """
    Create a new plagiarism detection batch
    """
    batch = api.create_plagiarism_batch(tool, tool_params)
    click.echo(batch["id"])


@cli.command()
@click.argument("id")
@click.option("--upload-completed/--upload-reopen", "completed", default=True)
@pass_api_client
def update_batch(api: ApiClient, id, completed):
    """
    Update a plagiarism detection batch (whether its upload has been completed)
    """
    api.update_plagiarism_batch(id, completed)


@cli.command()
@click.argument("id")
@click.argument("solution_id")
@click.option("--json/--yaml", "useJson", default=True)
@pass_api_client
def add_similarity(api: ApiClient, id, solution_id, useJson):
    """
    Add detected similarity record to open plagiarism detection batch
    """

    if useJson:
        data = json.load(sys.stdin)
    else:
        data = yaml.safe_load(sys.stdin)
    print(data)
    api.add_plagiarism_detected_similarity(id, solution_id, data)
