# -*- coding: utf-8 -*-

from copy import deepcopy
import datetime


def convert_to_crontabs_time_str(crontab_times):
    def _convert_to_crontab_time_str(crontab_time):
        return ' '.join([crontab_time['minute'], crontab_time['hour'], crontab_time['day_of_month'], crontab_time['month_of_year'], crontab_time['day_of_week']])
    results = []
    for crontab_time in crontab_times:
        result = _convert_to_crontab_time_str(crontab_time)
        results.append(result)
    return results


def timezone_parser(crontab_time, hour_delta=-12):

    def copy_dict_with_stringfy_and_default_valuevalue(my_dict):
        keys = ['minute', 'hour', 'day_of_month', 'month_of_year', 'year', 'day_of_week']
        d = {k: str(v) for k, v in my_dict.items()}
        for key in keys:
            if key not in d.keys():
                d[key] = '*'
        return d

    crontab_time = copy_dict_with_stringfy_and_default_valuevalue(crontab_time)
    month_type = {
        28: [2],
        30: [4, 6, 9, 11],
        31: [1, 3, 5, 7, 8, 10, 12]
    }
    minute = int(crontab_time.get('minute')) if crontab_time.get('minute', '*').isdigit() else '*'
    hour = int(crontab_time.get('hour', '0'))
    day_of_week = int(crontab_time.get('day_of_week')) if crontab_time.get('day_of_week', '*').isdigit() else '*'
    day_of_month = int(crontab_time.get('day_of_month')) if crontab_time.get('day_of_month', '*').isdigit() else '*'
    month_of_year = int(crontab_time.get('month_of_year')) if crontab_time.get('month_of_year', '*').isdigit() else '*'
    year = int(crontab_time.get('year')) if crontab_time.get('year', '*').isdigit() else '*'

    if isinstance(day_of_week, int):
        result = deepcopy(crontab_time)
        result['hour'], result['day_of_week'] = (hour + hour_delta) % 24, (day_of_week - 1 + (hour + hour_delta) / 24) % 7 + 1
        return [copy_dict_with_stringfy_and_default_valuevalue(result)]

    elif all(isinstance(e, int) for e in [minute, hour, day_of_month, month_of_year, year]):
        dt = datetime.datetime(year, month_of_year, day_of_month, hour, minute) + datetime.timedelta(hours=hour_delta)
        result = deepcopy(crontab_time)
        result['year'], result['month_of_year'], result['day_of_month'], result['hour'] = dt.year, dt.month, dt.day, dt.hour
        return [copy_dict_with_stringfy_and_default_valuevalue(result)]
    else:
        result = deepcopy(crontab_time)
        result['hour'] = (hour + hour_delta) % 24
        if crontab_time['day_of_month'] == '*':
            return [copy_dict_with_stringfy_and_default_valuevalue(result)]
        else:
            results = []
            if crontab_time['month_of_year'].isdigit():
                result = deepcopy(crontab_time)
                new_month_of_year = (month_of_year - 1 + (hour + hour_delta) / 24) % 12 + 1
                for dates_num_in_month, months in month_type.items():
                    if new_month_of_year in months:
                        dates_num_in_month = dates_num_in_month
                        result['hour'], result['day_of_month'], result['month_of_year'] = (
                            hour + hour_delta) % 24, (day_of_month - 1 + (hour + hour_delta) / 24) % dates_num_in_month + 1, new_month_of_year
                        return [copy_dict_with_stringfy_and_default_valuevalue(result)]
            else:
                for dates_num_in_month, months in month_type.items():
                    result = deepcopy(crontab_time)
                    result['hour'] = (hour + hour_delta) % 24
                    result['day_of_month'] = (day_of_month - 1 + (hour + hour_delta) / 24) % dates_num_in_month + 1
                    result['month_of_year'] = ','.join([str(e) for e in months])
                    results.append(result)
            return [copy_dict_with_stringfy_and_default_valuevalue(result) for result in results]

