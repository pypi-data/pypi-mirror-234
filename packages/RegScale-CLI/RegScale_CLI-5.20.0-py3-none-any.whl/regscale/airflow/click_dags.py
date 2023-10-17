"""Create functions to generate a DAG based on click hierarchy."""

from typing import Optional
from datetime import datetime, timezone
import os

import click
from airflow import DAG
from airflow.operators.python import PythonOperator

from regscale.airflow.tasks.cli import make_login_task, make_set_domain_task
from regscale.airflow.tasks.click import execute_click_command
from regscale.regscale import cli

from regscale.models.click_models import ClickCommand


def generate_operator_for_command(
    command: ClickCommand,
    dag: DAG,
    command_name: str = None,
) -> PythonOperator:
    """Generate an Operator for click command
    :param command: a click.Command instruction
    :param dag: an Airflow DAG
    :param command_name: an optional string for command_name, will default to click.Command.name
    :returns: A PythonOperator configured with the click command.name
    """
    return PythonOperator(
        task_id=command_name or command.name,  # TODO - also name based on group id
        python_callable=execute_click_command,
        op_kwargs={"command": command},
        provide_context=True,  # required to pass required arguments to the dag run
        dag=dag,
    )


def generate_dag_for_group(
    group: click.Group,
    default_args: dict,
    command_name: str = None,
) -> DAG:
    """Generate a dag for a click group
    :param group: a click Group object to generate dags for
    :param default_args: dict to be passed when creating the DAGs
    :param command_name:
    :returns: a dag for each click group
    """
    if command_name is None:
        command_name = group.name
    dag = DAG(
        command_name,
        default_args=default_args,
        description=f"DAG for Click Group: {group.name}",
        schedule_interval=None,
    )

    # iterate through the group value commands
    for command in group.commands.values():
        if isinstance(command, click.Group):
            # if it is click.Group, call this recursively, adding to the command_name
            generate_dag_for_group(
                command,
                default_args,
                command_name="__".join([command_name, command.name]),
            )
        else:
            login_task = make_login_task(dag=dag)
            domain_task = make_set_domain_task(dag=dag)
            operator = generate_operator_for_command(
                command=command,
                dag=dag,
                command_name="__".join([command_name, command.name]),
            )
            # assign the relationships for the operators
            domain_task >> login_task >> operator
    return dag


def generate_dags_for_click_app(
    app: Optional[click.Group] = None,
    default_args: Optional[dict] = None,
    command_name: Optional[str] = None,
):
    """If App is None it will search the cli"""
    if app is None:
        app = cli
    if not default_args:
        default_args = dict(
            owner=os.getenv("REGSCALE_AIRFLOW_USER", "regscale"),
            start_date=datetime.now(timezone.utc),
        )
    if not command_name:
        command_name = "regscale" if app.name == "cli" else app.name
    dags = []
    for group in app.commands.values():
        if isinstance(group, click.Group):
            command_name = "regscale" if group.name == "cli" else group.name
            for sub_group in group.commands.values():
                if isinstance(sub_group, click.Group):
                    generate_dag_for_group(app=sub_group, default_args=default_args)
                else:
                    dag = generate_dag_for_group(
                        group=group,
                        default_args=default_args,
                        command_name=command_name,
                    )
                    dags.append(dag)
        elif isinstance(group, click.Command):
            dag = generate_dag_for_group(
                group=group,
                default_args=default_args,
                command_name=command_name,
            )
            dags.append(dag)

    return dags
