# any generic utilities

from datetime import datetime


def get_timestamp(date):
    dt_obj = datetime.strptime(date, '%d.%m.%Y')
    return int(dt_obj.timestamp())


def get_metric_name_by_input(num: int):
    switcher = {
        1: 'Subjectivity',
        2: 'FollowUps',
        3: 'Polarity',
        4: 'Popularity',
        5: 'Promotion'
    }
    return switcher.get(num, "Wrong metric number")
