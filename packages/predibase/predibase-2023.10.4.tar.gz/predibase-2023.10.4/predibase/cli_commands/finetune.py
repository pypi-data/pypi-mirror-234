from typing import Optional

import typer

from predibase.cli_commands.utils import get_client

app = typer.Typer(no_args_is_help=True)


@app.command(help="Fine-tune a Large Language Model (LLM)")
def llm(
    base_model_name: str = typer.Option(
        None,
        "--base-model",
        "-b",
        prompt="Name of the base model to fine-tune",
        prompt_required=True,
        help="Name of the base model to fine-tune",
    ),
    repo_name: Optional[str] = typer.Option(
        None,
        "--repo-name",
        "-r",
        prompt="Name of the repo in which to save the new model",
        prompt_required=True,
        help="Name of the repo in which to save the new model",
    ),
    prompt_template: str = typer.Option(
        None,
        "--prompt-template",
        prompt="Template input",
        prompt_required=True,
        help="Prompt template input text",
    ),
    target: str = typer.Option(
        None,
        "--target",
        prompt="Fine-tuning target column",
        prompt_required=True,
        help="Fine-tuning target column",
    ),
    dataset_name: Optional[str] = typer.Option(
        None,
        "--dataset",
        "-d",
        prompt="Dataset to fine-tune on",
        prompt_required=True,
        help="Dataset to fine-tune on",
    ),
    template_name: str = typer.Option(
        None,
        "--template",
        prompt="Fine-tuning template to use",
        prompt_required=False,
        help="Fine-tuning template to use (optional)",
    ),
    wait: Optional[bool] = typer.Option(
        None,
        "--wait",
        prompt="Whether to wait until training finishes",
        prompt_required=False,
        help="If set, the deploy command will not return until the training process finishes",
    ),
):
    client = get_client()
    tmpls = client.LLM(base_model_name).get_finetune_templates()
    tmpl = tmpls.default
    if template_name:
        try:
            tmpl = tmpls[template_name]
        except KeyError:
            raise ValueError(f"provided template {template_name} does not exist") from None

    job = tmpl.run(
        prompt_template=prompt_template,
        target=target,
        dataset=dataset_name,
        repo=repo_name,
    )

    if wait:
        job.get()


@app.command(help="Get possible templates for fine-tuning a Large Language Model (LLM)")
def templates(
    base_model_name: str = typer.Option(
        None,
        "--base-model",
        "-b",
        prompt="Name of the base model to fine-tune",
        prompt_required=True,
        help="Name of the base model to fine-tune",
    ),
):
    client = get_client()
    tmpls = client.LLM(base_model_name).get_finetune_templates()
    tmpls.compare()


if __name__ == "__main__":
    app()
