import datetime
import time

import pytz

country_code_to_timezone = {
    'MX': 'America/Mexico_City',
    'BR': 'America/Sao_Paulo',
    'JP': 'Asia/Tokyo',
    'CO': 'America/Bogota',
    'CR': 'America/Costa_Rica',
    'AR': 'America/Argentina/Buenos_Aires',
    'CL': 'America/Santiago',
    'DO': 'America/Santo_Domingo',
    'PE': 'America/Lima',
    'BJ': 'Asia/Shanghai'
}


def get_time_stamp():
    return int(time.time())

def get_hour_time_stamp():
    current_datetime = datetime.datetime.now()
    current_hour = current_datetime.replace(minute=0, second=0, microsecond=0)
    current_timestamp = int(current_hour.timestamp())
    return current_timestamp

def get_local_hour(timezone): # timezone = pytz.timezone('时区名称')
    now = datetime.datetime.now()
    timezone1 = pytz.timezone(timezone)
    local_time = now.astimezone(timezone1)
    return str(local_time.hour).zfill(2)

def get_local_date(timezone):
    now = datetime.datetime.now()
    timezone1 = pytz.timezone(timezone)
    local_time = now.astimezone(timezone1)
    return str(local_time.date())

def get_weekday(timezone):
    now = datetime.datetime.now()
    timezone1 = pytz.timezone(timezone)
    local_time = now.astimezone(timezone1)
    return str(local_time.weekday)

def get_weekend(timezone):
    day = get_weekday(timezone)
    if day in [5,6,0]:
        return 1
    return 0

def get_timezone_by_city_id(city_id):
    if str(city_id)[:2] == '52':
        country_code = 'MX'
    elif str(city_id)[:2] == '57':
        country_code = 'CO'
    elif str(city_id)[:2] == '50':
        country_code = 'CR'
    elif str(city_id)[:2] == '56':
        country_code = 'CL'
    elif str(city_id)[:2] == '51':
        country_code = 'PE'
    elif str(city_id)[:2] == '80':
        country_code ='DO'
    return country_code_to_timezone[country_code]
