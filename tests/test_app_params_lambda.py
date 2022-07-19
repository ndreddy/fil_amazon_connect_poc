import pytest
from app.app_params.lambda_function import convert_ewt_to_minutes

test_data = [

    ({

        "multi_acd_mode": False,
        "launch_excessive_waittime": "30000",
        "queue_override_ewt": 100,
        "callback_min_attempt_delay": "00:03:00",
        "queue_allow_dtmf_skip_options": False
    }

    )
]


@pytest.mark.parametrize("body", test_data)
def test_callback_lambda(body):
    r = convert_ewt_to_minutes(body)
    print(r)
