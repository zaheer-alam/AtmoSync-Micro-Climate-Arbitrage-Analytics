select distinct
    container_id,
    location,
    temperature,
    humidity,
    rainfall,
    wind_speed,
    recorded_at
from {{ source('raw', 'sensor_data') }}
