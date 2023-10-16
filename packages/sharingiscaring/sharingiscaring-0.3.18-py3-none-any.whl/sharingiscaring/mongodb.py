# ruff: noqa :E501
from enum import Enum
from sharingiscaring.mongodb_queries._search_transfers import Mixin as _search_transfers
from sharingiscaring.mongodb_queries._subscriptions import Mixin as _subscriptions
from sharingiscaring.mongodb_queries._baker_distributions import Mixin as _distributions
from sharingiscaring.mongodb_queries._store_block import Mixin as _store_block
from sharingiscaring.mongodb_queries._apy_calculations import Mixin as _apy_calculations
from sharingiscaring.GRPCClient.CCD_Types import *  # noqa: F403

import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import MongoClient
from pymongo.collection import Collection

from rich.console import Console
from typing import Dict, Optional, Union
from sharingiscaring.tooter import Tooter, TooterType, TooterChannel
from pydantic import BaseModel, Field
import datetime as dt

console = Console()


class MongoTypeBlockPerDay(BaseModel):
    """
    Block Per Day. This type is stored in the collection `blocks_per_day`.

    :Parameters:
    - `_id`: the date of the day that ended
    - `date`: the date of the day that ended
    - `height_for_first_block`: height of the first block in the day
    - `height_for_last_block`: height of the last block in the day
    - `slot_time_for_first_block`: time of the first block in the day
    - `slot_time_for_last_block`: time of the last block in the day
    - `hash_for_first_block`: hash of the first block in the day
    - `hash_for_last_block`: hash of the last block in the day

    """

    id: str = Field(..., alias="_id")
    date: str
    height_for_first_block: int
    height_for_last_block: int
    slot_time_for_first_block: dt.datetime
    slot_time_for_last_block: dt.datetime
    hash_for_first_block: str
    hash_for_last_block: str


class MongoTypeInvolvedAccount(BaseModel):
    """
    Involved Account. This type is stored in the collections `involved_accounts_all` and
    `involved_accounts_transfer`.

    :Parameters:
    - `_id`: the hash of the transaction
    - `sender`: the sender account address
    - `receiver`: the receiver account address, might be null
    - `sender_canonical`: the canonical sender account address
    - `receiver_canonical`: the  canonical receiver account address, might be null
    - `amount`: amount of the transaction, might be null
    - `type`: dict with transaction `type` and `contents`
    - `block_height`: height of the block in which the transaction is executed
    """

    id: str = Field(..., alias="_id")
    sender: str
    receiver: Optional[str] = None
    sender_canonical: str
    receiver_canonical: Optional[str] = None
    amount: Optional[int] = None
    type: dict[str, str]
    block_height: int
    memo: Optional[int] = None


class MongoTypeInvolvedContract(BaseModel):
    """
    Involved Contract. This type is stored in the collection `involved_contracts`.

    :Parameters:
    - `_id`: the hash of the transaction - the `str` representation of the contract.
    - `index`: contract index
    - `subindex`: contract subindex
    - `contract`: the `str` representation of the contract
    - `type`: dict with transaction `type` and `contents`
    - `block_height`: height of the block in which the transaction is executed
    - `source_module`: hash of the source module from which this contract is instanciated.
    """

    id: str = Field(..., alias="_id")
    index: int
    subindex: int
    contract: str
    type: dict[str, str]
    block_height: int
    source_module: str


class MongoTypeModule(BaseModel):
    """
    Module. This type is stored in the collection `modules`.

    :Parameters:
    - `_id`: the hex string
    - `module_name`: the name from the module
    - `methods`: list of method names
    - `contracts`: list of contract instances from this module
    """

    id: str = Field(..., alias="_id")
    module_name: str
    methods: Optional[list[str]] = None
    contracts: list[str]
    init_date: Optional[dt.datetime] = None


class MongoTypeInstance(BaseModel):
    """
    Instance. This type is stored in the collection `instances`.

    :Parameters:
    - `_id`: the hex string
    - `module_name`: the name from the module
    - `methods`: list of method names
    - `contracts`: list of contract instances from this module
    """

    id: str = Field(..., alias="_id")
    v0: Optional[CCD_InstanceInfo_V0] = None  # noqa: F405
    v1: Optional[CCD_InstanceInfo_V1] = None  # noqa: F405


