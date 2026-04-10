import re
from pathlib import Path

import typer
import yaml
from jinja2 import Environment, PackageLoader, StrictUndefined

app = typer.Typer(help="Generate README.generated.md for an App Framework component.")

SCHEMA_FILE = "copier-module.yaml"
OUTPUT_FILE = "README.generated.md"
TEMPLATE_FILE = "README.md.jinja"


@app.command()
def generate(
    repo_path: Path = typer.Argument(
        Path("."),
        help="Path to the component repo (must contain copier-module.yaml).",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
) -> None:
    schema_path = repo_path / SCHEMA_FILE
    if not schema_path.exists():
        typer.echo(f"ERROR: {SCHEMA_FILE} not found in {repo_path}", err=True)
        raise typer.Exit(1)

    with schema_path.open() as fh:
        schema = yaml.safe_load(fh)

    schema.setdefault("depends_on", {})
    schema.setdefault("collaborates_with", {})
    schema.setdefault("repeatable", False)

    copier_path = repo_path / "copier.yml"
    answers_file = ""
    if copier_path.exists():
        with copier_path.open() as fh:
            copier_config = yaml.safe_load(fh)
        raw = copier_config.get("_answers_file", "")
        answers_file = re.sub(r"\{\{\s*(\w+)\s*\}\}", r"<\1>", raw)
    schema["answers_file"] = answers_file

    env = Environment(
        loader=PackageLoader("af_component_doc_update", "templates"),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(TEMPLATE_FILE)
    rendered = template.render(**schema)

    output_path = repo_path / OUTPUT_FILE
    output_path.write_text(rendered)
    typer.echo(f"Written: {output_path}")


if __name__ == "__main__":
    app()
