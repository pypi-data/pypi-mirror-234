import typer
from easy_pysy.core.lifecycle import start, stop, context, AppState
from easy_pysy.core import logging

main_typer = typer.Typer()
# main_typer.add_typer(run_typer, name="run")

command = main_typer.command


def run(auto_start=True):
    if auto_start and context.state == AppState.STOPPED:
        start()

    try:
        main_typer()
    except:
        logging.exception('Exception while running CLI')
        stop()
