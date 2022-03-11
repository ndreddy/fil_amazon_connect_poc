## Configuring environment variables

REGION: SSM client needs AWS Region to instantiate if ssm is not in default region - us-west-1
REQ_TIMEOUT: REST API request timeout in seconds
```commandline
aws lambda update-function-configuration --function-name callback_req_lambda --environment "Variables={REGION=us-west-2, REQ_TIMEOUT=1.5}"
aws lambda get-function-configuration --function-name callback_req_lambda
```

## Retrieve environment variables in function code

```python
region = os.environ.get('REGION')
```

## Configure SSM Parameters

Set the Callback url in the SSM param store Use "--overwrite" to change the parameter value

```commandline
aws ssm put-parameter --name "/FIL/CALLBACK_REQ_URL" --value "http://10.91.11.151:10080/filrestproxy/queuecallback" --type String --overwrite
aws ssm get-parameters --names "/FIL/CALLBACK_REQ_URL"
```

## Retrieve SSM Parameters in function code

```python
REGION = os.environ.get('REGION', "us-west-2")
ssm_client = boto3.client('ssm', REGION)
url = ssm_client.get_parameter(Name=f"/FIL/CALLBACK_REQ_URL", WithDecryption=True).get('Parameter').get('Value')
```

## Deployment package with dependencies
```shell
# Install the requests library to a new package directory
pip install --target ./package requests

# Create a deployment package with the installed library at the root.
cd package
zip -r ../callback-deployment-package.zip .


cd ..
# Repeat these when ever you change the code.
# Add the lambda_function.py file to the root of the zip file.
zip -g callback-deployment-package.zip lambda_function.py
# Deploy your .zip file to the function
aws lambda update-function-code --function-name callback_req_lambda --zip-file fileb://callback-deployment-package.zip

# Invoke the function
aws lambda invoke --function-name callback_req_lambda --log-type Tail --payload file://payload.json response.json --query 'LogResult' --output text |  base64 -d

```