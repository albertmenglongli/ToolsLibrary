import datetime

def get_date_str(base_date_str=None, delta_day=0, input_format='%Y-%m-%d', output_format='%Y-%m-%d'):
    _base_date = datetime.datetime.strptime(base_date_str, input_format).date() if base_date_str else datetime.datetime.utcnow()
    delta_date = _base_date + datetime.timedelta(days=delta_day)
    return delta_date.strftime(output_format)

