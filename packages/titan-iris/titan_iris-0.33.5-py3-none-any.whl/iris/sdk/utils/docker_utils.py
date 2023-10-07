"""This file contains the docker related helper functions for the Iris package."""
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

import io
import tarfile
import os
from logging import getLogger

import docker
import shortuuid
from docker.errors import DockerException
from typing import Optional
from rich import print as rprint
from rich.progress import Progress

from ..conf_manager import conf_mgr

logger = getLogger("iris.utils.docker_utils")

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                     Docker Utils                                                     #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


def copy_local_folder_to_image(container, local_folder_path: str, image_folder_path: str) -> None:
    """Helper function to copy a local folder into a container."""
    tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode="w") as tar:
        tar.add(local_folder_path, arcname=".")
    tar_buffer.seek(0)

    # Copy the tar archive into the container
    container.put_archive(image_folder_path, tar_buffer)


def show_progress(line, progress, tasks):  # sourcery skip: avoid-builtin-shadow
    """Show task progress for docker pull command (red for download, green for extract)."""
    if line["status"] == "Downloading":
        id = f'[red][Download {line["id"]}]'
    elif line["status"] == "Extracting":
        id = f'[green][Extract  {line["id"]}]'
    else:
        # skip other statuses
        return

    if id not in tasks.keys():
        tasks[id] = progress.add_task(f"{id}", total=line["progressDetail"]["total"])
    else:
        progress.update(tasks[id], completed=line["progressDetail"]["current"])


def get_takeoff_image_name():
    """Get the image name for the takeoff container."""
    base_image = conf_mgr.FABULINUS_IMAGE.split(":")[0]
    image_tag = "latest"

    # allow the env var to override the configured image name
    image_name = os.environ.get("FABULINUS_IMAGE", base_image + ":" + image_tag)
    return image_name


def pull_fastapi_image(
    image_name: str,
    model_folder_path: str,
    device: str = "cpu",
    port: int = 8000,
    quant: Optional[str] = "int8",
    json_output: bool = False,
    extra_env_vars: Optional[dict] = None,
):
    """Pull the fastapi image from docker hub and run it, mounting the model folder.

    Args:
        image_name (str): image name to pull
        model_folder_path (str): path to the model folder
        device (str, optional): device to run the model on. Defaults to "cpu".
        port (int, optional): port to run the model on. Defaults to 8000.
        quant (Optional[str], optional): quantization type. Defaults to "int8".
        json_output (bool, optional): output to json or not. Defaults to False.
        extra_env_vars (dict[str, str], optional): extra environment variables to pass to the container.
            Defaults to None.
    """
    tasks = {}
    with Progress() as progress:
        # docker pull the base image
        client = docker.from_env()
        resp = client.api.pull(image_name, stream=True, decode=True)
        for line in resp:
            if not json_output:
                show_progress(line, progress, tasks)

    env_vars = {"TAKEOFF_MODEL_NAME": model_folder_path, "TAKEOFF_DEVICE": device, "TAKEOFF_QUANT_TYPE": quant}
    env_vars.update(extra_env_vars if extra_env_vars else {})

    cached_folder = conf_mgr.cache_dir
    # Define your volume bindings
    volume_bindings = {
        f"{cached_folder}": {
            "bind": "/code/models",
            "mode": "rw",
        },
    }
    port_bindings = {
        80: port,
    }

    device_requests = [docker.types.DeviceRequest(count=-1, capabilities=[["gpu"]])] if device == "cuda" else None
    container_name = model_folder_path.split("/")[-1] + f"-{shortuuid.uuid()}-takeoff"
    print(f"Starting takeoff server {container_name}...")
    # Run a container with the volume mounted and ports forwarded
    client.containers.run(
        image_name,
        volumes=volume_bindings,
        ports=port_bindings,
        environment=env_vars,
        device_requests=device_requests,
        detach=True,
        tty=True,
        stdin_open=True,
        name=container_name,
    )
    rprint(f"Takeoff Server [bright_cyan]{container_name} [/bright_cyan]started.")
    rprint("The server might take a few minutes to start while it optimizes your model.")
    rprint("You can check the progress of the optimization process by running:")
    rprint(f"\n[bright_red]docker logs {container_name} -f[/bright_red]\n")
    rprint(f"Once the server is ready, you can view the API docs at: http://localhost:{port}/docs")
    rprint(
        f"For interactive demos, navigate to http://localhost:{port}/demos/chat, or http://localhost:{port}/demos/playground"
    )


def pull_image(
    model_folder_path: str,
    container_name: str,
    job_tag: str,
    task_name: str,
    baseline_model_name: str,
    baseline: bool,
    json_output: bool = False,
):
    """Pull image.

    This function handles the logic of pulling the base image and creating a new image with
    the model files copied into it.

    Args:
        model_folder_path: The path to the model folder
        container_name: The name of the container
        job_tag: The tag of the job
        task_name: The name of the task
        baseline_model_name: The name of the baseline model
        baseline: Whether the model is the baseline model
        json_output: Whether to output the progress in json format

    """
    temp_container_name = f"temp-{container_name}"

    env_var = {
        "TASK_NAME": task_name,
        "BASELINE_MODEL_NAME": baseline_model_name,
        "BASELINE": str(baseline),
    }

    tasks = {}
    with Progress() as progress:
        # docker pull the base image
        client = docker.from_env()
        resp = client.api.pull(conf_mgr.HEPHAESTUS_IMAGE, stream=True, decode=True)
        for line in resp:
            if not json_output:
                show_progress(line, progress, tasks)

    # Create a new temp container
    container = client.containers.create(image=conf_mgr.HEPHAESTUS_IMAGE, name=temp_container_name, environment=env_var)

    copy_local_folder_to_image(container, model_folder_path, "/usr/local/triton/models/")

    # Commit the container to a new image
    container.commit(repository=container_name)

    client.images.get(container_name).tag(f"{container_name}:{job_tag}")

    # Remove the original tag
    client.images.remove(container_name)
    # Remove the temp container
    container.remove()


def list_running_servers():
    """List all running servers.

    Returns:
        list: a list of running servers.

    """
    client = docker.from_env()
    servers = [x for x in client.containers.list() if x.name.endswith("-takeoff")]
    return servers


def stop_and_remove_container(container_name):
    """Stop and remove a container.

    Args:
        container_name (str): the name of the container to stop and remove.
    """
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        container.stop()
        container.remove()
        print(f"Successfully stopped and removed container: {container_name}")
    except docker.errors.NotFound:
        print(f"Container: {container_name} not found")
    except docker.errors.APIError as e:
        print(f"Unexpected API error occurred: {e}")


def check_docker():
    """Check if docker is installed and running.

    Raises:
        EnvironmentError: _description_
    """
    try:
        client = docker.from_env()
        client.ping()
    except DockerException:
        raise EnvironmentError(
            "Docker is not installed or not running in this environment. Please install/start Docker."
        )
