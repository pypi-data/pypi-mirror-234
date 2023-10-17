from airflow import settings
from airflow.models import DagRun, TaskInstance
from airflow.utils.state import State
from airflow.exceptions import AirflowException


def mark_dag_run_as_success(dag_id, execution_date):
    """
    This function marks a DAG run as successful.

    :param dag_id: the id of the dag
    :param execution_date: the execution date of the dag run
    """
    session = settings.Session()

    dag_run = (
        session.query(DagRun)
        .filter(
            DagRun.dag_id == dag_id,
            DagRun.execution_date == execution_date,
        )
        .one_or_none()
    )

    if dag_run:
        dag_run.state = State.SUCCESS

        # Update state of the tasks of this dag run
        session.query(TaskInstance).filter(
            TaskInstance.dag_id == dag_id,
            TaskInstance.execution_date == execution_date,
        ).update({TaskInstance.state: State.SUCCESS})

    session.commit()
    session.close()


def fail_dag_run():
    """Fail a DAG run on purpose."""
    raise AirflowException("Failed DAGRun on Purpose")
