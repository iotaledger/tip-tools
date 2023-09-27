from typing import List
from schemas.output import output_type_field
from typedefs.field import ComplexField, Field, Schema, SimpleField
from typedefs.datatype import UInt64, UInt32, UInt16, UInt8, LengthPrefixedArray
from typedefs.subschema import OneOf


protocol_parameters_name = "Protocol Parameters"

param_type = SimpleField(
    "Type", UInt8(), "Set to <b>value 0</b> to denote IOTA 2.0 protocol parameters."
)

version = SimpleField(
    "Version",
    UInt8(),
    "The version of protocol parameters.",
)

network_name = SimpleField(
    "Network Name",
    LengthPrefixedArray(UInt8()),
    "The name of the network the node is running on.",
)

bech32HRP = SimpleField(
    "Bech32HRP",
    LengthPrefixedArray(UInt8()),
    "Bech32HRP defines the HRP prefix used for Bech32 addresses in the network.",
)

token_supply = SimpleField(
    "Token Supply",
    UInt64(),
    "Token Supply defines the current token supply on the network.",
)

genesis_unix_timestamp = SimpleField(
    "Genesis Unix Timestamp",
    UInt64(),
    "Genesis Unix Timestamp defines the genesis timestamp at which the slots start to count",
)

slot_duration_in_seconds = SimpleField(
    "Slot Duration In Seconds",
    UInt8(),
    "Slot Duration In Seconds defines the duration of each slot in seconds.",
)

slots_per_epoch_exponent = SimpleField(
    "Slots Per Epoch Exponent",
    UInt8(),
    "Slots Per Epoch Exponent is the number of slots in an epoch expressed as an exponent of 2. (2**SlotsPerEpochExponent) == slots in an epoch.",
)

staking_unbounding_period = SimpleField(
    "Staking Unbounding Period",
    UInt32(),
    "Staking Unbonding Period defines the unbonding period in epochs before an account can stop staking.",
)

validation_blocks_per_slot = SimpleField(
    "Validation Blocks Per Slot",
    UInt16(),
    "Validation Blocks Per Slot is the number of validation blocks that each validator should issue each slot.",
)

punishment_epochs = SimpleField(
    "Punishment Epochs",
    UInt32(),
    "The number of epochs worth of Mana that a node is punished with for each additional validation block it issues.",
)

liveness_threshold = SimpleField(
    "Liveness Threshold",
    UInt64(),
    "Liveness Threshold is used by tip-selection to determine if a block is eligible by evaluating issuingTimes and commitments in its past-cone to Accepted Tangle Time and lastCommittedSlot respectively.",
)

min_committable_age = SimpleField(
    "Min Committable Age",
    UInt64(),
    "Min Committable Age is the minimum age relative to the accepted tangle time slot index that a slot can be committed.",
)

max_committable_age = SimpleField(
    "Max Committable Age",
    UInt64(),
    "Max Committable Age is the maximum age for a slot commitment to be included in a block relative to the slot index of the block issuing time.",
)

epoch_nearing_threshold = SimpleField(
    "Epoch Nearing Threshold",
    UInt64(),
    "Epoch Nearing Threshold is used by the epoch orchestrator to detect the slot that should trigger a new committee selection for the next and upcoming epoch.",
)

# rent structure
vByte_cost = SimpleField(
    "VByte Cost",
    UInt32(),
    "VByte Cost defines the rent of a single virtual byte denoted in IOTA tokens.",
)
vByte_factor_data = SimpleField(
    "VByte Factor Data",
    UInt8(),
    "VByte Factor Data defines the factor to be used for data only fields.",
)
vByte_factor_key = SimpleField(
    "VByte Factor Key",
    UInt8(),
    "VByte Factor Key defines the factor to be used for key/lookup generating fields.",
)
vByte_factor_block_issuer_key = SimpleField(
    "VByte Factor Block Issuer Key",
    UInt8(),
    "VByte Factor Block Issuer Key defines the factor to be used for block issuer feature public keys.",
)
vByte_factor_staking_feature = SimpleField(
    "VByte Factor Staking Feature",
    UInt8(),
    "VByte Factor Staking Feature defines the factor to be used for staking feature.",
)
vByte_factor_delegation = SimpleField(
    "VByte Factor Delegation",
    UInt8(),
    "VByte Factor Delegation defines the factor to be used for delegation output.",
)

RentStructure = ComplexField(
    "Rent Structure",
    OneOf(),
    [
        Schema(
            "Rent Structure",
            "Rent Structure defines the rent structure used by a given node/network.",
            [
                vByte_cost,
                vByte_factor_data,
                vByte_factor_key,
                vByte_factor_block_issuer_key,
                vByte_factor_staking_feature,
                vByte_factor_delegation,
            ],
        )
    ],
)

