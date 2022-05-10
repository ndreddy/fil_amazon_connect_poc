import json

import pytest

from app.queue_details import lambda_function

test_data = [

    ({
        "announcementsXml": {},
        "callBackVdn": "Cbseg",
        "callCenterOpen": True,
        "callsInQueue": 0,
        "ewt": 130,
        "ewtHigh": -1,
        "ewtLow": 600,
        "express": False,
        "language": "english",
        "offerCallBack": True,
        "offerReason": "OFFER",
        "offerScheduledCallBack": False,
        "offerScheduledReason": "MIN_EWT_NOT_REACHED_ANNOUNCE_EWT",
        "queueId": 1,
        "queueName": "AFSkill",
        "queueParamsXml": {
            "queue.dialing_prefix": "+1",
            "callback.app.name": "SimpleOutbound",
            "callback.app.name.agent_first": "SimpleOutbound"
        },
        "queueTimeZone": "America/New_York",
        "queuingVdn": "Seg",
        "state": "OFFERING"
    }

    )
]


@pytest.mark.parametrize("body", test_data)
def test_filter_nested_items(body):
    result = lambda_function.filter_nested_items(body)
    print(str(result))
    assert result


