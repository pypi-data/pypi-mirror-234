# ruff: noqa: F403, F405, E402
from __future__ import annotations
from sharingiscaring.GRPCClient.types_pb2 import *
from sharingiscaring.enums import NET
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sharingiscaring.GRPCClient import GRPCClient
from sharingiscaring.GRPCClient.queries._SharedConverters import (
    Mixin as _SharedConverters,
)
import os
import sys

sys.path.append(os.path.dirname("sharingiscaring"))
from sharingiscaring.GRPCClient.CCD_Types import *


class Mixin(_SharedConverters):
    def convertSuccess(self, message) -> CCD_InvokeInstanceResponse_Success:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if key == "effects":
                result[key] = self.convertUpdateEvents(value)

            elif type(value) in self.simple_types:
                result[key] = self.convertType(value)

        return CCD_InvokeInstanceResponse_Success(**result)

    def convertFailure(self, message) -> CCD_InvokeInstanceResponse_Failure:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) == RejectReason:
                result[key], _ = self.convertRejectReason(value)

            elif type(value) in self.simple_types:
                result[key] = self.convertType(value)

        return CCD_InvokeInstanceResponse_Failure(**result)

    def invoke_instance(
        self: GRPCClient,
        block_hash: str,
        instance_index: int,
        instance_subindex: int,
        entrypoint: str,
        parameter_bytes: bytes,
        net: Enum = NET.MAINNET,
    ) -> CCD_InvokeInstanceResponse:
        result = {}
        blockHashInput = self.generate_block_hash_input_from(block_hash)
        invokeInstanceRequest = self.generate_invoke_instance_request_from(
            instance_index,
            instance_subindex,
            blockHashInput,
            entrypoint,
            parameter_bytes,
        )
        self.check_connection(net, sys._getframe().f_code.co_name)
        if net == NET.MAINNET:
            grpc_return_value: InvokeInstanceResponse = (
                self.stub_mainnet.InvokeInstance(request=invokeInstanceRequest)
            )
        else:
            grpc_return_value: InvokeInstanceResponse = (
                self.stub_testnet.InvokeInstance(request=invokeInstanceRequest)
            )

        for descriptor in grpc_return_value.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(
                descriptor, grpc_return_value
            )

            if type(value) == InvokeInstanceResponse.Success:
                result[key] = self.convertSuccess(value)

            elif type(value) == InvokeInstanceResponse.Failure:
                result[key] = self.convertFailure(value)

        return CCD_InvokeInstanceResponse(**result)
