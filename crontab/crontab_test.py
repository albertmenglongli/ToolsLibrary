from crontab import *

def test():
    ''' Oncely'''
    assert convert_to_crontabs_time_str(timezone_parser({'month_of_year': 3, 'day_of_month': 1, 'day_of_week': "*",
                                            'hour': 11, 'minute': 34, 'year': 2016})) == ['34 23 29 2 *']

    ''' Daily'''
    assert convert_to_crontabs_time_str(timezone_parser({'year': "*", 'month_of_year': '*', 'day_of_month': '*', 'hour': '11'})) == ['* 23 * * *']

    ''' Monthly'''
    assert convert_to_crontabs_time_str(timezone_parser({'year': "*", 'month_of_year': '*', 'day_of_month': '1', 'hour': '11'})
                           ) == ['* 23 28 2 *', '* 23 30 4,6,9,11 *', '* 23 31 1,3,5,7,8,10,12 *']

    ''' Yearly'''
    assert convert_to_crontabs_time_str(timezone_parser({'year': "*", 'month_of_year': '3', 'day_of_month': '1', 'hour': '10'})) == ['* 22 28 2 *']
    assert convert_to_crontabs_time_str(timezone_parser({'year': "*", 'month_of_year': '1', 'day_of_month': '1', 'hour': '10'})) == ['* 22 31 12 *']

    ''' Weeekly'''
    assert convert_to_crontabs_time_str(timezone_parser({'month_of_year': "*", 'day_of_month': "*",
                                            'day_of_week': 1, 'hour': 11, 'minute': 34, 'year': "*"})) == ['34 23 * * 7']
    assert convert_to_crontabs_time_str(timezone_parser({'month_of_year': "*", 'day_of_month': "*",
                                            'day_of_week': 2, 'hour': 11, 'minute': 34, 'year': "*"})) == ['34 23 * * 1']
    assert convert_to_crontabs_time_str(timezone_parser({'month_of_year': "*", 'day_of_month': "*",
                                            'day_of_week': 3, 'hour': 11, 'minute': 34, 'year': "*"})) == ['34 23 * * 2']
    assert convert_to_crontabs_time_str(timezone_parser({'month_of_year': "*", 'day_of_month': "*",
                                            'day_of_week': 4, 'hour': 11, 'minute': 34, 'year': "*"})) == ['34 23 * * 3']
    assert convert_to_crontabs_time_str(timezone_parser({'month_of_year': "*", 'day_of_month': "*",
                                            'day_of_week': 5, 'hour': 11, 'minute': 34, 'year': "*"})) == ['34 23 * * 4']
    assert convert_to_crontabs_time_str(timezone_parser({'month_of_year': "*", 'day_of_month': "*",
                                            'day_of_week': 6, 'hour': 11, 'minute': 34, 'year': "*"})) == ['34 23 * * 5']
    assert convert_to_crontabs_time_str(timezone_parser({'month_of_year': "*", 'day_of_month': "*",
                                            'day_of_week': 7, 'hour': 11, 'minute': 34, 'year': "*"})) == ['34 23 * * 6']

    assert convert_to_crontabs_time_str(timezone_parser({'month_of_year': "*", 'day_of_month': "*", 'day_of_week': 1,
                                            'hour': 13, 'minute': 34, 'year': "*"}, 18)) == ['34 7 * * 2']
    assert convert_to_crontabs_time_str(timezone_parser({'month_of_year': "*", 'day_of_month': "*", 'day_of_week': 2,
                                            'hour': 13, 'minute': 34, 'year': "*"}, 18)) == ['34 7 * * 3']
    assert convert_to_crontabs_time_str(timezone_parser({'month_of_year': "*", 'day_of_month': "*", 'day_of_week': 3,
                                            'hour': 13, 'minute': 34, 'year': "*"}, 18)) == ['34 7 * * 4']
    assert convert_to_crontabs_time_str(timezone_parser({'month_of_year': "*", 'day_of_month': "*", 'day_of_week': 4,
                                            'hour': 13, 'minute': 34, 'year': "*"}, 18)) == ['34 7 * * 5']
    assert convert_to_crontabs_time_str(timezone_parser({'month_of_year': "*", 'day_of_month': "*", 'day_of_week': 5,
                                            'hour': 13, 'minute': 34, 'year': "*"}, 18)) == ['34 7 * * 6']
    assert convert_to_crontabs_time_str(timezone_parser({'month_of_year': "*", 'day_of_month': "*", 'day_of_week': 6,
                                            'hour': 13, 'minute': 34, 'year': "*"}, 18)) == ['34 7 * * 7']
    assert convert_to_crontabs_time_str(timezone_parser({'month_of_year': "*", 'day_of_month': "*", 'day_of_week': 7,
                                            'hour': 13, 'minute': 34, 'year': "*"}, 18)) == ['34 7 * * 1']

    assert convert_to_crontabs_time_str(timezone_parser({'month_of_year': "*", 'day_of_month': "*", 'day_of_week': 1,
                                            'hour': 23, 'minute': 34, 'year': "*"}, 23)) == ['34 22 * * 2']
    assert convert_to_crontabs_time_str(timezone_parser({'month_of_year': "*", 'day_of_month': "*", 'day_of_week': 7,
                                            'hour': 23, 'minute': 34, 'year': "*"}, 23)) == ['34 22 * * 1']
test()