# work score structure
data_byte = SimpleField(
    "Data Byte", UInt32(), "Accounts for the network traffic per byte."
)
block = SimpleField(
    "Block", UInt32(), "Accounts for work done to process a block in the node software."
)
missing_parent = SimpleField(
    "Missing Parent",
    UInt32(),
    "The work score factor to apply when not enough strong parents are present as determined by <code>Min Strong Parents Threshold</code>.",
)
input = SimpleField(
    "Input",
    UInt32(),
    "Accounts for loading the UTXO from the database and performing the mana balance check.",
)
context_input = SimpleField(
    "Context Input", UInt32(), "Accounts for loading and checking the context input."
)
output = SimpleField(
    "Output", UInt32(), "Accounts for storing the UTXO in the database."
)
native_token = SimpleField(
    "Native Token",
    UInt32(),
    "Accounts for native token balance checks which use big integers.",
)
staking = SimpleField(
    "Staking",
    UInt32(),
    "Accounts for the cost of updating the staking vector when a staking feature is present.",
)
block_issuer = SimpleField(
    "Block Issuer",
    UInt32(),
    "Accounts for the cost of updating the block issuer keys when a block issuer feature is present.",
)
allotment = SimpleField(
    "Allotment",
    UInt32(),
    "Accounts for accessing the account based ledger to transform the allotted mana to block issuance credits.",
)
signature_ed25519 = SimpleField(
    "Signature Ed25519", UInt32(), "Accounts for an Ed25519 signature check."
)
min_strong_parents_threshold = SimpleField(
    "Min Strong Parents Threshold",
    UInt8(),
    "The minimum number of strong parents needed in a basic block. If not reached, the block's work score increases.",
)

WorkScoreStructure = ComplexField(
    "Work Score Structure",
    OneOf(),
    [
        Schema(
            "Work Score Structure",
            "Work Score Structure defines the work score structure used by a given node/network.",
            [
                data_byte,
                block,
                missing_parent,
                input,
                context_input,
                output,
                native_token,
                staking,
                block_issuer,
                allotment,
                signature_ed25519,
                min_strong_parents_threshold,
            ],
        )
    ],
)

# mana structure
bits_count = SimpleField(
    "Bits Count", UInt8(), "Bits Count is the number of bits used to represent Mana."
)
generation_rate = SimpleField(
    "Generation Rate",
    UInt8(),
    "Generation Rate is the amount of potential Mana generated by 1 IOTA in 1 slot.",
)
generation_rate_exponent = SimpleField(
    "Generation Rate Exponent",
    UInt8(),
    "Generation Rate Exponent is the scaling of Mana Generation Rate expressed as an exponent of 2.",
)
decay_factors = SimpleField(
    "Decay Factors",
    LengthPrefixedArray(UInt16(), UInt32()),
    "Decay Factors is the number of decay factors used to calculate the decay of Mana.",
)
decay_factors_exponent = SimpleField(
    "Decay Factors Exponent",
    UInt8(),
    "Decay Factors Exponent is the scaling of ManaDecayFactors expressed as an exponent of 2.",
)
decay_factors_epochs_sum = SimpleField(
    "Decay Factors Epochs Sum",
    UInt32(),
    "Decay Factor Epochs Sum is an integer approximation of the sum of decay over epochs.",
)
decay_factors_epochs_sum_exponent = SimpleField(
    "Decay Factors Epochs Sum Exponent",
    UInt8(),
    "Decay Factor Epochs Sum Exponent is the scaling of Decay Factor Epochs Sum expressed as an exponent of 2.",
)

ManaStructure = ComplexField(
    "Mana Structure",
    OneOf(),
    [
        Schema(
            "Mana Structure",
            "Mana Structure defines the parameters used by mana calculation.",
            [
                bits_count,
                generation_rate,
                generation_rate_exponent,
                decay_factors,
                decay_factors_exponent,
                decay_factors_epochs_sum,
                decay_factors_epochs_sum_exponent,
            ],
        )
    ],
)

