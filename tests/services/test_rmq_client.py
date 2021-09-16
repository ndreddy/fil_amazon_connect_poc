import pytest

from app.rmq_client import send_to_rabbitmq


@pytest.mark.unittest
@pytest.mark.asyncio
def test_send_to_rabbitmq():
    send_to_rabbitmq({"test": "message"}, "queue.stat.event")
