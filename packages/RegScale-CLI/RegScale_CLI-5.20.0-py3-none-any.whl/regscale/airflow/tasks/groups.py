"""Define pre-made TaskGroups for usage across DAGs."""
from uuid import uuid4

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

from regscale.airflow.tasks.init import get_shared_keys, set_shared_config_values
from regscale.airflow.tasks.click import execute_click_command
from regscale.airflow.hierarchy import AIRFLOW_CLICK_OPERATORS as OPERATORS


def setup_task_group(
    dag: DAG,
    setup_tag: str = None,
) -> TaskGroup:
    """Create a TaskGroup for setting up the init.yaml and initialization of the DAG
    :param DAG dag: an Airflow DAG
    :param str setup_tag: a unique identifier for the task
    :returns: a setup TaskGroup
    :rtype TaskGroup:
    """
    if not setup_tag:
        setup_tag = str(uuid4())[
            :8
        ]  # give the task setup group a unique name for tracking
    setup_name = f"setup-{setup_tag}"
    with TaskGroup(setup_name, dag=dag) as setup:
        # initialize the init yaml
        init_yaml = PythonOperator(
            task_id=f"initialize_init_yaml-{setup_tag}",
            task_group=setup,
            python_callable=execute_click_command,
            op_kwargs={
                "command": OPERATORS["init"]["command"],
                "skip-prompts": True,
                "skip_prompts": True,
                "domain": "{{ dag_run.conf['domain'] }}",
                "token": "{{ dag_run.conf['token'] }}",
                "user_id": "{{ dag_run.conf['userId'] }}",
            },
            provide_context=True,
            dag=dag,
        )
        # find keys shared between the dag_run.config object and init.yaml
        shared_keys_task_name = f"get_shared_keys-{setup_tag}"

        login = PythonOperator(
            task_id=f"login-{setup_tag}",
            task_group=setup,
            python_callable=execute_click_command,
            op_kwargs={
                "command": OPERATORS["login"]["command"],
                "token": '{{ dag_run.conf["token"] }}',
                "domain": '{{ dag_run.conf["domain"] }}',
            },
        )

        shared_keys_task = PythonOperator(
            task_id=shared_keys_task_name,
            task_group=setup,
            python_callable=get_shared_keys,
            provide_context=True,
            dag=dag,
        )

        init_yaml >> shared_keys_task >> login
        return setup
