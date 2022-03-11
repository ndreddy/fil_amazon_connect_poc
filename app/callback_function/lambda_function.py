import json
import logging
import os

import boto3
import requests

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

REGION = os.environ.get('REGION', "us-west-2")
REQ_TIMEOUT = os.environ.get('REQ_TIMEOUT', 1.5)
USERNAME = os.environ.get('CALLBACK_USERNAME', "mike")
PASSWORD = os.environ.get('CALLBACK_PASSWORD', "mike1")

ssm_client = boto3.client('ssm', REGION)


def lambda_handler(event, context):
    logger.info(f'lambda started {event} context: {context}')
    data = event['body']
    logger.info(f'Request body {data} context: {context}')
    url = ssm_client.get_parameter(Name=f"/FIL/CALLBACK_REQ_URL", WithDecryption=True).get(
        'Parameter').get('Value')
    headers = {'Content-Type': 'application/json; utf-8'}
    return make_post_request(url, data, headers, (USERNAME, PASSWORD), timeout=float(REQ_TIMEOUT))


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
        r = requests.post(url, json=data, headers=headers, auth=auth, timeout=timeout)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Http Error Occurred:{r.text}")
        return {"Error": e.response}
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Error Connecting Occurred:{e}")
        return {"Error": e.response}
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout Error Occurred:{e}")
        return {"Error": e.response}
    except requests.exceptions.RequestException as e:
        logger.error(f"OOps: Something wrong:{e}")
        return {"Error": e.response}

    logger.debug(f"POST Response status: {r.status_code}, Response text: {r.text}")
    response = json.loads(r.text).get("return")
    response["statusCode"] = r.status_code

    logger.debug(f'Returning response = {response}')
    return response
