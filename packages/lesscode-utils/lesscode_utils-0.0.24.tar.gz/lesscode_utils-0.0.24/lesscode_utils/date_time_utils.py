import math
import time
from datetime import datetime, timedelta, date
from typing import Union

from dateutil.relativedelta import relativedelta

from lesscode_utils.common_utils import fill


def date_time_add(date_time: datetime, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0,
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
    date_time = date_time + timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days)
    date_time = date_time + relativedelta(months=months)
    date_time = datetime(year=date_time.year + years, month=date_time.month, day=date_time.day,
                         hour=date_time.hour,
                         minute=date_time.minute, second=date_time.second)
    if is_format:
        date_str = date_time.strftime(template)
        return date_str
    else:
        return date_time


def date_time_diff(date_time1: datetime, date_time2: datetime, return_type: str = None,
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
        return round(((date_time2.year - date_time1.year) + (date_time2.month - date_time1.month)) / 12.0,
                     digits)
    else:
        diff = date_time2 - date_time1
        return diff


def get_time_year(time: Union[date, datetime]):
    return time.year


def get_time_month(time: Union[date, datetime]):
    month_str = fill(time.month, 2, '0', position="font")
    return {"year": time.year, "month": time.month, "month_str": month_str, "full_month": f"{time.year}-{month_str}"}


def get_time_days(time: Union[date, datetime]):
    start_date = date(time.year - 1, 12, 31)
    end_date = time.date() if isinstance(time, datetime) else time
    return (end_date - start_date).days


def get_time_week(time: Union[date, datetime]):
    week = math.ceil(get_time_days(time) / 7)
    return {"year": time.year, "month": time.month, "day": time.day, "days": get_time_days(time),
            "week": week, "full_week": f'{time.year}-{week}'}


def get_time_quarter(time: Union[date, datetime]):
    month = time.month
    quarter = math.ceil(month / 3)
    return {"year": time.year, "month": month, "quarter": quarter, "quarter_str": f"Q{quarter}",
            "full_quarter": f"{time.year}-Q{quarter}"}


def gen_date_series(start_time: Union[date, datetime], end_time: Union[date, datetime], series_type: str = "year"):
    if series_type == "year":
        return [str(_) for _ in range(start_time.year, end_time.year + 1)]
    elif series_type == "month":
        months = []
        start_month_dict = get_time_month(start_time)
        start_year = start_month_dict.get("year")
        start_month = start_month_dict.get("month")
        end_month_dict = get_time_month(end_time)
        end_year = end_month_dict.get("year")
        end_month = end_month_dict.get("month")
        for year in range(start_year, end_year + 1):
            if year == start_year:
                for month in range(start_month, 12 + 1):
                    month_str = fill(month, 2, '0', position="font")
                    months.append(f"{year}-{month_str}")
            elif year == end_year:
                for month in range(1, end_month + 1):
                    month_str = fill(month, 2, '0', position="font")
                    months.append(f"{year}-{month_str}")
            else:
                for month in range(1, 13):
                    month_str = fill(month, 2, '0', position="font")
                    months.append(f"{year}-{month_str}")
        return months
    elif series_type == "week":
        weeks = []
        start_week_dict = get_time_week(start_time)
        end_week_dict = get_time_week(end_time)
        start_year = start_week_dict.get("year")
        end_year = end_week_dict.get("year")
        start_week = start_week_dict.get("week")
        end_week = end_week_dict.get("week")
        for year in range(start_year, end_year + 1):
            if year == start_year:
                for week in range(start_week, 54):
                    weeks.append(f"{year}-{week}")
            elif year == end_year:
                for week in range(1, end_week + 1):
                    weeks.append(f"{year}-{week}")
            else:
                for week in range(1, 54):
                    weeks.append(f"{year}-{week}")
        return weeks
    elif series_type == "quarter":
        quarters = []
        start_year = start_time.year
        start_month = start_time.month
        start_quarter = math.ceil(start_month / 3)
        end_year = end_time.year
        end_month = end_time.month
        end_quarter = math.ceil(end_month / 3)
        for year in range(start_year, end_year + 1):
            if year == start_year:
                for quarter in range(start_quarter, 5):
                    quarters.append(f"{year}-Q{quarter}")
            elif year == end_year:
                for quarter in range(1, end_quarter + 1):
                    quarters.append(f"{year}-Q{quarter}")
            else:
                for quarter in range(1, 5):
                    quarters.append(f"{year}-Q{quarter}")
        return quarters
    else:
        raise Exception(f"series_type={series_type} is not supported")
