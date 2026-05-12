<h1 align="center">
  <img src="https://github.com/user-attachments/assets/0cc687fb-89c4-43fa-a056-d89c307215ad" alt="Kuest" height="96" /><br/>
  Kuest Python CLOB Client
</h1>

<a href='https://pypi.org/project/kuest-py-clob-client'>
    <img src='https://img.shields.io/pypi/v/kuest-py-clob-client.svg' alt='PyPI'/>
</a>

Python SDK for the Kuest CLOB.

## Installation

```bash
pip install kuest-py-clob-client
```

## Read-Only Usage

```python
from py_clob_client.client import ClobClient

client = ClobClient("https://clob.kuest.com")

print(client.get_ok())
print(client.get_server_time())
```

## Wallet-Only Trading

Kuest trading uses Deposit Wallet orders only. The public order path defaults to `signature_type=3` and rejects signature types `0`, `1`, and `2`.

```python
from py_clob_client.client import ClobClient

HOST = "https://clob.kuest.com"
CHAIN_ID = 80002
PRIVATE_KEY = "<owner-private-key>"
DEPOSIT_WALLET = "<deposit-wallet-address>"

client = ClobClient(
    HOST,
    chain_id=CHAIN_ID,
    key=PRIVATE_KEY,
    signature_type=3,
    funder=DEPOSIT_WALLET,
)
client.set_api_creds(client.create_or_derive_api_creds())
```

## Place a Limit Order

```python
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY

client = ClobClient(
    "https://clob.kuest.com",
    chain_id=80002,
    key="<owner-private-key>",
    signature_type=3,
    funder="<deposit-wallet-address>",
)
client.set_api_creds(client.create_or_derive_api_creds())

order = OrderArgs(token_id="<token-id>", price=0.42, size=5.0, side=BUY)
signed = client.create_order(order)
response = client.post_order(signed, OrderType.GTC)
print(response)
```

## Place a Market Order

```python
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import MarketOrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY

client = ClobClient(
    "https://clob.kuest.com",
    chain_id=80002,
    key="<owner-private-key>",
    signature_type=3,
    funder="<deposit-wallet-address>",
)
client.set_api_creds(client.create_or_derive_api_creds())

order = MarketOrderArgs(token_id="<token-id>", amount=25.0, side=BUY, order_type=OrderType.FOK)
signed = client.create_market_order(order)
response = client.post_order(signed, OrderType.FOK)
print(response)
```

## Manage Orders

```python
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OpenOrderParams

client = ClobClient(
    "https://clob.kuest.com",
    chain_id=80002,
    key="<owner-private-key>",
    signature_type=3,
    funder="<deposit-wallet-address>",
)
client.set_api_creds(client.create_or_derive_api_creds())

open_orders = client.get_orders(OpenOrderParams())
if open_orders:
    client.cancel(open_orders[0]["id"])

client.cancel_all()
```

## Notes

- Use `KUEST_API_KEY`, `KUEST_SECRET`, and `KUEST_PASSPHRASE` credentials for authenticated Level 2 calls.
- `API_KEY`, `API_SECRET`, `API_PASSPHRASE`, and `PRIVATE_KEY` may be used as local input aliases by applications, but SDK wire headers remain `KUEST_*`.
- USDC remains the settlement collateral.