class MongoTypeReward(BaseModel):
    """
    Module. This type is stored in the collection `payday_rewards`, property `reward`.

    """

    pool_owner: Optional[Union[int, str]] = None
    account_id: Optional[str] = None
    transaction_fees: int
    baker_reward: int
    finalization_reward: int


class MongoTypePoolReward(BaseModel):
    """
    Module. This type is stored in the collection `payday_rewards`.

    :Parameters:
    - `_id`: the hex string

    """

    id: str = Field(..., alias="_id")
    pool_owner: Union[int, str]
    pool_status: dict
    reward: MongoTypeReward
    date: str
    slot_time: dt.datetime


class MongoTypeAccountReward(BaseModel):
    """
    Module. This type is stored in the collection `payday_rewards`.

    :Parameters:
    - `_id`: the hex string
    - `module_name`: the name from the module
    - `methods`: list of method names
    - `contracts`: list of contract instances from this module
    """

    id: str = Field(..., alias="_id")
    account_id: str
    staked_amount: int
    account_is_baker: Optional[bool] = None
    baker_id: Optional[int] = None
    reward: MongoTypeReward
    date: str
    slot_time: dt.datetime


class Delegator(BaseModel):
    account: str
    stake: int


class MongoTypePayday(BaseModel):
    """
    Payday. This type is stored in collection `paydays`.

    :Parameters:
    - `_id`: hash of the block that contains payday information for
    this payday.
    - `date`: the payday date
    - `height_for_first_block`: height of the first block in the payday
    - `height_for_last_block`: height of the last block in the payday
    - `hash_for_first_block`: hash of the first block in the payday
    - `hash_for_last_block`: hash of the last block in the payday
    - `payday_duration_in_seconds`: duration of the payday in seconds (used for
    APY calculation)
    - `payday_block_slot_time`: time of payday reward block
    - `bakers_with_delegation_information`: bakers with delegators for reward period, retrieved
    from `get_delegators_for_pool_in_reward_period`, using the hash of the last block
    - `baker_account_ids`: mapping from baker_id to account_address
    - `pool_status_for_bakers`: dictionary, keyed on pool_status, value
    is a list of bakers, retrieved using the hash of the first block
    """

    id: str = Field(..., alias="_id")
    date: str
    height_for_first_block: int
    height_for_last_block: int
    hash_for_first_block: str
    hash_for_last_block: str
    payday_duration_in_seconds: float
    payday_block_slot_time: dt.datetime
    bakers_with_delegation_information: dict[str, list[Delegator]]
    baker_account_ids: dict[int, str]
    pool_status_for_bakers: Optional[dict[str, list[int]]] = None


class MongoTypePaydayAPYIntermediate(BaseModel):
    """
    Payday APY Intermediate. This type is stored in collection `paydays_apy_intermediate`.

    :Parameters:
    - `_id`: baker_is or account address

    """

    id: str = Field(..., alias="_id")
    daily_apy_dict: dict
    d30_apy_dict: Optional[dict] = None
    d90_apy_dict: Optional[dict] = None
    d180_apy_dict: Optional[dict] = None


class MongoTypePaydaysPerformance(BaseModel):
    """
    Payday Performance. This is a collection that stores daily performance characteristics
    for bakers.


    :Parameters:
    - `_id`: unique id in the form of `date`-`baker_id`
    - `expectation`: the daily expected number of blocks for this baker in this payday.
    Calculated as the lottery power * 8640 (the expected number of blocks in a day)
    - `payday_block_slot_time`: Slot time of the payday block
    - `baker_id`: the baker_id
    - `pool_status`:

    """

    id: str = Field(..., alias="_id")
    pool_status: CCD_PoolInfo  # noqa: F405
    expectation: float
    date: str
    payday_block_slot_time: dt.datetime
    baker_id: str


