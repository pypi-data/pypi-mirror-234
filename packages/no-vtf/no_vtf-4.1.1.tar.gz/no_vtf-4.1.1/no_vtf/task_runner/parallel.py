# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import functools
import multiprocessing
import signal

from collections.abc import Callable, Iterable, Sequence
from typing import ClassVar, Final, Optional, TypeVar, Union

from no_vtf._typing import mypyc_attr
from no_vtf.task_runner.sequential import SequentialRunner
from no_vtf.task_runner.task_runner import Task, TaskRunner

_A_co = TypeVar("_A_co", covariant=True)


@mypyc_attr(allow_interpreted_subclasses=True)
class ParallelRunner(TaskRunner):
    _multiprocessing_initialized: ClassVar[bool] = False

    @classmethod
    def initialize(cls, *, _recursive: bool = True) -> None:
        super().initialize(_recursive=False)

        if not ParallelRunner._multiprocessing_initialized:
            multiprocessing.freeze_support()
            ParallelRunner._multiprocessing_initialized = True

        if _recursive:
            for subclass in cls.__subclasses__():
                subclass.initialize()

    def __init__(
        self, *, max_workers: Optional[int] = None, initializer: Optional[Callable[[], None]] = None
    ) -> None:
        assert (
            ParallelRunner._multiprocessing_initialized
        ), "ParallelRunner.initialize() must be called early"

        self.max_workers: Final = max_workers
        self.initializer: Final = initializer

    def __call__(
        self, tasks: Sequence[Task[_A_co]]
    ) -> Iterable[tuple[Task[_A_co], Union[_A_co, Exception]]]:
        initializer = functools.partial(ParallelRunner._worker_initializer, self.initializer)
        with multiprocessing.Pool(self.max_workers, initializer=initializer) as pool:
            for task, result in pool.imap_unordered(SequentialRunner.process, tasks):
                yield (task, result)

    @staticmethod
    def _worker_initializer(additional_initializer: Optional[Callable[[], None]]) -> None:
        signal.signal(signal.SIGINT, signal.SIG_IGN)

        if additional_initializer:
            additional_initializer()


@mypyc_attr(allow_interpreted_subclasses=True)
class _DummyParallelRunner(ParallelRunner):  # pyright: ignore [reportUnusedClass]
    pass
