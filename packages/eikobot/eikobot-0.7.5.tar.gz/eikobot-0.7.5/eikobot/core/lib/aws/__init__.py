"""
Abstracts the management of AWS resources,
such IAM credentials, IAM roles, VPCs, VMs and EKS clusters.
"""
from eikobot.core.handlers import CRUDHandler, HandlerContext
from eikobot.core.helpers import EikoBaseModel

from . import aws_api


class IAMRoleModel(EikoBaseModel):
    """
    An IAM role in AWS.
    """

    __eiko_resource__ = "IAMRole"

    name: str
    permissions: list[str]


class IAMRoleHandler(CRUDHandler):
    """
    An IAM role in AWS.
    """

    __eiko_resource__ = "IAMRole"

    async def read(self, ctx: HandlerContext[IAMRoleModel]) -> None:
        pass

    async def create(self, ctx: HandlerContext[IAMRoleModel]) -> None:
        pass
