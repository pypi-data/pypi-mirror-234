#!/usr/bin/env python3
#                      _     _
# _ __ ___   __ _  ___| |__ (_)_ __   ___ _ __ _   _
# | '_ ` _ \ / _` |/ __| '_ \| | '_ \ / _ \ '__| | | |
# | | | | | | (_| | (__| | | | | | | |  __/ |  | |_| |
# |_| |_| |_|\__,_|\___|_| |_|_|_| |_|\___|_|   \__, |
#                                              |___/
#
# machinery - framework for descriptive functional applications
# Copyright (C) 2023 - Frans Fürst
#
# machinery is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# machinery is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details at <http://www.gnu.org/licenses/>.
#
# Anyway this project is not free for machine learning. If you're using any content of this
# repository to train any sort of machine learned model (e.g. LLMs), you agree to make the whole
# model trained with this repository and all data needed to train (i.e. reproduce) the model
# publicly and freely available (i.e. free of charge and with no obligation to register to any
# service) and make sure to inform the author (me, frans.fuerst@protonmail.com) via email how to
# get and use that model and any sources needed to train it.

""" Function plumbing stuff

https://sethmlarson.dev/security-developer-in-residence-weekly-report-9?date=2023-09-05

"""
# pylint: disable=protected-access,too-few-public-methods

import asyncio
import logging
from collections.abc import (
    AsyncIterable,
    AsyncIterator,
    Callable,
    Iterable,
    MutableMapping,
    MutableSequence,
    Sequence,
)
from contextlib import suppress
from pathlib import Path
from typing import TypeVar, Union

from asyncinotify import Inotify, Mask


def log() -> logging.Logger:
    """Logger for this module"""
    return logging.getLogger("machinery")


T = TypeVar("T")

PipeT = TypeVar("PipeT")
PipeChainT = TypeVar("PipeChainT")


class Pipeline(AsyncIterable[PipeT]):
    """Data emitter used for plumbing"""

    def __init__(
        self,
        source: Union["Pipeline[PipeT]", AsyncIterable[PipeT]],
        name: None | str = None,
        terminal: bool = False,
    ):
        self._subscribers: MutableSequence[asyncio.Queue[PipeT]] = []
        self.name = name
        self.terminal = terminal

        self.source = self._aemit(
            self._alisten(source.subscribe()) if isinstance(source, Pipeline) else source
        )

    def __aiter__(self) -> AsyncIterator[PipeT]:
        """Returns the previously created iterator"""
        return self.source.__aiter__()

    @staticmethod
    async def _alisten(queue: asyncio.Queue[PipeT]) -> AsyncIterable[PipeT]:
        while True:
            yield await queue.get()

    async def _aemit(
        self,
        source: AsyncIterable[PipeT],
    ) -> AsyncIterable[PipeT]:
        """Yields and publishes values read from data source"""
        try:
            async for value in source:
                yield value
                for subscriber in self._subscribers:
                    await subscriber.put(value)
        except StopAsyncIteration:
            pass
        except Exception as exc:  # pylint: disable=broad-except
            log().error("Exception in async Pipeline head: %s", exc)

    def chain(self, function: Callable[[PipeT], Iterable[PipeChainT]]) -> "Pipeline[PipeChainT]":
        """Function chainer"""

        async def helper() -> AsyncIterable[PipeChainT]:
            async for value in self:
                try:
                    for final in function(value):
                        yield final
                except Exception as exc:  # pylint: disable=broad-except
                    log().error("Exception in chain function %s(): '%s'", function.__name__, exc)

        return Pipeline(helper())

    def subscribe(self) -> asyncio.Queue[PipeT]:
        """Creates, registeres and returns a new queue for message publishing"""
        queue: asyncio.Queue[PipeT] = asyncio.Queue()
        self._subscribers.append(queue)
        return queue


async def merge(*iterables: AsyncIterator[T]) -> AsyncIterator[T]:
    """Iterates over provided async generators combined"""

    def task_from(iterator: AsyncIterator[T]) -> asyncio.Task[T]:
        fut = asyncio.ensure_future(anext(iterator))
        fut._orig_iter = iterator  # type: ignore[attr-defined]
        return fut

    iter_next: MutableMapping[AsyncIterator[T], asyncio.Task[T]] = {
        (iterator := aiter(it)): task_from(iterator) for it in iterables
    }

    try:
        while iter_next:
            done, _ = await asyncio.wait(iter_next.values(), return_when=asyncio.FIRST_COMPLETED)

            for future in done:
                with suppress(StopAsyncIteration):
                    ret = future.result()
                    iter_next[future._orig_iter] = task_from(  # type: ignore[attr-defined]
                        future._orig_iter  # type: ignore[attr-defined]
                    )
                    yield ret
                    continue
                del iter_next[future._orig_iter]  # type: ignore[attr-defined]
    except asyncio.CancelledError:
        ...
    finally:
        for task in iter_next.values():
            task.cancel()
            with suppress(StopAsyncIteration):
                await task


