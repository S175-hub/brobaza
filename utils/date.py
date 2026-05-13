from datetime import datetime, timedelta

RUS_MONTHS = {
    1: 'января',
    2: 'февраля',
    3: 'марта',
    4: 'апреля',
    5: 'мая',
    6: 'июня',
    7: 'июля',
    8: 'августа',
    9: 'сентября',
    10: 'октября',
    11: 'ноября',
    12: 'декабря'
}


def format_time(dt):
    return dt.strftime('%H:%M')


def format_date(dt):
    day = dt.day
    month = RUS_MONTHS[dt.month]
    return f'{day} {month}'


def time_ago(dt):
    now = datetime.utcnow()
    diff = now - dt

    seconds = diff.total_seconds()
    if seconds < 10:
        return 'только что'
    if seconds < 60:
        return f'{int(seconds)} сек назад'
    if seconds < 3600:
        return f'{int(seconds // 60)} мин назад'

    today = now.date()
    dt_date = dt.date()
    yesterday = today - timedelta(days=1)
    if dt_date == today:
        return f'сегодня в {format_time(dt)}'
    if dt_date == yesterday:
        return f'вчера в {format_time(dt)}'
    if dt.year == now.year:
        return f'{format_date(dt)} в {format_time(dt)}'

    return f'{format_date(dt)} {dt.year} в {format_time(dt)}'


def register_date(dt):
    day = dt.day
    month = RUS_MONTHS[dt.month]
    year = dt.year
    return f'{day} {month} {year}'
