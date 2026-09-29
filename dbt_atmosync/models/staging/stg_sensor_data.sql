select distinct
    container_id,
    location,
    temperature,
    humidity,
    rainfall,
    wind_speed,
    vibration,
    recorded_at
from {{ source('raw', 'sensor_data') }}
