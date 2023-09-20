import json
import datetime

dct = json.loads(
    json.dumps({"user": "CCT", "usr_pass": "200318", "db_adress": "10.10.4.4", "db_login": "sa", "db_pass": "qwEr12#4",
                "db_name": "dozor_2023_07_29", "time_interval": "00:15", "tm_begin": "17:00", "dt_begin": "2023-09-06",
                "tm_end": "00:00", "dt_end": "2023-12-06"}))

hour_interval, minute_interval = dct['time_interval'].split(':')
hour_begin, minute_begin = dct['tm_begin'].split(':')
year_begin, month_begin, day_begin = dct['dt_begin'].split('-')
hour_end, minute_end = dct['tm_end'].split(':')
year_end, month_end, day_end = dct['dt_end'].split('-')

print(hour_interval, minute_interval, hour_begin, minute_begin, year_begin, month_begin, day_begin, hour_end,
      minute_end, year_end, month_end, day_end, sep='\n')
