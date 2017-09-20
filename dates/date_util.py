class DateUtil(object):
    from enum import Enum

    class HandlingDateType(Enum):
        raw_string = 1
        raw_date = 2

    @staticmethod
    def get_first_day_of_month(dt=None, delta_of_year=0, delta_of_month=0, date_format="%Y-%m-%d"):
        import datetime
        if not dt:
            dt = datetime.date.today()
        elif isinstance(dt, str):
            dt = datetime.datetime.strptime(dt, date_format).date()

        y, m = dt.year + delta_of_year, dt.month + delta_of_month
        a, m = divmod(m - 1, 12)
        return datetime.date(y + a, m + 1, 1)

    @staticmethod
    def get_last_month_str():
        import datetime
        today = datetime.date.today()
        first = today.replace(day=1)
        lastMonth = first - datetime.timedelta(days=1)
        return lastMonth.strftime("%Y-%m")

    @staticmethod
    def split_dates(start_date, end_date, piece_length, date_format="%Y-%m-%d"):
        import datetime

        hanlding_type = None
        if isinstance(start_date, str) and isinstance(end_date, str):
            hanlding_type = DateUtil.HandlingDateType.raw_string
            start_date = datetime.datetime.strptime(start_date, date_format).date()
            end_date = datetime.datetime.strptime(end_date, date_format).date()
        elif isinstance(start_date, datetime.date) and isinstance(end_date, datetime.date):
            hanlding_type = DateUtil.HandlingDateType.raw_date

        if not (hanlding_type and end_date > start_date and isinstance(piece_length, int) and piece_length >= 1):
            raise ValueError("Parameters Error")

        nums = (end_date - start_date).days
        step = piece_length
        pieces_of_dates = [(start_date + datetime.timedelta(days=x), start_date + datetime.timedelta(days=(x + step - 1) if x + step - 1 < nums else nums))
                           for x in range(0, nums + 1, step)]
        if hanlding_type is DateUtil.HandlingDateType.raw_date:
            return pieces_of_dates
        elif hanlding_type is DateUtil.HandlingDateType.raw_string:
            return [(e[0].strftime("%Y-%m-%d"), e[1].strftime("%Y-%m-%d")) for e in pieces_of_dates]


def main():
    print(DateUtil.get_first_day_of_month('2014-3-4', delta_of_year=-1, delta_of_month=-1))

    print(DateUtil.get_last_month_str())

    print(DateUtil.split_dates("2016-01-01", "2016-05-8", 50))

    import datetime
    date_format = "%Y%m%d"
    start_date = datetime.datetime.strptime("20160101", date_format)
    end_date = datetime.datetime.strptime("20160508", date_format)
    print(DateUtil.split_dates(start_date, end_date, 50, date_format))


if __name__ == '__main__':
    main()
