import calendar
import datetime

def add_months_to_now(months):
    today = datetime.datetime.now(tz=None)
    month = today.month - 1 + months
    year = today.year + month // 12
    month = month % 12 + 1
    day = min(today.day, calendar.monthrange(year, month)[1])
    return datetime.datetime(year, month, day, hour=today.hour, minute=today.minute, second=today.second)