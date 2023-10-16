"""
This script defines the function gcloud_vm_deletes_itself()
"""

import sys
from typing import Any

import google.api_core.extended_operation
import google.cloud.compute_v1  # pylint: disable=import-error, no-name-in-module

import requests  # type: ignore


def wait_for_extended_operation(
    operation: google.api_core.extended_operation.ExtendedOperation,
    verbose_name: str = "operation",
    timeout: int = 300,
) -> Any:
    """
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
    """
    result = operation.result(timeout=timeout)

    if operation.error_code:
        print(
            f"Error during {verbose_name}: [Code: {operation.error_code}]: {operation.error_message}",  # pylint: disable=line-too-long
            file=sys.stderr,
            flush=True,
        )
        print(f"Operation ID: {operation.name}", file=sys.stderr, flush=True)
        raise operation.exception() or RuntimeError(operation.error_message)

    if operation.warnings:
        print(f"Warnings during {verbose_name}:\n", file=sys.stderr, flush=True)
        for warning in operation.warnings:
            print(f" - {warning.code}: {warning.message}", file=sys.stderr, flush=True)

    return result


def gcloud_vm_deletes_itself() -> None:
    """Running this function on a google cloud Virtual Machine causes it to delete itself"""
    instance_client = (
        google.cloud.compute_v1.InstancesClient()  # pylint: disable=c-extension-no-member
    )
    # fetch Virtual Machine information from the metadata server #
    metadata_server_headers: dict[str, str] = {
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
