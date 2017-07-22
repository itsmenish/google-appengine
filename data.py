import logging
import os
import cloudstorage as gcs
import json

from google.appengine.api import app_identity

def get_default_bucket():
    bucket_name = os.environ.get('BUCKET_NAME',
                                app_identity.get_default_gcs_bucket_name())
    # stats = repr(gcs.open("/" + bucket_name + "/batchmonitor/monitoring_config.json").read())
    return bucket_name

def get_projects():
    project_conf = gcs.open("/" + get_default_bucket() + "/batchmonitor/monitoring_config.json").read()
    parsed_conf = json.loads(project_conf)
    projects = parsed_conf["projects"].keys()
    return projects

def get_slo_sla(project):
    project_conf = gcs.open("/" + get_default_bucket() + "/batchmonitor/monitoring_config.json").read()
    parsed_conf = json.loads(project_conf)
    slo = parsed_conf["projects"][project]["slo"]
    sla = parsed_conf["projects"][project]["sla"]
    return {"slo": slo, "sla": sla}

def get_batch_status(project):
    batch_output = gcs.open("/" + get_default_bucket() 
                            + "/batchmonitor/" + project.lower() 
                            + "/batch_output.txt").read()
    success = "blue"
    failed = "red"
    waiting = "white"
    running = "green"
    if not failed in batch_output and not waiting in batch_output and not running in batch_output:
        status = "Success"
    elif (running in batch_output or waiting in batch_output) and not failed in batch_output:
        status = "In Progress"
    else:
        status = "Failed"
    
    sla_slo = get_slo_sla(project)
    
    batch = {"status": status, "slo": sla_slo["slo"], "sla": sla_slo["sla"]}
    return batch