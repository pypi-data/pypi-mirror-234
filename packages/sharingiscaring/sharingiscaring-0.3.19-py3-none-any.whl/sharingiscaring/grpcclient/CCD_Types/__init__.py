# ruff: noqa: F403, F405, E402
from pydantic import BaseModel
import datetime as dt
from enum import Enum
from typing import Optional


################
#
# CCD_ is the prefix for all Pydantic classes
# to prevent namespace collision with the
# protobuf generated classes.
#
################


class CredentialElement(Enum):
    firstName = 0
    lastName = 1
    sex = 2
    dob = 3
    countryOfResidence = 4
    nationality = 5
    idDocType = 6
    idDocNo = 7
    idDocIssuer = 8
    idDocIssuedAt = 9
    idDocExpiresAt = 10
    nationalIdNo = 11
    taxIdNo = 12


class CredentialDocType(Enum):
    na = "0"
    Passport = "1"
    National_ID_Card = "2"
    Driving_License = "3"
    Immigration_Card = "4"


class ProtocolVersions(Enum):
    PROTOCOL_VERSION_1 = 0
    PROTOCOL_VERSION_2 = 1
    PROTOCOL_VERSION_3 = 2
    PROTOCOL_VERSION_4 = 3
    PROTOCOL_VERSION_5 = 4
    PROTOCOL_VERSION_6 = 5


class OpenStatus(Enum):
    open_for_all = 0
    closed_for_new = 1
    closed_for_all = 2


CCD_ArIdentity = int
CCD_IpIdentity = int
CCD_ArPublicKey = str
CCD_IpVerifyKey = str
CCD_IpCdiVerifyKey = str
CCD_BlockHash = str
CCD_TransactionHash = str
CCD_AccountAddress = str
CCD_AccountIndex = int
CCD_DelegatorId = CCD_AccountIndex
microCCD = int
CCD_BakerId = int
CCD_Epoch = int
CCD_Energy = int
CCD_DurationSeconds = int
CCD_Duration = int
CCD_ModuleRef = str
CCD_ContractEvent = str
CCD_Memo = str
CCD_RegisteredData = str
CCD_BakerSignatureVerifyKey = str
CCD_OpenStatus = int
CCD_BakerElectionVerifyKey = str
CCD_BakerAggregationVerifyKey = str
CCD_Parameter = str
CCD_AmountFraction = float
CCD_ReceiveName = str
CCD_CredentialsPerBlockLimit = int
CCD_LeadershipElectionNonce = str
CCD_CredentialRegistrationId = str
CCD_Sha256Hash = str
CCD_ElectionDifficulty = float
CCD_UpdatePublicKey = str
CCD_UpdateKeysIndex = int
CCD_UpdateKeysThreshold = int
CCD_TransactionTime = int
CCD_SignatureThreshold = int
CCD_IdentityProviderIdentity = int
CCD_ArThreshold = int
CCD_Commitment = str
CCD_VersionedModuleSource_ModuleSourceV0 = str
CCD_VersionedModuleSource_ModuleSourceV1 = str
CCD_ProtocolVersion = int
CCD_StateHash = str
CCD_TimeStamp = dt.datetime

CCD_SequenceNumber = int
CCD_StakePendingChange_Remove = CCD_TimeStamp
CCD_ContractStateV0 = str
CCD_InitName = str
CCD_EncryptedAmount = str
CCD_Empty = None
CCD_AccountThreshold = int
CCD_Policy_Attributes = str
CCD_Round = int
CCD_Epoch = int

# class CCD_Policy_Attributes(BaseModel):
#     key: int
#     value: str


class CCD_ContractAddress(BaseModel):
    index: int
    subindex: int

    def to_str(self):
        return f"<{self.index},{self.subindex}>"

    @classmethod
    def from_str(self, str_repr: str):
        """
        Returns a CCD_ContractAddress when the input is formed as '<2350,0>'.
        """
        contract_string = str_repr.split("-")[0]
        c = CCD_ContractAddress(
            **{
                "index": contract_string.split(",")[0][1:],
                "subindex": contract_string.split(",")[1][:-1],
            }
        )

        return c

    @classmethod
    def from_index(self, index: int, subindex: int):
        s = CCD_ContractAddress(**{"index": index, "subindex": subindex})
        return s


class CCD_Address(BaseModel):
    account: Optional[CCD_AccountAddress] = None
    contract: Optional[CCD_ContractAddress] = None


class CCD_RejectReason_InvalidInitMethod(BaseModel):
    module_ref: CCD_ModuleRef
    init_name: CCD_InitName


class CCD_RejectReason_InvalidReceiveMethod(BaseModel):
    module_ref: CCD_ModuleRef
    receive_name: CCD_ReceiveName


class CCD_RejectReason_AmountTooLarge(BaseModel):
    address: CCD_Address
    amount: microCCD


class CCD_RejectReason_RejectedInit(BaseModel):
    reject_reason: int


class CCD_RejectReason_RejectedReceive(BaseModel):
    reject_reason: int
    contract_address: CCD_ContractAddress
    receive_name: CCD_ReceiveName
    parameter: CCD_Parameter


class CCD_RejectReason_DuplicateCredIds(BaseModel):
    ids: list[CCD_CredentialRegistrationId]


class CCD_RejectReason_NonExistentCredIds(BaseModel):
    ids: list[CCD_CredentialRegistrationId]


