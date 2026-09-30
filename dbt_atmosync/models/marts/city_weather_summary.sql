select
    location,
    count(*) as total_readings,
    round(avg(temperature), 2) as avg_temperature,
    round(avg(humidity), 2) as avg_humidity,
    round(avg(rainfall), 2) as avg_rainfall,
    round(avg(wind_speed), 2) as avg_wind_speed,
    min(temperature) as min_temperature,
    max(temperature) as max_temperature
from {{ ref('stg_sensor_data') }}
group by location
