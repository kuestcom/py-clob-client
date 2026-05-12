from enum import IntEnum


class SignatureTypeV2(IntEnum):
    """
    Supported signature type for Kuest V2 orders.
    """

    DEPOSIT_WALLET = 3
    """EIP-1271 signatures for Deposit Wallet orders."""