# congestion control parameter
min_reference_mana_cost = SimpleField(
    "Min Reference Mana Cost",
    UInt64(),
    "Min Reference Mana Cost is the minimum value of the Reference Mana Cost.",
)
increase = SimpleField(
    "Increase",
    UInt64(),
    "Increase is the increase step size of the Reference Mana Cost.",
)
decrease = SimpleField(
    "Decrease",
    UInt64(),
    "Decrease is the decrease step size of the Reference Mana Cost.",
)
increase_threshold = SimpleField(
    "Increase Threshold",
    UInt32(),
    "Increase Threshold is the threshold for increasing the Reference Mana Cost.",
)
decrease_threshold = SimpleField(
    "Decrease Threshold",
    UInt32(),
    "Decrease Threshold is the threshold for decreasing the Reference Mana Cost.",
)
scheduler_rate = SimpleField(
    "Scheduler Rate",
    UInt32(),
    "Scheduler Rate is the rate at which the scheduler runs in workscore units per second.",
)
min_mana = SimpleField(
    "Min Mana",
    UInt64(),
    "Min Mana is the minimum amount of Mana that an account must have to have a block scheduled.",
)
max_buffer_size = SimpleField(
    "Max Buffer Size",
    UInt32(),
    "Max Buffer Size is the maximum size of the buffer in scheduler.",
)
max_validation_buffer_size = SimpleField(
    "Max Validation Buffer Size",
    UInt32(),
    "The maximum number of blocks in the validation buffer.",
)

CongestionControlParameters = ComplexField(
    "Congestion Control Parameters",
    OneOf(),
    [
        Schema(
            "Congestion Control Parameters",
            "Congestion Control Parameters defines the parameters that are used to calculate the Reference Mana Cost (RMC).",
            [
                min_reference_mana_cost,
                increase,
                decrease,
                increase_threshold,
                decrease_threshold,
                scheduler_rate,
                min_mana,
                max_buffer_size,
                max_validation_buffer_size,
            ],
        )
    ],
)

# version signaling
window_size = SimpleField(
    "Window Size",
    UInt8(),
    "The size of the window in epochs to find which version of protocol parameters was most signaled, from currentEpoch - windowSize to currentEpoch.",
)
window_target_ration = SimpleField(
    "Window Target Ratio",
    UInt8(),
    "The target number of supporters for a version to win in a windowSize.",
)
activation_offset = SimpleField(
    "Activation Offset",
    UInt8(),
    "The offset in epochs to activate the new version of protocol parameters.",
)

VersionSignaling = ComplexField(
    "Version Signaling",
    OneOf(),
    [
        Schema(
            "Version Signaling",
            "Version Signaling defines the parameters used by signaling protocol parameters upgrade.",
            [window_size, window_target_ration, activation_offset],
        )
    ],
)

# rewards parameters

reward_validation_blocks_per_slot = SimpleField(
    "Validation Blocks Per Slot",
    UInt8(),
    "The number of validation blocks that should be issued by a selected validator per slot during its epoch duties.",
)
profit_margin_exponent = SimpleField(
    "Profit Margin Exponent",
    UInt8(),
    "Profit Margin Exponent is used for shift operation for calculation of profit margin.",
)
bootstrapping_duration = SimpleField(
    "Bootstrapping Duration",
    UInt64(),
    "The length in epochs of the bootstrapping phase.",
)
mana_share_coefficient = SimpleField(
    "Mana Share Coefficient",
    UInt64(),
    "Mana Share Coefficient is the coefficient used for calculation of initial rewards.",
)
decay_balancing_constant_exponent = SimpleField(
    "Decay Balancing Constant Exponent",
    UInt8(),
    "Decay Balancing Constant Exponent is the exponent used for calculation of the initial reward.",
)
decay_balancing_constant = SimpleField(
    "Decay Balancing Constant",
    UInt64(),
    "Decay Balancing Constant is an integer approximation calculated based on chosen DecayBalancingConstantExponent.",
)
pool_coefficient_exponent = SimpleField(
    "Pool Coefficient Exponent",
    UInt8(),
    "Pool Coefficient Exponent is the exponent used for shifting operation in the pool rewards calculations.",
)

RewardsParameters = ComplexField(
    "Rewards Parameters",
    OneOf(),
    [
        Schema(
            "Rewards Parameters",
            "Rewards Parameters defines the parameters that are used to calculate Mana rewards.",
            [
                reward_validation_blocks_per_slot,
                profit_margin_exponent,
                bootstrapping_duration,
                mana_share_coefficient,
                decay_balancing_constant_exponent,
                decay_balancing_constant,
                pool_coefficient_exponent,
            ],
        )
    ],
)


protocol_parameters_fields: List[Field] = [
    param_type,
    version,
    network_name,
    bech32HRP,
    RentStructure,
    WorkScoreStructure,
    token_supply,
    genesis_unix_timestamp,
    slot_duration_in_seconds,
    slots_per_epoch_exponent,
    ManaStructure,
    staking_unbounding_period,
    validation_blocks_per_slot,
    punishment_epochs,
    liveness_threshold,
    min_committable_age,
    max_committable_age,
    epoch_nearing_threshold,
    CongestionControlParameters,
    VersionSignaling,
    RewardsParameters,
]

ProtocolParameters = Schema(protocol_parameters_name, None, protocol_parameters_fields)
