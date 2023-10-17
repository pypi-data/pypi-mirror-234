#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Rich Logging """

# standard python imports
import logging
import os
import tempfile
from typing import Optional
from logging.handlers import TimedRotatingFileHandler

import click
from rich.logging import RichHandler
from rich.traceback import install

from regscale import exceptions

install(suppress=[click, exceptions])


def create_logger(propagate: Optional[bool] = None, custom_handler: any = None):
    """
    Create a logger for use in all cases
    :return: logger object
    """
    loglevel = os.environ.get("LOGLEVEL", "INFO").upper()
    rich_handler = RichHandler(rich_tracebacks=False, markup=True)
    file_handler = TimedRotatingFileHandler(
        filename=f"{tempfile.gettempdir()}{os.sep}RegScale.log",
        when="D",
        interval=3,
        backupCount=10,
    )

    logging.getLogger("botocore").setLevel(logging.CRITICAL)
    logging.basicConfig(
        level=loglevel,
        format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
        datefmt="[%Y/%m/%d %H:%M;%S]",
        handlers=[rich_handler, file_handler, custom_handler]
        if custom_handler
        else [rich_handler, file_handler],
    )
    logger = logging.getLogger("rich")
    if propagate is not None:
        logger.propagate = propagate
    return logger
