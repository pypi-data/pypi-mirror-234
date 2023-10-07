import os
import time
from pathlib import Path
from typing import Tuple, Optional
import click
import eventlet


def run_forever():
    while True:
        time.sleep(8888)


@click.group()
def pon_cli():
    pass


@pon_cli.command()
@click.argument('services', nargs=-1, required=True)
@click.option('--config', help='config file path')
def run(services: Tuple[str], config: Optional[str] = None):
    """ run pon services """
    config_filepath: Path = Path(os.getcwd())/config
    from pon.events import EventletEventRunner
    from pon.web import EventletAPIRunner

    ROOT_DIR = Path(os.path.abspath(os.curdir))
    PROJECT_NAME = ROOT_DIR.name

    os.environ['ROOT_DIR'] = str(ROOT_DIR)
    os.environ['PROJECT_NAME'] = PROJECT_NAME

    gt = eventlet.spawn(EventletEventRunner().run, services, config_filepath)
    gt.wait()


@pon_cli.command()
@click.option('--config', help='config file path')
def shell(file_path: str = None):
    """ shell interactive environment """
    pass


cli = click.CommandCollection(sources=[pon_cli])

if __name__ == '__main__':
    cli()