class CCD_RejectReason(BaseModel):
    module_not_wf: Optional[CCD_Empty] = None
    module_hash_already_exists: Optional[CCD_ModuleRef] = None
    invalid_account_reference: Optional[CCD_AccountAddress] = None
    invalid_init_method: Optional[CCD_RejectReason_InvalidInitMethod] = None
    invalid_receive_method: Optional[CCD_RejectReason_InvalidReceiveMethod] = None
    invalid_module_reference: Optional[CCD_ModuleRef] = None
    invalid_contract_address: Optional[CCD_ContractAddress] = None
    runtime_failure: Optional[CCD_Empty] = None
    amount_too_large: Optional[CCD_RejectReason_AmountTooLarge] = None
    serialization_failure: Optional[CCD_Empty] = None
    out_of_energy: Optional[CCD_Empty] = None
    rejected_init: Optional[CCD_RejectReason_RejectedInit] = None
    rejected_receive: Optional[CCD_RejectReason_RejectedReceive] = None
    invalid_proof: Optional[CCD_Empty] = None
    already_a_baker: Optional[CCD_BakerId] = None
    not_a_baker: Optional[CCD_AccountAddress] = None
    insufficient_balance_for_baker_stake: Optional[CCD_Empty] = None
    stake_under_minimum_threshold_for_baking: Optional[CCD_Empty] = None
    baker_in_cooldown: Optional[CCD_Empty] = None
    duplicate_aggregation_key: Optional[CCD_BakerAggregationVerifyKey] = None
    non_existent_credential_id: Optional[CCD_Empty] = None
    key_index_already_in_use: Optional[CCD_Empty] = None
    invalid_account_threshold: Optional[CCD_Empty] = None
    invalid_credential_key_sign_threshold: Optional[CCD_Empty] = None
    invalid_encrypted_amount_transfer_proof: Optional[CCD_Empty] = None
    invalid_transfer_to_public_proof: Optional[CCD_Empty] = None
    encrypted_amount_self_transfer: Optional[CCD_AccountAddress] = None
    invalid_index_on_encrypted_transfer: Optional[CCD_Empty] = None
    zero_scheduledAmount: Optional[CCD_Empty] = None
    non_increasing_schedule: Optional[CCD_Empty] = None
    first_scheduled_release_expired: Optional[CCD_Empty] = None
    scheduled_self_transfer: Optional[CCD_AccountAddress] = None
    invalid_credentials: Optional[CCD_Empty] = None
    duplicate_cred_ids: Optional[CCD_RejectReason_DuplicateCredIds] = None
    non_existent_cred_ids: Optional[CCD_RejectReason_NonExistentCredIds] = None
    remove_first_credential: Optional[CCD_Empty] = None
    credential_holder_did_not_sign: Optional[CCD_Empty] = None
    not_allowed_multiple_credentials: Optional[CCD_Empty] = None
    not_allowed_to_receive_encrypted: Optional[CCD_Empty] = None
    not_allowed_to_handle_encrypted: Optional[CCD_Empty] = None
    missing_baker_add_parameters: Optional[CCD_Empty] = None
    finalization_reward_commission_not_in_range: Optional[CCD_Empty] = None
    baking_reward_commission_not_in_range: Optional[CCD_Empty] = None
    transaction_fee_commission_not_in_range: Optional[CCD_Empty] = None
    already_a_delegator: Optional[CCD_Empty] = None
    insufficient_balance_for_delegation_stake: Optional[CCD_Empty] = None
    missing_delegation_add_parameters: Optional[CCD_Empty] = None
    insufficient_delegation_stake: Optional[CCD_Empty] = None
    delegator_in_cooldown: Optional[CCD_Empty] = None
    not_a_delegator: Optional[CCD_AccountAddress] = None
    delegation_target_not_a_baker: Optional[CCD_BakerId] = None
    stake_over_maximum_threshold_for_pool: Optional[CCD_Empty] = None
    pool_would_become_over_delegated: Optional[CCD_Empty] = None
    pool_closed: Optional[CCD_Empty] = None


class CCD_CredentialType(Enum):
    initial = 0
    normal = 1


class CCD_StakePendingChange_Reduce(BaseModel):
    new_stake: microCCD
    effective_time: CCD_TimeStamp


class CCD_StakePendingChange(BaseModel):
    reduce: Optional[CCD_StakePendingChange_Reduce] = None
    remove: Optional[CCD_StakePendingChange_Remove] = None


class CCD_BakerStakePendingChange_Reduce(BaseModel):
    reduced_equity_capital: microCCD
    effective_time: CCD_TimeStamp


class CCD_BakerStakePendingChange_Remove(BaseModel):
    effective_time: CCD_TimeStamp


class CCD_BakerStakePendingChange(BaseModel):
    reduce: Optional[CCD_BakerStakePendingChange_Reduce] = None
    remove: Optional[CCD_BakerStakePendingChange_Remove] = None


class CCD_DelegatorInfo(BaseModel):
    account: CCD_AccountAddress
    stake: microCCD
    pending_change: Optional[CCD_StakePendingChange] = None


class CCD_DelegatorRewardPeriodInfo(BaseModel):
    account: CCD_AccountAddress
    stake: microCCD


class CCD_CurrentPaydayStatus(BaseModel):
    baker_equity_capital: microCCD
    blocks_baked: int
    delegated_capital: microCCD
    effective_stake: microCCD
    finalization_live: bool
    lottery_power: float
    transaction_fees_earned: microCCD


class CCD_CommissionRates(BaseModel):
    baking: float
    finalization: float
    transaction: float


class CCD_BakerPoolInfo(BaseModel):
    commission_rates: CCD_CommissionRates
    url: str
    open_status: str


class CCD_PoolInfo(BaseModel):
    all_pool_total_capital: microCCD
    address: CCD_AccountAddress
    equity_capital: microCCD
    baker: int
    equity_pending_change: Optional[CCD_BakerStakePendingChange] = None
    current_payday_info: Optional[CCD_CurrentPaydayStatus] = None
    delegated_capital: microCCD
    delegated_capital_cap: microCCD
    pool_info: CCD_BakerPoolInfo
    # poolType: str = None


