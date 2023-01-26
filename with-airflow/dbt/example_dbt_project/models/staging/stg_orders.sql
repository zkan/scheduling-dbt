select
    order_id,
    user_id,
    created_at,
    status

from {{ source('greenery', 'orders') }}