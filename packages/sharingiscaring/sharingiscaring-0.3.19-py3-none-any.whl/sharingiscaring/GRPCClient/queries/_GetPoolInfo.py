# ruff: noqa: F403, F405, E402
from __future__ import annotations
from sharingiscaring.GRPCClient.types_pb2 import *
from sharingiscaring.enums import NET
from enum import Enum
from sharingiscaring.GRPCClient.queries._SharedConverters import (
    Mixin as _SharedConverters,
)
import os
import sys

sys.path.append(os.path.dirname("sharingiscaring"))
# from sharingiscaring.pool import ConcordiumPoolFromClient
from sharingiscaring.GRPCClient.CCD_Types import CCD_PoolInfo
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sharingiscaring.GRPCClient import GRPCClient


class Mixin(_SharedConverters):
    def get_pool_info_for_pool(
        self: GRPCClient,
        pool_id: int,
        block_hash: str,
        net: Enum = NET.MAINNET,
    ) -> CCD_PoolInfo:
        prefix = ""
        result = {}
        blockHashInput = self.generate_block_hash_input_from(block_hash)
        baker_id = BakerId(value=pool_id)
        poolInfoRequest = PoolInfoRequest(baker=baker_id, block_hash=blockHashInput)

        self.check_connection(net, sys._getframe().f_code.co_name)
        if net == NET.MAINNET:
            grpc_return_value: PoolInfoResponse = self.stub_mainnet.GetPoolInfo(
                request=poolInfoRequest
            )
        else:
            grpc_return_value: PoolInfoResponse = self.stub_testnet.GetPoolInfo(
                request=poolInfoRequest
            )

        for descriptor in grpc_return_value.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(
                descriptor, grpc_return_value
            )
            key_to_store = f"{prefix}{key}"
            if type(value) in self.simple_types:
                result[key_to_store] = self.convertType(value)

            elif type(value) == BakerPoolInfo:
                result[key_to_store] = self.convertBakerPoolInfo(value)

            elif type(value) == PoolCurrentPaydayInfo:
                if self.valueIsEmpty(value):
                    result[key_to_store] = None
                else:
                    result[key_to_store] = self.convertPoolCurrentPaydayInfo(value)

            elif type(value) == PoolPendingChange:
                result[key_to_store] = self.convertPoolPendingChange(value)

        return CCD_PoolInfo(**result)
