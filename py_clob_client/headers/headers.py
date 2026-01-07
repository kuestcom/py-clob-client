from ..clob_types import ApiCreds, RequestArgs
from ..signing.hmac import build_hmac_signature
from ..signer import Signer
from ..signing.eip712 import sign_clob_auth_message

from datetime import datetime

KUEST_ADDRESS = "KUEST_ADDRESS"
KUEST_SIGNATURE = "KUEST_SIGNATURE"
KUEST_TIMESTAMP = "KUEST_TIMESTAMP"
KUEST_NONCE = "KUEST_NONCE"
KUEST_API_KEY = "KUEST_API_KEY"
KUEST_PASSPHRASE = "KUEST_PASSPHRASE"


def create_level_1_headers(signer: Signer, nonce: int = None, message: str = None):
    """
    Creates Level 1 Kuest headers for a request
    """
    timestamp = int(datetime.now().timestamp())

    n = 0
    if nonce is not None:
        n = nonce

    signature = sign_clob_auth_message(signer, timestamp, n, message=message)
    headers = {
        KUEST_ADDRESS: signer.address(),
        KUEST_SIGNATURE: signature,
        KUEST_TIMESTAMP: str(timestamp),
        KUEST_NONCE: str(n),
    }

    return headers


def create_level_2_headers(signer: Signer, creds: ApiCreds, request_args: RequestArgs):
    """Creates Level 2 Kuest headers for a request using pre-serialized body if provided"""
    timestamp = int(datetime.now().timestamp())

    # Prefer the pre-serialized body string for deterministic signing if available
    body_for_sig = (
        request_args.serialized_body
        if request_args.serialized_body is not None
        else request_args.body
    )

    hmac_sig = build_hmac_signature(
        creds.api_secret,
        timestamp,
        request_args.method,
        request_args.request_path,
        body_for_sig,
    )

    return {
        KUEST_ADDRESS: signer.address(),
        KUEST_SIGNATURE: hmac_sig,
        KUEST_TIMESTAMP: str(timestamp),
        KUEST_API_KEY: creds.api_key,
        KUEST_PASSPHRASE: creds.api_passphrase,
    }


def enrich_l2_headers_with_builder_headers(
    headers: dict, builder_headers: dict
) -> dict:
    return {**headers, **builder_headers}
