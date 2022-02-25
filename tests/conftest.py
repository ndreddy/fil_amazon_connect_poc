import uuid
from typing import Generator
from urllib.parse import urljoin
import json
import zipfile
import io

import pytest
import boto3
import os
from httpx import AsyncClient

from moto import mock_s3, mock_sqs, mock_lambda, mock_iam, mock_ssm

from app.callback_function import lambda_function


def pytest_addoption(parser):
    # ability to test API on different hosts
    parser.addoption("--host", action="store", default="http://localhost:8080")


def pytest_configure():
    pytest.profile_id = "codebuild-4a21500e-4763-4d70-95e0-97a6a1accc43"


@pytest.fixture(scope="session")
def host(request):
    return request.config.getoption("--host")


@pytest.fixture(scope="session")
def api_host(host):
    return urljoin(host, "api")


@pytest.fixture(scope="module")
def get_bearer():
    bearer = "Bearer " + "get_idtoken()"
    return bearer


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture
def region():
    return "us-east-1"


@pytest.fixture
def ssm_mock(aws_credentials):
    with mock_ssm():
        ssm = boto3.client("ssm")
        ssm.put_parameter(
            Name=f"/FIL/CALLBACK_REQ_URL", Description="FIL callback req url",
            Value="http://10.91.11.151:9845/filrestproxy/queuecallback", Type="String"
        )
        yield ssm


@pytest.fixture
def s3_mock(aws_credentials, region):
    """
       Mocked sqs queue
       @param region:
       @param aws_credentials:
       """
    with mock_s3():
        s3 = boto3.resource("s3", region_name=region)
        # s3.create_bucket(Bucket=tx_sync_service.bucket_name)
        # tx_sync_service.s3 = s3
        yield s3


@pytest.fixture
def sqs_mock(aws_credentials, region):
    """
    Mocked sqs queue
    @param region:
    @param aws_credentials:
    """
    with mock_sqs():
        sqs = boto3.resource("sqs", region_name=region)
        # create 1 queue for sync and register
        # queue = sqs.create_queue(QueueName=f"{settings.TX_SYNC_QUEUE_NAME}")
        # tx_sync_service.tx_queue = queue
        # user_sync_service.user_queue = queue
        # yield queue


@pytest.fixture
def lambda_mock(aws_credentials, region):
    with mock_lambda():
        m_lambda = boto3.client("lambda", region_name=region)
        # tx_sync_service.lambda_client = m_lambda
        yield m_lambda


def _process_lambda(func_str):
    zip_output = io.BytesIO()
    zip_file = zipfile.ZipFile(zip_output, "w", zipfile.ZIP_DEFLATED)
    zip_file.writestr("lambda_function.py", func_str)
    zip_file.close()
    zip_output.seek(0)
    return zip_output.read()


def get_test_zip_file1():
    pfunc = """
def lambda_handler(event, context):
    print("custom log event")
    return event
"""
    return _process_lambda(pfunc)


def get_role_name(region):
    with mock_iam():
        iam = boto3.client("iam", region_name=region)
        return iam.create_role(
            RoleName="my-role",
            AssumeRolePolicyDocument="some policy",
            Path="/my-path/",
        )["Role"]["Arn"]


@pytest.fixture
def lambda_function_name():
    return "test_get_to_config"


@pytest.fixture
def create_mock_lambda(lambda_mock, region, lambda_function_name):
    lambda_mock.create_function(
        FunctionName=lambda_function_name,
        Runtime="python3.8",
        Role=get_role_name(region),
        Handler="lambda_function.lambda_handler",
        Code={"ZipFile": get_test_zip_file1()},
        Description="test lambda function",
        Timeout=3,
        MemorySize=128,
        Publish=True,
    )
