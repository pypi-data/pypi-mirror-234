import datetime

from dateutil.relativedelta import relativedelta


def date_time_add(date_time: datetime.datetime, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0,
                  months: int = 0, years: int = 0, is_format=False, template="%Y-%m-%d %H:%M:%S"):
    """
        时间偏移，可以正向偏移或者负向偏移，值大于0为正向偏移，值小于0为负向偏移
    :param date_time: 时间格式的时间
    :param seconds: 秒数
    :param minutes: 分钟数
    :param hours: 小时数
    :param days: 天数
    :param months: 月数
    :param years: 年数
    :param is_format: 是否格式化时间
    :param template: 格式时间模版
    :return:
    """
    date_time = date_time + datetime.timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days)
    date_time = date_time + relativedelta(months=months)
    date_time = datetime.datetime(year=date_time.year + years, month=date_time.month, day=date_time.day,
                                  hour=date_time.hour,
                                  minute=date_time.minute, second=date_time.second)
    if is_format:
        date_str = date_time.strftime(template)
        return date_str
    else:
        return date_time


def date_time_diff(date_time1: datetime.datetime, date_time2: datetime.datetime, return_type: str = None,
                   digits: int = None):
    """
        时间差计算
    :param date_time1: 时间格式的时间
    :param date_time2: 时间格式的时间
    :param return_type: 不同单位的时间差的单位
    :param digits: 保留几位小数
    :return:
    """
    if date_time1 > date_time2:
        date_time1, date_time2 = date_time2, date_time1
    if return_type == "seconds":
        diff = date_time2 - date_time1
        return round(diff.total_seconds(), digits)
    elif return_type == "minutes":
        diff = date_time2 - date_time1
        return round(diff.total_seconds() / 60.0, digits)
    elif return_type == "hours":
        diff = date_time2 - date_time1
        return round(diff.total_seconds() / 3600.0, digits)
    elif return_type == "days":
        diff = date_time2 - date_time1
        return round(diff.total_seconds() / (3600.0 * 24), digits)
    elif return_type == "weeks":
        diff = date_time2 - date_time1
        return round(diff.total_seconds() / (3600.0 * 24 * 7), digits)
    elif return_type == "months":
        return round((date_time2.year - date_time1.year) * 12 + (date_time2.month - date_time1.month), digits)
    elif return_type == "years":
        return round(((date_time2.year - date_time1.year) * 12 + (date_time2.month - date_time1.month)) / 12.0,
                     digits)
    else:
        diff = date_time2 - date_time1
        return diff
