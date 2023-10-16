from datetime import date, datetime


def normalize_date(yyyymmdd):
    if isinstance(yyyymmdd, str):
        year, month, day = int(yyyymmdd[:4]), int(yyyymmdd[4:6]), int(yyyymmdd[6:])
    else:
        year, month, day = yyyymmdd.year, yyyymmdd.month, yyyymmdd.day
    return date(year, month, day)


def normalize_iso_datetime(d):
    if isinstance(d, str):
        return datetime.fromisoformat(d)
    else:
        return d
