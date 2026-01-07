# Kuest Python CLOB Client

<a href='https://pypi.org/project/py-clob-client'>
    <img src='https://img.shields.io/pypi/v/py-clob-client.svg' alt='PyPI'/>
</a>

Python client for the Kuest Central Limit Order Book (CLOB).

## Documentation

## Installation

```bash
# install from PyPI (Python 3.9>)
pip install py-clob-client
```
## Usage

The examples below are short and copy‑pasteable.

- What you need:
  - **Python 3.9+**
  - **Private key** that owns funds on Kuest
  - Optional: a **proxy/funder address** if you use an email or smart‑contract wallet
  - Tip: store secrets in environment variables (e.g., with `.env`)

### Quickstart (read‑only)

```python
from py_clob_client.client import ClobClient

client = ClobClient("https://clob.kuest.com")  # Level 0 (no auth)

ok = client.get_ok()
time = client.get_server_time()
print(ok, time)
```

### WebSocket

Use the WebSocket gateway for live market or user updates:

`wss://ws-subscriptions-clob.kuest.com/ws/{market|user}`

### Start trading (EOA)

**Note**: If using MetaMask or hardware wallet, you must first set token allowances. See [Token Allowances section](#important-token-allowances-for-metamaskeoa-users) below.

```python
from py_clob_client.client import ClobClient

HOST = "https://clob.kuest.com"
CHAIN_ID = 80002
PRIVATE_KEY = "<your-private-key>"
FUNDER = "<your-funder-address>"

client = ClobClient(
    HOST,  # The CLOB API endpoint
    key=PRIVATE_KEY,  # Your wallet's private key
    chain_id=CHAIN_ID,  # Polygon Amoy chain ID (80002)
    signature_type=0,  # 0 for EOA signatures
    funder=FUNDER  # Address that holds your funds
)
client.set_api_creds(client.create_or_derive_api_creds())
```

### Start trading (proxy wallet)

For factory proxy wallets or Gnosis Safe wallets, you need to specify two additional parameters:

#### Funder Address
The **funder address** is the actual address that holds your funds on Kuest. When using proxy wallets (factory proxies or Gnosis Safe wallets), the signing key differs from the address holding the funds. The funder address ensures orders are properly attributed to your funded account.

#### Signature Types
The **signature_type** parameter tells the system how to verify your signatures:
- `signature_type=0` (default): EOA signatures (MetaMask, hardware wallets, direct private keys)
- `signature_type=1`: Factory proxy wallet signatures (EOA signs, maker is the proxy)
- `signature_type=2`: Gnosis Safe wallet signatures (EOA signs, maker is the Safe)
- `signature_type=3`: EIP-1271 contract wallet signatures (signer is a contract)

```python
from py_clob_client.client import ClobClient

HOST = "https://clob.kuest.com"
CHAIN_ID = 80002
PRIVATE_KEY = "<your-private-key>"
PROXY_FUNDER = "<your-proxy-or-smart-wallet-address>"  # Address that holds your funds

client = ClobClient(
    HOST,  # The CLOB API endpoint
    key=PRIVATE_KEY,  # Your wallet's private key
    chain_id=CHAIN_ID,  # Polygon Amoy chain ID (80002)
    signature_type=1,  # 1 for factory proxy wallet signatures
    funder=PROXY_FUNDER  # Address that holds your funds
)
client.set_api_creds(client.create_or_derive_api_creds())
```

### Find markets, prices, and orderbooks

```python
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import BookParams

client = ClobClient("https://clob.kuest.com")  # read-only

token_id = "<token-id>"  # Get a token ID: https://docs.kuest.com/developers/gamma-markets-api/get-markets

mid = client.get_midpoint(token_id)
price = client.get_price(token_id, side="BUY")
book = client.get_order_book(token_id)
books = client.get_order_books([BookParams(token_id=token_id)])
print(mid, price, book.market, len(books))
```

### Place a market order (buy by $ amount)

**Note**: EOA/MetaMask users must set token allowances before trading. See [Token Allowances section](#important-token-allowances-for-metamaskeoa-users) below.

```python
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import MarketOrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY

HOST = "https://clob.kuest.com"
CHAIN_ID = 80002
PRIVATE_KEY = "<your-private-key>"
FUNDER = "<your-funder-address>"

client = ClobClient(
    HOST,  # The CLOB API endpoint
    key=PRIVATE_KEY,  # Your wallet's private key
    chain_id=CHAIN_ID,  # Polygon Amoy chain ID (80002)
    signature_type=0,  # 0 for EOA signatures
    funder=FUNDER  # Address that holds your funds
)
client.set_api_creds(client.create_or_derive_api_creds())

mo = MarketOrderArgs(token_id="<token-id>", amount=25.0, side=BUY, order_type=OrderType.FOK)  # Get a token ID: https://docs.kuest.com/developers/gamma-markets-api/get-markets
signed = client.create_market_order(mo)
resp = client.post_order(signed, OrderType.FOK)
print(resp)
```

### Place a limit order (shares at a price)

**Note**: EOA/MetaMask users must set token allowances before trading. See [Token Allowances section](#important-token-allowances-for-metamaskeoa-users) below.

```python
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY

HOST = "https://clob.kuest.com"
CHAIN_ID = 80002
PRIVATE_KEY = "<your-private-key>"
FUNDER = "<your-funder-address>"

client = ClobClient(
    HOST,  # The CLOB API endpoint
    key=PRIVATE_KEY,  # Your wallet's private key
    chain_id=CHAIN_ID,  # Polygon Amoy chain ID (80002)
    signature_type=0,  # 0 for EOA signatures
    funder=FUNDER  # Address that holds your funds
)
client.set_api_creds(client.create_or_derive_api_creds())

order = OrderArgs(token_id="<token-id>", price=0.01, size=5.0, side=BUY)  # Get a token ID: https://docs.kuest.com/developers/gamma-markets-api/get-markets
signed = client.create_order(order)
resp = client.post_order(signed, OrderType.GTC)
print(resp)
```

### Manage orders

**Note**: EOA/MetaMask users must set token allowances before trading. See [Token Allowances section](#important-token-allowances-for-metamaskeoa-users) below.

```python
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OpenOrderParams

HOST = "https://clob.kuest.com"
CHAIN_ID = 80002
PRIVATE_KEY = "<your-private-key>"
FUNDER = "<your-funder-address>"

client = ClobClient(
    HOST,  # The CLOB API endpoint
    key=PRIVATE_KEY,  # Your wallet's private key
    chain_id=CHAIN_ID,  # Polygon Amoy chain ID (80002)
    signature_type=0,  # 0 for EOA signatures
    funder=FUNDER  # Address that holds your funds
)
client.set_api_creds(client.create_or_derive_api_creds())

open_orders = client.get_orders(OpenOrderParams())

order_id = open_orders[0]["id"] if open_orders else None
if order_id:
    client.cancel(order_id)

client.cancel_all()
```

### Markets (read‑only)

```python
from py_clob_client.client import ClobClient

client = ClobClient("https://clob.kuest.com")
markets = client.get_simplified_markets()
print(markets["data"][:1])
```

### User trades (requires auth)

**Note**: EOA/MetaMask users must set token allowances before trading. See [Token Allowances section](#important-token-allowances-for-metamaskeoa-users) below.

```python
from py_clob_client.client import ClobClient

HOST = "https://clob.kuest.com"
CHAIN_ID = 80002
PRIVATE_KEY = "<your-private-key>"
FUNDER = "<your-funder-address>"

client = ClobClient(
    HOST,  # The CLOB API endpoint
    key=PRIVATE_KEY,  # Your wallet's private key
    chain_id=CHAIN_ID,  # Polygon Amoy chain ID (80002)
    signature_type=0,  # 0 for EOA signatures
    funder=FUNDER  # Address that holds your funds
)
client.set_api_creds(client.create_or_derive_api_creds())

last = client.get_last_trade_price("<token-id>")
trades = client.get_trades()
print(last, len(trades))
```

## Important: Token Allowances for MetaMask/EOA Users

### Do I need to set allowances?
- **Using a factory proxy wallet?** No action needed - allowances are set automatically.
- **Using MetaMask or hardware wallet?** You need to set allowances before trading.

### What are allowances?
Think of allowances as permissions. Before Kuest can move your funds to execute trades, you need to give the exchange contracts permission to access your USDC and conditional tokens.

### Quick Setup
You need to approve two types of tokens:
1. **USDC** (for deposits and trading)
2. **Conditional Tokens** (the outcome tokens you trade)

Each needs approval for the exchange contracts to work properly.

### Setting Allowances
Here's a simple breakdown of what needs to be approved:

**For USDC (your trading currency):**
- Token: `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`
- Approve for these contracts:
  - `0xE79717fE8456C620cFde6156b6AeAd79C4875Ca2` (Main exchange)
  - `0xe2ed8eE54fa279b1006333EbeE68192EDB141207` (Neg risk exchange)
  - `0xA8D45917999a9c3833C797EFfB31e3D878e27A33` (Neg risk adapter)

**For Conditional Tokens (your outcome tokens):**
- Token: `0x9432978d0f8A0E1a5317DD545B4a9ad32da8AD59`
- Approve for the same three contracts above

### Example Code
See [this Python example](https://gist.github.com/poly-rodr/44313920481de58d5a3f6d1f8226bd5e) for setting allowances programmatically.

**Pro tip**: You only need to set these once per wallet. After that, you can trade freely.

## Notes
- To discover token IDs, use the Markets API Explorer: [Get Markets](https://docs.kuest.com/developers/gamma-markets-api/get-markets).
- Prices are in dollars from 0.00 to 1.00. Shares are whole or fractional units of the outcome token.

See [/example](/examples) for more.
