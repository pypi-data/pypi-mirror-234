import enum

from easy_pysy.core import logging
from easy_pysy.core.event import Event, emit
from easy_pysy.core.signal import sigint_callback
from easy_pysy.utils.common import require


class AppState(enum.Enum):
    STOPPED = 1
    STARTING = 2
    STARTED = 3
    STOPPING = 4


class EzContext:
    state = AppState.STOPPED


context = EzContext()


def start():
    require(context.state == AppState.STOPPED, f"Can't start application, current state: {context.state}]")

    logging.info('Starting')
    context.state = AppState.STARTING
    emit(AppStarting())

    logging.info('Started')
    context.state = AppState.STARTED
    emit(AppStarted())


def stop():
    require(context.state == AppState.STARTED, f"Can't stop application, current state: {context.state}")


    try:
        logging.info(f'Stopping')
        context.state = AppState.STOPPING
        emit(AppStopping())
    except BaseException:
        logging.exception('Error while stopping application ! Some AppStopping subscribers may not have been called')

    logging.info('Stopped')
    context.state = AppState.STOPPED


@sigint_callback
def shutdown(exit_code=0):
    stop()
    exit(exit_code)


class AppStarting(Event):
    pass


class AppStarted(Event):
    pass


class AppStopping(Event):
    pass


