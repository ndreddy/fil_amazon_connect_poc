import json
import logging

from queue_metrics import get_current_metric_data
from rmq_client import send_to_rabbitmq

logger = logging.getLogger(__name__)


def lambda_handler(event, context):
    # Gets the metrics from the endpoint
    metrics = get_current_metric_data()

    # Sends to RabbitMQ
    send_to_rabbitmq(json.dumps(metrics), 'agent.status.event')

    logger.info(f"Metrics {metrics} sent to Amazon MQ ")
    return create_response(200, "Updated queue stats successfully")


def create_response(status_code, body):
    return {
        "isBase64Encoded": False,
        "statusCode": status_code,
        "headers": {
            'Access-Control-Allow-Headers': 'Content-Type, Accept, Authorization, X-Requested-With, Origin',
            "Access-Control-Allow-Credentials": 'true',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS, GET, POST',
        },
        "body": body
    }
