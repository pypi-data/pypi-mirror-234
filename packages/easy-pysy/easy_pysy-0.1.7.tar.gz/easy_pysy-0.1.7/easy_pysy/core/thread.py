import time
from threading import Thread, Event, Timer
from typing import Callable, Optional

from easy_pysy.utils.common import require
from easy_pysy.core.environment import env
from easy_pysy.core.logging import logger
from easy_pysy.core.lifecycle import AppStopping
from easy_pysy.core.event import on

stop_timeout = env('ez.thread.stop_timeout', config_type=int, default=1)


class EzThread(Thread):  # TODO: test
    def __init__(self, target, args=(), kwargs=None, name=None, daemon=False):
        if kwargs is None:
            kwargs = {}
        self.stop_event = Event()
        super().__init__(None, target, name, args, kwargs, daemon=daemon)
        self.target = target

    def start(self):
        require(not self.is_alive(), 'Interval already started')
        self.stop_event.clear()
        threads.append(self)
        super().start()

    def stop(self, timeout=10):
        require(self.is_alive(), 'Thread already stopped')
        self.stop_event.set()
        self.join(timeout)

    def join(self, timeout=None):
        super().join(timeout)
        if self.is_alive():
            assert timeout is not None
            # timeout can't be None here because if it was, then join()
            # wouldn't return until the thread was dead
            raise ZombieThread(f"Thread failed to die within {timeout} seconds")
        else:
            threads.remove(self)


class Interval(Timer):
    def __init__(self, interval_ms, function, on_error, args=(), kwargs=None):
        super().__init__(
            interval_ms / 1000.0,
            function,
            args=args,
            kwargs=kwargs or {},
        )
        self.on_error = on_error

    def run(self):
        next_time = time.time() + self.interval
        wait_time = next_time - time.time()
        while not self.finished.wait(wait_time):
            try:
                next_time += self.interval
                self.function(*self.args, **self.kwargs)
                wait_time = next_time - time.time()
            except BaseException as exc:
                self.on_error(exc)
                wait_time = next_time - time.time()


class ZombieThread(Exception):
    pass


threads: list[EzThread] = []


def get_thread(target: Callable) -> Optional[EzThread]:
    for t in threads:
        if t.target == target:
            return t
    return None


@on(AppStopping)
def on_stop(event: AppStopping):
    logger.debug('Stopping threads')
    while threads:
        running_threads = [thread for thread in threads if thread.is_alive()]
        # Optimization: instead of calling stop() which implicitly calls
        # join(), set all the stopping events simultaneously, *then* join
        # threads with a reasonable timeout
        for thread in running_threads:
            thread.stop_event.set()
        for thread in running_threads:
            logger.debug(f'Stopping thread: {thread}')
            thread.join(stop_timeout)
    logger.debug('Threads stopped')
