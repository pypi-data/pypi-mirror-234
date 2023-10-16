from datetime import datetime


def unixtime_to_date(unixtime: int):
    return datetime.utcfromtimestamp(unixtime).strftime('%Y-%m-%d')
