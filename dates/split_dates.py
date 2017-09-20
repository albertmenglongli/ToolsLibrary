'''
Usage: 
Sometime, when backfill old data, we need to split the dates into small ranges to avoid of too much data to handle.
print split_dates("2016-01-01", "2016-05-08", 10)
[('2016-01-01', '2016-01-10'), ('2016-01-11', '2016-01-20'), ('2016-01-21', '2016-01-30'),
('2016-01-31', '2016-02-09'), ('2016-02-10', '2016-02-19'), ('2016-02-20', '2016-02-29'),
('2016-03-01', '2016-03-10'), ('2016-03-11', '2016-03-20'), ('2016-03-21', '2016-03-30'),
('2016-03-31', '2016-04-09'), ('2016-04-10', '2016-04-19'), ('2016-04-20', '2016-04-29'), ('2016-04-30', '2016-05-08')]
'''

def split_dates(start_date, end_date, piece_length, date_format="%Y-%m-%d"):
    import datetime
    assert isinstance(piece_length, int)
    assert piece_length >= 1

    if isinstance(start_date, str):
        start_date = datetime.datetime.strptime(start_date, date_format).date()
    if isinstance(end_date, str):
        end_date = datetime.datetime.strptime(end_date, date_format).date()

    if not (isinstance(start_date, datetime.date) and isinstance(end_date, datetime.date)):
        raise ValueError("Parameters Error")
    assert end_date > start_date
    nums = (end_date - start_date).days
    step = piece_length
    pieces_of_dates = [(start_date + datetime.timedelta(days=x), start_date + datetime.timedelta(days=x + step - 1 if x + step - 1 < nums else nums)) for x in range(0, nums + 1, step)]
    pieces_of_dates_str =[(e[0].strftime("%Y-%m-%d"), e[1].strftime("%Y-%m-%d")) for e in pieces_of_dates]
    return pieces_of_dates_str
