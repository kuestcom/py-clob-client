SITE_CONFIG = {
    "site_url": "",
    "fee_bps": 0,
    "fee_receiver": "",
    "builder_mode": False,
    "geoblock": False,
}

GEOBLOCK_HOST = "https://geoblock.kuest.com"


def get_site_order_payload() -> dict:
    fee_receiver = SITE_CONFIG["fee_receiver"].strip()
    if not fee_receiver:
        return {}

    return {
        "fee_bps": SITE_CONFIG["fee_bps"],
        "fee_receiver": fee_receiver,
    }
