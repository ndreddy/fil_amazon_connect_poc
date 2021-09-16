import json

from rmq_client import send_to_rabbitmq


def lambda_handler(event, context):
    print(f"Call Event Received: {json.dumps(event)}" )
    send_to_rabbitmq(json.dumps(event), "call.queue.event")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Call Event sent to RabbitMQ"
        })
    }
