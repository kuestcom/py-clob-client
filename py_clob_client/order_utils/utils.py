import random
import time


def generate_order_salt() -> str:
    # Keep salt generation aligned with the TS client behavior used by Kuest today.
    # Using very large 256-bit salts can break downstream validation in some stacks.
    now_ms = int(time.time() * 1000)
    return str(round(random.random() * now_ms))
