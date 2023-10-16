# ruff: noqa: F403, F405, E402
from __future__ import annotations
from sharingiscaring.GRPCClient.types_pb2 import *
from sharingiscaring.enums import NET
from enum import Enum
from sharingiscaring.GRPCClient.queries._SharedConverters import (
    Mixin as _SharedConverters,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sharingiscaring.GRPCClient import GRPCClient
import os
import sys
from typing import Iterator

sys.path.append(os.path.dirname("sharingiscaring"))
from sharingiscaring.GRPCClient.CCD_Types import CCD_BlockInfo, CCD_BlockHash


class Mixin(_SharedConverters):
    def get_blocks_at_height(
        self: GRPCClient,
        block_height: int,
        net: Enum = NET.MAINNET,
    ) -> list[CCD_BlockHash]:
        result = []
        absoluteBlockHeight = AbsoluteBlockHeight(value=block_height)
        blocksAtHeightRequestAbsolute = BlocksAtHeightRequest.Absolute(
            height=absoluteBlockHeight
        )
        blocksAtHeightRequest = BlocksAtHeightRequest(
            absolute=blocksAtHeightRequestAbsolute
        )

        self.check_connection(net, sys._getframe().f_code.co_name)
        if net == NET.MAINNET:
            grpc_return_value: Iterator[
                BlocksAtHeightResponse
            ] = self.stub_mainnet.GetBlocksAtHeight(request=blocksAtHeightRequest)
        else:
            grpc_return_value: Iterator[
                BlocksAtHeightResponse
            ] = self.stub_testnet.GetBlocksAtHeight(request=blocksAtHeightRequest)

        for descriptor in grpc_return_value.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(
                descriptor, grpc_return_value
            )

            if key == "blocks":
                result = self.convertList(value)

        return result

    def get_finalized_block_at_height(
        self,
        block_height: int,
        net: Enum = NET.MAINNET,
    ) -> CCD_BlockInfo:
        # blocks_at_height = self.get_blocks_at_height(block_height, net)
        try:
            bi: CCD_BlockInfo = self.get_block_info(block_height, net)
        except:  # noqa
            return None
        if bi.finalized:
            return bi

        return None
