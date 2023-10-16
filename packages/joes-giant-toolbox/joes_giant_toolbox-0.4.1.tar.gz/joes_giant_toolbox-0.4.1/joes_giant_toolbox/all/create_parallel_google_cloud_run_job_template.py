"""This script defines the function create_parallel_google_cloud_run_job_template()"""

import pathlib
from typing import Any, Dict, List


# pylint: disable=too-many-arguments, too-many-locals
def create_parallel_google_cloud_run_job_template(
    cloud_run_job_name: str,
    target_dir: str,
    gcp_region: str,
    instruction_file_bucket_name: str,
    instruction_file_path: str,
    additional_imports_code: List[str],
    pre_task_code: List[str],
    task_code: List[str],
    cloud_run_job_params: Dict[str, Any],
    requirements_list: List[str],
) -> None:
    """Run a task in parallel using a Google Cloud Run job (code-generating function)\n
    This is a code-generating function.
    It generates all of the scripts necessary to build and run a google Cloud Run job,
        in a user-specified folder.
    After running this function, you can simply navigate to the code output folder and
        execute the bash script "create_cloud_run_job.sh" in order to start the Cloud Run job.
    The list of items to be processed by the Cloud Run job is read from a pre-existing text
        file stored in a google cloud bucket. Each line in this instruction file represents a
        single item to be processed.
    The full run is split into a user-specified number of batches (using the flag --tasks),
        where each batch sequentially processes (n_items/n_batches) items.
    The batches are run in parallel.\n
    For an end-to-end example, refer to "Example Usage" below.\n
    Parameters
    ----------
    cloud_run_job_name : str
        The desired name for the Cloud Run job on the google cloud platform
    target_dir : str
        A path (absolute or relative) to the folder in which code should be generated
    gcp_region : str
        The (gcloud) name of the region in which the Cloud Run job should be run
        e.g. gcp_region="europe-west2"
    instruction_file_bucket_name : str
        The name of the gcloud bucket containing the file which lists the items to process
        e.g. instruction_file_bucket_name="temp_bucket"
    instruction_file_path : str
        The path (on the gcloud bucket) to the file which lists the items to process
        e.g. instruction_file_path="process_control/cloud_run_job/items_to_process.txt"
    additional_imports_code : str
        This code is added to the "imports" code at the top of the python script main.py
        It is run once at the start of a batch
        The code is passed as a list, where each list element is 1 line of code
        This list may be empty
    pre_task_code : List[str]
        This code is added into the python script main.py
        It is run once at the start of a batch, appearing just above the task_code loop
        The code is passed as a list, where each list element is 1 line of code
        This list may be empty
    task_code : List[str]
        This code is added into the python script main.py
        This code runs once per item (i.e. it is the code used to process each item)
        This code uses the variable "item" (the line to be processed from the instruction file),
            and optionally the variable "item_idx" (the index of the item in the batch)
        The code is passed as a list, where each list element is 1 line of code
        Refer to a simple example in "Example Usage" below
    cloud_run_job_params : Dict[str, Any]
        Command line arguments passed to the gcloud cli command "gcloud beta run jobs create"
        These arguments control parameters/behaviour of the cloud run job (number of batches etc.)
        e.g. cloud_run_job_params={"--tasks": 100, "--task-timeout": "1m30s"}
        The only required argument is "--tasks" (the number of parallel batches to run)
    requirements_list : List[str]
        The list of python packages required by the [pre_task_code] and [task_code]
        These entries are written to readme.txt
        This list may be empty\n
    Example Usage
    -------------
    >>> import os
    >>> import random
    >>> import string
    >>> import subprocess
    >>> import joes_giant_toolbox.google_cloud
    >>> # create list of names to process (in parallel) using a Cloud Run job #
    >>> names_to_process: list = [
    ...    "".join(random.choices(string.ascii_lowercase, k=8)) for name in range(100_000)
    ... ]
    >>> names_to_process
    ['rhfdlmqq', 'hjogakjd', 'cfbhrhfj', ...]
    >>> # upload list of names to process to gcloud bucket #
    >>> joes_giant_toolbox.google_cloud.upload_file_python_to_gcloud_bucket(
    ...     contents_str = "\n".join(names_to_process),
    ...     bucket_name="cloud_run_jobs_test",
    ...     filename_on_bucket="names_to_process.txt",
    ...     file_type="text"
    ... )
    >>> code_output_dir: str = f"{pathlib.Path.home()}/Documents/temp/define_cloud_run_job/"
    >>> joes_giant_toolbox.google_cloud.create_parallel_google_cloud_run_job_template(
    ...     additional_imports_code=[
    ...         "import random",
    ...         "import time",
    ...         "import joes_giant_toolbox.google_cloud",
    ...     ],
    ...     pre_task_code=[],
    ...     task_code=[
    ...         "joes_giant_toolbox.google_cloud.upload_file_python_to_gcloud_bucket(",
    ...         '   contents_str=f"batch {BATCH_ID}, item {item_idx}",',
    ...         '   bucket_name="cloud_run_jobs_test",',
    ...         '   filename_on_bucket=f"completed_files/{item}.txt",',
    ...         '   file_type="text"',
    ...         ")",
    ...         "time.sleep( random.uniform(0.1,0.5) )",
    ...     ],
    ...     target_dir=code_output_dir,
    ...     gcp_region="europe-west2",
    ...     cloud_run_job_name="temp-once-off-job",
    ...     instruction_file_bucket_name="cloud_run_jobs_test",
    ...     instruction_file_path="names_to_process.txt",
    ...     requirements_list=[
    ...         "joes-giant-toolbox>=0.2.23",
    ...         "google-cloud-bigquery",
    ...         "google-cloud-storage",
    ...         "pandas",
    ...     ],
    ...     cloud_run_job_params={
    ...         "--tasks": 10,      # run process in 10 batches
    ...         "--max-retries": 3,
    ...         "--task-timeout": "5m30s",
    ...     },
    ... )
    # Navigate to directory in which Cloud Run code was
    >>> os.chdir(code_output_dir)
    # Run the bash script which creates and runs the Cloud Run job #
    >>> subprocess.run(["bash", "create_cloud_run_job.sh"], check=True)
    < process runs >
    """

    if "--tasks" not in cloud_run_job_params:
        raise ValueError('cloud_run_job_params must include argument "--tasks"')

    # create target directory if it does not exist #
    pathlib.Path(target_dir).mkdir(parents=True, exist_ok=True)

    # define contents of Procfile #
    procfile_contents: str = """
# Buildpacks require a web process to be defined
# but this process will not be used
web: echo "no web"
python: python
"""

    # define contents of requirements.txt
    requirements_txt_contents: str = ""
    for pkg in requirements_list + [
        "click",
        "google-auth",
        "google-cloud-logging",
        "google-cloud-storage",
    ]:
        requirements_txt_contents += f"{pkg}\n"

    # define contents of python script main.py #
    main_py_contents: str = f"""
import logging
import math
import os
import time\n
from typing import Final
import click
import google.auth
import google.cloud.logging
import google.cloud.storage\n
# user-specified additional imports --------------------------------------- #
{chr(10).join(additional_imports_code)}
# ------------------------------------------------------------------------- #\n
# connect to google cloud logging and storage services #
gcp_logging_client = google.cloud.logging.Client()
gcp_storage_client = google.cloud.storage.Client()\n
_, PROJECT_ID = google.auth.default()
BATCH_ID: Final = int(os.environ.get("CLOUD_RUN_TASK_INDEX", 0))
N_BATCHES: Final = int(os.environ.get("CLOUD_RUN_TASK_COUNT", 1))\n
gcp_logging_client.setup_logging()\n
@click.command()
@click.argument("input_bucket_name")
@click.argument("file_path_on_input_bucket")
def process(input_bucket_name, file_path_on_input_bucket):
    batch_start_time = time.time()
    logging.info(
        f"STARTED batch {{BATCH_ID:,}} of {{N_BATCHES:,}}\\n"
        f"Instructions list is gs://{{input_bucket_name}}/{{file_path_on_input_bucket}}\\n"
    )
    gcp_bucket = gcp_storage_client.bucket(input_bucket_name)
    gcp_bucket_file = gcp_bucket.blob(file_path_on_input_bucket)\n
    file_contents: str = gcp_bucket_file.download_as_string().decode("utf-8")
    items_list: list = file_contents.split("\\n")
    batch_size: int = math.ceil(len(items_list) / N_BATCHES)
    batch_start_idx: int = batch_size * BATCH_ID
    batch_end_idx: int = batch_start_idx + batch_size\n
    logging.info(
        f"This batch ({{BATCH_ID:,}}) processing items {{batch_start_idx:,}} to {{batch_end_idx-1:,}}"
    )\n
    # user-specified pre-task code -------------------------------------------- #
{chr(10).join(['    '+line for line in pre_task_code])}
    # ------------------------------------------------------------------------- #
    for item_idx, item in enumerate(items_list[batch_start_idx:batch_end_idx]):
        # user-specified task code --------------------------------------------- #
{chr(10).join(['        '+line for line in task_code])}
        # ---------------------------------------------------------------------- #\n
    batch_end_time = time.time()
    logging.info(
        f"COMPLETED: batch {{BATCH_ID:,}} of {{N_BATCHES:,}}\\n"
        f"..from instruction list gs://{{input_bucket_name}}/{{file_path_on_input_bucket}}\\n"
        f"Number of minutes taken: {{(batch_end_time-batch_start_time)/60:,.5f}}"
    )\n
if __name__=="__main__":
    process()
"""

    # define contents of bash script create_cloud_run_job.sh #
    create_cloud_run_job_sh_contents: str = f"""
GCP_PROJECT_ID=$(gcloud config get project)
GCP_REGION={gcp_region}
GCP_CLOUD_RUN_JOB_NAME={cloud_run_job_name}
DOCKER_IMAGE_PATH=gcr.io/${{GCP_PROJECT_ID}}/${{GCP_CLOUD_RUN_JOB_NAME}}
INSTRUCTION_FILE_BUCKET_NAME={instruction_file_bucket_name}
INSTRUCTION_FILE_PATH={instruction_file_path}
echo "Setting gcloud to use region=$GCP_REGION for Cloud Run"
gcloud config set run/region ${{GCP_REGION}}\n
echo "...done"
echo "Enabling required gcloud services"
gcloud services enable run.googleapis.com cloudbuild.googleapis.com
echo "...done"
echo "Building process docker container and pushing to gcloud"
gcloud builds submit --pack image=${{DOCKER_IMAGE_PATH}}
echo "...done"
echo "Deleting cloud run job (if it already exists)"
gcloud beta run jobs delete ${{GCP_CLOUD_RUN_JOB_NAME}} --quiet
echo "Executing Cloud Run Job..."
echo "  ...with {cloud_run_job_params["--tasks"]} batches"
echo "  ...instructions file is gs://$INSTRUCTION_FILE_BUCKET_NAME/$INSTRUCTION_FILE_PATH"
gcloud beta run jobs create \\
${{GCP_CLOUD_RUN_JOB_NAME}} \\
--execute-now \\
--image ${{DOCKER_IMAGE_PATH}} \\
--command python \\
--args main.py,${{INSTRUCTION_FILE_BUCKET_NAME}},${{INSTRUCTION_FILE_PATH}} \\
{" ".join([f"{k} {cloud_run_job_params[k]} " for k in cloud_run_job_params])}
echo "...done"
echo "NOTE: the Cloud Run Job persists in google cloud, and you will need to delete it manually"
"""
    with open(f"{target_dir}/Procfile", "w", encoding="utf-8") as file:
        file.write(procfile_contents)

    with open(f"{target_dir}/main.py", "w", encoding="utf-8") as file:
        file.write(main_py_contents)

    with open(f"{target_dir}/create_cloud_run_job.sh", "w", encoding="utf-8") as file:
        file.write(create_cloud_run_job_sh_contents)

    with open(f"{target_dir}/requirements.txt", "w", encoding="utf-8") as file:
        file.write(requirements_txt_contents)
