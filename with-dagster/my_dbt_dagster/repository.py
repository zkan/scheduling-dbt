import os

from dagster import load_assets_from_package_module, repository, with_resources
from dagster_dbt import dbt_cli_resource
from dagster_duckdb_pandas import duckdb_pandas_io_manager

from my_dbt_dagster import assets
from my_dbt_dagster.assets import DBT_PROFILES, DBT_PROJECT_PATH


@repository
def my_dbt_dagster():
    return with_resources(
        definitions=load_assets_from_package_module(assets),
        resource_defs={
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
