# ruff: noqa: F403, F405, E402
from __future__ import annotations
import sys
import os


sys.path.append(os.path.dirname("sharingiscaring"))
from sharingiscaring.GRPCClient.service_pb2_grpc import QueriesStub


from sharingiscaring.GRPCClient.types_pb2 import *
import grpc
from sharingiscaring.enums import NET
import sys
import os
from rich.console import Console

console = Console()

HOME_IP = os.environ.get("HOME_IP", "")

from sharingiscaring.GRPCClient.queries._GetPoolInfo import Mixin as _GetPoolInfo
from sharingiscaring.GRPCClient.queries._GetPoolDelegatorsRewardPeriod import (
    Mixin as _GetPoolDelegatorsRewardPeriod,
)
from sharingiscaring.GRPCClient.queries._GetPassiveDelegatorsRewardPeriod import (
    Mixin as _GetPassiveDelegatorsRewardPeriod,
)
from sharingiscaring.GRPCClient.queries._GetAccountList import Mixin as _GetAccountList
from sharingiscaring.GRPCClient.queries._GetBakerList import Mixin as _GetBakerList
from sharingiscaring.GRPCClient.queries._GetBlocksAtHeight import (
    Mixin as _GetBlocksAtHeight,
)
from sharingiscaring.GRPCClient.queries._GetFinalizedBlocks import (
    Mixin as _GetFinalizedBlocks,
)
from sharingiscaring.GRPCClient.queries._GetInstanceInfo import (
    Mixin as _GetInstanceInfo,
)
from sharingiscaring.GRPCClient.queries._GetInstanceList import (
    Mixin as _GetInstanceList,
)
from sharingiscaring.GRPCClient.queries._GetAnonymityRevokers import (
    Mixin as _GetAnonymityRevokers,
)
from sharingiscaring.GRPCClient.queries._GetIdentityProviders import (
    Mixin as _GetIdentityProviders,
)
from sharingiscaring.GRPCClient.queries._GetPoolDelegators import (
    Mixin as _GetPoolDelegators,
)
from sharingiscaring.GRPCClient.queries._GetPassiveDelegators import (
    Mixin as _GetPassiveDelegators,
)
from sharingiscaring.GRPCClient.queries._GetAccountInfo import Mixin as _GetAccountInfo
from sharingiscaring.GRPCClient.queries._GetBlockInfo import Mixin as _GetBlockInfo
from sharingiscaring.GRPCClient.queries._GetElectionInfo import (
    Mixin as _GetElectionInfo,
)
from sharingiscaring.GRPCClient.queries._GetTokenomicsInfo import (
    Mixin as _GetTokenomicsInfo,
)
from sharingiscaring.GRPCClient.queries._GetPassiveDelegationInfo import (
    Mixin as _GetPassiveDelegationInfo,
)
from sharingiscaring.GRPCClient.queries._GetBlockTransactionEvents import (
    Mixin as _GetBlockTransactionEvents,
)
from sharingiscaring.GRPCClient.queries._GetBlockSpecialEvents import (
    Mixin as _GetBlockSpecialEvents,
)
from sharingiscaring.GRPCClient.queries._GetBlockPendingUpdates import (
    Mixin as _GetBlockPendingUpdates,
)
from sharingiscaring.GRPCClient.queries._GetModuleSource import (
    Mixin as _GetModuleSource,
)
from sharingiscaring.GRPCClient.queries._GetBlockChainParameters import (
    Mixin as _GetBlockChainParameters,
)
from sharingiscaring.GRPCClient.queries._InvokeInstance import (
    Mixin as _InvokeInstance,
)
from sharingiscaring.GRPCClient.queries._GetConsensusInfo import (
    Mixin as _GetConsensusInfo,
)

from sharingiscaring.GRPCClient.queries._CheckHealth import (
    Mixin as _CheckHealth,
)


