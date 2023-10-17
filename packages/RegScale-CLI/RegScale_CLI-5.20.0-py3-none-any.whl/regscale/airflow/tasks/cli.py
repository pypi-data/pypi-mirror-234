"""Tasks for interacting with the RegScale-CLI."""
from typing import Union
from uuid import uuid4

from airflow.operators.python import PythonOperator

from regscale.utils.shell import run_command


def construct_regscale_login_command(rg_un: str, rg_pw: str) -> str:
    """Construct the RegScale-CLI login command

    :param rg_un: a string representing the RegScale User
    :param rg_pw: a string representing the RegScale User's password
    :returns: a str of the login command
    """
    return f"regscale login --username {rg_un} --password {rg_pw}"


def run_login_command(rg_un: str, rg_pw: str):
    """Execute the CLI login command
    :param rg_un: a string representing the RegScale User
    :param rg_pw: a string representing the RegScale User's password
    """
    return run_command(cmd=construct_regscale_login_command(rg_un=rg_un, rg_pw=rg_pw))


def make_cli_task(task_id: str, cmd: Union[str, list], **kwargs) -> PythonOperator:
    """Construct a cli task.

    :param task_id: a task id to assign to the operator
    :param cmd: a str or list of commands to invoke in the cli.
    """
    return PythonOperator(
        task_id=task_id,
        python_callable=run_command,
        op_kwargs={"cmd": cmd},
        **kwargs,
    )


def make_login_task(**kwargs) -> PythonOperator:
    """Construct the regscale login task
    This login task uses the dag_run.conf keys
       * `regscale-username`
       * `regscale-password`
    :returns: a PythonOperator task configured to execute run_login_command
    """
    return PythonOperator(
        task_id=f"regscale_login_{str(uuid4())[:8]}",
        python_callable=run_command,
        op_kwargs={
            "cmd": 'regscale login --username {{ dag_run.conf["regscale-username"] }}'
            ' --password {{ dag_run.conf["regscale-password"] }}'
        },
        # op_kwargs={
        #     "rg_un": '{{ dag_run.conf["regscale-username"] }}',
        #     "rg_pw": '{{ dag_run.conf["regscale-password"] }}',
        # },
        **kwargs,
    )


def make_config_task(key: str, value: str, **kwargs) -> PythonOperator:
    """Construct a config task to set key to value
    :param key: str representing the key to set in the config
    :param value: str representing the value to set for the key in the config

    :returns: a PythonOperator task configured to execute the run_command to set a config
    """
    return PythonOperator(
        task_id=f"regscale_config_{key}_{str(uuid4())[:8]}",
        python_callable=run_command,
        op_kwargs={"cmd": f"regscale config --param {key} --val {value}"},
        **kwargs,
    )


def make_set_domain_task(**kwargs) -> PythonOperator:
    """Construct as config to set the domain
    This uses the dag_run.conf["domain"] key.
    :returns: a PythonOperator that sets the domain
    """
    return PythonOperator(
        task_id=f"set_domain_{str(uuid4())[:8]}",
        python_callable=run_command,
        op_kwargs={
            "cmd": 'regscale config --param domain --val {{ dag_run.conf["domain"] }}'
        },
        **kwargs,
    )


def make_azure_config_task(**context):
    """Construct azure config tasks."""
    keys = dict(
        domain=context["dag_run"].conf.get("domain"),
        azure365ClientId=context["dag_run"].conf.get("azure365ClientId"),
        azure365Secret=context["dag_run"].conf.get("azure365Secret"),
        azure365TenantId=context["dag_run"].conf.get("azure365TenantId"),
    )
    for key, value in keys.items():
        run_command(cmd=f"regscale config --param {key} --val {value}")
