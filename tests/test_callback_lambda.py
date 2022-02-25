import json

import pytest

from app.callback_function import lambda_function

test_data = [

    ({
        "ani": "37532",
        "applicationName": "fil_template",
        "banner": [
            "FIL Callback From "
        ],
        "callTime": "2021-08-03T05:23:51.216",
        "dialEndpoint": [
            "6666"
        ],
        "dialName": [
            "37532"
        ],
        "dialedNumber": "callback",
        "dnis": "n/a",
        "sessionId": "unknown",
        "switchId": 0,
        "transferNumber": "n/a",
        "ucid": "92e8fd31-5a12-4e9a-a",
        "uniqueId": "92e8fd31-5a12-4e9a-abee-67d8c4-0",
        "uui": "62dc6223-6599-4d9d-94a0-6e226ce8e351",
        "callDetailsNVP": {
            "reasonText": "",
            "dialentry": "6666",
            "nameUrl": "",
            "totalAttempts": "1",
            "OcmDispositionEndpoint": "https://10.91.11.161:9443/FILServer/AgentFirst?DISPOSITION&src=FINESSE&call_back_id=FIL-444663-1&sessionid=FIL-444663-1-0&queue_id=1",
            "reasonAudio": "",
            "OcmDispositionGroup": "FILReturn",
            "nameText": "aaaa|null",
            "attempt": "1",
            "nameAudio": "",
            "callType": "ASAP",
            "offerTime": "2021-08-03T09:23:51.216Z",
            "reasonUrl": "",
            "offerEwt": "120",
            "callBackExtension": "",
            "geolocation": ""
        }
    })
]


@pytest.mark.parametrize("body", test_data)
def test_callback_lambda(ssm_mock, body):
    event = {'httpMethod': "POST", 'body': json.dumps(body)}
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