class Collections(Enum):
    blocks = "blocks"
    transactions = "transactions"
    instances = "instances"
    modules = "modules"
    messages = "messages"
    paydays = "paydays"
    paydays_performance = "paydays_performance"
    paydays_rewards = "paydays_rewards"
    paydays_apy_intermediate = "paydays_apy_intermediate"
    paydays_current_payday = "paydays_current_payday"
    paydays_helpers = "paydays_helpers"
    involved_accounts_all = "involved_accounts_all"
    involved_accounts_all_top_list = "involved_accounts_all_top_list"
    involved_accounts_transfer = "involved_accounts_transfer"
    involved_contracts = "involved_contracts"
    nightly_accounts = "nightly_accounts"
    blocks_at_end_of_day = "blocks_at_end_of_day"
    blocks_per_day = "blocks_per_day"
    helpers = "helpers"
    memo_transaction_hashes = "memo_transaction_hashes"
    cns_domains = "cns_domains"
    bot_messages = "bot_messages"
    dashboard_nodes = "dashboard_nodes"
    tokens_accounts = "tokens_accounts"
    tokens_tags = "tokens_tags"
    tokens_logged_events = "tokens_logged_events"
    tokens_token_addresses = "tokens_token_addresses"
    memos_to_hashes = "memos_to_hashes"
    credentials_issuers = "credentials_issuers"


class CollectionsUtilities(Enum):
    labeled_accounts = "labeled_accounts"
    labeled_accounts_metadata = "labeled_accounts_metadata"
    users_prod = "users_prod"
    users_dev = "users_dev"
    exchange_rates = "exchange_rates"
    exchange_rates_historical = "exchange_rates_historical"


FALLBACK_URI = "linode.sprocker.nl:27027,contabo.sprocker.nl:27027,nas.sprocker.nl:27017/?replicaSet=rs2"


class MongoDB(
    _search_transfers,
    _subscriptions,
    _distributions,
    _store_block,
    _apy_calculations,
):
    def __init__(self, mongo_config, tooter: Tooter):
        self.tooter: Tooter = tooter
        if "MONGODB_URI" not in mongo_config:
            MONGO_URI = FALLBACK_URI
        else:
            MONGO_URI = (
                mongo_config["MONGODB_URI"]
                if mongo_config["MONGODB_URI"] is not None
                else FALLBACK_URI
            )
        try:
            con = MongoClient(
                f'mongodb://admin:{mongo_config["MONGODB_PASSWORD"]}@{MONGO_URI}'
            )
            self.connection: MongoClient = con

            self.mainnet_db = con["concordium_mainnet"]
            self.mainnet: Dict[Collections, Collection] = {}
            for collection in Collections:
                self.mainnet[collection] = self.mainnet_db[collection.value]

            self.testnet_db = con["concordium_testnet"]
            self.testnet: Dict[Collections, Collection] = {}
            for collection in Collections:
                self.testnet[collection] = self.testnet_db[collection.value]

            self.utilities_db = con["concordium_utilities"]
            self.utilities: Dict[CollectionsUtilities, Collection] = {}
            for collection in CollectionsUtilities:
                self.utilities[collection] = self.utilities_db[collection.value]

            console.log(con.server_info()["version"])
        except Exception as e:
            print(e)
            tooter.send(
                channel=TooterChannel.NOTIFIER,
                message=f"BOT ERROR! Cannot connect to MongoDB, with error: {e}",
                notifier_type=TooterType.MONGODB_ERROR,
            )


class MongoMotor(
    _search_transfers,
    _subscriptions,
    _distributions,
    _store_block,
    _apy_calculations,
):
    def __init__(self, mongo_config, tooter: Tooter):
        self.tooter: Tooter = tooter
        if "MONGODB_URI" not in mongo_config:
            MONGO_URI = FALLBACK_URI
        else:
            MONGO_URI = (
                mongo_config["MONGODB_URI"]
                if mongo_config["MONGODB_URI"] is not None
                else FALLBACK_URI
            )
        try:
            con = motor.motor_asyncio.AsyncIOMotorClient(
                f'mongodb://admin:{mongo_config["MONGODB_PASSWORD"]}@{MONGO_URI}'
            )

            self.mainnet_db = con["concordium_mainnet"]
            self.mainnet: Dict[Collections, AsyncIOMotorCollection] = {}
            for collection in Collections:
                self.mainnet[collection] = self.mainnet_db[collection.value]

            self.testnet_db = con["concordium_testnet"]
            self.testnet: Dict[Collections, AsyncIOMotorCollection] = {}
            for collection in Collections:
                self.testnet[collection] = self.testnet_db[collection.value]

            # console.log(f'Motor: {con.server_info()["version"]}')
        except Exception as e:
            print(e)
            tooter.send(
                channel=TooterChannel.NOTIFIER,
                message=f"BOT ERROR! Cannot connect to Motor MongoDB, with error: {e}",
                notifier_type=TooterType.MONGODB_ERROR,
            )
