from contextlib import asynccontextmanager
from typing import Any, Callable, Coroutine

import anyio


def ensure_afunc(coro: Coroutine | Callable) -> Callable:
    """Wrap coroutine to be async function"""
    if callable(coro):
        return coro

    async def do_await():
        return await coro

    return do_await


def run_async(coro: Coroutine | Callable) -> Any:
    """Compare with anyio.run and asyncio.run

    Usage::
        >>> async def afunc(n=1):
        ...     return n
        ...
        >>> run_async(afunc)  # get the same result as: await afunc()
        1
        >>> run_async(afunc(2))  # get the same result as: await afunc(2)
        2
    """
    return anyio.run(ensure_afunc(coro))


async def gather(*coros) -> list:
    """Similar like asyncio.gather, but return a list"""
    results = [None] * len(coros)

    async def runner(coro, i):
        results[i] = await coro

    async with anyio.create_task_group() as tg:
        for i, coro in enumerate(coros):
            tg.start_soon(runner, coro, i)

    return results


@asynccontextmanager
async def start_tasks(coro: Coroutine | Callable, *more: Coroutine | Callable):
    """Make it easy to convert asyncio.create_task

    Usage:

    .. code-block:: python3

        async def startup():
            # cost a long time to do sth async
            await anyio.sleep(1000)

        @contextlib.asynccontextmanager
        async def lifespan(app):
            async with start_tasks(startup()):
                yield
    """
    async with anyio.create_task_group() as tg:
        with anyio.CancelScope(shield=True):
            tg.start_soon(ensure_afunc(coro))
            for c in more:
                tg.start_soon(ensure_afunc(c))
            try:
                yield
            finally:
                tg.cancel_scope.cancel()


async def wait_for(coro: Coroutine, timeout: int | float) -> Any:
    """Similar like asyncio.wait_for"""
    with anyio.fail_after(timeout):
        return await coro
