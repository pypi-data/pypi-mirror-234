import json
import os
from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, Extra, Field
import io
import chardet

# from fastapi import Request

from .GRPCClient import GRPCClient
from .mongodb import (
    MongoDB,
    Collections,
    MongoTypeInvolvedAccount,
    CollectionsUtilities,
)
from enum import Enum
import datetime as dt
import dateutil.parser
from datetime import timezone
from rich.console import Console

console = Console()


class SmartContractRequest(BaseModel):
    chat_id: str
    init: bool
    update: bool
    cns_domain: bool


class UnstakeLimitRequest(BaseModel):
    chat_id: str
    limit: int


class TransactionLimitRequest(BaseModel):
    chat_id: str
    limit: int
    exch_only: bool


class CheckItemRequest(BaseModel):
    chat_id: str
    itemId: str


class AddEditItemRequest(BaseModel):
    chat_id: str
    itemId: str
    account_id: str = None
    baker_id: int = None
    label: str = None
    node_ip: str = None
    node_port: str = None
    account_notify: bool
    baker_notify: bool
    edit_save: bool = False


class DeleteItemRequest(BaseModel):
    chat_id: str
    account_id: str
    baker_id: int = None


class UserReminderStatus(Enum):
    NO_NEED = -1  # there is no need to remind. The bot has plenty of credits
    RUNNING_OUT_IN_2_DAYS = 0  #
    OUT_OF_CREDITS_1 = 1
    OUT_OF_CREDITS_2 = 2
    OUT_OF_CREDITS_3 = 3
    NOT_RESPONDING = 4


class SubscriptionDetails(Enum):
    EXPLORER_CCD = os.environ.get(
        "EXPLORER_CCD", "3cunMsEt2M3o9Rwgs2pNdsCWZKB5MkhcVbQheFHrvjjcRLSoGP"
    )
    BAKER_ID = int(os.environ.get("BAKER_ID", 72723))

    SUBSCRIPTION_ONE_TIME_FEE = int(os.environ.get("SUBSCRIPTION_ONE_TIME_FEE", 1000))
    SUBSCRIPTION_DELEGATION_FEE = int(os.environ.get("SUBSCRIPTION_DELEGATION_FEE", 1))
    SUBSCRIPTION_MESSAGE_CREDITS_IN_FEE = int(
        os.environ.get("SUBSCRIPTION_MESSAGE_CREDITS_IN_FEE", 50)
    )
    SUBSCRIPTION_WARN_HOURS_BEFORE = int(
        os.environ.get("SUBSCRIPTION_WARN_HOURS_BEFORE", 48)
    )
    SUBSCRIPTION_MESSAGE_FEE = int(os.environ.get("SUBSCRIPTION_MESSAGE_FEE", 1))
    SUBSCRIPTION_UNLIMITED = int(os.environ.get("SUBSCRIPTION_UNLIMITED", 5000))
    SUBSCRIPTION_DELEGATOR_STAKE_LIMIT = int(
        os.environ.get("SUBSCRIPTION_DELEGATOR_STAKE_LIMIT", 100_000)
    )
    SUBSCRIPTION_PLAN_START_DATE = dateutil.parser.parse(
        os.environ.get("SUBSCRIPTION_PLAN_START_DATE", "2022-12-01 01:00:00")
    ).astimezone(timezone.utc)


class SubscriptionPlans(Enum):
    PLUS = "Plus"
    DELEGATION = "Delegation"
    UNLIMITED = "Unlimited"
    NO_PLAN = "No Plan"


class Subscription(BaseModel):
    start_date: dt.datetime = None
    payment_transactions: list = []
    subscription_active: bool = False
    subscription_active: bool = (
        False  # If True, the user has paid enough to pay for one-time fee
    )
    delegator_active: bool = False  # If True, the user has paid any amount from an account that is an active delegator
    site_active: bool = False  # This is the indicator that a user can use the site
    bot_active: bool = False  # If True, the user has paid enough to cover the one-time fee and sent messages

    unlimited: bool = (
        False  # If True, the user has paid enough for subscription_unlimited
    )
    # unlimited credits
    unlimited_end_date: dt.datetime = None
    remaining_message_credits: int = 0
    count_messages: int = 0
    paid_amount: int = 0
    messages_per_hour: int = 0
    plan: SubscriptionPlans = SubscriptionPlans.NO_PLAN


