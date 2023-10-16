# Commutauto

CLI to interact with your car sharing service API.

Search for available vehicles, manage your bookings and more...

## Credentials management

To set your credentials as environment variable, either run the following commands in your terminal:

```
export USER_NAME=""
export PASSWORD=""
```

or create a .env file in the location from where you will run the CLI commands/your python script:

```
#.env

USER_NAME=""
PASSWORD=""
```
## Verbosity management

Set the log level using an environment variable

```
export LOG_LEVEL=""
```

## CLI Examples
### Search station

```
commutauto station search \
        --city montreal \
        --latitude 45.5212748 \
        --longitude -73.574787 \
        --radius 0.3 \
        --start_date 2023-03-13T06:30:00 \
        --end_date 2023-03-13T07:00:00 \
        --search_duration 2 \
        --book
```


### Book station

```
commutauto station book \
        --city montreal \
        --latitude 45.5212748 \
        --longitude -73.574787 \
        --start_date 2023-03-13T06:30:00 \
        --end_date 2023-03-13T07:00:00 \
        --car_id 1234
```

### List station bookings
```
commutauto station list_booking
```

### Cancel station booking

```
commutauto station cancel_booking \
        --reservation_id 29633225
```

### Search flex

```
commutauto flex search \
        --city montreal \
        --latitude 45.5212748 \
        --longitude -73.574787 \
        --radius 2 \
        --search_duration 2 \
        --book
```

### Book flex

```
commutauto flex book \
    --city montreal \
    --car_vin XXXXXXXXXXXXXXXXX
```

### Cancel flex booking

```
commutauto flex cancel_booking \
                --city montreal 
```
## Python code Examples

## Search and book station

```python

import datetime as dt

from commutauto.client import CommutautoClient
import commutauto.booking_service.station as bs_station
from commutauto.constants import Cities

# Some functions do not require authentication
client = CommutautoClient(authenticated=False)

# Some functions do  require authentication
auth_client = CommutautoClient(authenticated=True)

start_date=dt.datetime(year=2023, month=3, day=19, hour=6, minute=0)
end_date=dt.datetime(year=2023, month=3, day=19, hour=18, minute=30)
city = Cities.MONTREAL
latitude=45.507723
longitude=-73.562757
radius=0.5 #km

stations = bs_station.get_available_stations_whithin_radius(
                                client, 
                                start_date=start_date,
                                end_date=end_date,
                                latitude=latitude,
                                longitude=longitude,
                                city_id=city,
                                radius=radius)

if stations:
    reservation_id = bs_station.book_car_from_id(auth_client, 
                                            start_date=start_date, 
                                            end_date=end_date, 
                                            car_id=stations[0].CarID, 
                                            latitude=latitude, 
                                            longitude=longitude,
                                            city_id=city)

```

## Search station with retries and book station

```python
import datetime as dt

from commutauto.client import CommutautoClient
import commutauto.booking_service.station as bs_station
from commutauto.constants import Cities

# Some functions do not require authentication
client = CommutautoClient(authenticated=False)

# Some functions do  require authentication
auth_client = CommutautoClient(authenticated=True)

start_date=dt.datetime(year=2023, month=3, day=19, hour=6, minute=0)
end_date=dt.datetime(year=2023, month=3, day=19, hour=18, minute=30)
city = Cities.MONTREAL
latitude=45.507723
longitude=-73.562757
radius=0.5 #km

closest_available_station = bs_station.available_station_search_with_retries(
                                                                        client, 
                                                                        start_date=start_date, 
                                                                        end_date=end_date, 
                                                                        latitude=latitude, 
                                                                        longitude=longitude, 
                                                                        radius=radius,
                                                                        city_id=city,
                                                                        expiration_time_second=6*60*60 # 6 hours
                                                                    )

if closest_available_station:
    reservation_id = bs_station.book_car_from_id(auth_client, 
                                            start_date=start_date, 
                                            end_date=end_date, 
                                            car_id=closest_available_station.CarID, 
                                            latitude=latitude, 
                                            longitude=longitude,
                                            city_id=city)

```

## List station bookings

```python
import commutauto.booking_service.station as bs_station
from commutauto.client import CommutautoClient

auth_client = CommutautoClient(authenticated=True)

bs_station.get_car_booking_list(auth_client)

for reservation in reservations:
    print(reservation)
```

## Cancel station booking

```python
import commutauto.booking_service.station as bs_station
from commutauto.client import CommutautoClient

auth_client = CommutautoClient(authenticated=True)

latitude=45.507723
longitude=-73.562757

reservation = bs_station.get_car_booking(auth_client, reservation_id)
canceled = bs_station.cancel_car_booking(
    auth_client, 
    reservation=reservation, 
    latitude=latitude, 
    longitude=longitude
    )
print(canceled)
```

## Search and book flex

```python
import commutauto.booking_service.flex as bs_flex
from commutauto.client import CommutautoClient
from commutauto.constants import Cities

auth_client = CommutautoClient(authenticated=True)

latitude=45.507723
longitude=-73.562757
city = Cities.MONTREAL
radius = 0.5 # km

flexes_whithin_radius = bs_flex.get_available_flexess_whithin_radius(client,
                                                                    branch_id=branch,
                                                                    city_id=city,
                                                                    latitude=latitude, 
                                                                    longitude=longitude, 
                                                                    radius=radius)
        
if flexes_whithin_radius:
    booking_result = bs_flex.book_flex_from_vin(authenticated_client, 
                                            car_vin=flexes_whithin_radius[0].CarVin,
                                            branch_id=branch)
    print(booking_result)
```

## Search flex with retries and book flex if found

```python
from commutauto.client import CommutautoClient

auth_client = CommutautoClient(authenticated=True)

latitude=45.507723
longitude=-73.562757
city = Cities.MONTREAL
branch = CitiesToBranchesMapping[city]
radius=0.5

flex = bs_flex.available_flexes_search_with_retries(auth_client, 
                                latitude=latitude,
                                longitude=longitude,
                                branch_id=branch,
                                city_id=city,
                                radius=radius,
                                expiration_time_second=2*60*60 # 2 hours
                                )

if flex:
    booking_result = bs_flex.book_flex_from_vin(authenticated_client, 
                                            car_vin=flex[0].CarVin,
                                            branch_id=branch)
    print(booking_result)
```

## Cancel flex booking

```python
import commutauto.booking_service.flex as bs_flex
from commutauto.constants import Cities, CitiesToBranchesMapping
from commutauto.client import CommutautoClient

city = Cities.MONTREAL
branch = CitiesToBranchesMapping[city]
auth_client = CommutautoClient(authenticated=True)

cancel_result = bs_flex.cancel_flex_booking(auth_client, branch_id=branch)
```
## Get current flex booking

```python
import commutauto.booking_service.flex as bs_flex
from commutauto.constants import Cities, CitiesToBranchesMapping

city = Cities.MONTREAL
branch = CitiesToBranchesMapping[city]
auth_client = CommutautoClient(authenticated=True)

bs_flex.get_current_flex(auth_client, branch_id=branch)
```