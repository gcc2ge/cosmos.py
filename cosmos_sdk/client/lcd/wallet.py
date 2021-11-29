from __future__ import annotations

from typing import List, Optional, Union

from cosmos_sdk.core import Coins, Numeric
from cosmos_sdk.core.msg import Msg
from cosmos_sdk.key.key import Key, SignOptions

from .api.tx import CreateTxOptions, SignerOptions

__all__ = ["Wallet", "AsyncWallet"]

from ...core.tx import SignMode, Tx


class AsyncWallet:
    def __init__(self, lcd, key: Key):
        self.lcd = lcd
        self.key = key

    async def account_number(self) -> int:
        res = await self.lcd.auth.account_info(self.key.acc_address)
        return res.account_number

    async def sequence(self) -> int:
        res = await self.lcd.auth.account_info(self.key.acc_address)
        return res.sequence

    async def account_number_and_sequence(self) -> dict:
        res = await self.lcd.auth.account_info(self.key.acc_address)
        return {"account_number": res.account_number, "sequence": res.sequence}

    async def create_tx(
        self, signers: List[SignerOptions], options: CreateTxOptions
    ) -> Tx:
        return await self.lcd.tx.create(signers, options)

    async def create_and_sign_tx(
        self, signers: List[SignerOptions], options: CreateTxOptions
    ) -> Tx:
        if options.account_number is None or options.sequence is None:
            res = await self.account_number_and_sequence()
            if options.account_number is None:
                options.account_number = res.get("account_number")
            if options.sequence is None:
                options.sequence = res.get("sequence")

        tx = await self.create_tx(signers, options)
        sign_options = SignOptions(
            options.account_number,
            options.sequence,
            options.sign_mode,
            self.lcd.chain_id,
        )
        return self.key.sign_tx(tx, sign_options)


class Wallet:
    """Wraps around a :class:`Key` implementation and provides transaction building and
    signing functionality. It is recommended to create this object through
    :meth:`LCDClient.wallet()<cosmos_sdk.client.lcd.LCDClient.wallet>`."""

    def __init__(self, lcd, key: Key):
        self.lcd = lcd
        self.key = key

    def account_number(self) -> int:
        """Fetches account number for the account associated with the Key."""
        res = self.lcd.auth.account_info(self.key.acc_address)
        return res.account_number

    def sequence(self) -> int:
        """Fetches the sequence number for the account associated with the Key."""
        res = self.lcd.auth.account_info(self.key.acc_address)
        return res.sequence

    def account_number_and_sequence(self) -> dict:
        """Fetches both account and sequence number associated with the Key."""
        res = self.lcd.auth.account_info(self.key.acc_address)
        return {"account_number": res.account_number, "sequence": res.sequence}

    def create_tx(self, options: CreateTxOptions) -> Tx:
        """Builds an unsigned transaction object. The ``Wallet`` will first
        query the blockchain to fetch the latest ``account`` and ``sequence`` values for the
        account corresponding to its Key, unless the they are both provided. If no ``fee``
        parameter is set, automatic fee estimation will be used (see `fee_estimation`).

        Args:
            msgs (List[Msg]): list of messages to include
            fee (Optional[Fee], optional): transaction fee. If ``None``, will be estimated.
                See more on `fee estimation`_.
            memo (str, optional): optional short string to include with transaction.
            gas_prices (Optional[Coins.Input], optional): gas prices for fee estimation.
            gas_adjustment (Optional[Numeric.Input], optional): gas adjustment for fee estimation.
            fee_denoms (Optional[List[str]], optional): list of denoms to use for fee after estimation.
            account_number (Optional[int], optional): account number (overrides blockchain query if
                provided)
            sequence (Optional[int], optional): sequence (overrides blockchain qu ery if provided)

        Returns:
            Tx: unsigned transaction
        """
        sigOpt = [
            SignerOptions(
                address=self.key.acc_address,
                sequence=options.sequence,
                public_key=self.key.public_key,
            )
        ]
        return self.lcd.tx.create(sigOpt, options)

    def create_and_sign_tx(self, options: CreateTxOptions) -> Tx:
        """Creates and signs a :class:`Tx` object in a single step. This is the recommended
        method for preparing transaction for immediate signing and broadcastring. The transaction
        is generated exactly as :meth:`create_tx`.

        Args:
            msgs (List[Msg]): list of messages to include
            fee (Optional[Fee], optional): transaction fee. If ``None``, will be estimated.
                See more on `fee estimation`_.
            memo (str, optional): optional short string to include with transaction.
            gas_prices (Optional[Coins.Input], optional): gas prices for fee estimation.
            gas_adjustment (Optional[Numeric.Input], optional): gas adjustment for fee estimation.
            fee_denoms (Optional[List[str]], optional): list of denoms to use for fee after estimation.
            account_number (Optional[int], optional): account number (overrides blockchain query if
                provided)
            sequence (Optional[int], optional): sequence (overrides blockchain qu ery if provided)

        Returns:
            Tx: signed transaction
        """

        account_number = options.account_number
        sequence = options.sequence
        if account_number is None or sequence is None:
            res = self.account_number_and_sequence()
            if account_number is None:
                account_number = res.get("account_number")
            if sequence is None:
                sequence = res.get("sequence")
        options.sequence = sequence
        options.account_number = account_number
        return self.key.sign_tx(
            tx=self.create_tx(options),
            options=SignOptions(
                account_number=account_number,
                sequence=sequence,
                chain_id=self.lcd.chain_id,
                sign_mode=options.sign_mode
                if options.sign_mode
                else SignMode.SIGN_MODE_DIRECT,
            ),
        )
