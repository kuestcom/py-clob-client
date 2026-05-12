from .clob_types import ContractConfig


def get_contract_config(chainID: int, neg_risk: bool = False) -> ContractConfig:
    """
    Get the contract configuration for the chain
    """

    CONFIG = {
        # Kuest contracts (Polygon mainnet)
        137: ContractConfig(
            exchange="0x4bB1871fdaE80331ce5fF87547b8ff886D1695a5",
            collateral="0x3c499c542cef5e3811e1192ce70d8cc03d5c3359",
            conditional_tokens="0x4682048725865bf17067bd85fF518527A262A9C7",
        ),
        # Kuest contracts (Polygon Amoy)
        80002: ContractConfig(
            exchange="0x4bB1871fdaE80331ce5fF87547b8ff886D1695a5",
            collateral="0x41E94Eb019C0762f9Bfcf9Fb1E58725BfB0e7582",
            conditional_tokens="0x4682048725865bf17067bd85fF518527A262A9C7",
        ),
    }

    NEG_RISK_CONFIG = {
        # Kuest NegRisk contracts (Polygon mainnet)
        137: ContractConfig(
            exchange="0xdb1E374a05130d7DE3F16677066553F225D2eE53",
            collateral="0x3c499c542cef5e3811e1192ce70d8cc03d5c3359",
            conditional_tokens="0x4682048725865bf17067bd85fF518527A262A9C7",
        ),
        # Kuest NegRisk contracts (Polygon Amoy)
        80002: ContractConfig(
            exchange="0xdb1E374a05130d7DE3F16677066553F225D2eE53",
            collateral="0x41E94Eb019C0762f9Bfcf9Fb1E58725BfB0e7582",
            conditional_tokens="0x4682048725865bf17067bd85fF518527A262A9C7",
        ),
    }

    if neg_risk:
        config = NEG_RISK_CONFIG.get(chainID)
    else:
        config = CONFIG.get(chainID)
    if config is None:
        raise Exception("Invalid chainID: ${}".format(chainID))

    return config
