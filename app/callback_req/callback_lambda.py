import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

region = os.getenv("REGION", "us-west-2")
ssm = boto3.client('ssm', region)

CALLBACK_REQ_URL = "/test"
# CALLBACK_REQ_URL = ssm.get_parameter(Name=f"/FIL/CALLBACK_REQ_URL", WithDecryption=True).get('Parameter').get('Value')
print(f"Callback Req Url = {CALLBACK_REQ_URL}")
headers = {'Content-Type': 'application/json; utf-8'}


def lambda_handler(event, context):
    logger.info(f'lambda started {event} context: {context}')
    data = event['body']
    logger.info(f'Making POST request to {CALLBACK_REQ_URL} with payload = {data}')
    # res = requests.post(CALLBACK_REQ_URL, headers=headers, data=data)

    response = {
        "statusCode": 200,
        "authenticationToken": "9124de26-b105-403f-8dde-9f9f744455b3",
        "callBackRequestId": "FIL-13-1",
        "errorMsg": "Success",
        "ewt": 130,
        "ewtHigh": 195,
        "ewtLow": 91,
        "preExistingCallbackTime": "",
        "queueName": "AFSkill",
        "queuePos": 1,
        "result": "SUCCESS"
    }
    logger.info(f'API response = {response}')
    return response
