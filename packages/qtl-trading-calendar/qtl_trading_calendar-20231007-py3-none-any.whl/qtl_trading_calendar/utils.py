from datetime import date


def is_weekend(d: date):
    weekday = d.weekday()
    #  Saturday, Sunday
    if weekday in (5, 6):
        return True
    return False