class CCD_PassiveDelegationInfo(BaseModel):
    all_pool_total_capital: microCCD
    delegated_capital: microCCD
    current_payday_transaction_fees_earned: microCCD
    current_payday_delegated_capital: microCCD
    commission_rates: CCD_CommissionRates


class CCD_FinalizedBlockInfo(BaseModel):
    hash: CCD_BlockHash
    height: int


class CCD_BlockInfo(BaseModel):
    arrive_time: Optional[CCD_TimeStamp] = None
    baker: Optional[int] = None
    hash: CCD_BlockHash
    height: int
    last_finalized_block: CCD_BlockHash
    parent_block: CCD_BlockHash
    receive_time: Optional[CCD_TimeStamp] = None
    slot_number: Optional[int] = None
    slot_time: CCD_TimeStamp
    era_block_height: int
    finalized: bool
    genesis_index: int
    transaction_count: int
    transactions_energy_cost: int
    transactions_size: int
    transaction_hashes: Optional[list[CCD_TransactionHash]] = None
    state_hash: Optional[CCD_StateHash] = None
    protocol_version: Optional[
        str
    ] = None  # note this is not optional from the specification,
    # but this type is also used in retrieving blockInfo from MongoDB, where protocol_version
    # isn't stored (currently).
    round: Optional[CCD_Round] = None
    epoch: Optional[CCD_Epoch] = None


class CCD_AccountTransactionEffects_None(BaseModel):
    transaction_type: Optional[int] = None
    reject_reason: CCD_RejectReason


class CCD_ContractInitializedEvent(BaseModel):
    contract_version: int
    origin_ref: CCD_ModuleRef
    address: CCD_ContractAddress
    amount: microCCD = 0
    init_name: str
    events: list[CCD_ContractEvent]


class CCD_InstanceUpdatedEvent(BaseModel):
    contract_version: int
    address: CCD_ContractAddress
    instigator: CCD_Address
    amount: microCCD
    parameter: CCD_Parameter
    receive_name: CCD_ReceiveName
    events: Optional[list[CCD_ContractEvent]] = None


class CCD_ContractTraceElement_Interrupted(BaseModel):
    address: CCD_ContractAddress
    events: list[CCD_ContractEvent]


class CCD_ContractTraceElement_Resumed(BaseModel):
    address: CCD_ContractAddress
    success: bool


class CCD_ContractTraceElement_Transferred(BaseModel):
    sender: CCD_ContractAddress
    amount: microCCD
    receiver: CCD_AccountAddress


class CCD_ContractTraceElement(BaseModel):
    updated: Optional[CCD_InstanceUpdatedEvent] = None
    transferred: Optional[CCD_ContractTraceElement_Transferred] = None
    interrupted: Optional[CCD_ContractTraceElement_Interrupted] = None
    resumed: Optional[CCD_ContractTraceElement_Resumed] = None


class CCD_ContractUpdateIssued(BaseModel):
    effects: list[CCD_ContractTraceElement]


class CCD_EncryptedAmountRemovedEvent(BaseModel):
    account: CCD_AccountAddress
    new_amount: CCD_EncryptedAmount
    input_amount: CCD_EncryptedAmount
    up_to_index: int


class CCD_NewEncryptedAmountEvent(BaseModel):
    receiver: CCD_AccountAddress
    new_index: int
    encrypted_amount: CCD_EncryptedAmount


class CCD_AccountTransactionEffects_EncryptedAmountTransferred(BaseModel):
    removed: Optional[CCD_EncryptedAmountRemovedEvent] = None
    added: Optional[CCD_NewEncryptedAmountEvent] = None
    memo: Optional[CCD_Memo] = None


class CCD_EncryptedSelfAmountAddedEvent(BaseModel):
    account: CCD_AccountAddress
    new_amount: CCD_EncryptedAmount
    amount: microCCD


class CCD_AccountTransactionEffects_TransferredToPublic(BaseModel):
    removed: CCD_EncryptedAmountRemovedEvent
    amount: microCCD


class CCD_AccountTransactionEffects_CredentialsUpdated(BaseModel):
    new_cred_ids: list[CCD_CredentialRegistrationId]
    removed_cred_ids: list[CCD_CredentialRegistrationId]
    new_threshold: CCD_AccountThreshold


class CCD_BakerKeysEvent(BaseModel):
    baker_id: CCD_BakerId
    account: CCD_AccountAddress
    sign_key: CCD_BakerSignatureVerifyKey
    election_key: CCD_BakerElectionVerifyKey
    aggregation_key: CCD_BakerAggregationVerifyKey


class CCD_BakerAdded(BaseModel):
    keys_event: CCD_BakerKeysEvent
    stake: microCCD
    restake_earnings: bool


class CCD_AccountTransfer(BaseModel):
    amount: microCCD = 0
    receiver: CCD_AccountAddress
    memo: Optional[CCD_Memo] = None


class CCD_NewRelease(BaseModel):
    timestamp: CCD_TimeStamp
    amount: microCCD


class CCD_TransferredWithSchedule(BaseModel):
    receiver: CCD_AccountAddress
    amount: list[CCD_NewRelease]
    memo: Optional[CCD_Memo] = None


class CCD_BakerStakeUpdatedData(BaseModel):
    baker_id: CCD_BakerId
    new_stake: microCCD
    increased: bool


class CCD_BakerStakeUpdated(BaseModel):
    update: CCD_BakerStakeUpdatedData


class CCD_BakerStakeIncreased(BaseModel):
    baker_id: CCD_BakerId
    new_stake: microCCD


