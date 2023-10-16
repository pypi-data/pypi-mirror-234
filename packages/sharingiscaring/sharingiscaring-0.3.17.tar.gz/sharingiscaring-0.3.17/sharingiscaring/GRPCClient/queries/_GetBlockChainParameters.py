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
    def convertAccountAmountsEntries(
        self, message
    ) -> list[CCD_BlockSpecialEvent_AccountAmounts_Entry]:
        entries = []

        for list_entry in message:
            entries.append(
                CCD_BlockSpecialEvent_AccountAmounts_Entry(
                    **self.convertTypeWithSingleValues(list_entry)
                )
            )

        return entries

    def convertAccountAmountsBakingRewards(
        self, message
    ) -> CCD_BlockSpecialEvent_BakingRewards:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            result[key] = self.convertAccountAmountsEntries(value)

        return CCD_BlockSpecialEvent_AccountAmounts(**result)

    def convertAccountAmountsFinalizationRewards(
        self, message
    ) -> CCD_BlockSpecialEvent_FinalizationRewards:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            result[key] = self.convertAccountAmountsEntries(value)

        return CCD_BlockSpecialEvent_AccountAmounts(**result)

    def convertBakingRewards(self, message) -> CCD_BlockSpecialEvent_BakingRewards:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)

            if type(value) == BlockSpecialEvent.AccountAmounts:
                result[key] = self.convertAccountAmountsBakingRewards(value)

            elif type(value) in self.simple_types:
                result[key] = self.convertType(value)

        return CCD_BlockSpecialEvent_BakingRewards(**result)

    def convertFinalizationRewards(
        self, message
    ) -> CCD_BlockSpecialEvent_FinalizationRewards:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)

            if type(value) == BlockSpecialEvent.AccountAmounts:
                result[key] = self.convertAccountAmountsFinalizationRewards(value)

            elif type(value) in self.simple_types:
                result[key] = self.convertType(value)

        return CCD_BlockSpecialEvent_FinalizationRewards(**result)

    def convertv0(self, message) -> CCD_ChainParametersV0:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)

            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

            elif type(value) == ExchangeRate:
                value_as_dict = MessageToDict(value)
                result[key] = CCD_ExchangeRate(
                    **{
                        "numerator": value_as_dict["value"]["numerator"],
                        "denominator": value_as_dict["value"]["denominator"],
                    }
                )

            elif type(value) == MintDistributionCpv0:
                result[key] = self.convertMintDistributionCpv0(value)

            elif type(value) == TransactionFeeDistribution:
                result[key] = self.convertTransactionFeeDistribution(value)

            elif type(value) == GasRewards:
                result[key] = self.convertGasRewards(value)

            elif type(value) == HigherLevelKeys:
                result[key] = self.convertHigherLevelKeys(value)

            elif type(value) == AuthorizationsV0:
                result[key] = self.convertAuthorizationsV0(value)

        return CCD_ChainParametersV0(**result)

    def convertv1(self, message) -> CCD_ChainParametersV1:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)

            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

            elif type(value) == CooldownParametersCpv1:
                result[key] = self.convertCooldownParametersCpv1(value)

            elif type(value) == TimeParametersCpv1:
                result[key] = self.convertTimeParametersCpv1(value)

            elif type(value) == ExchangeRate:
                value_as_dict = MessageToDict(value)
                result[key] = CCD_ExchangeRate(
                    **{
                        "numerator": value_as_dict["value"]["numerator"],
                        "denominator": value_as_dict["value"]["denominator"],
                    }
                )

            elif type(value) == MintDistributionCpv1:
                result[key] = self.convertMintDistributionCpv1(value)

            elif type(value) == TransactionFeeDistribution:
                result[key] = self.convertTransactionFeeDistribution(value)

            elif type(value) == GasRewards:
                result[key] = self.convertGasRewards(value)

            elif type(value) == PoolParametersCpv1:
                result[key] = self.convertPoolParametersCpv1(value)

            elif type(value) == HigherLevelKeys:
                result[key] = self.convertHigherLevelKeys(value)

            elif type(value) == AuthorizationsV1:
                result[key] = self.convertAuthorizationsV1(value)

        return CCD_ChainParametersV1(**result)

    def convertv2(self, message) -> CCD_ChainParametersV2:
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)

            if type(value) in self.simple_types:
                result[key] = self.convertType(value)

            elif type(value) == ConsensusParametersV1:
                result[key] = self.convertConsensusParametersV1(value)

            elif type(value) == CooldownParametersCpv1:
                result[key] = self.convertCooldownParametersCpv1(value)

            elif type(value) == TimeParametersCpv1:
                result[key] = self.convertTimeParametersCpv1(value)

            elif type(value) == ExchangeRate:
                value_as_dict = MessageToDict(value)
                result[key] = CCD_ExchangeRate(
                    **{
                        "numerator": value_as_dict["value"]["numerator"],
                        "denominator": value_as_dict["value"]["denominator"],
                    }
                )

            elif type(value) == MintDistributionCpv1:
                result[key] = self.convertMintDistributionCpv1(value)

            elif type(value) == TransactionFeeDistribution:
                result[key] = self.convertTransactionFeeDistribution(value)

            elif type(value) == GasRewardsCpv2:
                result[key] = self.convertGasRewardsV2(value)

            elif type(value) == PoolParametersCpv1:
                result[key] = self.convertPoolParametersCpv1(value)

            elif type(value) == HigherLevelKeys:
                result[key] = self.convertHigherLevelKeys(value)

            elif type(value) == AuthorizationsV1:
                result[key] = self.convertAuthorizationsV1(value)

            elif type(value) == FinalizationCommitteeParameters:
                result[key] = self.convertFinalizationCommitteeParameters(value)

        return CCD_ChainParametersV2(**result)

    def get_block_chain_parameters(
        self: GRPCClient,
        block_hash: str,
        net: Enum = NET.MAINNET,
    ) -> CCD_ChainParameters:
        result = {}

        blockHashInput = self.generate_block_hash_input_from(block_hash)

        self.check_connection(net, sys._getframe().f_code.co_name)
        if net == NET.MAINNET:
            grpc_return_value: ChainParameters = (
                self.stub_mainnet.GetBlockChainParameters(request=blockHashInput)
            )
        else:
            grpc_return_value: ChainParameters = (
                self.stub_testnet.GetBlockChainParameters(request=blockHashInput)
            )

        for descriptor in grpc_return_value.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(
                descriptor, grpc_return_value
            )

            if key == "v0" and not self.valueIsEmpty(value):
                # result_type = "v0"
                result[key] = self.convertv0(value)

            elif key == "v1" and not self.valueIsEmpty(value):
                # result_type = "v1"
                result[key] = self.convertv1(value)

            elif key == "v2" and not self.valueIsEmpty(value):
                # result_type = "v2"
                result[key] = self.convertv2(value)

        return CCD_ChainParameters(**result)
