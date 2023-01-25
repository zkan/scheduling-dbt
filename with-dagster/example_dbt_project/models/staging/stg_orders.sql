select
    id as order_id,
    user_id as customer_id,
    order_date,
    status

from {{ source('example_dbt_project', 'orders_raw') }}