class CCD_BakerStakeDecreased(BaseModel):
    baker_id: CCD_BakerId
    new_stake: microCCD


class CCD_BakerRestakeEarningsUpdated(BaseModel):
    baker_id: CCD_BakerId
    restake_earnings: bool


class CCD_BakerSetOpenStatus(BaseModel):
    baker_id: CCD_BakerId
    open_status: CCD_OpenStatus


class CCD_BakerSetMetadataUrl(BaseModel):
    baker_id: CCD_BakerId
    url: str


class CCD_BakerSetTransactionFeeCommission(BaseModel):
    baker_id: CCD_BakerId
    transaction_fee_commission: CCD_AmountFraction


class CCD_BakerSetBakingRewardCommission(BaseModel):
    baker_id: CCD_BakerId
    baking_reward_commission: CCD_AmountFraction


class CCD_BakerSetFinalizationRewardCommission(BaseModel):
    baker_id: CCD_BakerId
    finalization_reward_commission: CCD_AmountFraction


class CCD_BakerEvent(BaseModel):
    baker_added: Optional[CCD_BakerAdded] = None
    baker_removed: Optional[CCD_BakerId] = None
    baker_stake_increased: Optional[CCD_BakerStakeIncreased] = None
    baker_stake_decreased: Optional[CCD_BakerStakeDecreased] = None
    baker_restake_earnings_updated: Optional[CCD_BakerRestakeEarningsUpdated] = None
    baker_keys_updated: Optional[CCD_BakerKeysEvent] = None
    baker_set_open_status: Optional[CCD_BakerSetOpenStatus] = None
    baker_set_metadata_url: Optional[CCD_BakerSetMetadataUrl] = None
    baker_set_transaction_fee_commission: Optional[
        CCD_BakerSetTransactionFeeCommission
    ] = None
    baker_set_baking_reward_commission: Optional[
        CCD_BakerSetBakingRewardCommission
    ] = None
    baker_set_finalization_reward_commission: Optional[
        CCD_BakerSetFinalizationRewardCommission
    ] = None


class CCD_BakerConfigured(BaseModel):
    events: list[CCD_BakerEvent]


class CCD_DelegationStakeIncreased(BaseModel):
    delegator_id: CCD_DelegatorId
    new_stake: microCCD


class CCD_DelegationStakeDecreased(BaseModel):
    delegator_id: CCD_DelegatorId
    new_stake: microCCD


class CCD_DelegationSetRestakeEarnings(BaseModel):
    delegator_id: CCD_DelegatorId
    restake_earnings: bool


class CCD_DelegationTarget(BaseModel):
    passive_delegation: Optional[bool] = None
    baker: Optional[CCD_BakerId] = None


class CCD_DelegationSetDelegationTarget(BaseModel):
    delegator_id: CCD_DelegatorId
    delegation_target: CCD_DelegationTarget


class CCD_DelegationEvent(BaseModel):
    delegation_added: Optional[CCD_DelegatorId] = None
    delegation_removed: Optional[CCD_DelegatorId] = None
    delegation_stake_increased: Optional[CCD_DelegationStakeIncreased] = None
    delegation_stake_decreased: Optional[CCD_DelegationStakeDecreased] = None
    delegation_set_restake_earnings: Optional[CCD_DelegationSetRestakeEarnings] = None
    delegation_set_delegation_target: Optional[CCD_DelegationSetDelegationTarget] = None


class CCD_DelegationConfigured(BaseModel):
    events: list[CCD_DelegationEvent]


class CCD_BakerEvent_BakerRestakeEarningsUpdated(BaseModel):
    baker_id: CCD_BakerId
    restake_earnings: bool


class CCD_AccountTransactionEffects(BaseModel):
    none: Optional[CCD_AccountTransactionEffects_None] = None
    module_deployed: Optional[CCD_ModuleRef] = None
    contract_initialized: Optional[CCD_ContractInitializedEvent] = None
    contract_update_issued: Optional[CCD_ContractUpdateIssued] = None
    account_transfer: Optional[CCD_AccountTransfer] = None
    baker_added: Optional[CCD_BakerAdded] = None
    baker_removed: Optional[CCD_BakerId] = None
    baker_stake_updated: Optional[CCD_BakerStakeUpdated] = None
    baker_restake_earnings_updated: Optional[
        CCD_BakerEvent_BakerRestakeEarningsUpdated
    ] = None
    baker_keys_updated: Optional[CCD_BakerKeysEvent] = None
    encrypted_amount_transferred: Optional[
        CCD_AccountTransactionEffects_EncryptedAmountTransferred
    ] = None
    transferred_to_encrypted: CCD_EncryptedSelfAmountAddedEvent = None
    transferred_to_public: CCD_AccountTransactionEffects_TransferredToPublic = None
    transferred_with_schedule: CCD_TransferredWithSchedule = None
    credential_keys_updated: CCD_CredentialRegistrationId = None
    credentials_updated: CCD_AccountTransactionEffects_CredentialsUpdated = None
    data_registered: CCD_RegisteredData = None
    baker_configured: CCD_BakerConfigured = None
    delegation_configured: CCD_DelegationConfigured = None


class CCD_AccountTransactionDetails(BaseModel):
    cost: microCCD
    sender: CCD_AccountAddress
    outcome: str
    effects: CCD_AccountTransactionEffects


class CCD_AccountCreationDetails(BaseModel):
    credential_type: int
    address: CCD_AccountAddress
    reg_id: CCD_CredentialRegistrationId


class CCD_ProtocolUpdate(BaseModel):
    message_: str
    specification_url: str
    specificationHash: CCD_Sha256Hash
    specification_auxiliary_data: Optional[bytes] = None


