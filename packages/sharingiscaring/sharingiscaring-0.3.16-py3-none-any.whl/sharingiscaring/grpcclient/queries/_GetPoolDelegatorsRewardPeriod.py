# ruff: noqa: F403, F405, E402
from __future__ import annotations
from sharingiscaring.GRPCClient.types_pb2 import *
from sharingiscaring.enums import NET
from enum import Enum
from sharingiscaring.GRPCClient.queries._SharedConverters import (
    Mixin as _SharedConverters,
)
from typing import Iterator
from typing import TYPE_CHECKING
import sys

if TYPE_CHECKING:
    from sharingiscaring.GRPCClient import GRPCClient
from sharingiscaring.GRPCClient.CCD_Types import CCD_DelegatorRewardPeriodInfo


class Mixin(_SharedConverters):
    def get_delegators_for_pool_in_reward_period(
        self: GRPCClient,
        pool_id: int,
        block_hash: str,
        net: Enum = NET.MAINNET,
    ) -> list[CCD_DelegatorRewardPeriodInfo]:
        result = []
        blockHashInput = self.generate_block_hash_input_from(block_hash)
        baker_id = BakerId(value=pool_id)
        delegatorsRequest = GetPoolDelegatorsRequest(
            baker=baker_id, block_hash=blockHashInput
        )

        self.check_connection(net, sys._getframe().f_code.co_name)
        if net == NET.MAINNET:
            grpc_return_value: Iterator[
                DelegatorRewardPeriodInfo
            ] = self.stub_mainnet.GetPoolDelegatorsRewardPeriod(
                request=delegatorsRequest
            )
        else:
            grpc_return_value: Iterator[
                DelegatorRewardPeriodInfo
            ] = self.stub_testnet.GetPoolDelegatorsRewardPeriod(
                request=delegatorsRequest
            )

        for delegator in list(grpc_return_value):
            result.append(
                CCD_DelegatorRewardPeriodInfo(
                    **{
                        "account": self.convertAccountAddress(delegator.account),
                        "stake": self.convertAmount(delegator.stake),
                    }
                )
            )

        return result
