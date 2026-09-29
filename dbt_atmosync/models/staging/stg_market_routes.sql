select
    current_location,
    market,
    distance_km
from {{ source('raw', 'market_routes') }}