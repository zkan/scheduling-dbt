select
    id as customer_id,
    first_name,
    last_name

from {{ source('example_dbt_project', 'customers_raw') }}