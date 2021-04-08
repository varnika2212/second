from datetime import datetime


def validate(date_text):
    try:
        datetime.strptime(date_text,'%Y-%m-%dT%H:%M:%S%z')
    except ValueError:
        return False
    return True
