import os
import random
import time
import typing as t

from ._logging import logger


def construct_random(seed: t.Any) -> random.Random:
    seed = seed if seed is not None else _generate_seed()

    rnd = random.Random(seed)
    logger.debug(f"seed: {seed}")
    return rnd


def _generate_seed() -> int:
    try:
        return int.from_bytes(os.urandom(8), "big")
    except Exception:
        return int(time.time())
