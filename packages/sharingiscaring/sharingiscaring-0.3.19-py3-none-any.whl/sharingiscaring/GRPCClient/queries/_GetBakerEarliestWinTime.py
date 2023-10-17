# ruff: noqa: F403, F405, E402
from __future__ import annotations
from sharingiscaring.GRPCClient.types_pb2 import *
from sharingiscaring.enums import NET
from sharingiscaring.GRPCClient.queries._SharedConverters import (
    Mixin as _SharedConverters,
)
from typing import TYPE_CHECKING
import sys
import grpc
from datetime import timezone

if TYPE_CHECKING:
    from sharingiscaring.GRPCClient import GRPCClient
from sharingiscaring.GRPCClient.CCD_Types import *


class Mixin(_SharedConverters):
    def get_baker_earliest_win_time(
        self: GRPCClient,
        baker_id: int,
        net: Enum = NET.MAINNET,
    ) -> CCD_TimeStamp:
        self.check_connection(net, sys._getframe().f_code.co_name)
        if net == NET.MAINNET:
            stub = self.stub_mainnet
        else:
            stub = self.stub_testnet

        try:
            grpc_return_value: BlockInfo = stub.GetBakerEarliestWinTime(
                request=BakerId(value=baker_id)
            )
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.UNIMPLEMENTED:
                print("Not implemented on mainnet")
                return None

        win_time = None

        for descriptor in grpc_return_value.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(
                descriptor, grpc_return_value
            )

            if key == "value":
                win_time = dt.datetime.fromtimestamp(value / 1_000).astimezone(
                    tz=timezone.utc
                )

        return win_time
