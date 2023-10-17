# ruff: noqa: F403, F405, E402
from __future__ import annotations
from sharingiscaring.GRPCClient.types_pb2 import *
from sharingiscaring.enums import NET
from sharingiscaring.GRPCClient.queries._SharedConverters import (
    Mixin as _SharedConverters,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sharingiscaring.GRPCClient import GRPCClient
import os
import sys

sys.path.append(os.path.dirname("sharingiscaring"))
from sharingiscaring.GRPCClient.CCD_Types import *
from google.protobuf.json_format import MessageToDict


class Mixin(_SharedConverters):
    def convertUpdatePayload(self, message) -> CCD_UpdatePayload:
        if MessageToDict(message) == {}:
            return None
        else:
            result = {}
            _type = {"type": "update"}
            for descriptor in message.DESCRIPTOR.fields:
                key, value = self.get_key_value_from_descriptor(descriptor, message)

                if self.valueIsEmpty(value):
                    pass
                else:
                    _type.update({"contents": key})

            return CCD_UpdatePayload(**result), _type

    def convertUpdateDetails(self, message) -> CCD_AccountCreationDetails:
        if MessageToDict(message) == {}:
            return None
        else:
            result = {}
            _type = {"type": "update"}
            for descriptor in message.DESCRIPTOR.fields:
                key, value = self.get_key_value_from_descriptor(descriptor, message)

                if self.valueIsEmpty(value):
                    pass
                else:
                    if type(value) == UpdatePayload:
                        result[key], _type = self.convertUpdatePayload(value)

                    elif type(value) in self.simple_types:
                        result[key] = self.convertType(value)

            return CCD_UpdateDetails(**result), _type

    def get_block_pending_updates(
        self: GRPCClient,
        block_hash: str,
        net: Enum = NET.MAINNET,
    ) -> list[CCD_BlockSpecialEvent]:
        blockHashInput = self.generate_block_hash_input_from(block_hash)

        self.check_connection(net, sys._getframe().f_code.co_name)
        if net == NET.MAINNET:
            grpc_return_value = self.stub_mainnet.GetBlockPendingUpdates(
                request=blockHashInput
            )
        else:
            grpc_return_value = self.stub_testnet.GetBlockPendingUpdates(
                request=blockHashInput
            )

        events = []
        for tx in list(grpc_return_value):
            result = {}
            for descriptor in tx.DESCRIPTOR.fields:
                key, value = self.get_key_value_from_descriptor(descriptor, tx)
                if self.valueIsEmpty(value):
                    pass
                else:
                    if type(value) == ExchangeRate:
                        value_as_dict = MessageToDict(value)
                        result[key] = CCD_ExchangeRate(
                            **{
                                "numerator": value_as_dict["value"]["numerator"],
                                "denominator": value_as_dict["value"]["denominator"],
                            }
                        )

                    elif type(value) in [BakerStakeThreshold, ProtocolUpdate]:
                        result[key] = self.convertTypeWithSingleValues(value)

                    elif type(value) == Level1Update:
                        result[key] = self.convertLevel1Update(value)

                    elif type(value) == IpInfo:
                        result[key] = self.convertIpInfo(value)

                    elif type(value) in self.simple_types:
                        result[key] = self.convertType(value)

                    # TODO: no test available
                    elif type(value) == ElectionDifficulty:
                        result[key] = self.convertElectionDifficulty(value)

                    # TODO: no test available
                    elif type(value) == MintDistributionCpv0:
                        result[key] = self.convertMintDistributionCpv0(value)

                    # TODO: no test available
                    elif type(value) == TransactionFeeDistribution:
                        result[key] = self.convertTransactionFeeDistribution(value)

                    # TODO: no test available
                    elif type(value) == GasRewards:
                        result[key] = self.convertGasRewards(value)

                    # TODO: no test available
                    elif type(value) == RootUpdate:
                        result[key] = self.convertRootUpdate(value)

                    # TODO: no test available
                    elif type(value) == ArInfo:
                        result[key] = self.convertArInfo(value)

                    # TODO: no test available
                    elif type(value) == CooldownParametersCpv1:
                        result[key] = self.convertCooldownParametersCpv1(value)

                    # TODO: no test available
                    elif type(value) == PoolParametersCpv1:
                        result[key] = self.convertPoolParametersCpv1(value)

                    # TODO: no test available
                    elif type(value) == TimeParametersCpv1:
                        result[key] = self.convertTimeParametersCpv1(value)

                    # TODO: no test available
                    elif type(value) == MintDistributionCpv1:
                        result[key] = self.convertMintDistributionCpv1(value)
            events.append(CCD_BlockSpecialEvent(**result))

        return events
