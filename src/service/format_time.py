from datetime import datetime

def format_timestamp(timestamp):
    """Format a timestamp to a formatted datetime string."""
    seconds = int(timestamp / 1000.0)
    datetime_obj = datetime.utcfromtimestamp(seconds)
    formatted_datetime = datetime_obj.strftime('%Y-%m-%d %H:%M:%S.%f')
    return formatted_datetime
