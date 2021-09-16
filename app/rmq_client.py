import logging
import os
import ssl

import boto3
import pika  # Python AMQP Library

# boto3.setup_default_session(profile_name='swampfox')
logger = logging.getLogger(__name__)

# get Environment Variables
RABBIT_HOST = os.environ.get('RABBIT_HOST', 'b-78a044ce-fde9-44c4-be17-8e2254aae353.mq.us-west-2.amazonaws.com')
RABBIT_USER = os.environ.get('RABBIT_USER', 'ewtuser')
# RABBIT_PWD_ENCRYPTED = os.environ.get('RABBIT_PWD','xxxxx')
RABBIT_PWD = os.environ.get('RABBIT_PWD','xxxxx')

# Decrypt Password
# RABBIT_PWD_DECRYPTED = boto3.client('kms').decrypt(CiphertextBlob=b64decode(RABBIT_PWD_ENCRYPTED))['Plaintext']
credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PWD)
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
parameters = pika.ConnectionParameters(port=5671, host=RABBIT_HOST, credentials=credentials,
                                       ssl_options=pika.SSLOptions(context))


def send_to_rabbitmq(message, rt_key):
    logging.info(f"Sending message {message} with routing key {rt_key} to RabbitMQ")
    # Establishes TCP Connection with RabbitMQ
    connection = pika.BlockingConnection(parameters)
    # Establishes logical channel within Connection
    channel = connection.channel()
    # Creates the exchange, if it does not exists
    channel.exchange_declare(exchange='sf.ewt.mon.exchange', exchange_type='direct', durable='True')
    # Sends message to the exchange with the routing key
    channel.basic_publish(exchange='sf.ewt.mon.exchange', routing_key=rt_key, body=message)
    # Close Connection and Channel(s) within
    connection.close()