class User(BaseModel):
    id: str = Field(..., alias="_id")
    nodes: dict = None
    bakers_to_follow: list[int] = []
    chat_id: int = None
    first_name: str = None
    language_code: str = None
    token: str = "x" * 10
    username: str = None
    accounts_to_follow: list[str] = []
    labels: dict = {}
    tags: dict = {}
    transactions_downloaded: dict = None
    smart_init: bool = None
    smart_update: bool = None
    cns_domain: bool = None
    unstake_limit_notifier: int = None
    transaction_limit_notifier_to_exchange_only: bool = None
    subscription: Subscription = Subscription()
    explorer_ccd_transactions: list[dict] = []
    explorer_ccd_delegators: dict = {}
    last_refreshed_for_user: dt.datetime = None
    transaction_limit_notifier: int = None
    environment: str = "dev"
    testing: bool = False

    @classmethod
    def read_user_from_collection(self, chat_id, mongodb: MongoDB):
        coll = mongodb.utilities[CollectionsUtilities.users_prod]

        user = coll.find_one({"chat_id": chat_id})
        existing_user = None
        if user:
            existing_user = User(**user)
        return existing_user

    def save_user_to_collection(self, request=None, mongodb: MongoDB = None):
        query = {"_id": self.token}
        if mongodb:
            m = mongodb
        else:
            m = request.app.mongodb

        if self.environment == "prod":
            coll = m.utilities[CollectionsUtilities.users_prod]
        else:
            coll = m.utilities[CollectionsUtilities.users_dev]

        coll.replace_one(
            query,
            json.loads(self.json(exclude_none=True)),
            upsert=True,
        )

    def save_smart_contracts(
        self, request, smart_contract_request: SmartContractRequest
    ):
        self.smart_init = smart_contract_request.init
        self.smart_update = smart_contract_request.update
        self.cns_domain = smart_contract_request.cns_domain
        self.save_user_to_collection(request)

    def save_unstake_limit(self, request, unstake_limit_request: UnstakeLimitRequest):
        self.unstake_limit_notifier = unstake_limit_request.limit
        self.save_user_to_collection(request)

    def save_limit(self, request, transaction_limit_request: TransactionLimitRequest):
        self.transaction_limit_notifier = transaction_limit_request.limit
        self.transaction_limit_notifier_to_exchange_only = (
            transaction_limit_request.exch_only
        )
        self.save_user_to_collection(request)

    def save_transactions_download(self, request, account_id):
        self.transactions_downloaded[account_id] = (
            self.transactions_downloaded.get(account_id, 0) + 1
        )
        self.save_user_to_collection(request)

    def add_edit_item(
        self,
        request,
        add_edit_item_request: AddEditItemRequest,
    ):
        if add_edit_item_request.baker_id:
            if add_edit_item_request.baker_notify:
                self.bakers_to_follow.append(add_edit_item_request.baker_id)
                self.bakers_to_follow = sorted(list(set(self.bakers_to_follow)))
            else:
                try:
                    self.bakers_to_follow.remove(add_edit_item_request.baker_id)
                except:
                    pass

            # node
            if add_edit_item_request.node_ip and add_edit_item_request.node_port:
                nodes = self.nodes
                nodes[str(add_edit_item_request.baker_id)] = {
                    "ip": add_edit_item_request.node_ip,
                    "port": add_edit_item_request.node_port,
                }
                self.nodes = nodes

        if add_edit_item_request.account_notify:
            self.accounts_to_follow.append(add_edit_item_request.account_id)
            self.accounts_to_follow = sorted(list(set(self.accounts_to_follow)))
        else:
            try:
                self.accounts_to_follow.remove(add_edit_item_request.account_id)
            except:
                pass

        self.labels[add_edit_item_request.account_id] = add_edit_item_request.label
        self.save_user_to_collection(request)

    def remove_item(self, request, delete_item_request: DeleteItemRequest):
        try:
            self.accounts_to_follow.remove(delete_item_request.account_id)
        except:
            pass

        try:
            self.bakers_to_follow.remove(delete_item_request.baker_id)
        except:
            pass

        try:
            del self.nodes[str(delete_item_request.baker_id)]
        except:
            pass

        # remove label
        if delete_item_request.account_id in self.labels:
            _ = self.labels.pop(delete_item_request.account_id, None)

        self.save_user_to_collection(request)

    def add_user_from_telegram(self, user):
        self.first_name = user.first_name
        self.username = user.username
        self.chat_id = user.id
        self.language_code = user.language_code
        return self

    def read_user_from_git(self, user):
        # Testing is enabled through a parameters in pytest tests
        self.testing = user.get("testing", False)
        self.bakers_to_follow = user.get("bakers_to_follow", [])
        self.chat_id = user.get("chat_id", None)
        self.token = user.get("token", None)
        self.first_name = user.get("first_name", None)
        self.username = user.get("username", None)
        self.accounts_to_follow = user.get("accounts_to_follow", [])
        self.labels = user.get("labels", None)
        self.transactions_downloaded = user.get("transactions_downloaded", {})
        self.transaction_limit_notifier = user.get("transaction_limit_notifier", -1)
        self.transaction_limit_notifier_to_exchange_only = user.get(
            "transaction_limit_notifier_to_exchange_only", False
        )
        self.unstake_limit_notifier = user.get("unstake_limit_notifier", -1)
        self.smart_init = user.get("smart_init", False)
        self.smart_update = user.get("smart_update", False)
        self.cns_domain = user.get("cns_domain", False)
        self.nodes = user.get("nodes", {})
        # self.subscription                   = Subscription()
        return self

    def prepare_for_subscription_logic(
        self,
        mongodb: MongoDB,
        grpcclient: GRPCClient,
        txs_as_receiver: list[MongoTypeInvolvedAccount] = None,
        explorer_ccd_delegators: dict = None,
    ):
        grpcclient.switch_to_net("mainnet")
        if not txs_as_receiver:
            console.log("Need to get explorer transactions...")
            self.get_explorer_transactions(mongodb, grpcclient)
        else:
            self.explorer_ccd_transactions = txs_as_receiver

        if not explorer_ccd_delegators:
            console.log("Need to get explorer delegators...")
            self.get_explorer_delegators(grpcclient)
        else:
            self.explorer_ccd_delegators = explorer_ccd_delegators
        self.last_refreshed_for_user = dt.datetime.utcnow()

    def get_explorer_transactions(self, mongodb: MongoDB, grpcclient: GRPCClient):
        try:
            pipeline = mongodb.search_txs_hashes_for_account_as_receiver_with_params(
                SubscriptionDetails.EXPLORER_CCD.value, 0, 1_000_000_000
            )
            txs_as_receiver = [
                MongoTypeInvolvedAccount(**x)
                for x in mongodb.mainnet[
                    Collections.involved_accounts_transfer
                ].aggregate(pipeline)
            ]

            self.explorer_ccd_transactions = txs_as_receiver
        except:
            self.explorer_ccd_transactions = []

    def get_explorer_delegators(self, grpcclient: GRPCClient):
        try:
            explorer_ccd_delegators = grpcclient.get_delegators_for_pool(
                SubscriptionDetails.BAKER_ID.value, "last_final"
            )

            # keyed on accountAddress
            self.explorer_ccd_delegators = {
                x.account: x for x in explorer_ccd_delegators
            }
        except:
            self.explorer_ccd_delegators = []

    def set_count_messages(self, mongodb: MongoDB, ENVIRONMENT: str):
        # get count of messages sent to this user
        # only count from subscription.start_date
        if self.subscription.start_date:
            try:
                pipeline = mongodb.get_bot_messages_for_user(
                    self, ENVIRONMENT, self.subscription.start_date
                )
                result = list(
                    mongodb.mainnet[Collections.bot_messages].aggregate(pipeline)
                )

                self.subscription.count_messages = 0
                if len(result) > 0:
                    if "count_messages" in result[0]:
                        self.subscription.count_messages = result[0]["count_messages"]

            except:
                pass

    def decode_memo(self, hex):
        # bs = bytes.fromhex(hex)
        # return bytes.decode(bs[1:], 'UTF-8')
        try:
            bs = io.BytesIO(bytes.fromhex(hex))
            value = bs.read()

            encoding_guess = chardet.detect(value)
            if encoding_guess["confidence"] < 0.1:
                encoding_guess = chardet.detect(value[2:])
                value = value[2:]

            if encoding_guess["encoding"] and encoding_guess["confidence"] > 0.5:
                try:
                    memo = bytes.decode(value, encoding_guess["encoding"])

                    # memo = bytes.decode(value, "UTF-8")
                    return memo[1:]
                except UnicodeDecodeError:
                    memo = bytes.decode(value[1:], "UTF-8")
                    return memo[1:]
            else:
                return "Decoding failure..."
        except:
            return "Decoding failure..."

    def perform_subscription_logic(self, grpcclient: GRPCClient):
        grpcclient.switch_to_net("mainnet")
        payment_memo = self.token[:6]

        # check if the right memo is set, if so, count towards user.
        payment_txs = []
        paid_amount = 0
        SUBSCRIPTION_ONE_TIME_FEE_set = False
        ACTIVE_DELEGATOR_set = False

        for concordium_tx in self.explorer_ccd_transactions:
            if concordium_tx.memo:
                memo = self.decode_memo(concordium_tx.memo)
                if payment_memo in memo:
                    concordium_tx.memo = memo
                    slot_time = grpcclient.get_finalized_block_at_height(
                        concordium_tx.block_height
                    ).slot_time

                    paid_amount += concordium_tx.amount / 1_000_000

                    # Is this sender a current active delegator?
                    if not ACTIVE_DELEGATOR_set:
                        if concordium_tx.sender in self.explorer_ccd_delegators:
                            sender_delegated_stake = (
                                self.explorer_ccd_delegators[concordium_tx.sender].stake
                                / 1_000_000
                            )
                            self.subscription.delegator_active = (
                                sender_delegated_stake
                                >= SubscriptionDetails.SUBSCRIPTION_DELEGATOR_STAKE_LIMIT.value
                            )

                            # Make sure that multiple transactions to not UNset this if later transactions make this invalid.
                            if self.subscription.delegator_active:
                                ACTIVE_DELEGATOR_set = True
                                self.subscription.plan = SubscriptionPlans.DELEGATION

                                # some users have purchased before the official start date.
                                self.subscription.start_date = max(
                                    SubscriptionDetails.SUBSCRIPTION_PLAN_START_DATE.value,
                                    slot_time,
                                )

                    # Has the user paid the one time fee? If so, record the subscription start date
                    if not SUBSCRIPTION_ONE_TIME_FEE_set:
                        self.subscription.subscription_active = (
                            paid_amount
                            >= SubscriptionDetails.SUBSCRIPTION_ONE_TIME_FEE.value
                        )

                        # Make sure that multiple transactions to not UNset this if later transactions make this invalid.
                        if self.subscription.subscription_active:
                            SUBSCRIPTION_ONE_TIME_FEE_set = True
                            self.subscription.plan = SubscriptionPlans.PLUS

                            # some users have purchased before the official start date.
                            self.subscription.start_date = max(
                                SubscriptionDetails.SUBSCRIPTION_PLAN_START_DATE.value,
                                slot_time,
                            )

                    # Has the user paid enough for unlimited? If so, record the unlimited end date
                    self.subscription.unlimited = (
                        paid_amount >= SubscriptionDetails.SUBSCRIPTION_UNLIMITED.value
                    )
                    if self.subscription.unlimited:
                        self.subscription.plan = SubscriptionPlans.UNLIMITED
                        self.subscription.unlimited_end_date = (
                            slot_time + relativedelta(years=1)
                        )
                        # if isinstance(
                        #     concordium_tx.block["blockSlotTime"], dt.datetime
                        # ):
                        #     self.subscription.unlimited_end_date = concordium_tx.block[
                        #         "blockSlotTime"
                        #     ] + relativedelta(years=1)
                        # else:
                        #     self.subscription.unlimited_end_date = (
                        #         dateutil.parser.parse(
                        #             concordium_tx.block["blockSlotTime"]
                        #         )
                        #         + relativedelta(years=1)
                        #     )
                    payment_txs.append(concordium_tx)

        self.subscription.payment_transactions = payment_txs
        self.subscription.paid_amount = paid_amount

        # This is the indicator that a user can use the site.
        self.subscription.site_active = (
            self.subscription.delegator_active or self.subscription.subscription_active
        )

        # exclude me
        if self.token == "e2410784-fde1-11ec-a3b9-de5c44736176":
            self.subscription.bot_active = True
            self.subscription.site_active = True
            self.subscription.subscription_active = True
            self.subscription.unlimited = True
            self.subscription.unlimited_end_date = dt.datetime(
                2040, 4, 16, 23, 59, 59
            ).astimezone(timezone.utc)
            self.subscription.plan = SubscriptionPlans.UNLIMITED

    def determine_bot_status(self):
        # update remaining message credits
        FEE_TO_USE = (
            SubscriptionDetails.SUBSCRIPTION_DELEGATION_FEE
            if self.subscription.plan == SubscriptionPlans.DELEGATION
            else SubscriptionDetails.SUBSCRIPTION_ONE_TIME_FEE
        )
        self.subscription.remaining_message_credits = max(
            0,
            (self.subscription.paid_amount - FEE_TO_USE.value)
            / SubscriptionDetails.SUBSCRIPTION_MESSAGE_FEE.value
            - self.subscription.count_messages
            + SubscriptionDetails.SUBSCRIPTION_MESSAGE_CREDITS_IN_FEE.value,
        )

        # finally, determine if the bot is active
        if self.subscription.site_active:
            if self.subscription.remaining_message_credits > 0:
                self.subscription.bot_active = True
            else:
                self.subscription.bot_active = False

        if self.subscription.unlimited:
            self.subscription.bot_active = True

        if self.subscription.start_date:
            hours_plan_active = (
                dt.datetime.now().astimezone(timezone.utc)
                - self.subscription.start_date
            ).total_seconds() / (60 * 60)
            self.subscription.messages_per_hour = (
                self.subscription.count_messages / hours_plan_active
            )

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)
