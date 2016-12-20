def parse_timezone_to_oclock_sharp(timezone_str):
    # parse timezone to [-12:00, -11:00, ... -01:00, +00:00, +01:00, +02:00, ... , +11:00, +12:00]
    import re
    timezone_str = timezone_str.strip().replace(' ', '')
    if timezone_str and re.match(r'^[+-]?(0[0-9]|[0-9]|1[012]):([0-5][0-9])$', timezone_str):
        valid_timezone_str = re.sub(r'^([+-]?(0[0-9]|[0-9]|1[012]):)([0-9]{2})$', r'\g<1>00', timezone_str)
        if not (valid_timezone_str.startswith('+') or valid_timezone_str.startswith('-')):
            valid_timezone_str = '+' + valid_timezone_str
        m = re.match(r'^([+-])(0[0-9]|[0-9]|1[012])(:00)$', valid_timezone_str)
        return ''.join([m.group(1), m.group(2).zfill(2), m.group(3)])
    else:
        raise Exception('Timezone invalid: %s' % timezone_str)
 
 if __name__ == "__main__":
    lst = ['00:00', '00: 00', '1:00', '01:00\n', '+01:30', '-11:00', '-11:30', '-12:00']
    print(map(parse_timezone_str_to_supported_if_valid, lst))
    # ['+00:00', '+00:00', '+01:00', '+01:00', '+01:00', '-11:00', '-11:00', '-12:00']
