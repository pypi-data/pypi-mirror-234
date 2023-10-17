#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" RegScale Healthcheck Status"""

# standard python imports
import sys

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger

logger = create_logger()


def status() -> None:
    """
    Get Status of Client Application via RegScale API
    :raises: FileNotFoundError if init.yaml was unable to be loaded
    :raises: ValueError if domain in init.yaml is missing or null
    :raises: General Error if unable to retrieve health check from RegScale API
    :return: None
    """
    app = Application()
    api = Api(app)
    config = {}
    try:
        # load the config from YAML
        config = app.load_config()
    except FileNotFoundError:
        logger.error("No init.yaml file or permission error when opening file.")
        sys.exit(1)
    # make sure config is set before processing
    if "domain" not in config:
        raise ValueError("No domain set in the initialization file.")
    if config["domain"] == "":
        raise ValueError("The domain is blank in the initialization file.")
    if ("token" not in config) or (config["token"] == ""):
        raise ValueError("The token has not been set in the initialization file.")
    # set health check URL
    url_login = config["domain"] + "/health"

    # get the health check data
    response = api.get(url=url_login)
    health_data = {}
    try:
        health_data = response.json()
    except Exception as ex:
        logger.error("Unable to retrieve health check data from RegScale.\n%s", ex)
        sys.exit(1)
    # output the result
    if "status" in health_data:
        if health_data["status"] == "Healthy":
            logger.info("System Status: Healthy")
        elif health_data["status"] == "Degraded":
            logger.warning("System Status: Degraded")
        elif health_data["status"] == "Unhealthy":
            logger.error("System Status: Unhealthy")
        else:
            logger.info("System Status: Unknown")
    else:
        logger.error("No data returned from system health check.")
        sys.exit(1)
    # process checks
    if "entries" in health_data:
        checks = health_data["entries"]
        for chk in checks:
            logger.info(f"System: {chk}, Status: " + checks[chk]["status"])
    return health_data
