from enum import Enum
import logging
import os
import subprocess
from typing import List, Optional, Tuple

from yandexcloud import SDK
from yandex.cloud.iam.v1.iam_token_service_pb2_grpc import IamTokenServiceStub
from yandex.cloud.iam.v1.iam_token_service_pb2 import CreateIamTokenRequest

logger = logging.getLogger(__name__)


class ServerEnv(Enum):
    DEV = 'DEV'
    PREPROD = 'PREPROD'
    PROD = 'PROD'


env_str: Optional[str] = os.getenv('SERVER_ENV', None)
env: ServerEnv = ServerEnv(env_str.upper()) if env_str else ServerEnv.PROD
endpoint, op_endpoint = {
    ServerEnv.DEV: ('localhost:50051', 'localhost:50051'),
    ServerEnv.PREPROD: ('datasphere.api.cloud-preprod.yandex.net:443', 'operation.api.cloud-preprod.yandex.net:443'),
    ServerEnv.PROD: ('datasphere.api.cloud.yandex.net:443', 'operation.api.cloud.yandex.net:443'),
}[env]


def create_iam_token(oauth_token: Optional[str]) -> str:
    if oauth_token:
        return create_iam_token_by_oauth_token(oauth_token)

    # If user does not provide OAuth token, or OAuth token is not applicable (i.e. for YC staff with federations),
    # we consider that `yc` CLI is installed and configured properly (either on prod or preprod installation).
    return create_iam_token_with_yc()


def create_iam_token_by_oauth_token(oauth_token: str) -> str:
    logger.debug('creating iam token using oauth token ...')
    sdk = SDK()
    client = sdk.client(IamTokenServiceStub)
    req = CreateIamTokenRequest(yandex_passport_oauth_token=oauth_token)
    resp = client.Create(req)
    return resp.iam_token


def create_iam_token_with_yc() -> str:
    logger.debug('oauth token is not provided, creating iam token through `yc` ...')
    try:
        # TODO: capture stderr, process return code
        process = subprocess.run(
            ['yc', 'iam', 'create-token', '--no-user-output'],
            stdout=subprocess.PIPE, universal_newlines=True,
        )
    except FileNotFoundError:
        raise RuntimeError('You have not provided OAuth token. You have to install Yandex Cloud CLI '
                           '(https://cloud.yandex.com/docs/cli/) to authenticate automatically.')

    # There may be another output before the token, for example, info about opening the browser.
    # TODO: not sure if token will be last line (update suggestion appears regardless of --no-user-output flag
    return process.stdout.strip().split('\n')[-1]


def get_md(oauth_token: Optional[str]) -> List[Tuple[str, str]]:
    if env != ServerEnv.DEV:
        iam_token = create_iam_token(oauth_token)
        return [('authorization', f'Bearer {iam_token}')]
    return []
