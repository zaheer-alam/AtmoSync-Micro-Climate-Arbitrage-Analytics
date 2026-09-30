select
    price_date,
    commodity,
    market,
    price_per_kg,

    lag(price_per_kg) over (
        partition by commodity, market
        order by price_date
    ) as previous_price_per_kg,

    round(
        price_per_kg - lag(price_per_kg) over (
            partition by commodity, market
            order by price_date
        ),
        2
    ) as price_change_per_kg

from {{ ref('stg_historical_commodity_prices') }}
