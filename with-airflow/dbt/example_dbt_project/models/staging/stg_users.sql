select
    user_id,
    first_name,
    last_name

from {{ source('greenery', 'users') }}