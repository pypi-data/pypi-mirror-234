import itertools
import asyncio
from collections.abc import Iterable


def chunk(iterator: Iterable, size: int) -> Iterable[tuple]:
    it = iter(iterator)

    return iter(lambda: tuple(itertools.islice(it, size)), ())


async def gather_with_concurrency(n, *coros, return_exceptions=False):
    semaphore = asyncio.Semaphore(n)

    async def sem_coro(coro):
        async with semaphore:
            return await coro

    return await asyncio.gather(
        *(sem_coro(c) for c in coros),
        return_exceptions=return_exceptions,
    )
