# Create SQS client
import json
import logging

import boto3

from app.services import sqs_client
from app.services.queue_metrics import get_current_metric_data
from app.services.sqs_client import create_queue
from ischedule import schedule, run_loop

logger = logging.getLogger(__name__)
boto3.setup_default_session(profile_name='swampfox')

sqs = boto3.client('sqs')

# Create a SQS queue
# fil_queue = create_queue(sqs)
fil_queue = sqs.get_queue_url(QueueName=f"FIL_QUEUE")['QueueUrl']


def run():
    metrics = get_current_metric_data()
    msg_id = sqs_client.send_message(sqs, fil_queue, json.dumps(metrics))
    logger.info(f"Metrics {metrics} sent to msg id = {msg_id} ")


if __name__ == '__main__':
    schedule(run, interval=10)
    run_loop()
