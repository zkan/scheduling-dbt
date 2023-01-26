from airflow.utils import timezone

from airflow import DAG
from airflow.operators.empty import EmptyOperator

from cosmos.providers.dbt.task_group import DbtTaskGroup


with DAG(
    dag_id="demo_dbt_task_group",
    start_date=timezone.datetime(2022, 11, 27),
    schedule="@daily",
    catchup=False,
) as dag:

    e1 = EmptyOperator(task_id="ingestion_workflow")

    dbt_tg = DbtTaskGroup(
        group_id="dbt_tg",
        conn_id="example_db",
        dbt_project_name="example_dbt_project",
        dbt_args={
            "schema": "public",
        },
        dbt_root_path="/opt/airflow/dbt",
        dag=dag,
    )

    e2 = EmptyOperator(task_id="some_extraction")

    e1 >> dbt_tg >> e2