class GRPCClient(
    _GetPoolInfo,
    _GetAccountList,
    _GetBakerList,
    _GetInstanceInfo,
    _GetInstanceList,
    _GetFinalizedBlocks,
    _GetBlocksAtHeight,
    _GetIdentityProviders,
    _GetAnonymityRevokers,
    _GetPassiveDelegationInfo,
    _GetPassiveDelegators,
    _GetPoolDelegators,
    _GetPoolDelegatorsRewardPeriod,
    _GetPassiveDelegatorsRewardPeriod,
    _GetAccountInfo,
    _GetBlockInfo,
    _GetElectionInfo,
    _GetBlockTransactionEvents,
    _GetBlockSpecialEvents,
    _GetBlockPendingUpdates,
    _GetTokenomicsInfo,
    _GetModuleSource,
    _GetBlockChainParameters,
    _InvokeInstance,
    _GetConsensusInfo,
    _CheckHealth,
):
    def __init__(self, net: str = "mainnet"):
        self.net = NET(net)
        # self.channel_mainnet: grpc.Channel
        # self.channel_testnet: grpc.Channel
        self.stub_mainnet: QueriesStub
        self.stub_testnet: QueriesStub
        # self.stub_to_net: dict[NET:QueriesStub]
        self.host_index = {NET.MAINNET: 0, NET.TESTNET: 0}
        self.hosts = {}
        self.hosts[NET.MAINNET] = [
            {"host": "localhost", "port": 20000},
            {"host": "contabo.sprocker.nl", "port": 20000},
            {"host": "primary.sprocker.nl", "port": 20001},
        ]
        self.hosts[NET.TESTNET] = [
            {"host": "localhost", "port": 20001},
            {"host": "primary.sprocker.nl", "port": 20002},
            {"host": "contabo.sprocker.nl", "port": 20002},
        ]
        self.connect()

    def connect(self):
        host = self.hosts[NET.MAINNET][self.host_index[NET.MAINNET]]["host"]
        port = self.hosts[NET.MAINNET][self.host_index[NET.MAINNET]]["port"]
        self.channel_mainnet = grpc.insecure_channel(f"{host}:{port}")
        try:
            grpc.channel_ready_future(self.channel_mainnet).result(timeout=1)
            console.log(
                f"GRPCClient for {NET.MAINNET.value} connected on: {host}:{port}"
            )
        except grpc.FutureTimeoutError:
            pass

        host = self.hosts[NET.TESTNET][self.host_index[NET.TESTNET]]["host"]
        port = self.hosts[NET.TESTNET][self.host_index[NET.TESTNET]]["port"]
        self.channel_testnet = grpc.insecure_channel(f"{host}:{port}")
        try:
            grpc.channel_ready_future(self.channel_testnet).result(timeout=1)
            console.log(
                f"GRPCClient for {NET.TESTNET.value} connected on: {host}:{port}"
            )
        except grpc.FutureTimeoutError:
            pass

        self.stub_mainnet = QueriesStub(self.channel_mainnet)
        self.stub_testnet = QueriesStub(self.channel_testnet)

        self.channel = grpc.insecure_channel(
            f"{self.hosts[self.net][self.host_index[self.net]]['host']}:{self.hosts[self.net][self.host_index[self.net]]['port']}"
        )

        self.stub = QueriesStub(self.channel)

    def switch_to_net(self, net: str = "mainnet"):
        # only switch when we need to connect to a different net
        if not net:
            net = NET.MAINNET.value

        if net != self.net.value:
            self.net = NET(net)
            self.connect()

    def check_connection(self, net: NET = NET.MAINNET, function_name=None):
        connected = {NET.MAINNET: False, NET.TESTNET: False}

        while not connected[net]:
            channel_to_check = (
                self.channel_mainnet if net == NET.MAINNET else self.channel_testnet
            )
            try:
                grpc.channel_ready_future(channel_to_check).result(timeout=1)
                connected[net] = True

            except grpc.FutureTimeoutError:
                console.log(
                    f"""GRPCClient for {net.value} Timeout for :
                      {self.hosts[net][self.host_index[net]]['host']}:
                      {self.hosts[net][self.host_index[net]]['port']}"""
                )
                self.host_index[net] += 1
                if self.host_index[net] == len(self.hosts[net]):
                    self.host_index[net] = 0
                self.connect()
