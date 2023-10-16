#!/usr/bin/env python3
"""
 base classes for roxbot.
 Provides interface definitions for bridges, drivers etc.

 Copyright (c) 2023 ROX Automation - Jev Kuznetsov
"""
import asyncio
import json
import logging
from logging.handlers import QueueHandler
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional


from roxbot.topics import Topics

LOG_Q_LENGTH = 50

LOG_FMT = "%(asctime)s [%(name)s] %(levelname)s %(message)s"
DATE_FMT = "%H:%M:%S"


class Bridge(ABC):
    """base class for creating websocket bridges"""

    def __init__(self, name: str = "Bridge") -> None:
        self._log = logging.getLogger(name)
        self._cmd_callbacks: Dict = {}  # receive data callbacks

        # logging queue
        self._log_q: asyncio.Queue = asyncio.Queue(LOG_Q_LENGTH)
        self._log_handler: Optional[QueueHandler] = None

    @abstractmethod
    def send(self, topic: str, data):
        """send data to topic

        Args:
            topic (str): topic to post on
            data (any): json serializable data payload
        """

    def register_callback(self, topic: str, fcn: Callable):
        """add callback to topic."""
        assert (
            topic not in self._cmd_callbacks
        ), f"topic {topic} already has a callback registered"

        self._cmd_callbacks[topic] = fcn

    def remove_callback(self, topic: str):
        """remove topic callback"""
        del self._cmd_callbacks[topic]

    def _execute_command(self, message: str) -> Any:
        """execute command from message, message is a string for a simple command or
        a [cmd, args] string for a command with arguments. Returns the result of the command
        """
        self._log.debug("%s", f"executing {message=}")
        ret = None
        # try to parse message as json
        try:
            cmd, args = json.loads(message)
        except json.JSONDecodeError:  # if not json, assume simple command
            cmd = message
            args = None

        try:
            # check if command is registered
            assert (
                cmd in self._cmd_callbacks
            ), f"command {cmd} is not registered, cannot execute"

            if args is not None:
                self._log.info("%s", f"Running {cmd=} {args=}")
                ret = self._cmd_callbacks[cmd](args)
            else:
                self._log.info("%s", f"Running {cmd=}")
                ret = self._cmd_callbacks[cmd]()

        except AssertionError as e:
            self._log.warning("%s", e)
        except Exception as e:  # pylint: disable=broad-except
            self._log.exception("%s", e)

        return ret

    def add_log_handler(self, logger: logging.Logger, level: int = logging.INFO):
        """add log handler to logger, this wil forward all logs to the client via the bridge"""
        self._log_handler = QueueHandler(self._log_q)  # type: ignore
        self._log_handler.setLevel(level)
        logger.addHandler(self._log_handler)

    async def _handle_logging(self):
        """handle logging messages"""
        formatter = logging.Formatter(fmt=LOG_FMT, datefmt=DATE_FMT)

        while True:
            item = await self._log_q.get()
            msg = formatter.format(item)
            self.send(Topics.log, msg)
            self._log_q.task_done()

    @abstractmethod
    async def serve(self):
        """start serving, implement required tasks here"""
