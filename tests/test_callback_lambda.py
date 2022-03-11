import json

import pytest

from app.callback_function import lambda_function

test_data = [

    ({

        "ani": "2011231556",
        "appData": "param_map=<?xml version\\x3d'1.0' encoding\\x3d'UTF-8'?>\n<concurrent-hash-map>\n  <entry>\n    <string>contact.offer.ani</string>\n    <string>2011231556</string>\n  </entry>\n  <entry>\n    <string>language</string>\n    <string>english</string>\n  </entry>\n  <entry>\n    <string>contact.offer.time</string>\n    <string>2022-03-11 15:53:13</string>\n  </entry>\n  <entry>\n    <string>queue.id</string>\n    <string>1</string>\n  </entry>\n  <entry>\n    <string>callback.offer.type</string>\n    <string>asap</string>\n  </entry>\n  <entry>\n    <string>contact.offer.uui</string>\n    <string>a3a88bad-b43c-4421-82ab-ced63815b20c</string>\n  </entry>\n  <entry>\n    <string>contact.callback.ext</string>\n    <string>null</string>\n  </entry>\n  <entry>\n    <string>callback.type</string>\n    <string>CALLBACK_NORMAL</string>\n  </entry>\n  <entry>\n    <string>contact.offer.vdn</string>\n    <string>Seg</string>\n  </entry>\n  <entry>\n    <string>contact.offer.ewt</string>\n    <int>0</int>\n  </entry>\n  <entry>\n    <string>contact.offer.ucid</string>\n    <string>7567556f-9b6d-454e-b4f4-51557d570ae1</string>\n  </entry>\n  <entry>\n    <string>queue.agent.first</string>\n    <boolean>false</boolean>\n   </entry>\n  <entry>\n    <string>contact.callback_uri</string>\n    <string>2011231556</string>\n  </entry>\n  <entry>\n    <string>contact.offer.session_id</string>\n    <string>a3a88bad-b43c-4421-82ab-ced63815b20c</string>\n  </entry>\n  <entry>\n    <string>contact.offer.dnis</string>\n    <string>Seg</string>\n  </entry>\n</concurrent-hash-map>",
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
