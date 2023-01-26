with users as (

    select * from {{ ref('stg_users') }}

),

orders as (

    select * from {{ ref('stg_orders') }}

),

final as (

    select
        orders.order_id
        , users.user_id
        , users.first_name
        , users.last_name
        , orders.status
        

    from orders
    left join users
    on users.user_id = orders.user_id

)

select * from final