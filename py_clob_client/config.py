from .clob_types import ContractConfig


def get_contract_config(chainID: int, neg_risk: bool = False) -> ContractConfig:
    """
    Get the contract configuration for the chain
    """

    CONFIG = {
        # Kuest contracts (Polygon mainnet)
        137: ContractConfig(
            exchange="0xB5592f7CccA122558D2201e190826276f3a661cb",
            collateral="0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
            conditional_tokens="0x4682048725865bf17067bd85fF518527A262A9C7",
        ),
        # Kuest contracts (Polygon Amoy)
        80002: ContractConfig(
            exchange="0xB5592f7CccA122558D2201e190826276f3a661cb",
            collateral="0x41E94Eb019C0762f9Bfcf9Fb1E58725BfB0e7582",
            conditional_tokens="0x4682048725865bf17067bd85fF518527A262A9C7",
        ),
    }

    NEG_RISK_CONFIG = {
        # Kuest NegRisk contracts (Polygon mainnet)
        137: ContractConfig(
            exchange="0xef02d1Ea5B42432C4E99C2785d1a4020d2FB24F5",
            collateral="0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
            conditional_tokens="0x4682048725865bf17067bd85fF518527A262A9C7",
        ),
        # Kuest NegRisk contracts (Polygon Amoy)
        80002: ContractConfig(
            exchange="0xef02d1Ea5B42432C4E99C2785d1a4020d2FB24F5",
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
