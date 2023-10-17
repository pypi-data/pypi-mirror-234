"""Use a regscale config session to try to import the dag_run_conf keys"""

from airflow.models import Variable, DagRun
from airflow.utils.db import provide_session


@provide_session
def get_dag_run_conf_keys(session=None):
    """Get a DagRun's conf Keys and store as a variable."""
    dag_run_conf_keys = []
    for dag_run in session.query(DagRun).all():
        if dag_run.conf:
            dag_run_conf_keys.extend(dag_run.conf.keys())
