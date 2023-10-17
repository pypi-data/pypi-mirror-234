# ruff: noqa: F403, F405, E402
from __future__ import annotations
from sharingiscaring.GRPCClient.types_pb2 import *
from sharingiscaring.enums import NET
from sharingiscaring.GRPCClient.queries._SharedConverters import (
    Mixin as _SharedConverters,
)
import sys
from typing import Iterator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sharingiscaring.GRPCClient import GRPCClient
from sharingiscaring.GRPCClient.CCD_Types import *


class Mixin(_SharedConverters):
    def get_identity_providers(
        self: GRPCClient,
        block_hash: str,
        net: Enum = NET.MAINNET,
    ) -> list[CCD_IpInfo]:
        result = []
        blockHashInput = self.generate_block_hash_input_from(block_hash)

        self.check_connection(net, sys._getframe().f_code.co_name)
        if net == NET.MAINNET:
            grpc_return_value: Iterator[
                IpInfo
            ] = self.stub_mainnet.GetIdentityProviders(request=blockHashInput)
        else:
            grpc_return_value: Iterator[
                IpInfo
            ] = self.stub_testnet.GetIdentityProviders(request=blockHashInput)

        for ip in list(grpc_return_value):
            result.append(self.convertIpInfo(ip))

        return result
