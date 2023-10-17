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
from sharingiscaring.GRPCClient.CCD_Types import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sharingiscaring.GRPCClient import GRPCClient


class Mixin(_SharedConverters):
    def convertTokenomicsV0(self, message) -> CCD_TokenomicsInfo_V0:
        if self.valueIsEmpty(message):
            return None
        else:
            result = {}
            for descriptor in message.DESCRIPTOR.fields:
                key, value = self.get_key_value_from_descriptor(descriptor, message)

                if type(value) in self.simple_types:
                    result[key] = self.convertType(value)

            return CCD_TokenomicsInfo_V0(**result)

    def convertTokenomicsV1(self, message) -> CCD_TokenomicsInfo_V1:
        if self.valueIsEmpty(message):
            return None
        else:
            result = {}
            for descriptor in message.DESCRIPTOR.fields:
                key, value = self.get_key_value_from_descriptor(descriptor, message)

                if type(value) in self.simple_types:
                    result[key] = self.convertType(value)

                elif type(value) == MintRate:
                    result[key] = CCD_MintRate(
                        **{"mantissa": value.mantissa, "exponent": value.exponent}
                    )

            return CCD_TokenomicsInfo_V1(**result)

    def get_tokenomics_info(
        self: GRPCClient,
        block_hash: str,
        net: Enum = NET.MAINNET,
    ) -> CCD_TokenomicsInfo:
        prefix = ""
        result = {}
        blockHashInput = self.generate_block_hash_input_from(block_hash)

        self.check_connection(net, sys._getframe().f_code.co_name)
        if net == NET.MAINNET:
            grpc_return_value: BlockInfo = self.stub_mainnet.GetTokenomicsInfo(
                request=blockHashInput
            )
        else:
            grpc_return_value: BlockInfo = self.stub_testnet.GetTokenomicsInfo(
                request=blockHashInput
            )

        for descriptor in grpc_return_value.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(
                descriptor, grpc_return_value
            )

            if type(value) == TokenomicsInfo.V0:
                result[f"{prefix}{key}"] = self.convertTokenomicsV0(value)
            elif type(value) == TokenomicsInfo.V1:
                result[f"{prefix}{key}"] = self.convertTokenomicsV1(value)

        return CCD_TokenomicsInfo(**result)
