from unittest import TestCase

from py_clob_client.clob_types import CreateOrderOptions, OrderArgs, OrderType
from py_clob_client.constants import AMOY
from py_clob_client.order_builder.builder import OrderBuilder
from py_clob_client.order_builder.constants import BUY
from py_clob_client.signer import Signer
from py_clob_client.utilities import order_to_json


class TestV2OrderFields(TestCase):
    def test_builder_metadata_and_timestamp_are_serialized(self):
        signer = Signer(
            private_key="0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80",
            chain_id=AMOY,
        )
        deposit_wallet = "0x1111111111111111111111111111111111111111"
        builder = OrderBuilder(signer, funder=deposit_wallet)
        builder_code = (
            "0x0000000000000000000000001111111111111111111111111111111111111111"
        )
        metadata = "0x0000000000000000000000000000000000000000000000000000000000000042"

        order = builder.create_order(
            order_args=OrderArgs(
                token_id="100",
                price=0.5,
                size=100,
                side=BUY,
                builder_code=builder_code,
                metadata=metadata,
            ),
            options=CreateOrderOptions(tick_size="0.1", neg_risk=False),
        )

        payload = order_to_json(
            order=order, owner="owner-api-key", orderType=OrderType.GTC
        )
        order_payload = payload["order"]

        self.assertEqual(order_payload["builder"], builder_code)
        self.assertEqual(order_payload["metadata"], metadata)
        self.assertEqual(order_payload["maker"], deposit_wallet)
        self.assertEqual(order_payload["signer"], deposit_wallet)
        self.assertEqual(order_payload["signatureType"], 3)
        self.assertTrue(str(order_payload["timestamp"]).isdigit())