class CCD_Ratio(BaseModel):
    # note these are ints, but need to convert to str
    # as the int amounts are sometimes too big (for MongoDB)
    numerator: str
    denominator: str


class CCD_ExchangeRate(BaseModel):
    numerator: str
    denominator: str


class CCD_MintRate(BaseModel):
    mantissa: int
    exponent: int


class CCD_MintDistributionCpv0(BaseModel):
    mint_per_slot: CCD_MintRate
    baking_reward: CCD_AmountFraction
    finalization_reward: CCD_AmountFraction


class CCD_TransactionFeeDistribution(BaseModel):
    baker: Optional[CCD_AmountFraction] = None
    gas_account: Optional[CCD_AmountFraction] = None


class CCD_GasRewards(BaseModel):
    baker: CCD_AmountFraction
    finalization_proof: CCD_AmountFraction
    account_creation: CCD_AmountFraction
    chain_update: CCD_AmountFraction


class CCD_HigherLevelKeys(BaseModel):
    keys: list[CCD_UpdatePublicKey]
    threshold: CCD_UpdateKeysThreshold


class CCD_AccessStructure(BaseModel):
    access_public_keys: list[CCD_UpdateKeysIndex]
    access_threshold: CCD_UpdateKeysThreshold


class CCD_AuthorizationsV0(BaseModel):
    keys: list[CCD_UpdatePublicKey]
    emergency: CCD_AccessStructure
    protocol: CCD_AccessStructure
    parameter_election_difficulty: Optional[CCD_AccessStructure] = None
    parameter_euro_per_energy: CCD_AccessStructure
    parameter_micro_CCD_per_euro: CCD_AccessStructure
    parameter_foundation_account: CCD_AccessStructure
    parameter_mint_distribution: CCD_AccessStructure
    parameter_transaction_fee_distribution: CCD_AccessStructure
    parameter_gas_rewards: CCD_AccessStructure
    pool_parameters: CCD_AccessStructure
    add_anonymity_revoker: CCD_AccessStructure
    add_identity_provider: CCD_AccessStructure


class CCD_AuthorizationsV1(BaseModel):
    v0: CCD_AuthorizationsV0
    parameter_cooldown: CCD_AccessStructure
    parameter_time: CCD_AccessStructure


class CCD_RootUpdate(BaseModel):
    root_keys_update: CCD_HigherLevelKeys
    level_1_keys_update: CCD_HigherLevelKeys
    level_2_keys_update_v0: CCD_AuthorizationsV0
    level_2_keys_update_v1: CCD_AuthorizationsV1


class CCD_Level1Update(BaseModel):
    level_1_keys_update: Optional[CCD_HigherLevelKeys] = None
    level_2_keys_update_v0: Optional[CCD_AuthorizationsV0] = None
    level_2_keys_update_v1: Optional[CCD_AuthorizationsV1] = None


class CCD_Description(BaseModel):
    name: str
    url: str
    description: str


class CCD_ArInfo(BaseModel):
    identity: CCD_ArIdentity
    description: CCD_Description
    public_key: CCD_ArPublicKey


class CCD_IpInfo(BaseModel):
    identity: CCD_IpIdentity
    description: CCD_Description
    verify_key: CCD_IpVerifyKey
    cdi_verify_key: CCD_IpCdiVerifyKey


class CCD_CooldownParametersCpv1(BaseModel):
    pool_owner_cooldown: Optional[CCD_DurationSeconds] = None
    delegator_cooldown: Optional[CCD_DurationSeconds] = None


class CCD_InclusiveRangeAmountFraction(BaseModel):
    min: CCD_AmountFraction
    max_: CCD_AmountFraction


class CCD_CommissionRanges(BaseModel):
    finalization: CCD_InclusiveRangeAmountFraction
    baking: CCD_InclusiveRangeAmountFraction
    transaction: CCD_InclusiveRangeAmountFraction


class CCD_CapitalBound(BaseModel):
    value: CCD_AmountFraction


class CCD_LeverageFactor(BaseModel):
    value: CCD_Ratio


class CCD_PoolParametersCpv1(BaseModel):
    passive_finalization_commission: CCD_AmountFraction
    passive_baking_commission: CCD_AmountFraction
    passive_transaction_commission: CCD_AmountFraction
    commission_bounds: CCD_CommissionRanges
    minimum_equity_capital: microCCD
    capital_bound: CCD_CapitalBound
    leverage_bound: CCD_LeverageFactor


class CCD_RewardPeriodLength(BaseModel):
    value: CCD_Epoch


class CCD_TimeParametersCpv1(BaseModel):
    reward_period_length: CCD_Epoch
    mint_per_payday: CCD_MintRate


class CCD_MintDistributionCpv1(BaseModel):
    baking_reward: CCD_AmountFraction
    finalization_reward: CCD_AmountFraction


class CCD_BakerStakeThreshold(BaseModel):
    baker_stake_threshold: microCCD


class CCD_TransactionType(BaseModel):
    type: str
    contents: str


class CCD_UpdatePayload(BaseModel):
    protocol_update: CCD_ProtocolUpdate = None
    election_difficulty_update: CCD_ElectionDifficulty = None
    euro_per_energy_update: CCD_ExchangeRate = None
    micro_ccd_per_euro_update: CCD_ExchangeRate = None
    foundation_account_update: CCD_AccountAddress = None
    mint_distribution_update: CCD_MintDistributionCpv0 = None
    transaction_fee_distribution_update: CCD_TransactionFeeDistribution = None
    baker_stake_threshold_update: CCD_BakerStakeThreshold = None
    root_update: CCD_RootUpdate = None
    level_1_update: CCD_Level1Update = None
    add_anonymity_revoker_update: CCD_ArInfo = None
    add_identity_provider_update: CCD_IpInfo = None
    cooldown_parameters_cpv_1_update: CCD_CooldownParametersCpv1 = None
    pool_parameters_cpv_1_update: CCD_PoolParametersCpv1 = None
    time_parameters_cpv_1_update: CCD_TimeParametersCpv1 = None
    mint_distribution_cpv_1_update: CCD_MintDistributionCpv1 = None


