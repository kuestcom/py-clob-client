import time

from .helpers import (
    to_token_decimals,
    round_down,
    round_normal,
    decimal_places,
    round_up,
)
from .constants import BUY, SELL
from ..config import get_contract_config
from ..signer import Signer
from ..utilities import builder_code_to_bytes32
from ..order_utils import ExchangeOrderBuilderV2, SignatureTypeV2, Side
from ..order_utils.model.order_data_v2 import OrderDataV2, SignedOrderV2
from ..clob_types import (
    OrderArgs,
    CreateOrderOptions,
    TickSize,
    RoundConfig,
    MarketOrderArgs,
    OrderSummary,
    OrderType,
)

ROUNDING_CONFIG: dict[TickSize, RoundConfig] = {
    "0.1": RoundConfig(price=1, size=2, amount=3),
    "0.01": RoundConfig(price=2, size=2, amount=4),
    "0.001": RoundConfig(price=3, size=2, amount=5),
    "0.0001": RoundConfig(price=4, size=2, amount=6),
}


class OrderBuilder:
    def __init__(self, signer: Signer, sig_type=None, funder=None):
        self.signer = signer

        self.sig_type = (
            sig_type if sig_type is not None else SignatureTypeV2.DEPOSIT_WALLET
        )
        if int(self.sig_type) != int(SignatureTypeV2.DEPOSIT_WALLET):
            raise ValueError(
                "Kuest order flow supports only Deposit Wallet signature type 3"
            )

        self.funder = funder

    def get_order_amounts(
        self, side: str, size: float, price: float, round_config: RoundConfig
    ):
        raw_price = round_normal(price, round_config.price)

        if side == BUY:
            raw_taker_amt = round_down(size, round_config.size)

            raw_maker_amt = raw_taker_amt * raw_price
            if decimal_places(raw_maker_amt) > round_config.amount:
                raw_maker_amt = round_up(raw_maker_amt, round_config.amount + 4)
                if decimal_places(raw_maker_amt) > round_config.amount:
                    raw_maker_amt = round_down(raw_maker_amt, round_config.amount)

            maker_amount = to_token_decimals(raw_maker_amt)
            taker_amount = to_token_decimals(raw_taker_amt)

            return Side.BUY, maker_amount, taker_amount
        elif side == SELL:
            raw_maker_amt = round_down(size, round_config.size)

            raw_taker_amt = raw_maker_amt * raw_price
            if decimal_places(raw_taker_amt) > round_config.amount:
                raw_taker_amt = round_up(raw_taker_amt, round_config.amount + 4)
                if decimal_places(raw_taker_amt) > round_config.amount:
                    raw_taker_amt = round_down(raw_taker_amt, round_config.amount)

            maker_amount = to_token_decimals(raw_maker_amt)
            taker_amount = to_token_decimals(raw_taker_amt)

            return Side.SELL, maker_amount, taker_amount
        else:
            raise ValueError(f"order_args.side must be '{BUY}' or '{SELL}'")

    def get_market_order_amounts(
        self, side: str, amount: float, price: float, round_config: RoundConfig
    ):
        raw_price = round_normal(price, round_config.price)

        if side == BUY:
            raw_maker_amt = round_down(amount, round_config.size)
            raw_taker_amt = raw_maker_amt / raw_price
            if decimal_places(raw_taker_amt) > round_config.amount:
                raw_taker_amt = round_up(raw_taker_amt, round_config.amount + 4)
                if decimal_places(raw_taker_amt) > round_config.amount:
                    raw_taker_amt = round_down(raw_taker_amt, round_config.amount)

            maker_amount = to_token_decimals(raw_maker_amt)
            taker_amount = to_token_decimals(raw_taker_amt)

            return Side.BUY, maker_amount, taker_amount

        elif side == SELL:
            raw_maker_amt = round_down(amount, round_config.size)

            raw_taker_amt = raw_maker_amt * raw_price
            if decimal_places(raw_taker_amt) > round_config.amount:
                raw_taker_amt = round_up(raw_taker_amt, round_config.amount + 4)
                if decimal_places(raw_taker_amt) > round_config.amount:
                    raw_taker_amt = round_down(raw_taker_amt, round_config.amount)

            maker_amount = to_token_decimals(raw_maker_amt)
            taker_amount = to_token_decimals(raw_taker_amt)

            return Side.SELL, maker_amount, taker_amount
        else:
            raise ValueError(f"order_args.side must be '{BUY}' or '{SELL}'")

    def create_order(
        self, order_args: OrderArgs, options: CreateOrderOptions
    ) -> SignedOrderV2:
        """
        Creates and signs an order
        """
        if not self.funder:
            raise ValueError(
                "Deposit Wallet funder address is required for Kuest orders"
            )

        side, maker_amount, taker_amount = self.get_order_amounts(
            order_args.side,
            order_args.size,
            order_args.price,
            ROUNDING_CONFIG[options.tick_size],
        )

        data = OrderDataV2(
            maker=self.funder,
            tokenId=order_args.token_id,
            makerAmount=str(maker_amount),
            takerAmount=str(taker_amount),
            side=side,
            signer=self.funder,
            expiration=str(order_args.expiration),
            timestamp=str(time.time_ns() // 1_000_000),
            metadata=order_args.metadata,
            builder=builder_code_to_bytes32(order_args.builder_code),
            signatureType=self.sig_type,
        )

        contract_config = get_contract_config(
            self.signer.get_chain_id(), options.neg_risk
        )

        order_builder = ExchangeOrderBuilderV2(
            contract_config.exchange,
            self.signer.get_chain_id(),
            self.signer,
        )

        return order_builder.build_signed_order(data)

    def create_market_order(
        self, order_args: MarketOrderArgs, options: CreateOrderOptions
    ) -> SignedOrderV2:
        """
        Creates and signs a market order
        """
        if not self.funder:
            raise ValueError(
                "Deposit Wallet funder address is required for Kuest orders"
            )

        side, maker_amount, taker_amount = self.get_market_order_amounts(
            order_args.side,
            order_args.amount,
            order_args.price,
            ROUNDING_CONFIG[options.tick_size],
        )

        data = OrderDataV2(
            maker=self.funder,
            tokenId=order_args.token_id,
            makerAmount=str(maker_amount),
            takerAmount=str(taker_amount),
            side=side,
            signer=self.funder,
            expiration="0",
            timestamp=str(time.time_ns() // 1_000_000),
            metadata=order_args.metadata,
            builder=builder_code_to_bytes32(order_args.builder_code),
            signatureType=self.sig_type,
        )

        contract_config = get_contract_config(
            self.signer.get_chain_id(), options.neg_risk
        )

        order_builder = ExchangeOrderBuilderV2(
            contract_config.exchange,
            self.signer.get_chain_id(),
            self.signer,
        )

        return order_builder.build_signed_order(data)

    def calculate_buy_market_price(
        self,
        positions: list[OrderSummary],
        amount_to_match: float,
        order_type: OrderType,
    ) -> float:
        if not positions:
            raise Exception("no match")

        sum = 0
        for p in reversed(positions):
            sum += float(p.size) * float(p.price)
            if sum >= amount_to_match:
                return float(p.price)

        if order_type == OrderType.FOK:
            raise Exception("no match")

        return float(positions[0].price)

    def calculate_sell_market_price(
        self,
        positions: list[OrderSummary],
        amount_to_match: float,
        order_type: OrderType,
    ) -> float:
        if not positions:
            raise Exception("no match")

        sum = 0
        for p in reversed(positions):
            sum += float(p.size)
            if sum >= amount_to_match:
                return float(p.price)

        if order_type == OrderType.FOK:
            raise Exception("no match")

        return float(positions[0].price)
