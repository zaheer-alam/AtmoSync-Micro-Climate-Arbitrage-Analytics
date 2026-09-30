with sensor_data as (

    select
        container_id,
        location,
        temperature,
        humidity,
        rainfall,
        wind_speed,
        vibration,
        recorded_at
    from {{ ref('stg_sensor_data') }}

),

risk_calculation as (

    select
        *,
        case
            when humidity >= 85 then 20
            when humidity >= 70 then 10
            else 0
        end
        +
        case
            when vibration >= 4 then 10
            when vibration >= 2.5 then 5
            else 0
        end as risk_score

    from sensor_data

)

select
    container_id,
    location,
    temperature,
    humidity,
    rainfall,
    wind_speed,
    vibration,
    recorded_at,
    risk_score,

    case
        when risk_score >= 70 then 'HIGH'
        when risk_score >= 40 then 'MEDIUM'
        else 'LOW'
    end as risk_level,

    case
        when risk_score >= 70 then 12
        when risk_score >= 40 then 24
        else 48
    end as estimated_hours_to_spoil

from risk_calculation
