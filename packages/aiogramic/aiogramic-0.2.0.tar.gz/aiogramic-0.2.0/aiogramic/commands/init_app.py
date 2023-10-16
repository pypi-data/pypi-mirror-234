import click

from os.path import join
from os.path import dirname
from os.path import abspath

import shutil


@click.command("init-app")
@click.option("--path", default=".")
@click.option("--docker", is_flag=True)
def init_app(
        path: str,
        docker: bool
):
    source_path = join(dirname(__file__), "../templates/app")
    destination_path = abspath(path)

    print(destination_path)

    shutil.copytree(source_path, destination_path, dirs_exist_ok=True)

    if docker:
        docker_source_path = join(dirname(__file__), "../templates/docker")
        shutil.copytree(docker_source_path, destination_path, dirs_exist_ok=True)
