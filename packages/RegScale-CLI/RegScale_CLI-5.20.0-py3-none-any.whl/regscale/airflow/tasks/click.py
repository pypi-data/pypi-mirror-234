import logging
from pathlib import Path
from pydantic import ValidationError

from regscale.models.click_models import ClickCommand


def execute_click_command_old(command: ClickCommand, **context):
    """Execute a click command
    :param command: a click command to execute
    :param kwargs: get dag_run from conf
    """
    dag_run = context["dag_run"]
    try:
        command_model = command.parse_obj(dag_run.conf)
    except ValidationError as exc:
        # This will raise a ValidationError if any required parameters are missing
        raise ValueError(
            f"Invalid parameters for command '{command.name}': {str(exc)}"
        ) from exc
    valid_params = {
        name: value
        for name, value in command_model.dict().items()
        if name in command.params
    }
    command.callback(**valid_params)


def execute_click_command(command: ClickCommand, **context):
    """Execute a click command
    :param command: a click command to execute
    :param context: get dag_run from conf
    """
    # Get the dag_run from the context, or raise an error if it's not present
    dag_run = context.get("dag_run")
    parameters = command.parameters
    logging.info(f"{parameters=}")
    op_kwargs = {param: context.get(param) for param in parameters}
    logging.info(f"{op_kwargs.keys()}")
    if dag_run is None:
        raise ValueError("No dag_run in context")
    if dag_run.conf is None:
        dag_run.conf = {}
    # merge the dictionaries, giving precedence to op_kwargs
    command_parameters = {**dag_run.conf, **op_kwargs}
    logging.info(f"{command_parameters.keys()}")
    try:
        # valid_params = command.get_callback_args(command_parameters)
        valid_params = {
            key: value
            for key, value in command_parameters.items()
            if key in command.parameters
        }
        logging.info(f"{valid_params=}")
    except Exception as exc:
        # Catch any other exceptions that might be raised
        logging.error(f"Error parsing command {command.name} parameters: {str(exc)}")
        raise
    try:
        command.call(**valid_params)
    except UnboundLocalError as exc:
        if "callback_results" in str(exc):
            return None
        # Catch any exceptions that might be raised by the command callback
        logging.error(f"Error executing command '{command.name}': {str(exc)}")
        raise
    return None
