select
    price_date,
    commodity,
    market,
    price_per_kg
from {{ source('raw', 'historical_commodity_prices') }}
