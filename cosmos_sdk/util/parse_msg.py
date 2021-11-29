from cosmos_sdk.core.authz import (
    MsgExecAuthorized,
    MsgGrantAuthorization,
    MsgRevokeAuthorization,
)
from cosmos_sdk.core.bank import MsgMultiSend, MsgSend
from cosmos_sdk.core.distribution import (
    MsgFundCommunityPool,
    MsgSetWithdrawAddress,
    MsgWithdrawDelegationReward,
    MsgWithdrawValidatorCommission,
)
from cosmos_sdk.core.gamm.msgs import MsgSwapExactAmountIn, MsgSwapExactAmountOut
from cosmos_sdk.core.gov.msgs import MsgDeposit, MsgSubmitProposal, MsgVote
from cosmos_sdk.core.ibc.msgs import MsgTransfer
from cosmos_sdk.core.market import MsgSwap, MsgSwapSend
from cosmos_sdk.core.oracle import (
    MsgAggregateExchangeRatePrevote,
    MsgAggregateExchangeRateVote,
    MsgDelegateFeedConsent,
)
from cosmos_sdk.core.slashing import MsgUnjail
from cosmos_sdk.core.staking import (
    MsgBeginRedelegate,
    MsgCreateValidator,
    MsgDelegate,
    MsgEditValidator,
    MsgUndelegate,
)
from cosmos_sdk.core.wasm import (
    MsgClearContractAdmin,
    MsgExecuteContract,
    MsgInstantiateContract,
    MsgMigrateCode,
    MsgMigrateContract,
    MsgStoreCode,
    MsgUpdateContractAdmin,
)

from .base import create_demux, create_demux_proto

bank_msgs = [MsgSend, MsgMultiSend]
distribution_msgs = [
    MsgFundCommunityPool,
    MsgSetWithdrawAddress,
    MsgWithdrawDelegationReward,
    MsgWithdrawValidatorCommission,
]
gamm_msgs = [MsgSwapExactAmountIn, MsgSwapExactAmountOut]
gov_msgs = [MsgDeposit, MsgSubmitProposal, MsgVote]
ibc_msgs = [MsgTransfer]
market_msgs = [MsgSwap, MsgSwapSend]
authz_msgs = [
    MsgExecAuthorized,
    MsgGrantAuthorization,
    MsgRevokeAuthorization,
]
oracle_msgs = [
    MsgAggregateExchangeRatePrevote,
    MsgAggregateExchangeRateVote,
    MsgDelegateFeedConsent,
]
slashing_msgs = [MsgUnjail]
staking_msgs = [
    MsgBeginRedelegate,
    MsgCreateValidator,
    MsgDelegate,
    MsgEditValidator,
    MsgUndelegate,
]
wasm_msgs = [
    MsgStoreCode,
    MsgMigrateCode,
    MsgInstantiateContract,
    MsgExecuteContract,
    MsgMigrateContract,
    MsgUpdateContractAdmin,
    MsgClearContractAdmin,
]

msgs = [
    *bank_msgs,
    *distribution_msgs,
    *gamm_msgs,
    *gov_msgs,
    *ibc_msgs,
    *market_msgs,
    *authz_msgs,
    *oracle_msgs,
    *slashing_msgs,
    *staking_msgs,
    *wasm_msgs,
]

parse_msg = create_demux(msgs)
parse_proto = create_demux_proto(msgs)
