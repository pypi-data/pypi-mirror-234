import re
from string import capwords
from typing import Optional

import typer
from rich.table import Table

from predibase.cli_commands.utils import get_client, get_console, get_repo

app = typer.Typer(no_args_is_help=True)

KEYS = [
    "name",
    "description",
    "modelName",
    "numShards",
    "quantize",
    "deploymentStatus",
    "promptTemplate",
    "created",
    "updated",
    "scaleDownPeriod",
    "engine",
    "errorText",
]


@app.command(help="List existing Large Langage Model (LLM) deployments")
def llms(
    all_llms: bool = typer.Option(False, "--all", "-a", help="List all LLMs, including those not yet deployed/failed"),
):
    client = get_client()
    if all_llms:
        llms = client.list_all_llms()
    else:
        llms = client.list_deployed_llms()
    camelCaseToTitle = lambda s: capwords(re.sub(r"((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))", r" \1", s).strip())
    table = Table(*[camelCaseToTitle(k) for k in KEYS])
    get_console().print(f"Found {len(llms)} LLMs:")
    prompt_templates = [llm["promptTemplate"].replace("[", r"\[") for llm in llms]
    llms = [dict(llm, promptTemplate=prompt_templates[i]) for i, llm in enumerate(llms)]
    for llm in llms:
        table.add_row(*[str(llm[k]) for k in KEYS])
    get_console().print(table)


@app.command(help="List existing models for a given repository")
def models(repo: Optional[str] = None):
    repo = get_repo(repo)
    table = Table("Version", "Description", "UUID")
    for model in repo.list_models():
        table.add_row(str(model.version), model.description, model.uuid)
    get_console().print(table)


@app.command(help="List existing repositories")
def repos():
    table = Table("Name", "UUID")
    repos = get_client().list_model_repos()
    for repo in repos:
        table.add_row(repo.name, repo.uuid)
    get_console().print(table)


if __name__ == "__main__":
    app()
