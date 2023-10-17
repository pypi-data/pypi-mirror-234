"""
Abstracted boto3 functionality
"""
from typing import TYPE_CHECKING

import boto3

if TYPE_CHECKING:
    from mypy_boto3_ec2 import EC2Client
    from mypy_boto3_ec2.type_defs import TagTypeDef


class BotoCache:
    _ec2_clients: dict[str, "EC2Client"] = {}

    @classmethod
    def get_ec2_client(cls, region: str) -> "EC2Client":
        """
        Retrieves a cached client or creates and caches it.
        """
        client = cls._ec2_clients.get(region)
        if client is None:
            client = boto3.client("ec2", region_name=region)
            cls._ec2_clients[region] = client

        return client


def import_key_pair(
    public_key: bytes,
    key_name: str,
    region: str,
    dry_run: bool = False,
    tags: dict[str, str] | None = None,
) -> None:
    """
    Import a key pair to a specific region.
    """
    _tags: list["TagTypeDef"] = []
    if tags is not None:
        for key, value in tags.items():
            _tags.append({"Key": key, "Value": value})

    client = BotoCache.get_ec2_client(region)
    response = client.import_key_pair(
        DryRun=dry_run,
        KeyName=key_name,
        PublicKeyMaterial=public_key,
        TagSpecifications=[
            {
                "ResourceType": "key-pair",
                "Tags": _tags,
            }
        ],
    )
