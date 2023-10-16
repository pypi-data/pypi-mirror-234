"""This script defines the function create_gcloud_vm_docker_template()"""

import pathlib
from typing import List


# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=duplicate-code
def create_gcloud_vm_docker_template(
    target_dir: str,
    base_docker_image: str,
    package_dependencies: List[str],
    gcloud_artifact_registry_domain: str,
    gcloud_project_name: str,
    gcloud_repository_id: str,
    docker_image_name: str,
    install_chrome_browser_on_container: bool = False,
    install_gcloud_sdk_on_container: bool = False,
) -> None:
    """Creates a folder containing the files necessary to quickly build a python docker container
    to run on a google cloud Virtual Machine\n
    The following structure is created in the target directory:
    /target_dir/
        Dockerfile
        gcloud_utils.py
        main.py
        requirements.txt\n
    The command-line commands for building and pushing the docker container to google cloud are
    stored as comments in the Dockerfile itself\n
    Parameters
    ----------
    target_dir : str
        The path to the local directory in which the folder (and contents) should be created
    base_docker_image : str
        The base image to use for the docker container (e.g. "python:3.11-slim")
    package_dependencies : List[str]
        A list of the package dependencies (these are written to requirements.txt)
    gcloud_artifact_registry_domain : str
        The domain of the google cloud artifact registry (e.g. "europe-west2")
    gcloud_project_name : str
        The name of the google cloud project in which the docker image will be stored
    gcloud_repository_id : str
        The name of the google cloud artifact repository in which the docker image will be stored
        (must already exist)
    docker_image_name : str
        The desired name for the docker image
    install_chrome_browser_on_container : bool, (Default=False)
        Whether to install the latest google chrome browser in the docker container or not
        e.g. for running Selenium on the container
        (this code is added to the Dockerfile)
    install_gcloud_sdk_on_container: bool, (Default=False)
        Whether to install the google cloud Software Development Kit (SDK) in the docker
        container or not
        (this code is added to the Dockerfile)\n
    Example Usage
    -------------
    >>> import joes_giant_toolbox.google_cloud
    >>> joes_giant_toolbox.google_cloud.create_gcloud_vm_docker_template(
    ...     target_dir="/Users/josephbolton/Documents/temp/docker_test/",
    ...     base_docker_image="python:3.11-slim",
    ...     package_dependencies=["numpy==1.24.1","tqdm"],
    ...     gcloud_artifact_registry_domain="europe-west2",
    ...     gcloud_project_name="my-project-name",
    ...     gcloud_repository_id="my-docker-repo-name",
    ...     docker_image_name="my-docker-image-name",
    ...     install_chrome_browser_on_container=True,
    ...     install_gcloud_sdk_on_container=True,
    ... )
    >>> os.listdir("/Users/josephbolton/Documents/temp/docker_test/")
    ['requirements.txt', 'Dockerfile', 'main.py', 'gcloud_utils.py']
    """
    # create target directory if it does not exist #
    target_path: pathlib.Path = pathlib.Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True)
    # pylint: disable=line-too-long
    if install_chrome_browser_on_container:
        install_chrome_browser_code = """
# install google chrome #
RUN apt-get -y update
RUN apt install -y wget
RUN apt install -y curl
RUN apt install -y gnupg
RUN apt install -y unzip
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver #
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/"""
    else:
        install_chrome_browser_code = ""

    if install_gcloud_sdk_on_container:
        install_gcloud_sdk_code = """
# set up gcloud CLI (SDK) in the container #
RUN apt-get update
RUN apt-get -y install curl
RUN curl -sSL https://sdk.cloud.google.com > /tmp/gcl && bash /tmp/gcl --install-dir=~/gcloud --disable-prompts
ENV PATH $PATH:/root/gcloud/google-cloud-sdk/bin
"""
    else:
        install_gcloud_sdk_code = ""

    # create files in target directory #
    with open(f"{target_dir}/main.py", "w", encoding="utf-8") as file:
        file.write(
            """
# initial setup #
import requests
import gcloud_utils\n
# fetch the name of this Virtual Machine from the google metadata server #
# (useful to include in logging messages)
SELF_VM_NAME: str = requests.get(
    "http://metadata.google.internal/computeMetadata/v1/instance/name",
    headers={"Metadata-Flavor": "Google"},
    timeout=10,
).text\n
# set up google cloud logging #
import logging
import google.cloud.logging
logging_client = google.cloud.logging.Client()
logging_client.setup_logging()\n
logging.info("this message will appear in google cloud logging (VM='{}')".format(SELF_VM_NAME))\n
# write your python code here #\n
# Virtual Machine deletes itself #
try:
    gcloud_utils.gcloud_vm_deletes_itself()
except:
    logging.warning("Virtual Machine '{}' failed to delete itself".format(SELF_VM_NAME))
"""
        )

    with open(f"{target_dir}/requirements.txt", "w", encoding="utf-8") as file:
        for pkg in package_dependencies + [
            "requests",
            "google-cloud-compute",
            "google-cloud-logging",
        ]:
            file.write(pkg + "\n")

    with open(f"{target_dir}/Dockerfile", "w", encoding="utf-8") as file:
        file.write(
            f"""
# gcloud auth configure-docker {gcloud_artifact_registry_domain}-docker.pkg.dev
# cd {target_dir}
# docker buildx build --platform linux/amd64 --tag {gcloud_artifact_registry_domain}-docker.pkg.dev/{gcloud_project_name}/{gcloud_repository_id}/{docker_image_name} .
# docker push {gcloud_artifact_registry_domain}-docker.pkg.dev/{gcloud_project_name}/{gcloud_repository_id}/{docker_image_name}\n
FROM {base_docker_image}\n
# copy all code in folder to the container #
WORKDIR /{target_path.parts[-1]}
COPY . ./\n
# install packages #
RUN pip install --no-cache-dir -r requirements.txt\n
{install_chrome_browser_code}
{install_gcloud_sdk_code}
# execute python script #
CMD ["python","main.py"]
"""
        )
    with open(f"{target_dir}/gcloud_utils.py", "w", encoding="utf-8") as file:
        file.write(
            """
import sys
from typing import Any
import google.api_core.extended_operation
import google.cloud.compute_v1
import requests\n
def wait_for_extended_operation(
    operation: google.api_core.extended_operation.ExtendedOperation,
    verbose_name: str = "operation",
    timeout: int = 300,
) -> Any:
    \"\"\"
    This method will wait for the extended (long-running) operation to
    complete. If the operation is successful, it will return its result.
    If the operation ends with an error, an exception will be raised.
    If there were any warnings during the execution of the operation
    they will be printed to sys.stderr.

    Notes:
        This code is taken straight from the google cloud documentation:
        https://cloud.google.com/compute/docs/instances/stop-start-instance#python

    Args:
        operation: a long-running operation you want to wait on.
        verbose_name: (optional) a more verbose name of the operation,
            used only during error and warning reporting.
        timeout: how long (in seconds) to wait for operation to finish.
            If None, wait indefinitely.

    Returns:
        Whatever the operation.result() returns.

    Raises:
        This method will raise the exception received from `operation.exception()`
        or RuntimeError if there is no exception set, but there is an `error_code`
        set for the `operation`.

        In case of an operation taking longer than `timeout` seconds to complete,
        a `concurrent.futures.TimeoutError` will be raised.
    \"\"\"
    result = operation.result(timeout=timeout)\n
    if operation.error_code:
        print(
            f"Error during {verbose_name}: [Code: {operation.error_code}]: {operation.error_message}",
            file=sys.stderr,
            flush=True,
        )
        print(f"Operation ID: {operation.name}", file=sys.stderr, flush=True)
        raise operation.exception() or RuntimeError(operation.error_message)\n
    if operation.warnings:
        print(f"Warnings during {verbose_name}:\\n", file=sys.stderr, flush=True)
        for warning in operation.warnings:
            print(f" - {warning.code}: {warning.message}", file=sys.stderr, flush=True)\n
    return result\n

def gcloud_vm_deletes_itself() -> None:
    \"\"\"Running this function on a google cloud Virtual Machine (VM) causes the VM to delete itself\"\"\"
    instance_client = google.cloud.compute_v1.InstancesClient()

    # fetch Virtual Machine information from the metadata server #
    metadata_server_headers: dict = {
        "Metadata-Flavor": "Google",
    }
    gcp_project_name: str = requests.get(
        "http://metadata.google.internal/computeMetadata/v1/project/project-id",
        headers=metadata_server_headers,
        timeout=10,
    ).text
    vm_name: str = requests.get(
        "http://metadata.google.internal/computeMetadata/v1/instance/name",
        headers=metadata_server_headers,
        timeout=10,
    ).text
    vm_zone: str = requests.get(
        "http://metadata.google.internal/computeMetadata/v1/instance/zone",
        headers=metadata_server_headers,
        timeout=10,
    ).text.split("/")[-1]

    # Delete the Virtual Machine #
    operation = instance_client.delete(
        project=gcp_project_name, zone=vm_zone, instance=vm_name
    )
    wait_for_extended_operation(operation, "instance deletion")

"""
        )


# pylint: enable=line-too-long
