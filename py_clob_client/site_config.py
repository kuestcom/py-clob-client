ZERO_BYTES32 = "0x0000000000000000000000000000000000000000000000000000000000000000"

SITE_CONFIG = {
    "site_url": "",
    "builder_mode": False,
    "geoblock": False,
    "builder_code": "",
    "order_metadata": ZERO_BYTES32,
}

GEOBLOCK_HOST = "https://geoblock.kuest.com"


def get_site_order_context() -> dict:
    context = {}
    builder_code = SITE_CONFIG["builder_code"].strip()
    if builder_code:
        context["builder_code"] = builder_code
    metadata = SITE_CONFIG["order_metadata"].strip()
    if metadata and metadata != ZERO_BYTES32:
        context["metadata"] = metadata
    return context
