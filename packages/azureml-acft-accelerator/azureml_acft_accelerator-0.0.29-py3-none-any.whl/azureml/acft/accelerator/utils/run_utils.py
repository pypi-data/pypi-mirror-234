# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""
This file contains functions for getting run parameters
"""
import os
from azureml.core import Run
from azureml.core.compute import ComputeTarget

from .config import Config

run = Run.get_context()


def _get_run_id():
    """
    Returns run ID of parent of current run
    """

    if "OfflineRun" in run.id:
        return run.id
    return run.parent.id


def _get_sub_id():
    """
    Returns subscription ID of workspace where current run is executing
    """

    if "OfflineRun" in run.id:
        return Config.OFFLINE_RUN_MESSAGE
    return run.experiment.workspace.subscription_id


def _get_ws_name():
    """
    Returns name of the workspace where current run is submitted
    """

    if "OfflineRun" in run.id:
        return Config.OFFLINE_RUN_MESSAGE
    return run.experiment.workspace.name


def _get_region():
    """
    Returns the region of the workspace
    """

    if "OfflineRun" in run.id:
        return Config.OFFLINE_RUN_MESSAGE
    return run.experiment.workspace.location


def _get_compute():
    """
    Returns compute target of current run
    """

    if "OfflineRun" in run.id:
        return Config.OFFLINE_RUN_MESSAGE
    details = run.get_details()
    return details.get("target", "")


def _get_compute_vm_size():
    """
    Returns VM size on which current run is executing
    """

    if "OfflineRun" in run.id:
        return Config.OFFLINE_RUN_MESSAGE
    compute_name = _get_compute()
    if compute_name == "":
        return "No compute found."

    try:
        cpu_cluster = ComputeTarget(workspace=run.experiment.workspace, name=compute_name)
    except Exception:
        # cannot log here, logger is not yet instantiated
        return f"could not retrieve vm size for compute {compute_name}"

    return cpu_cluster.vm_size


def find_root(run):
    """
    Return the root run of current run.
    """

    if not run.parent:
        return run

    root_run = run.parent
    while root_run.parent:
        root_run = root_run.parent

    return root_run


def add_run_properties(properties, logger, add_to_root=False):
    """
    Add properties to current run context.
    For offline run _OfflineRun object handles it (azureml.core.run._OfflineRun)
    """

    if add_to_root and not "OfflineRun" in run.id:

        root_run = find_root(run)

        properties_to_add = {}
        root_run_properties = root_run.get_properties()

        # only add properties which are not already present
        for property in properties:
            if property not in root_run_properties:
                properties_to_add[property] = properties[property]
            else:
                logger.info(f"skip adding property to root: {property}")

        root_run.add_properties(properties=properties_to_add)
        logger.info(f"added run properties to root: {properties_to_add}")
    else:
        run.add_properties(properties=properties)
        logger.info(f"added run properties: {properties}")


def is_main_process():
    """
    Function for determining whether the current process is master.
    :return: Boolean for whether this process is master.
    """
    return os.environ.get('AZUREML_PROCESS_NAME', 'main') in {'main', 'rank_0'}