"""
Contains wrappers around the AWS api.
Allowing the use of async calls to it.
"""
import json
from asyncio.subprocess import PIPE, create_subprocess_shell
from datetime import datetime

from pydantic import BaseModel

from eikobot.core.errors import EikoError


class AWSCredential(BaseModel):
    """
    A set of credentials retrieved using the AWS API.
    """

    access_key_id: str
    secret_access_key: str
    session_token: str
    expiration: datetime

    def __repr__(self) -> str:
        _repr = f"AWSCredential(access_key_id: {self.access_key_id}, "
        _repr += f"secret_access_key: ****, session_token: ****, expiration: {self.expiration})"
        return _repr


_AWS_CREDENTIAL: AWSCredential | None = None


async def _get_credentials() -> AWSCredential:
    """
    Gets a set of useable keys and tokens using a configured aws CLI.
    """
    global _AWS_CREDENTIAL  # pylint: disable=global-statement
    if _AWS_CREDENTIAL is not None:
        return _AWS_CREDENTIAL

    process = await create_subprocess_shell(
        "aws sts get-session-token",
        stdout=PIPE,
        stderr=PIPE,
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        raise EikoError(
            f"Failed to get aws token: \n{stdout.decode('utf-8')}\n{stderr.decode('utf-8')}"
        )

    credentials = json.loads(stdout)["Credentials"]
    _AWS_CREDENTIAL = AWSCredential(
        access_key_id=credentials["AccessKeyId"],
        secret_access_key=credentials["SecretAccessKey"],
        session_token=credentials["SessionToken"],
        expiration=credentials["Expiration"],
    )

    return _AWS_CREDENTIAL
