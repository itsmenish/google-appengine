import logging
import os
import cloudstorage as gcs
import json

from google.appengine.api import app_identity

BATCH_MONITOR_GCS_PREFIX = "/batchmonitor/"

def get_default_bucket():
    bucket_name = os.environ.get('BUCKET_NAME',
                                app_identity.get_default_gcs_bucket_name())
    # stats = repr(gcs.open("/" + bucket_name + "/batchmonitor/monitoring_config.json").read())
    return bucket_name

def get_batch_monitor_config():
    monitoring_conf = gcs.open("/" + get_default_bucket() + BATCH_MONITOR_GCS_PREFIX + "monitoring_config.json").read()
    parsed_conf = json.loads(monitoring_conf)
    return parsed_conf

def get_projects():
    parsed_conf = get_batch_monitor_config()
    projects = parsed_conf["projects"].keys()
    return projects

def get_project_details(project):
    parsed_conf = get_batch_monitor_config()
    project_details = parsed_conf["projects"][project]
    return project_details

def get_batch_status(project):
    project_details = get_project_details(project)
    batch_output = gcs.open("/" + get_default_bucket() 
                            + "/batchmonitor/" + project.lower() 
                            + "/batch_output.txt").read()
    
    # logging for debug purpose
    logging.debug("This is the project details we got: " + str(project_details))
    logging.debug("SLO and SLA are: " + project_details["SLO"] + " and " + project_details["SLA"])

    success = project_details["batchParser"]["success"]
    failed = project_details["batchParser"]["failed"]
    waiting = project_details["batchParser"]["waiting"]
    running = project_details["batchParser"]["running"]
    
    SLO = project_details["SLO"]
    SLA = project_details["SLA"]

    if not failed in batch_output and not waiting in batch_output and not running in batch_output:
        status = "Success"
    elif (running in batch_output or waiting in batch_output) and not failed in batch_output:
        status = "In Progress"
    else:
        status = "Failed"

    batch = {"status": status, "SLO": SLO, "SLA": SLA}
    return batch