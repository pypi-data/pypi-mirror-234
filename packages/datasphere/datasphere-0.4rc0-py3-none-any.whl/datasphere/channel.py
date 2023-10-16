import json
import os
from typing import Tuple

import grpc

from datasphere.auth import env, ServerEnv, endpoint, op_endpoint

CHANNEL_OPTIONS = [
    ('grpc.enable_retries', 1),
    ('grpc.http2.max_pings_without_data', 0),
    ('grpc.keepalive_permit_without_calls', 1),
    # ('grpc.keepalive_time_ms', 3 * 60 * 1000),
    ('grpc.keepalive_timeout_ms', 10 * 1000),
    ('grpc.initial_reconnect_backoff_ms', 1000),
    ('grpc.min_reconnect_backoff_ms', 1000),
    ('grpc.max_reconnect_backoff_ms', 5000),
    ('grpc.service_config', json.dumps({
        'methodConfig': [
            {
                'name': [{'service': name}],
                'retryPolicy': {
                    'maxAttempts': 5,
                    'initialBackoff': '1s',
                    'maxBackoff': '5s',
                    'backoffMultiplier': 1.0,
                    'retryableStatusCodes': [
                        code.name for code in (grpc.StatusCode.UNAVAILABLE, grpc.StatusCode.CANCELLED)
                    ],
                },
            } for name in ('ProjectJobService', 'OperationService')
        ]
    }))
]


# Channels to Datasphere and Operation domains.
def get_channels() -> Tuple[grpc.Channel, grpc.Channel]:
    if env == ServerEnv.DEV:
        chan = grpc.insecure_channel(endpoint)
        return chan, chan
    else:
        if env == ServerEnv.PREPROD:
            root_ca_path = os.environ['ROOT_CA']
            with open(root_ca_path, 'rb') as f:
                creds = grpc.ssl_channel_credentials(f.read())
        else:
            creds = grpc.ssl_channel_credentials()
        chan, op_chan = (grpc.secure_channel(e, creds, options=CHANNEL_OPTIONS) for e in (endpoint, op_endpoint))
        return chan, op_chan
