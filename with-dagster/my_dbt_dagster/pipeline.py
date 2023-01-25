import os

from dagster import (
    asset,
    AssetIn,
    AssetSelection,
    define_asset_job,
    Definitions,
    file_relative_path,
    MetadataValue,
    ScheduleDefinition,
)
from dagster_dbt import (
    dbt_cli_resource,
    load_assets_from_dbt_project,
)

import pandas as pd
import plotly.express as px
from dagster_duckdb_pandas import duckdb_pandas_io_manager


@asset(key_prefix=["example_dbt_project"], group_name="staging")
def customers_raw() -> pd.DataFrame:
    data = pd.read_csv("https://docs.dagster.io/assets/customers.csv")
    return data


@asset(key_prefix=["example_dbt_project"], group_name="staging")
def orders_raw() -> pd.DataFrame:
    data = pd.read_csv("https://docs.dagster.io/assets/orders.csv")
    return data


DBT_PROJECT_PATH = file_relative_path(__file__, "../example_dbt_project")
DBT_PROFILES = file_relative_path(__file__, "../example_dbt_project/config")

# if larger project use load_assets_from_dbt_manifest
# dbt_assets = load_assets_from_dbt_manifest(json.load(DBT_PROJECT_PATH + "manifest.json", encoding="utf8"))
dbt_assets = load_assets_from_dbt_project(
    project_dir=DBT_PROJECT_PATH, profiles_dir=DBT_PROFILES, key_prefix=["example_dbt_project"]
)


@asset(ins={"customers": AssetIn(key_prefix=["example_dbt_project"])}, key_prefix=["example_output"], group_name="staging")
def order_count_chart(context, customers: pd.DataFrame) -> None:
    fig = px.histogram(customers, x="number_of_orders")
    fig.update_layout(bargap=0.2)
    save_chart_path = file_relative_path(__file__, "order_count_chart.html")
    fig.write_html(save_chart_path, auto_open=True)

    context.add_output_metadata({"plot_url": MetadataValue.url("file://" + save_chart_path)})


my_job = define_asset_job(
    name="my_job", selection=AssetSelection.all()
)

my_job_schedule = ScheduleDefinition(
    name="my_job_schedule", job=my_job, cron_schedule="* * * * *"
)

defs = Definitions(
    assets=dbt_assets + [customers_raw, orders_raw, order_count_chart],
    schedules=[my_job_schedule],
    jobs=[my_job],
    resources={
        "dbt": dbt_cli_resource.configured(
            {
                "project_dir": DBT_PROJECT_PATH,
                "profiles_dir": DBT_PROFILES,
            },
        ),
        "io_manager": duckdb_pandas_io_manager.configured(
            {"database": os.path.join(DBT_PROJECT_PATH, "example.duckdb")}
        ),
    },
)
