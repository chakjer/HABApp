import asyncio
from asyncio import Task, create_task, run_coroutine_threadsafe, sleep
from collections.abc import Awaitable, Callable
from typing import Any

from HABApp.core.const import loop


# TODO: switch to time.monotonic for measurements instead of fixed sleep time

class PendingFuture:
    def __init__(self, future: Callable[[], Awaitable[Any]], secs: int | float) -> None:
        assert asyncio.iscoroutinefunction(future), type(future)
        if not isinstance(secs, (int, float)) or secs < 0:
            raise ValueError(f'Pending time must be int/float and >= 0! Is: {secs} ({type(secs)})')

        self.func: Callable[[], Awaitable[Any]] = future
        self.secs = secs
        self.task: Task | None = None

        self.is_canceled: bool = False

    def cancel(self) -> None:
        self.is_canceled = True

        if self.task is not None:
            # only cancel if it is not run or canceled
            if not (self.task.done() or self.task.cancelled()):
                self.task.cancel()
            self.task = None

    def reset(self, thread_safe=False):
        if self.is_canceled:
            return None

        if self.task is not None:
            # only cancel if it is not run or canceled
            if not (self.task.done() or self.task.cancelled()):
                self.task.cancel()
            self.task = None

        if thread_safe:
            self.task = run_coroutine_threadsafe(self.__countdown(), loop)
        else:
            self.task = create_task(self.__countdown())

    async def __countdown(self) -> None:
        await sleep(self.secs)
        await self.func()