class Bundler(AsyncIterable[tuple[str, T]]):
    """Generic class for type wrapping `bundle`"""

    def __init__(self, **generators: AsyncIterable[T]) -> None:
        self.source = bundle(**generators)

    def __aiter__(self) -> AsyncIterator[tuple[str, T]]:
        """Returns the previously created iterator"""
        return self.source.__aiter__()


async def bundle(**generators: AsyncIterable[T]) -> AsyncIterable[tuple[str, T]]:
    """Iterates over provided async generators combined"""

    async def decorate_with(
        prefix: str, iterator: AsyncIterable[T]
    ) -> AsyncIterator[tuple[str, T]]:
        async for item in iterator:
            yield prefix, item

    async for named_result in merge(*(decorate_with(*i) for i in dict(generators).items())):
        yield named_result


async def collect_chunks(
    generator: AsyncIterator[T],
    *,
    postpone: bool = False,
    min_interval: float = 2,
    bucket_size: int = 0,
) -> AsyncIterator[Sequence[T]]:
    """Collect elements read from @generator and wait for a given condition before yielding them
    in chunks.
    Condition is meat only after @min_interval seconds have passed since
    [1] first element received since last bucket if @postpone is set to False or
    [2] since last received element if @postpone is set to True.
    If @bucket_size > 0 the chunk will be returned immediately regardless of @postpone if the
    number of collected elements has reached @bucket_size.
    """
    async def iterate(generator: AsyncIterator[T], queue: asyncio.Queue[T|Exception]) -> None:
        """Writes elements read from @generator to @queue in order to not access @generator
        from more than one context
        see https://stackoverflow.com/questions/77245398"""
        while True:
            try:
                queue.put_nowait(await anext(generator))
            except Exception as exc:  # pylint: disable=broad-except
                queue.put_nowait(exc)
                break

    async def add_next(queue: asyncio.Queue[T|Exception], collector: MutableSequence[T]) -> None:
        """Reads one element from @queue and puts it into @collector. Together with `iterate`
        this gives us an awaitable read-only-one-element-with-timeout semantic"""
        elem = await queue.get()
        print(elem)
        if isinstance(elem, Exception):
            raise elem
        collector.append(elem)

    event_tunnel: asyncio.Queue[T|Exception] = asyncio.Queue()
    asyncio.ensure_future(iterate(generator, event_tunnel))
    collected_events: MutableSequence[T] = []
    fuse_task = None
    tasks = {asyncio.create_task(add_next(event_tunnel, collected_events), name="add_next")}

    with suppress(asyncio.CancelledError):
        while True:
            finished, tasks = await asyncio.wait(fs=tasks, return_when=asyncio.FIRST_COMPLETED)
            assert len(finished) == 1
            finished_task = tuple(finished)[0]
            if isinstance(finished_task.exception(), StopAsyncIteration):
                break


            if (event_name := finished_task.get_name()) == "add_next":
                tasks.add(
                    asyncio.create_task(add_next(event_tunnel, collected_events), name="add_next")
                )
                '''
                # in case we're postponing we 'reset' the timeout fuse by removing it
                if postpone and fuse_task:
                    tasks.remove(fuse_task)
                    fuse_task.cancel()
                    await fuse_task
                    del fuse_task
                    fuse_task = None

                # we've had a new event - start the timeout fuse
                if not fuse_task:
                    tasks.add(
                        fuse_task := asyncio.create_task(
                            asyncio.sleep(min_interval), name="fuse"
                        )
                    )
                    '''

            if event_name in {"fuse", "abort"} or (
                bucket_size and len(collected_events) >= bucket_size
            ):
                if fuse_task:
                    if event_name != "fuse":
                        tasks.remove(fuse_task)
                        fuse_task.cancel()
                        with suppress(asyncio.CancelledError):
                            await fuse_task
                    del fuse_task
                    fuse_task = None
                if collected_events:
                    yield collected_events
                    collected_events.clear()
                if event.get_name() == "abort":
                    for task in tasks:
                        task.cancel()
                    return
                continue


async def fs_changes(
    *paths: Path,
    mask: Mask = Mask.CLOSE_WRITE
    | Mask.MOVED_TO
    | Mask.CREATE
    | Mask.MODIFY
    | Mask.MOVE
    | Mask.DELETE
    | Mask.MOVE_SELF,
) -> AsyncIterator[Path]:
    """Controllable, timed filesystem watcher"""

    def expand_paths(path: Path, recursive: bool = True) -> Iterable[Path]:
        yield path
        if path.is_dir() and recursive:
            for file_or_directory in path.rglob("*"):
                if file_or_directory.is_dir() and all(
                    p not in file_or_directory.absolute().as_posix()
                    for p in (
                        "/.venv",
                        "/.git",
                        "/.mypy_cache",
                        "/dist",
                        "/__pycache__",
                    )
                ):
                    yield file_or_directory

    with Inotify() as inotify:
        for path in set(sub_path.absolute() for p in paths for sub_path in expand_paths(Path(p))):
            log().debug("add fs watch for %s", path)
            inotify.add_watch(path, mask)

        async for event_value in inotify:
            if event_value.path:
                yield event_value.path
