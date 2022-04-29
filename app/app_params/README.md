## Configuring environment variables

REGION: SSM client needs AWS Region to instantiate if ssm is not in default region - us-west-1 REQ_TIMEOUT: REST API
request timeout in seconds

```commandline
First Time
aws iam create-role --role-name fil_lambda-ex-role --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
aws iam attach-role-policy --role-name fil_lambda-ex-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam attach-role-policy --role-name fil_lambda-ex-role --policy-arn arn:aws:iam::aws:policy/AmazonSSMFullAccess

aws ssm put-parameter --name "/FIL/REST_PROXY_BASE_URL" --value "http://54.187.79.192:10180/filrestproxy" --type String --overwrite
aws ssm get-parameters --names "/FIL/REST_PROXY_BASE_URL"

aws lambda create-function \
    --function-name app_params \
    --region us-west-2  \
    --zip-file fileb://deployment-package.zip \
    --handler init_db.lambda_handler \
    --runtime python3.9 \
    --role arn:aws:iam::<account-id>:role/fil_lambda-ex-role \
    --environment "Variables={REGION=us-west-2, REQ_TIMEOUT=1.5}"
    
aws lambda update-function-configuration --function-name app_params --environment "Variables={REGION=us-west-2, REQ_TIMEOUT=1.5}"
aws lambda get-function-configuration --function-name app_params
```

## Retrieve environment variables in function code

```python
region = os.environ.get('REGION')
```

## Configure SSM Parameters

Set the Callback url in the SSM param store Use "--overwrite" to change the parameter value

```commandline

```

## Retrieve SSM Parameters in function code

```python
REGION = os.environ.get('REGION', "us-west-2")
ssm_client = boto3.client('ssm', REGION)
url = ssm_client.get_parameter(Name=f"/FIL/APP_PARAMS_URL", WithDecryption=True).get('Parameter').get('Value')
```

## Deployment package with dependencies

```shell
# Install the requests library to a new package directory
pip install --target ./package requests

# Create a deployment package with the installed library at the root.
cd package
zip -r ../deployment-package.zip.zip .


cd ..
# Repeat these when ever you change the code.
# Add the lambda_function.py file to the root of the zip file.
zip -g deployment-package.zip.zip lambda_function.py
# Deploy your .zip file to the function
aws lambda update-function-code --function-name app_params --zip-file fileb://deployment-package.zip.zip

# Invoke the function
aws lambda invoke --function-name app_params --log-type Tail --payload file://payload.json response.json --query 'LogResult' --output text |  base64 -d

```