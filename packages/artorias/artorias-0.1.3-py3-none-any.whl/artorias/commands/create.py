import shutil
import subprocess
from pathlib import Path
from string import Template

import typer

app = typer.Typer(name="create", help="Create project from template")
templates_dir = Path(__file__).parent.parent / "templates"


def create(framework: str, name: str, python: str):
    try:
        import pipenv
    except ImportError:
        print("You must install pipenv first!")
        exit(-1)

    framework_template_path = templates_dir / framework
    project_path = Path.cwd() / name

    print(f"Create directory {project_path}.", flush=True)
    if project_path.exists():
        print(f"Directory already exists: {project_path}.", flush=True)
        raise typer.Exit(-1)

    shutil.copytree(framework_template_path, project_path)
    shutil.move(project_path / "project", project_path / name)
    for path in project_path.glob("**/*.t"):
        path.write_text(Template(path.read_text()).substitute({"python_version": python, "project_name": name}))
        shutil.move(path, path.parent / path.name.rstrip(".t"))

    try:
        subprocess.run(["pipenv", "install", "--verbose", "--python", python], check=True, cwd=project_path)
        print("Pipenv packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running Pipenv install command: {e}")

    print("Done.")


@app.command(name="flask", help="Create flask project")
def create_flask(name: str, python: str = "3.9"):
    create("flask", name, python)


@app.command(name="fastapi", help="Create fastapi project")
def create_fastapi(name: str, python: str = "3.9"):
    create("fastapi", name, python)
