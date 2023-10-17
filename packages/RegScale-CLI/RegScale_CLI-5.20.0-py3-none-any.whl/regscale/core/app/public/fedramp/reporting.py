"""Provide modules for logging and reporting."""
from datetime import datetime

import pandas as pd

from regscale.core.app.logz import create_logger

logger = create_logger()


def log_event(
    record_type: str,
    event_msg: str,
    model_layer: str = "Undefined",
    level: str = "Info",
) -> dict:
    """
    Function to log events
    :param record_type: record type (SSP, Control Implementation, etc)
    :param event_msg: Message to log for the event
    :param model_layer: relevant NIST SSP model layer missing from, such as 'metadata' or 'system-characteristics'
    :param level: Level of logging, defaults to info
    :returns: dict to save to logs
    :return: Dict
    """

    logger.info(f"Layer: {model_layer} |  {record_type} | {event_msg}")

    event_entry = {
        "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
        "level": level,
        "model_layer": model_layer,
        "record_type": record_type,
        "event": event_msg,
    }
    return event_entry


def log_error(
    record_type: str,
    missing_element: str = "Undefined",
    model_layer: str = "Undefined",
    level: str = "Error",
    event_msg: str = None,
) -> dict:
    """
    :param record_type: record type (SSP, Control Implementation, etc)
    :param missing_element: the name data element expected but not found, defaults to 'Undefined'
    :param model_layer: relevant NIST SSP model layer missing from, such as 'metadata' or 'system-characteristics'
    :param level: Level of the logging, defaults to error
    :param event_msg: Event such as data element recorded
    :returns: dict to save to logs
    :rtype: dict
    """

    if event_msg is None:
        event_msg = f"Failed to locate required element: {missing_element}"
    msg = f"Layer: {model_layer} |  {record_type} | " + event_msg
    logger.error(msg)

    event_entry = {
        "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
        "level": level,
        "model_layer": model_layer,
        "record_type": record_type,
        "event": event_msg,
    }
    return event_entry


def write_events(events_list) -> None:
    """
    Write events to CSV file
    :param events_list: list of events to be written to CSV
    :return: None
    """
    events_df = pd.DataFrame(events_list)
    events_df.to_csv("artifacts/import-results.csv")
