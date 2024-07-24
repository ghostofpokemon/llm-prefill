import click
import llm
from pathlib import Path
import os

PREFILLS_DIR = Path(os.environ.get("LLM_PREFILLS_DIR", Path.home() / ".llm" / "prefills"))

@llm.hookimpl
def register_commands(cli):
    @cli.group()
    def prefill():
        "Manage prefill templates"

    @prefill.command(name="add")
    @click.argument("name")
    @click.argument("content", required=False)
    @click.option("-f", "--file", type=click.Path(exists=True, dir_okay=False))
    def add_prefill(name, content, file):
        "Add a new prefill template"
        if file:
            with open(file, 'r') as f:
                content = f.read()
        elif not content:
            content = click.edit()

        if not content:
            raise click.ClickException("No content provided")

        path = PREFILLS_DIR / f"{name}.txt"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        click.echo(f"Prefill '{name}' added successfully")

    @prefill.command(name="list")
    def list_prefills():
        "List all available prefill templates"
        for path in PREFILLS_DIR.glob("*.txt"):
            click.echo(path.stem)

    @prefill.command(name="remove")
    @click.argument("name")
    def remove_prefill(name):
        "Remove a prefill template"
        path = PREFILLS_DIR / f"{name}.txt"
        if path.exists():
            path.unlink()
            click.echo(f"Prefill '{name}' removed successfully")
        else:
            click.echo(f"Prefill '{name}' not found")

@llm.hookimpl
def register_options(extra_options):
    extra_options.append(
        click.option("--prefill", help="Name of the prefill to use")
    )

@llm.hookimpl
def process_options(options):
    if options.get("prefill"):
        prefill_name = options["prefill"]
        prefill_path = PREFILLS_DIR / f"{prefill_name}.txt"
        if not prefill_path.exists():
            raise click.ClickException(f"Prefill '{prefill_name}' not found")
        prefill_content = prefill_path.read_text()
        # Modify the prompt or options to include the prefill
        # This part depends on how you want to integrate the prefill with the existing prompt
        # For example:
        if 'prompt' in options:
            options['prompt'] = prefill_content + "\n" + options['prompt']
        else:
            options['prompt'] = prefill_content
    return options
