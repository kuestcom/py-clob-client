from typing import Optional

from kuest_eip712_structs import make_domain
from eth_utils import keccak
from py_order_utils.utils import prepend_zx

from .model import ClobAuth
from ..signer import Signer

CLOB_DOMAIN_NAME = "ClobAuthDomain"
CLOB_VERSION = "1"
DEFAULT_AUTH_MESSAGE = "This message attests that I control the given wallet"


def get_clob_auth_domain(chain_id: int):
    return make_domain(name=CLOB_DOMAIN_NAME, version=CLOB_VERSION, chainId=chain_id)


def resolve_auth_message(message: Optional[str] = None) -> str:
    return message or DEFAULT_AUTH_MESSAGE


def sign_clob_auth_message(
    signer: Signer, timestamp: int, nonce: int, message: Optional[str] = None
) -> str:
    clob_auth_msg = ClobAuth(
        address=signer.address(),
        timestamp=str(timestamp),
        nonce=nonce,
        message=resolve_auth_message(message),
    )
    chain_id = signer.get_chain_id()
    auth_struct_hash = prepend_zx(
        keccak(clob_auth_msg.signable_bytes(get_clob_auth_domain(chain_id))).hex()
    )
    return prepend_zx(signer.sign(auth_struct_hash))
