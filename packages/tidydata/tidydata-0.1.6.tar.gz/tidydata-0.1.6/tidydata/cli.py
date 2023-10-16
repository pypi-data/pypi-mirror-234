import click
import shutil
from pathlib import Path
from tidydata.config import Config  # Assumption that you have a Config class in config module of your package
from tidydata.core import TidySource, TidyExport
import os

@click.group()
def tidydata():
    pass

@tidydata.command()
@click.argument('name')
def new(name):
    """Creates a new project with the given name."""
    base_dir = Path(name)
    base_dir.mkdir(parents=True, exist_ok=True)
    (base_dir / ".data/raw").mkdir(parents=True, exist_ok=True)
    (base_dir / ".data/preload").mkdir(parents=True, exist_ok=True)

    yaml_file = base_dir / "data.yaml"
    with yaml_file.open("w") as f:
        f.write("sources:")

@tidydata.command()
@click.argument('name')
def remove(name):
    """Removes an existing project with the given name."""
    base_dir = Path(name)
    if base_dir.exists():
        shutil.rmtree(base_dir)
    else:
        click.echo(f"The project '{name}' does not exist.")

@tidydata.command()
@click.option('-f', '--from-yaml', default='data.yaml', help='Name of the YAML file to process.')
@click.option('-t','--to-dir', default=None, help='Specify the export directory.')
@click.option('-p','--project-dir', default=None, help='Specify the project working directory.')
def run(from_yaml, to_dir, project_dir):
    """Processes the specified YAML file and creates a Config object from it."""
    
    original_dir = os.getcwd()  # Save the original working directory

    # If a project directory is specified, change to it
    if project_dir:
        os.chdir(project_dir)

    yaml_file = Path(from_yaml)
    if not yaml_file.exists():
        click.echo(f"The file '{from_yaml}' does not exist in the current directory.")
    else:
        config = Config.from_yaml(yaml_file)
        TidySource(config)
        TidyExport(config, export_dir=to_dir)
        click.echo(f"Data in '{from_yaml}' was successfully cleaned, and are saved to {to_dir}")

    os.chdir(original_dir)  



if __name__ == "__main__":
    tidydata()
