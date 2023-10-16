#!/usr/bin/env python3
"""
roxbot CLI
"""
# pylint: disable=broad-except
# type: ignore
import asyncio
import logging

import click
import coloredlogs

import roxbot.bridges.ws_bridge as ws_bridge
from roxbot import LOG_FORMAT
from roxbot.version import get_version

log = logging.getLogger(__name__)
coloredlogs.install(level="INFO", fmt=LOG_FORMAT)


@click.group()
def cli():
    pass  # pragma: no cover


@click.group()
def bridge():
    pass


@cli.command()
def info():
    """Print package info"""
    print(get_version())


@bridge.command()
@click.option("--port", default=ws_bridge.DEFAULT_PORT, help="port to listen on")
def echo(port: int):
    """echo all messages"""
    try:
        asyncio.run(ws_bridge.echo(port=port))
    except KeyboardInterrupt:
        print("exiting")
    except Exception as e:
        print(e)


cli.add_command(bridge)

if __name__ == "__main__":
    cli()  # pragma: no cover
