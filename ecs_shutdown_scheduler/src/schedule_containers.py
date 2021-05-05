import logging
import os
import boto3
from . import ECSService


logging.getLogger().setLevel(os.environ.get("LOG_LEVEL", "INFO"))

ecs = boto3.client("ecs")


def whitelisted(service_arn: str):
    """ Determines whether or not a service is whitelisted for this scheduler
    """
    whitelist = os.getenv("WHITELIST").split(",")

    return any([True for x in whitelist if x in service_arn])


def lambda_handler(event, _context):
    clusters = ecs.list_clusters()

    for cluster_arn in clusters["clusterArns"]:
        # list each service for ecs clusters
        cluster_services = ecs.list_services(cluster=cluster_arn)

        for service_arn in cluster_services["serviceArns"]:
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
