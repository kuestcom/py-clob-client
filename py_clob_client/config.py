from .clob_types import ContractConfig


def get_contract_config(chainID: int, neg_risk: bool = False) -> ContractConfig:
    """
    Get the contract configuration for the chain
    """

    CONFIG = {
        137: ContractConfig(
            exchange="0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E",
            collateral="0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
            conditional_tokens="0x4D97DCd97eC945f40cF65F87097ACe5EA0476045",
        ),
        80002: ContractConfig(
            exchange="0xE79717fE8456C620cFde6156b6AeAd79C4875Ca2",
            collateral="0x29604FdE966E3AEe42d9b5451BD9912863b3B904",
            conditional_tokens="0x9432978d0f8A0E1a5317DD545B4a9ad32da8AD59",
        ),
    }

    NEG_RISK_CONFIG = {
        137: ContractConfig(
            exchange="0xC5d563A36AE78145C45a50134d48A1215220f80a",
            collateral="0x2791bca1f2de4661ed88a30c99a7a9449aa84174",
            conditional_tokens="0x4D97DCd97eC945f40cF65F87097ACe5EA0476045",
        ),
        80002: ContractConfig(
            exchange="0xe2ed8eE54fa279b1006333EbeE68192EDB141207",
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
