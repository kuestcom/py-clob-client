from unittest import TestCase

from py_clob_client.clob_types import (
    CreateOrderOptions,
    MarketOrderArgs,
    OrderArgs,
    RoundConfig,
)
from py_clob_client.constants import AMOY
from py_clob_client.order_builder.builder import OrderBuilder
from py_clob_client.order_builder.constants import BUY, SELL
from py_clob_client.signer import Signer


PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
DEPOSIT_WALLET = "0x1111111111111111111111111111111111111111"


class TestOrderBuilder(TestCase):
    def setUp(self):
        self.signer = Signer(private_key=PRIVATE_KEY, chain_id=AMOY)

    def test_rejects_legacy_signature_type(self):
        with self.assertRaisesRegex(
            ValueError, "supports only Deposit Wallet signature type 3"
        ):
            OrderBuilder(self.signer, sig_type=1, funder=DEPOSIT_WALLET)

    def test_requires_deposit_wallet_funder(self):
        builder = OrderBuilder(self.signer)

        with self.assertRaisesRegex(ValueError, "funder address is required"):
            builder.create_order(
                order_args=OrderArgs(
                    token_id="100",
                    price=0.5,
                    size=10,
                    side=BUY,
                ),
                options=CreateOrderOptions(tick_size="0.1", neg_risk=False),
            )

    def test_create_limit_order_uses_deposit_wallet_type_3(self):
        builder = OrderBuilder(self.signer, funder=DEPOSIT_WALLET)

        order = builder.create_order(
            order_args=OrderArgs(
                token_id="100",
                price=0.5,
                size=10,
                side=BUY,
            ),
            options=CreateOrderOptions(tick_size="0.1", neg_risk=False),
        )

        self.assertEqual(order.maker, DEPOSIT_WALLET)
        self.assertEqual(order.signer, DEPOSIT_WALLET)
        self.assertEqual(int(order.signatureType), 3)
        self.assertNotIn("feeRateBps", order.__dict__)
        self.assertNotIn("nonce", order.__dict__)

    def test_create_market_order_uses_deposit_wallet_type_3(self):
        builder = OrderBuilder(self.signer, funder=DEPOSIT_WALLET)

        order = builder.create_market_order(
            order_args=MarketOrderArgs(
                token_id="100",
                amount=10,
                price=0.5,
                side=SELL,
            ),
            options=CreateOrderOptions(tick_size="0.1", neg_risk=False),
        )

        self.assertEqual(order.maker, DEPOSIT_WALLET)
        self.assertEqual(order.signer, DEPOSIT_WALLET)
        self.assertEqual(int(order.signatureType), 3)

    def test_amount_calculation_is_preserved(self):
        builder = OrderBuilder(self.signer, funder=DEPOSIT_WALLET)
        side, maker_amount, taker_amount = builder.get_order_amounts(
            BUY,
            size=10,
            price=0.5,
            round_config=RoundConfig(price=1, size=2, amount=3),
        )

        self.assertEqual(int(side), 0)
        self.assertEqual(maker_amount, 5_000_000)
        self.assertEqual(taker_amount, 10_000_000)
