import logging.config
import os
from os import path

import boto3

log_file_path = os.path.normpath(path.join(path.dirname(path.abspath(__file__)), '../logging.conf'))
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

ENV = os.getenv("ENV", "STG")
region = os.getenv("REGION", "us-west-2")
logger.info(f'ENV={ENV}, region={region}')

# Chacko's Env
# queue_arn = 'arn:aws:connect:us-east-1:627757629993:instance/bead81b4-1bad-4582-9efc-15fde1c3178b/queue/0dfbc6dd-7702-468f-923d-75aee9fb1d80'
# instance_id = 'bead81b4-1bad-4582-9efc-15fde1c3178b'
# queue_id = '0dfbc6dd-7702-468f-923d-75aee9fb1d80'

# Nagendra's Env
# TODO: comment out this if you have one AWS account.
boto3.setup_default_session(profile_name='swampfox')
queue_arn = 'arn:aws:connect:us-west-2:804094754830:instance/ba24bb27-e8be-415f-9f82-8de74eb8ce78/queue/1a7164b5-3846-4a7d-a328-71437aa75f57'
instance_id = 'ba24bb27-e8be-415f-9f82-8de74eb8ce78'
queue_id = '1a7164b5-3846-4a7d-a328-71437aa75f57'

metric_filters = {
    'Queues': [
        queue_id,
        queue_arn
    ],
    'Channels': [
        'VOICE'
    ]
}

current_metrics = [
    {
        'Name': 'AGENTS_ONLINE',
        'Unit': 'COUNT'
    },
    {
        'Name': 'AGENTS_AVAILABLE',
        'Unit': 'COUNT'
    },
    {
        'Name': 'AGENTS_ON_CALL',
        'Unit': 'COUNT'
    },
    {
        'Name': 'AGENTS_NON_PRODUCTIVE',
        'Unit': 'COUNT'
    },
    {
        'Name': 'AGENTS_AFTER_CONTACT_WORK',
        'Unit': 'COUNT'
    },
    {
        'Name': 'AGENTS_STAFFED',
        'Unit': 'COUNT'
    },
    {
        'Name': 'CONTACTS_IN_QUEUE',
        'Unit': 'COUNT'
    },
    {
        'Name': 'OLDEST_CONTACT_AGE',
        'Unit': 'SECONDS'
    },
    {
        'Name': 'CONTACTS_SCHEDULED',
        'Unit': 'COUNT'
    },
    {
        'Name': 'AGENTS_ON_CONTACT',
        'Unit': 'COUNT'
    },
    {
        'Name': 'SLOTS_ACTIVE',
        'Unit': 'COUNT'
    },
    {
        'Name': 'SLOTS_AVAILABLE',
        'Unit': 'COUNT'
    }
]
