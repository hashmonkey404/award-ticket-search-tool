from datetime import datetime, timedelta


def date_range(start_date, future_date) -> list:
    """Generate a list of dates between start_date and end_date"""
    date_list = []
    start_dt = start_date
    end_dt = future_date
    delta = (end_dt - start_dt).days
    for i in range(delta + 1):
        d = start_dt + timedelta(days=i) # A duration expressing the time difference to microsecond resolution.
        date_list.append(d.strftime('%Y-%m-%d')) # .strftime() Return a string representing the date, controlled by an explicit format string.
    return date_list


def convert_miles(miles: int) -> str:
    return str(miles / 1000) + 'k pts'


def convert_duration(seconds: int) -> str:
    hour = int(seconds / 3600)
    min = int(seconds % 3600 / 60)
    return '{}h{:02d}m'.format(hour, min)


def convert_datetime(origin_str: str, with_date: bool) -> str:
    if 'Z' in origin_str:
        origin_str = origin_str[:-1]
    r1 = datetime.fromisoformat(origin_str)
    return r1.strftime('%a %Y-%m-%d %H:%M') if with_date is True else r1.strftime('%H:%M')


def convert_cash(cash: int) -> str:
    return 'C$' + '{:.2f}'.format(cash / 100)


def convert_mix(availabilityDetails) -> str:
    cabin_dict = {
        'business': 'J',
        'eco': 'Y',
        'ecoPremium': 'PY',
        'first': 'F'
    }
    return "\n".join(["{:.2f}".format(x['mileagePercentage']) + '% ' + cabin_dict[x['cabin']] for x in availabilityDetails])

