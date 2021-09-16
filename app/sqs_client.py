"""
    Consumes messages from Amazon Simple Queue Service (Amazon SQS).
"""
import logging
import time

from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


def receive_messages(queue, max_num=1000):
    """
    Receive a batch of messages in a single request from an SQS queue.

    @param queue:
    @param max_num: The maximum number of messages to be fetched from SQS in batches of 10 messages.
    The actual number of messages received might be less if queue length is < max_num.
    @return: Generator object for the messages

    """

    num = 0
    logger.info(f"Max limit on messages is {max_num} to drain from {queue}")
    t1 = time.time()
    while num < max_num:
        messages = queue.receive_messages(
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=10,
            WaitTimeSeconds=1
        )

        # Exits when receive_messages() returns empty list indicating queue is empty.
        if not messages:
            t2 = time.time()
            logger.info(f"Queue is empty, actual drained is {num} messages in {t2 - t1} seconds")
            return

        try:
            yield from messages
            num += len(messages)
        except Exception:
            logger.exception(f"Exception receiving messages from {queue}")
            return

    t2 = time.time()
    logger.info(f"Max limit {max_num} exceeded, actual drained is {num} messages in {t2 - t1} seconds")


def delete_messages(queue, messages):
    """
    Delete a batch of messages from a queue in a single request.

    Usage is shown in usage_demo at the end of this module.

    @param queue: The queue from which to delete the messages.
    @param messages: The list of messages to delete.
    @return: The response from SQS that contains the list of successful and failed
             message deletions.
    """
    if not messages:
        return
    try:
        entries = [{
            'Id': str(ind),
            'ReceiptHandle': msg.receipt_handle
        } for ind, msg in enumerate(messages)]
        response = queue.delete_messages(Entries=entries)
        if 'Successful' in response:
            for msg_meta in response['Successful']:
                logger.debug(f"Deleted {messages[int(msg_meta['Id'])].receipt_handle}")
        if 'Failed' in response:
            for msg_meta in response['Failed']:
                logger.warning(f"Could not delete {messages[int(msg_meta['Id'])].receipt_handle}")
    except ClientError:
        logger.exception(f"Exception deleting message from {queue}")
    else:
        return response


def send_message(sqs, queue_url, msg_body):
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageAttributes={
            'Title': {
                'DataType': 'String',
                'StringValue': 'The Whistler'
            },
            'Author': {
                'DataType': 'String',
                'StringValue': 'John Grisham'
            },
            'WeeksOn': {
                'DataType': 'Number',
                'StringValue': '6'
            }
        },
        MessageBody=msg_body
    )
    return response


def create_queue(sqs):
    response = sqs.create_queue(
        QueueName='FIL_QUEUE',
        Attributes={
            'DelaySeconds': '60',
            'MessageRetentionPeriod': '86400'
        }
    )
    return response['QueueUrl']
