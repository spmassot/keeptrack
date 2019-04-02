def format_datetime(value):
    if value:
        return value.strftime('%Y-%m-%d')
    else:
        return value


CUSTOM_FILTERS = dict(
    format_datetime=format_datetime
)
