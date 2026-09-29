select
    commodity,
    market,
    price_per_kg,
    distance_km
from {{ source('raw', 'commodity_prices') }}