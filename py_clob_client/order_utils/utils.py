import secrets


def generate_order_salt() -> str:
    return str(secrets.randbits(256))