class CCD_UpdateDetails(BaseModel):
    effective_time: CCD_TransactionTime = None
    payload: CCD_UpdatePayload


class CCD_ShortBlockInfo(BaseModel):
    height: int
    hash: CCD_BlockHash
    slot_time: CCD_TimeStamp


class CCD_BlockItemSummary(BaseModel):
    index: int = 0
    energy_cost: int = None
    hash: CCD_TransactionHash
    type: CCD_TransactionType = None
    account_transaction: CCD_AccountTransactionDetails = None
    account_creation: CCD_AccountCreationDetails = None
    update: CCD_UpdateDetails = None
    block_info: CCD_ShortBlockInfo = None


class CCD_Block(BaseModel):
    transaction_summaries: list[CCD_BlockItemSummary]


class AccountReleaseScheduleNodes(BaseModel):
    nodes: list


class CCD_Release(BaseModel):
    timestamp: CCD_TimeStamp
    amount: microCCD
    transactions: list[CCD_TransactionHash]


class CCD_ReleaseSchedule(BaseModel):
    schedules: list[CCD_Release]
    total: int


class CCD_BakerInfo(BaseModel):
    aggregation_key: str
    election_key: str
    baker_id: int
    signature_key: str


class CCD_AccountStakingInfo_Baker(BaseModel):
    baker_info: CCD_BakerInfo
    pool_info: CCD_BakerPoolInfo
    pending_change: CCD_StakePendingChange
    restake_earnings: bool
    staked_amount: microCCD


# class CCD_DelegationTarget(BaseModel):
#     baker_id: int = None
#     passive: str = None


class CCD_AccountStakingInfo_Delegator(BaseModel):
    target: CCD_DelegationTarget
    pending_change: CCD_StakePendingChange
    restake_earnings: bool
    staked_amount: microCCD


class CCD_AccountStakingInfo(BaseModel):
    baker: Optional[CCD_AccountStakingInfo_Baker] = None
    delegator: Optional[CCD_AccountStakingInfo_Delegator] = None


class CCD_AccountVerifyKey(BaseModel):
    ed25519_key: str


# class CCD_KeysEntry(BaseModel):
#     key: int
#     value: CCD_AccountVerifyKey


class CCD_CredentialPublicKeys(BaseModel):
    keys: dict[str, CCD_AccountVerifyKey]
    threshold: CCD_SignatureThreshold


class CCD_YearMonth(BaseModel):
    year: int
    month: int


class CCD_Policy(BaseModel):
    created_at: CCD_YearMonth
    valid_to: CCD_YearMonth
    attributes: dict[str, CCD_Policy_Attributes]


class CCD_InitialCredentialValues(BaseModel):
    credential_public_keys: CCD_CredentialPublicKeys
    cred_id: CCD_CredentialRegistrationId
    ip_id: CCD_IdentityProviderIdentity
    policy: CCD_Policy


class CCD_ChainArData(BaseModel):
    enc_id_cred_pub_share: str


# class CCD_ArDataEntry(BaseModel):
#     key: int
#     value: CCD_ChainArData


class CCD_CredentialCommitments_AttributesEntry(BaseModel):
    key: int
    value: CCD_Commitment


class CCD_CredentialCommitments(BaseModel):
    prf: CCD_Commitment
    cred_counter: CCD_Commitment
    max_accounts: CCD_Commitment
    attributes: dict[str, CCD_Commitment]
    id_cred_sec_sharing_coeff: list[CCD_Commitment]


class CCD_NormalCredentialValues(BaseModel):
    credential_public_keys: CCD_CredentialPublicKeys
    cred_id: CCD_CredentialRegistrationId
    ip_id: CCD_IdentityProviderIdentity
    policy: CCD_Policy
    ar_threshold: CCD_ArThreshold
    ar_data: dict[str, CCD_ChainArData]
    commitments: CCD_CredentialCommitments


class CCD_AccountCredential(BaseModel):
    initial: CCD_InitialCredentialValues = None
    normal: CCD_NormalCredentialValues = None


class CCD_EncryptedBalance(BaseModel):
    self_amount: CCD_EncryptedAmount
    start_index: int
    aggregated_amount: CCD_EncryptedAmount = None
    num_aggregated: int = None
    incoming_amounts: list[CCD_EncryptedAmount]


class CCD_AccountInfo(BaseModel):
    address: str
    amount: microCCD
    stake: CCD_AccountStakingInfo = None
    credentials: dict[str, CCD_AccountCredential]
    encrypted_balance: CCD_EncryptedBalance
    encryption_key: str
    index: int
    schedule: CCD_ReleaseSchedule = None
    threshold: int
    sequence_number: CCD_SequenceNumber


class CCD_TokenomicsInfo_V0(BaseModel):
    total_amount: microCCD
    total_encrypted_amount: microCCD
    baking_reward_account: microCCD
    finalization_reward_account: microCCD
    gas_account: microCCD
    protocol_version: int


class CCD_TokenomicsInfo_V1(BaseModel):
    total_amount: microCCD
    total_encrypted_amount: microCCD
    baking_reward_account: microCCD
    finalization_reward_account: microCCD
    gas_account: microCCD
    foundation_transaction_rewards: microCCD
    next_payday_time: CCD_TimeStamp
    next_payday_mint_rate: CCD_MintRate
    total_staked_capital: microCCD
    protocol_version: int


