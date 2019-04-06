def format_datetime(value):
    if value:
        return value.strftime('%Y-%m-%d')
    else:
        return ""


def format_bool(value):
    if value is None:
        return False
    return value


CUSTOM_FILTERS = dict(
    format_datetime=format_datetime,
    format_bool=format_bool
)
