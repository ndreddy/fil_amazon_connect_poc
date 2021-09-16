import logging
from datetime import datetime

import boto3

from config import region, CONNECT_INSTANCE_ID, CONNECT_QUEUE_ID, CONNECT_QUEUE_ARN, current_metrics, metric_filters

logger = logging.getLogger(__name__)
connect = boto3.client('connect', region_name=region)


def get_current_metric_data():
    """
    Gets current metrics from Amazon connect.
    :return: metrics in FIL format
    """
    response = connect.get_current_metric_data(
        InstanceId=CONNECT_INSTANCE_ID,
        Filters=metric_filters,
        CurrentMetrics=current_metrics,
        MaxResults=10
    )

    if len(response['MetricResults']) == 0:
        print("   Queue is INACTIVE. Either no agents logged in or no calls in the queue")
        return {}

    return transform_metrics(response)


def transform_metrics(response):
    """
    Converts metrics from Connect format to FIL format
    :param response: Amazon connect response
    :return: FIL metrics
    """
    queue_stats = get_stats_template()
    for metric in response['MetricResults']:
        for c in metric['Collections']:
            key = c['Metric']['Name']
            val = int(c['Value'])
            logger.debug(f"{key}: {val}")

            if key == "AGENTS_ONLINE":
                queue_stats["agentStates"]["LOG_IN"] = val
            elif key == "AGENTS_AVAILABLE":
                queue_stats["agentStates"]["READY"] = val
            elif key == "AGENTS_AFTER_CONTACT_WORK":
                queue_stats["agentStates"]["WORK_READY"] = val
            elif key == "AGENTS_ON_CALL" or key == "AGENTS_AFTER_CONTACT_WORK":
                queue_stats["agentStates"]["WORK_READY"] += val
            elif key == "CONTACTS_IN_QUEUE":
                queue_stats["queueCount"] = val
            elif key == "AGENTS_STAFFED":
                queue_stats["agentCount"] = val
    logger.info(f"Queue Stats = {queue_stats}")
    return queue_stats


def get_stats_template():
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "aesName": CONNECT_INSTANCE_ID,
        "skillExtension": CONNECT_QUEUE_ID,
        "queueCount": 0,
        "agentCount": 0,
        "mostIdleAgentTime": 0,
        "leastOccupiedAgent": 0.0,
        "skillHandleTime": 0,
        "agentStates": {
            "WORK_READY": 0,
            "LOG_OUT": 0,
            "UNKNOWN": 0,
            "BUSY": 0,
            "LOG_IN": 0,
            "READY": 0,
            "WORK_NOT_READY": 0,
            "NOT_READY": 0
        },
        "lastUpdate": datetime.utcnow().isoformat()
    }