class CCD_TokenomicsInfo(BaseModel):
    v0: Optional[CCD_TokenomicsInfo_V0] = None
    v1: Optional[CCD_TokenomicsInfo_V1] = None


class CCD_InstanceInfo_V0(BaseModel):
    model: CCD_ContractStateV0
    owner: CCD_AccountAddress
    amount: microCCD
    methods: list[CCD_ReceiveName]
    name: CCD_InitName
    source_module: CCD_ModuleRef


class CCD_InstanceInfo_V1(BaseModel):
    owner: CCD_AccountAddress
    amount: microCCD
    methods: list[CCD_ReceiveName]
    name: CCD_InitName
    source_module: CCD_ModuleRef


class CCD_InstanceInfo(BaseModel):
    v0: CCD_InstanceInfo_V0
    v1: CCD_InstanceInfo_V1


class CCD_BlocksAtHeightResponse(BaseModel):
    blocks: list[CCD_BlockHash]


class CCD_BlockSpecialEvent_PaydayPoolReward(BaseModel):
    pool_owner: CCD_BakerId = None
    transaction_fees: microCCD
    baker_reward: microCCD
    finalization_reward: microCCD


class CCD_BlockSpecialEvent_BlockAccrueReward(BaseModel):
    transaction_fees: microCCD
    old_gas_account: microCCD
    new_gas_account: microCCD
    baker_reward: microCCD
    passive_reward: microCCD
    foundation_charge: microCCD
    baker: CCD_BakerId


class CCD_BlockSpecialEvent_PaydayAccountReward(BaseModel):
    account: CCD_AccountAddress
    transaction_fees: microCCD
    baker_reward: microCCD
    finalization_reward: microCCD


class CCD_BlockSpecialEvent_PaydayFoundationReward(BaseModel):
    foundation_account: CCD_AccountAddress
    development_charge: microCCD


class CCD_BlockSpecialEvent_BlockReward(BaseModel):
    transaction_fees: microCCD
    old_gas_account: microCCD
    new_gas_account: microCCD
    baker_reward: microCCD
    foundation_charge: microCCD
    foundation_account: CCD_AccountAddress
    baker: CCD_AccountAddress


class CCD_BlockSpecialEvent_AccountAmounts_Entry(BaseModel):
    account: CCD_AccountAddress
    amount: microCCD


class CCD_BlockSpecialEvent_AccountAmounts(BaseModel):
    entries: list[CCD_BlockSpecialEvent_AccountAmounts_Entry]


class CCD_BlockSpecialEvent_FinalizationRewards(BaseModel):
    finalization_rewards: CCD_BlockSpecialEvent_AccountAmounts
    remainder: microCCD


class CCD_BlockSpecialEvent_BakingRewards(BaseModel):
    baker_rewards: CCD_BlockSpecialEvent_AccountAmounts
    remainder: microCCD


class CCD_BlockSpecialEvent_Mint(BaseModel):
    mint_baking_reward: microCCD
    mint_finalization_reward: microCCD
    mint_platform_development_charge: microCCD
    foundation_account: CCD_AccountAddress


class CCD_BlockSpecialEvent(BaseModel):
    baking_rewards: CCD_BlockSpecialEvent_BakingRewards = None
    mint: CCD_BlockSpecialEvent_Mint = None
    finalization_rewards: CCD_BlockSpecialEvent_FinalizationRewards = None
    block_reward: CCD_BlockSpecialEvent_BlockReward = None
    payday_foundation_reward: CCD_BlockSpecialEvent_PaydayFoundationReward = None
    payday_account_reward: CCD_BlockSpecialEvent_PaydayAccountReward = None
    block_accrue_reward: CCD_BlockSpecialEvent_BlockAccrueReward = None
    payday_pool_reward: CCD_BlockSpecialEvent_PaydayPoolReward = None


class CCD_PendingUpdate(BaseModel):
    effective_time: CCD_TransactionTime
    root_keys: CCD_HigherLevelKeys = None
    level1_keys: CCD_HigherLevelKeys = None
    level2_keys_cpc_0: CCD_AuthorizationsV0 = None
    level2_keys_cpc_1: CCD_AuthorizationsV1 = None
    protocol: CCD_ProtocolUpdate = None
    election_difficulty: CCD_ElectionDifficulty = None
    euro_per_energy: CCD_ExchangeRate = None
    micro_ccd_per_euro: CCD_ExchangeRate = None
    foundation_account: CCD_AccountAddress = None
    mint_distribution_cpv_0: CCD_MintDistributionCpv0 = None
    mint_distribution_cpv_1: CCD_MintDistributionCpv1 = None
    transaction_fee_distribution: CCD_TransactionFeeDistribution = None
    gas_rewards: CCD_GasRewards
    pool_parameters_cpv_0: CCD_BakerStakeThreshold = None
    pool_parameters_cpv_0: CCD_PoolParametersCpv1 = None
    add_anonymity_revoker: CCD_ArInfo = None
    add_identity_provider: CCD_IpInfo = None
    cooldown_parameters: CCD_CooldownParametersCpv1 = None
    pool_parameters_cpv_1_update: CCD_PoolParametersCpv1 = None
    time_parameters: CCD_TimeParametersCpv1 = None


class CCD_ElectionInfo_Baker(BaseModel):
    baker: CCD_BakerId
    account: CCD_AccountAddress
    lottery_power: float


class CCD_ElectionInfo(BaseModel):
    election_difficulty: CCD_ElectionDifficulty = None
    election_nonce: CCD_LeadershipElectionNonce
    baker_election_info: list[CCD_ElectionInfo_Baker]


