#  Copyright (c) 2023 Roboto Technologies, Inc.

import abc
from typing import Optional

import tqdm


class ProgressMonitor(abc.ABC):
    @abc.abstractmethod
    def update(self, uploaded_bytes: int):
        raise NotImplementedError("update")

    @abc.abstractmethod
    def close(self):
        raise NotImplementedError("close")

    @abc.abstractmethod
    def is_closed(self) -> bool:
        raise NotImplementedError("is_closed")


class ProgressMonitorFactory(abc.ABC):
    @abc.abstractmethod
    def upload_monitor(self, source: str, size: int) -> ProgressMonitor:
        raise NotImplementedError("upload_monitor")

    def download_monitor(self, source: str, size: int) -> ProgressMonitor:
        raise NotImplementedError("download_monitor")


class NoopProgressMonitor(ProgressMonitor):
    def update(self, uploaded_bytes: int):
        pass

    def close(self):
        pass

    def is_closed(self) -> bool:
        return False


class NoopProgressMonitorFactory(ProgressMonitorFactory):
    def upload_monitor(self, source: str, size: int) -> ProgressMonitor:
        return NoopProgressMonitor()

    def download_monitor(self, source: str, size: int) -> ProgressMonitor:
        return NoopProgressMonitor()


class TqdmProgressMonitor(ProgressMonitor):
    __tqdm: tqdm.tqdm
    __is_closed: bool

    def __init__(self, total: int, desc: str, position: int = 0, leave: bool = True):
        self.__tqdm = tqdm.tqdm(
            total=total,
            desc=desc,
            bar_format="{percentage:.1f}%|{bar:25} | {rate_fmt} | {desc}",
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            position=position,
            leave=leave,
        )
        self.__is_closed = False

    def update(self, uploaded_bytes: int):
        self.__tqdm.update(uploaded_bytes)

    def close(self):
        self.__tqdm.close()
        self.__is_closed = True

    def is_closed(self) -> bool:
        return self.__is_closed


class TqdmProgressMonitorFactory(ProgressMonitorFactory):
    __monitors: list[Optional[ProgressMonitor]]

    def __init__(self, concurrency: int = 1):
        self.__monitors = [None] * concurrency

    def __first_available_slot(self) -> Optional[int]:
        for idx in range(len(self.__monitors)):
            if self.__monitors[idx] is None or self.__monitors[idx].is_closed():  # type: ignore[union-attr]
                return idx

        return None

    def __any_monitor(self, source: str, size: int) -> ProgressMonitor:
        # This for sure is not fully threadsafe, but it 100% works for single threading and
        # _mostly_ works for multithreading.
        slot = self.__first_available_slot()
        if slot is None:
            raise ValueError("Number of concurrent monitors is exceeding concurrency!")

        monitor = TqdmProgressMonitor(
            total=size,
            desc=f"Source: {source}",
            position=slot,
            leave=len(self.__monitors) == 1,
        )

        self.__monitors[slot] = monitor

        return monitor

    def upload_monitor(self, source: str, size: int) -> ProgressMonitor:
        return self.__any_monitor(source=source, size=size)

    def download_monitor(self, source: str, size: int) -> ProgressMonitor:
        return self.__any_monitor(source=source, size=size)
