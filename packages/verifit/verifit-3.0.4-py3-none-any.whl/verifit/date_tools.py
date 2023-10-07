def date_subtract_in_minutes(from_date=None, date_to_subtract=None):
    difference = from_date - date_to_subtract
    minutes = difference.seconds // 60
    if difference.days < 0:
        minutes = minutes + difference.days * 24 * 60
    return minutes
