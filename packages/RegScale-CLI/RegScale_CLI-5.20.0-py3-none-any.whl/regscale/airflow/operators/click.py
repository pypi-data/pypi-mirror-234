"""Generate PythonOperators based on a click.Command."""
from typing import Union, Optional

from airflow import DAG
from airflow.operators.python import PythonOperator

import click

from regscale.models.click_models import ClickCommand
from regscale.airflow.tasks.click import execute_click_command


def generate_operator_for_command(
    command: Union[click.Command, ClickCommand],
    command_name: Optional[str] = None,
    dag: Optional[DAG] = None,
    **kwargs,
) -> PythonOperator:
    """Generate a PythonOperator for a Click Command
    :param command: the command to generate the operator for
    :param command_name: optional command name to specify as task_id
    :param dag: an Optional airflow DAG to pass
    :param kwargs: additional named parameters to pass to PythonOperator
    """
    if isinstance(command, click.Command):
        command = ClickCommand.from_command(command)
    return PythonOperator(
        task_id=command_name or command.name,
        python_callable=execute_click_command,
        op_kwargs={"command": command.callback},
        dag=dag,
        **kwargs,
    )
