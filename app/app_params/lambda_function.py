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
    details = event['Details']
    data = populate_data(details)
    logger.info(f'Request body {data} context: {context}')
    url = ssm_client.get_parameter(Name=f"/FIL/REST_PROXY_BASE_URL", WithDecryption=True).get(
        'Parameter').get('Value')
    url = f'{url}/appparameters'
    headers = {'Content-Type': 'application/json; utf-8'}
    return make_post_request(url, data, headers, (USERNAME, PASSWORD), timeout=float(REQ_TIMEOUT))


def populate_data(details):
    # Connect System parameters
    ani = details.get('ContactData', {}).get('CustomerEndpoint', {}).get("Address", "")
    dnis = details.get('ContactData', {}).get('SystemEndpoint', {}).get("Address", "")
    clientType = details.get('ContactData', {}).get('Channel', "VOICE")
    ucid = details.get('ContactData', {}).get('ContactId', "")
    queueId = details.get('ContactData', {}).get('Queue', "1")

    # Customer params sent from lambda
    params = details.get('Parameters', {})
    data = {}
    return data


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
    logger.debug(f'Making POST request to {url} with data = {json.dumps(data)} and headers = {headers}')
    response = {
        "errorMsg": "Internal Error Occurred",
        "result": "REQUEST_FAILED",
        "statusCode": 500
    }

    try:
        r = requests.post(url, json=data, headers=headers, auth=auth, timeout=timeout)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Http Error Occurred:{r.text}")
        return response
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Error Connecting Occurred:{e}")
        return response
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout Error Occurred:{e}")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"OOps: Something wrong:{e}")
        return response

    logger.debug(f"POST Success status: {r.status_code}, Response text: {r.text}")
    response = {"statusCode": r.status_code}
    return_val = json.loads(r.text).get("return")

    # Connect flow does not support nested items.
    return_val = filter_nested_items(return_val)
    return_val = convert_ewt_to_minutes(return_val)
    logger.debug(f'Filtered queue details = {return_val}')
    response = {"statusCode": r.status_code, **return_val}
    logger.debug(f'Returning response = {response}')

    return response


def filter_nested_items(data_dict):
    return {k.replace(".", "_"): v for (k, v) in data_dict.items() if not isinstance(v, dict)}


def convert_ewt_to_minutes(data_dict):
    ewt_minutes = round(int(data_dict.get("queue_override_ewt", 0)) / 60)
    data_dict.update(queue_override_ewt=ewt_minutes)
    return data_dict
