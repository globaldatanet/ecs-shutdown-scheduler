import logging
import os
import boto3
from . import ECSService

ecs = boto3.client("ecs")


def whitelisted(service_arn: str):
    """ Determines whether or not a service is whitelisted for this scheduler
    """
    whitelist = os.getenv("WHITELIST").split(",")

    for item in whitelist: # TODO convert to any
        if item in service_arn:
            return True

    return False


def lambda_handler(event, _context):
    # configure logging
    level = os.environ.get("LOG_LEVEL", "INFO") # TODO change to antons snippet (at the top)
    logger = logging.getLogger()
    logger.setLevel(level)

    clusters = ecs.list_clusters()

    for cluster_arn in clusters["clusterArns"]: # TODO what if no clusters exist? will this result in a lookup error? then get(, []) instead
        # list each service for ecs clusters
        cluster_services = ecs.list_services(cluster=cluster_arn)

        for service_arn in cluster_services["serviceArns"]: # TODO same
            service = ECSService.ECSService(cluster_arn, service_arn)

            if not whitelisted(service_arn):
                logging.info(f"Service {service.ecs_service_name} is not whitelisted. Skipping...")
                continue

            task = event.get("Task", "")
            if task == "shutdown":
                service.shutdown()
            elif task == "start":
                service.start()
            else:
                raise(f"Couldnt interpret TASK: {task}. Must be one of: shutdown, start. Exiting")
