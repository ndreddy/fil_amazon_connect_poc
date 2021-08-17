import pytest

from app.services.queue_metrics import get_current_metric_data

@pytest.mark.unittest
@pytest.mark.asyncio
def test_get_current_metric_data():
    metrics =  get_current_metric_data()
    assert metrics
    assert len(metrics) > 0
