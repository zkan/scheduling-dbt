from airflow.utils import timezone

from cosmos.providers.dbt import DbtDag


example_dbt_project = DbtDag(
    dag_id="demo_dbt_dag",
    schedule_interval="@daily",
    start_date=timezone.datetime(2022, 11, 27),
    conn_id="example_db",
    catchup=False,
    dbt_project_name="example_dbt_project",
    dbt_args={
        "schema": "public"
    },
    dbt_root_path="/opt/airflow/dbt",
)
