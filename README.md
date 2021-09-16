## Description of the app files

```text
- requirements.txt: Tracks the dependencies of your application 
- config.py: This configures your application. .
- main.py: This is the entry point to your application, 
- test: Contains tests for the API, which are written with library pytest-asyncio. The file conftest.py contains global fixtures that are automatically evaluated before running any of the tests.
```

## Environment Setting

```text
 App expects the following environment variables 
 REGION
 
 #Amazon Connect related
 CONNECT_QUEUE_ARN          # default is NR
 CONNECT_INSTANCE_ID
 CONNECT_QUEUE_ID
 
 #RabbitMQ related
 RABBIT_HOST    #default is 
 RABBIT_USER    # default is ewtuser
 RABBIT_PWD     # Must be correct one, default is xxxx which will fail to connect.
   
```

## Running the app

```
virtualenv -p python3 venv
source venv/bin/activate
```

Next, run

```
pip install -r requirements.txt
```

to get the dependencies.

Finally run the app with

```
app.main:app 
```
### Package Lambdas Functions
```
cd app
pip install --target ./package pika
cd package
zip -r ../lambda-deployment-package.zip .
zip -g lambda-deployment-package.zip call_events_lambda.py queue_stats_lambda.py queue_metrics.py rmq_client.py config.py logging.conf
```

## Running tests

To run the test suite, simply pip install it and run from the root directory like so

```commandline
pip install pytest-asyncio
pytest
```

### Event Bridge to call_event_lambda input transformer

Amazon Connect Call Queued Event.
```json
{
  "version": "0",
  "id": "3a3030ce-859f-fbc1-dcef-975a250de885",
  "detail-type": "Amazon Connect Contact Event",
  "source": "aws.connect",
  "account": "804094754830",
  "time": "2021-08-11T07:43:00Z",
  "region": "us-west-2",
  "resources": [
    "arn:aws:connect:us-west-2:804094754830:instance/ba24bb27-e8be-415f-9f82-8de74eb8ce78",
    "arn:aws:connect:us-west-2:804094754830:instance/ba24bb27-e8be-415f-9f82-8de74eb8ce78/contact/f65d6e8b-7a8d-4140-9c88-a7041333a39c"
  ],
  "detail": {
    "contactId": "f65d6e8b-7a8d-4140-9c88-a7041333a39c",
    "channel": "VOICE",
    "instanceArn": "arn:aws:connect:us-west-2:804094754830:instance/ba24bb27-e8be-415f-9f82-8de74eb8ce78",
    "initiationMethod": "INBOUND",
    "eventType": "QUEUED",
    "queueInfo": {
      "queueType": "STANDARD",
      "queueArn": "arn:aws:connect:us-west-2:804094754830:instance/ba24bb27-e8be-415f-9f82-8de74eb8ce78/queue/1a7164b5-3846-4a7d-a328-71437aa75f57"
    }
  }
}
```
Input path
```json
{
  "aesName": "$.detail.instanceArn",
  "agentId": "$.detail.initiationMethod",
  "callId": "$.detail.contactId",
  "calledNumber": "$.account",
  "callingNumber": "$.account",
  "createTime": "$.time",
  "eventType": "$.detail.eventType",
  "queueReason": "$.detail.initiationMethod",
  "reason": "$.detail.initiationMethod",
  "skillExt": "$.detail.queueInfo.queueArn",
  "skillId": "$.detail.queueInfo.queueArn",
  "skillName": "$.detail.queueInfo.queueArn",
  "ucid": "$.detail.contactId",
  "uui": "$.detail.contactId"
}

```
Input template
```json
{
  "eventType": "<eventType>",
  "aesName": "<aesName>",
  "callId": "<callId>",
  "callingNumber": "<callingNumber>",
  "calledNumber": "<calledNumber>",
  "skill": {
    "name": "<skillName>",
    "skillExtension": "<skillExt>",
    "skillId": "<skillId>"
  },
  "vdn": "9999",
  "ucid": "<ucid>",
  "uui": "<uui>",
  "createTime": "<createTime>",
  "reason": "<reason>",
  "agentId": "<agentId>",
  "queueReason": "<queueReason>",
  "agentStatusReport": "",
  "numberInQueue": 0,
  "callsQueued": 0,
  "skillName": "<skillName>"
}
```