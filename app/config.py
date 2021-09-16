import logging.config
import os
from os import path

import boto3

log_file_path = os.path.normpath(path.join(path.dirname(path.abspath(__file__)), 'logging.conf'))
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

region = os.getenv("REGION", "us-west-2")

# boto3.setup_default_session(profile_name='swampfox')
CONNECT_QUEUE_ARN = os.getenv("CONNECT_QUEUE_ARN",
                              'arn:aws:connect:us-west-2:804094754830:instance/ba24bb27-e8be-415f-9f82-8de74eb8ce78/queue/1a7164b5-3846-4a7d-a328-71437aa75f57')
CONNECT_INSTANCE_ID = os.getenv("CONNECT_INSTANCE_ID", 'ba24bb27-e8be-415f-9f82-8de74eb8ce78')
CONNECT_QUEUE_ID = os.getenv("CONNECT_QUEUE_ID", '1a7164b5-3846-4a7d-a328-71437aa75f57')

metric_filters = {
    'Queues': [
        CONNECT_QUEUE_ID,
        CONNECT_QUEUE_ARN
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
