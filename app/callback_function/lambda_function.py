import logging
import os

import boto3
import requests

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

REGION = os.environ.get('REGION', "us-west-2")
REQ_TIMEOUT = os.environ.get('REQ_TIMEOUT', 1.5)
ssm_client = boto3.client('ssm', REGION)


def lambda_handler(event, context):
    logger.info(f'lambda started {event} context: {context}')
    data = event['body']
    url = ssm_client.get_parameter(Name=f"/FIL/CALLBACK_REQ_URL", WithDecryption=True).get(
        'Parameter').get('Value')
    headers = {'Content-Type': 'application/json; utf-8'}
    return make_post_request(url, data, headers, timeout=float(REQ_TIMEOUT))


def make_post_request(url: str, data: dict, headers: dict, auth: tuple = None, timeout: float = None) -> dict:
    """
    Makes post request using requests module.
    :param timeout: request timeout
    :param url: endpoint url
    :param data: post body/payload to the url
    :param headers: request headders
    :param auth: tuple with user name and password
    :return: dict response
    """
    logger.debug(f'Making POST request to {url} with data = {data} and headers = {headers}')
    try:
        r = requests.post(url, headers=headers, data=data, auth=auth, timeout=timeout)
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        logger.error("Http Error:")
    except requests.exceptions.ConnectionError:
        logger.error("Error Connecting:")
    except requests.exceptions.Timeout:
        logger.error("Timeout Error:")
    except requests.exceptions.RequestException:
        logger.error("OOps: Something wrong")

    logger.debug("Returning hardcode response ...")
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
    logger.debug(f'API response = {response}')
    return response
