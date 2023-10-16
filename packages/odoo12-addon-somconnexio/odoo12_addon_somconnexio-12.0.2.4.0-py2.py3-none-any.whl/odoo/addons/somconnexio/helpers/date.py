import datetime


def first_day_next_month():
    return (datetime.date.today().replace(day=1) + datetime.timedelta(days=32)).replace(
        day=1
    )


def date_to_str(date):
    return date.strftime("%Y-%m-%d")