class CCD_ConsensusInfo(BaseModel):
    best_block: CCD_BlockHash
    genesis_block: CCD_BlockHash
    genesis_time: CCD_TimeStamp
    slot_duration: CCD_Duration = None
    epoch_duration: CCD_Duration
    last_finalized_block: CCD_BlockHash
    best_block_height: int
    last_finalized_block_height: int
    blocks_received_count: int
    block_last_received_time: CCD_TimeStamp = None
    block_receive_latency_ema: float
    block_receive_latency_emsd: float
    block_receive_period_ema: float = None
    block_receive_period_emsd: float = None
    blocks_verified_count: int
    block_last_arrived_time: CCD_TimeStamp = None
    block_arrive_latency_ema: float
    block_arrive_latency_emsd: float
    block_arrive_period_ema: float = None
    block_arrive_period_emsd: float = None
    transactions_per_block_ema: float
    transactions_per_block_emsd: float
    finalization_count: int
    last_finalized_time: CCD_TimeStamp = None
    finalization_period_ema: float = None
    finalization_period_emsd: float = None
    protocol_version: str
    genesis_index: int
    current_era_genesis_block: CCD_BlockHash
    current_era_genesis_time: CCD_TimeStamp
    current_timeout_duration: CCD_Duration = None
    current_round: CCD_Round = None
    current_epoch: CCD_Epoch = None
    trigger_block_time: CCD_TimeStamp = None


class CCD_VersionedModuleSource(BaseModel):
    v0: CCD_VersionedModuleSource_ModuleSourceV0 = None
    v1: CCD_VersionedModuleSource_ModuleSourceV1 = None


class CCD_ChainParametersV0(BaseModel):
    election_difficulty: CCD_ElectionDifficulty
    euro_per_energy: CCD_ExchangeRate
    micro_ccd_per_euro: CCD_ExchangeRate
    baker_cooldown_epochs: CCD_Epoch
    account_creation_limit: CCD_CredentialsPerBlockLimit
    mint_distribution: CCD_MintDistributionCpv0
    transaction_fee_distribution: CCD_TransactionFeeDistribution
    gas_rewards: CCD_GasRewards
    foundation_account: CCD_AccountAddress
    minimum_threshold_for_baking: microCCD
    root_keys: CCD_HigherLevelKeys
    level1_keys: CCD_HigherLevelKeys
    level2_keys: CCD_AuthorizationsV0


class CCD_ChainParametersV1(BaseModel):
    election_difficulty: CCD_ElectionDifficulty
    euro_per_energy: CCD_ExchangeRate
    micro_ccd_per_euro: CCD_ExchangeRate
    cooldown_parameters: CCD_CooldownParametersCpv1
    time_parameters: CCD_TimeParametersCpv1
    account_creation_limit: CCD_CredentialsPerBlockLimit
    mint_distribution: CCD_MintDistributionCpv1
    transaction_fee_distribution: CCD_TransactionFeeDistribution
    gas_rewards: CCD_GasRewards
    foundation_account: CCD_AccountAddress
    pool_parameters: CCD_PoolParametersCpv1
    root_keys: CCD_HigherLevelKeys
    level1_keys: CCD_HigherLevelKeys
    level2_keys: CCD_AuthorizationsV1


class CCD_TimeOutParameters(BaseModel):
    timeout_base: CCD_Duration
    timeout_increase: CCD_Ratio
    timeout_decrease: CCD_Ratio


class CCD_ConsensusParametersV1(BaseModel):
    timeout_parameters: CCD_TimeOutParameters
    min_block_time: CCD_Duration
    block_energy_limit: CCD_Energy


class CCD_GasRewardsV2(BaseModel):
    baker: CCD_AmountFraction
    account_creation: CCD_AmountFraction
    chain_update: CCD_AmountFraction


class CCD_FinalizationCommitteeParameters(BaseModel):
    minimum_finalizers: int
    maximum_finalizers: int
    finalizer_relative_stake_threshold: CCD_AmountFraction


class CCD_ChainParametersV2(BaseModel):
    consensus_parameters: CCD_ConsensusParametersV1
    euro_per_energy: CCD_ExchangeRate
    micro_ccd_per_euro: CCD_ExchangeRate
    cooldown_parameters: CCD_CooldownParametersCpv1
    time_parameters: CCD_TimeParametersCpv1
    account_creation_limit: CCD_CredentialsPerBlockLimit
    mint_distribution: CCD_MintDistributionCpv1
    transaction_fee_distribution: CCD_TransactionFeeDistribution
    gas_rewards: CCD_GasRewardsV2
    foundation_account: CCD_AccountAddress
    pool_parameters: CCD_PoolParametersCpv1
    root_keys: CCD_HigherLevelKeys
    level1_keys: CCD_HigherLevelKeys
    level2_keys: CCD_AuthorizationsV1
    finalization_committee_parameters: CCD_FinalizationCommitteeParameters


class CCD_ChainParameters(BaseModel):
    v0: CCD_ChainParametersV0 = None
    v1: CCD_ChainParametersV1 = None
    v2: CCD_ChainParametersV2 = None


class CCD_InvokeInstanceResponse_Success(BaseModel):
    return_value: bytes
    used_energy: CCD_Energy
    effects: list[CCD_ContractTraceElement]


class CCD_InvokeInstanceResponse_Failure(BaseModel):
    return_value: bytes
    used_energy: CCD_Energy
    reason: CCD_RejectReason


class CCD_InvokeInstanceResponse(BaseModel):
    success: CCD_InvokeInstanceResponse_Success
    failure: CCD_InvokeInstanceResponse_Failure


class CCD_BlockComplete(BaseModel):
    block_info: CCD_BlockInfo
    transaction_summaries: list[CCD_BlockItemSummary]
    special_events: list[CCD_BlockSpecialEvent]
    net: str = None
