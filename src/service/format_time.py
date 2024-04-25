from datetime import datetime

def convert_timestamp_to_datetime(timestamp):
    timestamp_seconds = int(timestamp / 1000.0)
    datetime_object = datetime.utcfromtimestamp(timestamp_seconds)
    formatted_datetime = datetime_object.strftime('%Y-%m-%d %H:%M:%S.%f')
    return formatted_datetime
