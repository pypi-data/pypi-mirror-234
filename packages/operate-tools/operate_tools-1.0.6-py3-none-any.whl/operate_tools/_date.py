# -*- coding: utf-8 -*-
# @Time: 2022/07/11 17:37:35
# @File: _date.py
# @Desc：日期操作

__all__ = ["DateTools"]

from datetime import datetime, timedelta, date

_en_week = {1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat", 7: "Sun"}
_zh_week = {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "日"}
_week_dict = {"zh": _zh_week, "en": _en_week}


class DateTools:

    # ----------- now -----------
    @staticmethod
    def now(fmt='%Y-%m-%d') -> str:
        """
        获取当前日期
        :param fmt: 日期格式
        :return: 格式化后的日期
        """
        now = datetime.now()
        return now.strftime(fmt)

    @staticmethod
    def timestamp():
        """
        获取当前时间戳
        :return:
        """
        return datetime.now().timestamp()

    @staticmethod
    def days_before(days=31, fmt="%Y-%m-%d") -> str:
        """
        获取前几天的日期
        :param days: 前n天. Defaults to 31.
        :param fmt: 日期格式. Defaults to "%Y-%m-%d".
        :return: 格式化后的日期
        """
        time_data = datetime.now() - timedelta(days=days)
        return time_data.strftime(fmt)

    @staticmethod
    def days_after(days=31, fmt="%Y-%m-%d") -> str:
        """
        获取后几天的日期
        :param days: 后n天. Defaults to 31.
        :param fmt: 日期格式. Defaults to "%Y-%m-%d".
        :return: 格式化后的日期
        """
        time_data = datetime.now() + timedelta(days=days)
        return time_data.strftime(fmt)

    @staticmethod
    def yesterday(fmt="%Y-%m-%d") -> str:
        """
        获取昨天的日期
        :param fmt: 日期格式. Defaults to "%Y-%m-%d".
        :return: 格式化后的日期
        """
        return DateTools.days_before(days=1, fmt=fmt)

    @staticmethod
    def tomorrow(fmt="%Y-%m-%d") -> str:
        """
        获取明天的日期
        :param fmt: 日期格式. Defaults to "%Y-%m-%d".
        :return: 格式化后的日期
        """
        return DateTools.days_after(days=1, fmt=fmt)

    @staticmethod
    def last_week(fmt="%Y-%m-%d") -> str:
        """
        获取上周前的日期
        :param fmt: 日期格式. Defaults to "%Y-%m-%d".
        :return: 格式化后的日期
        """
        return DateTools.days_before(days=7, fmt=fmt)

    @staticmethod
    def next_week(fmt="%Y-%m-%d") -> str:
        """
        获取下周的日期
        :param fmt: 日期格式. Defaults to "%Y-%m-%d".
        :return: 格式化后的日期
        """
        return DateTools.days_after(days=7, fmt=fmt)

    @staticmethod
    def last_month(fmt="%Y-%m-%d") -> str:
        """
        获取上个月的日期
        :param fmt: 日期格式. Defaults to "%Y-%m-%d".
        :return: 格式化后的日期
        """
        today = date.today()
        last_month = today.replace(month=today.month - 1)
        return last_month.strftime(fmt)

    @staticmethod
    def next_month(fmt="%Y-%m-%d") -> str:
        """
        获取下个月的日期
        :param fmt: 日期格式. Defaults to "%Y-%m-%d".
        :return: 格式化后的日期
        """
        today = date.today()
        next_month = today.replace(month=today.month + 1)
        return next_month.strftime(fmt)

    @staticmethod
    def every_day(begin_date: str, end_date: str, fmt="%Y-%m-%d") -> list:
        """
        获取开始到结束日期的每一天日期
        :param begin_date: 开始日期
        :param end_date: 结束日期
        :param fmt: 输入的日期格式. Defaults to "%Y-%m-%d".
        :return: 日期列表
        """
        date_list = []
        begin_date = datetime.strptime(begin_date, fmt)
        end_date = datetime.strptime(end_date, fmt)
        while begin_date <= end_date:
            date_str = begin_date.strftime(fmt)
            date_list.append(date_str)
            begin_date += timedelta(days=1)
        return date_list

    @staticmethod
    def time_difference(start_time: str, end_time: str) -> timedelta:
        """
        计算时间差
        :param start_time: 开始时间（e:2022-03-17 16:15:38）
        :param end_time: 结束时间（e:2022-03-17 16:15:40）
        :return: 时间间隔对象（e:0:00:02）
        """
        t1 = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        t2 = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        return t2 - t1

    @staticmethod
    def is_within_time_range(start="00:00", end="09:00") -> bool:
        """
        判断当前时间是否在指定时间范围内
        :param start: 起始时间. Defaults to "00:00".
        :param end: 终止时间. Defaults to "09:00".
        :return: bool: 结果
        """
        now_date = str(datetime.now().date())
        start_time = datetime.strptime(now_date + start, '%Y-%m-%d%H:%M')
        end_time = datetime.strptime(now_date + end, '%Y-%m-%d%H:%M')
        now_time = datetime.now()
        if all([now_time > start_time, now_time < end_time]):
            return True
        else:
            return False

    @staticmethod
    def timestamp_to_time(time_stamp: str, unit="s" or "ms", fmt="%Y-%m-%d %H:%M:%S") -> str:
        """
        时间戳转时间
        :param time_stamp: 时间戳
        :param unit: 单位. Defaults to "s"or"ms".
        :param fmt: 日期时间格式. Defaults to "%Y-%m-%d %H:%M:%S".
        :return: 转换的日期时间
        :raises ValueError: 单位输入错误异常
        """
        if unit == "ms":
            time_stamp = float(time_stamp) / 1000
        elif unit == "s":
            time_stamp = float(time_stamp)
        else:
            raise ValueError(
                "time_stamp's unit input error, unit value in ['s', 'ms']")
        t = datetime.fromtimestamp(time_stamp)
        return t.strftime(fmt)

    @staticmethod
    def now_week(lang='zh') -> str:
        """
        获取当前星期
        :param lang: 语言. Defaults Number. ['zh', 'en']
        :return:
        """
        return DateTools.week(DateTools.now(), lang=lang)

    @staticmethod
    def week(date: str, lang='zh') -> str:
        """
        获取某一日期的星期
        :param date: 日期
        :param lang: 语言. Defaults Number. ['zh', 'en']
        :return:
        """
        try:
            return _week_dict[lang][datetime.strptime(date, "%Y-%m-%d").isoweekday()]
        except KeyError as _:
            raise KeyError("lang value in ['zh', 'en']")

    @staticmethod
    def isleap(year: int) -> bool:
        """
        判断是否为闰年
        :param year: 年份
        :return: bool
        """
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
