from .clob_types import ContractConfig


def get_contract_config(chainID: int, neg_risk: bool = False) -> ContractConfig:
    """
    Get the contract configuration for the chain
    """

    CONFIG = {
        # Kuest contracts (Polygon mainnet)
        137: ContractConfig(
            exchange="0xE79717fE8456C620cFde6156b6AeAd79C4875Ca2",
            collateral="0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
            conditional_tokens="0x9432978d0f8A0E1a5317DD545B4a9ad32da8AD59",
        ),
        # Kuest contracts (Polygon Amoy)
        80002: ContractConfig(
            exchange="0xE79717fE8456C620cFde6156b6AeAd79C4875Ca2",
            collateral="0x29604FdE966E3AEe42d9b5451BD9912863b3B904",
            conditional_tokens="0x9432978d0f8A0E1a5317DD545B4a9ad32da8AD59",
        ),
    }

    NEG_RISK_CONFIG = {
        # Kuest NegRisk contracts (Polygon mainnet)
        137: ContractConfig(
            exchange="0xccBe425A0Aa24DCEf81f2e6edE3568a1683e7cbe",
            collateral="0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
            conditional_tokens="0x9432978d0f8A0E1a5317DD545B4a9ad32da8AD59",
        ),
        # Kuest NegRisk contracts (Polygon Amoy)
        80002: ContractConfig(
            exchange="0xccBe425A0Aa24DCEf81f2e6edE3568a1683e7cbe",
            collateral="0x29604FdE966E3AEe42d9b5451BD9912863b3B904",
            conditional_tokens="0x9432978d0f8A0E1a5317DD545B4a9ad32da8AD59",
        ),
    }

    if neg_risk:
        config = NEG_RISK_CONFIG.get(chainID)
    else:
        config = CONFIG.get(chainID)
    if config is None:
        raise Exception("Invalid chainID: ${}".format(chainID))

    return config
