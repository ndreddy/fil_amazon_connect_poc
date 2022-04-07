import json

import pytest

from app.callback_function import lambda_function

test_data = [

    ({

        "ani": "2011231556",
        "callBackPhone": "2011231556",
        "callBackExtension": "",
        "clientType": "WEB",
        "dnis": "99999",
        "ewt": "0",
        "nameText": "Anantha|null",
        "reasonText": None,
        "geolocation": None,
        "offerVdn": "Seg",
        "queueId": "1",
        "sessionId": "a3a88bad-b43c-4421-82ab-ced63815b20c",
        "ucid": "7567556f-9b6d-454e-b4f4-51557d570ae1",
        "uui": "a3a88bad-b43c-4421-82ab-ced63815b20c"
    }

    )
]


@pytest.mark.parametrize("body", test_data)
def test_callback_lambda(body):
    event = {'httpMethod': "POST", 'body': body}
    context = {'request_id': '1234'}

    result = lambda_function.lambda_handler(event, context)
    print(str(result))
    assert result


test_data = [('https://postman-echo.com/post', {'title': 'foo', 'body': 'bar', 'userId': 1, },
              {'Content-Type': 'application/json; utf-8'})]


@pytest.mark.parametrize("url, data, headers", test_data)
def test_make_post_request(url, data, headers):
    res = lambda_function.make_post_request(url, data, headers, ('user', 'pass'))
    print(res)
    assert res


test_data = [

    ({
        'ContactData': {
            'Attributes': {},
            'Channel': 'VOICE',
            'ContactId': '550de66e-5ca1-4b59-944c-9010c1fcfd6e',
            'CustomerEndpoint': {
                'Address': '+12082971868',
                'Type': 'TELEPHONE_NUMBER'
            },
            'CustomerId': None,
            'Description': None,
            'InitialContactId': '550de66e-5ca1-4b59-944c-9010c1fcfd6e',
            'InitiationMethod': 'INBOUND',
            'InstanceARN': 'arn:aws:connect:us-west-2:804094754830:instance/ba24bb27-e8be-415f-9f82-8de74eb8ce78',
            'LanguageCode': 'en-US',
            'MediaStreams': {
                'Customer': {
                    'Audio': None
                }
            },
            'Name': None,
            'PreviousContactId': '550de66e-5ca1-4b59-944c-9010c1fcfd6e',
            'Queue': None,
            'References': {},
            'SystemEndpoint': {
                'Address': '+12143069489',
                'Type': 'TELEPHONE_NUMBER'
            }
        },
        'Parameters': {
            'callBackPhone': '98459845',
            'callBackExtension': '1234'
        }
    }

    )
]


@pytest.mark.parametrize("details", test_data)
def test_populate_data(details):
    data = lambda_function.populate_data(details)
    assert data.get("ani") == '+12082971868'
    assert data.get("dnis") == '+12143069489'
    assert data.get("callBackPhone") == '98459845'
    assert data.get("callBackExtension") == '1234'
