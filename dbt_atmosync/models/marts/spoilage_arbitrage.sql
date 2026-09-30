with risk_data as (

    select
        container_id,
        location,
        temperature,
        humidity,
        risk_score,
        risk_level,
        estimated_hours_to_spoil,
        recorded_at
    from {{ ref('spoilage_risk') }}

),

market_prices as (

    select
        commodity,
        market,
        price_per_kg
    from {{ ref('stg_commodity_prices') }}

),

route_data as (

    select
        current_location,
        market,
        distance_km
    from {{ ref('stg_market_routes') }}

),

opportunities as (

    select
        r.container_id,
        r.location as current_location,
        r.temperature,
        r.humidity,
        r.risk_score,
        r.risk_level,
        r.estimated_hours_to_spoil,
        r.recorded_at,

        p.commodity,
        p.market as candidate_market,
        p.price_per_kg,

        current_price.price_per_kg as current_market_price,

        routes.distance_km,

        -- Demo assumption: average transport speed = 50 km/h
        round(routes.distance_km / 50.0, 2) as estimated_travel_hours,

        case
            when (routes.distance_km / 50.0) < r.estimated_hours_to_spoil
                then 'VIABLE'
            else 'NOT_VIABLE'
        end as route_status

    from risk_data r

    join route_data routes
        on r.location = routes.current_location

    join market_prices p
        on routes.market = p.market

    left join market_prices current_price
        on r.location = current_price.market
        and p.commodity = current_price.commodity

),

ranked_opportunities as (

    select
        *,

        row_number() over (
            partition by container_id, recorded_at
            order by
                case when route_status = 'VIABLE' then 0 else 1 end,
                case when route_status = 'VIABLE' then price_per_kg end desc,
                distance_km asc
        ) as market_rank

    from opportunities

)

select
    container_id,
    current_location,
    commodity,
    temperature,
    humidity,
    risk_score,
    risk_level,
    estimated_hours_to_spoil,

    current_market_price,
    candidate_market as recommended_market,
    price_per_kg as recommended_market_price,

    round(
        price_per_kg - current_market_price,
        2
    ) as arbitrage_gain_per_kg,

    distance_km,
    estimated_travel_hours,
    route_status,

    case
        when route_status = 'VIABLE'
            then round(
                estimated_hours_to_spoil - estimated_travel_hours,
                2
            )
        else null
    end as safety_margin_hours,

    recorded_at

from ranked_opportunities

where market_rank = 1