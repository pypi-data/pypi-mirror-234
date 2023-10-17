"""量化交易时间计时器"""


import time
import datetime
import contextlib
from typing import Any, Callable, List
from vxutils import logger, convertors

__all__ = ["vxtime"]


class vxtime:
    """量化交易时间机器"""

    _timefunc = time.time
    _delayfunc = time.sleep
    __holidays__ = set()

    @classmethod
    def now(cls, fmt: str = None) -> float:
        """当前时间

        Keyword Arguments:
            fmt {str} -- 时间格式 (default: {None}, 返回时间戳)

        Returns:
            _type_ -- _description_

        """
        if fmt and fmt.lower() in {"datetime", "dt"}:
            return datetime.datetime.now()

        now_timestamp = cls._timefunc()

        return (
            time.strftime(fmt, time.localtime(now_timestamp)) if fmt else now_timestamp
        )

    @classmethod
    def sleep(
        cls,
        seconds: float = 0,
        minutes: float = 0,
        hours: float = 0,
        weeks: float = 0,
        days: float = 0,
    ) -> None:
        """延时等待函数"""
        sleep_time = datetime.timedelta(
            seconds=seconds, minutes=minutes, hours=hours, weeks=weeks, days=days
        ).total_seconds()
        cls._delayfunc(sleep_time)

    @classmethod
    @contextlib.contextmanager
    def timeit(cls, prefix: str = None) -> None:
        """计时器"""
        start = time.perf_counter()
        if prefix is None:
            prefix = "default timer"
        try:
            yield
        finally:
            cost_str = f"{prefix} use time: {(time.perf_counter() - start)*1000:,.2f}"
            logger.warning(cost_str)

    @classmethod
    def is_holiday(cls, date_: Any = None) -> bool:
        """是否假日"""
        date_ = convertors.to_datetime(date_ or cls.now()).date()
        return True if date_.weekday in [0, 1] else date_ in cls.__holidays__

    @classmethod
    def set_timefunc(cls, timefunc: Callable) -> None:
        """设置timefunc函数"""
        if not callable(timefunc):
            raise ValueError(f"{timefunc} is not callable.")
        cls._timefunc = timefunc

    @classmethod
    def set_delayfunc(cls, delayfunc: Callable) -> None:
        """设置delayfunc函数"""
        if not callable(delayfunc):
            raise ValueError(f"{delayfunc} is not callable.")
        cls._delayfunc = delayfunc

    @classmethod
    def today(cls, time_str: str = "00:00:00") -> float:
        """今天 hh:mm:ss 对应的时间"""
        date_str = cls.now("%Y-%m-%d")
        return convertors.combine_datetime(date_str, time_str)

    @classmethod
    def date_range(
        cls,
        start_date: str = None,
        end_date: str = None,
        interval: int = 1,
        skip_holidays=False,
    ) -> List:
        """生成时间序列

        Arguments:
            start_date {str} -- 起始日期,默认值: None,即:2005-01-01
            end_date {str} -- 终止日期,默认值: None, 即: 当天
            interval {int} -- 间隔时间 默认值: 1天
            skip_holidays (bool) -- 是否跳过假期

        Returns:
            List -- 时间序列
        """
        start_date = (
            convertors.to_datetime(start_date)
            if start_date
            else convertors.to_datetime("2005-01-01")
        ).date()

        end_date = (
            convertors.to_datetime(end_date)
            if end_date
            else convertors.to_datetime(cls.today()).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        ).date()

        if start_date > end_date:
            raise ValueError(
                f"start_date({start_date}) must larger then end_date({end_date})."
            )

        delta = datetime.timedelta(days=1)
        result = []
        date = start_date
        while date <= end_date:
            if not (skip_holidays and date in cls.__holidays__):
                result.append(date)
            date += delta

        return result[::interval]

    @classmethod
    def add_holidays(cls, *holidays: List):
        """增加假期时间"""
        if len(holidays) == 1 and isinstance(holidays[0], list):
            holidays = holidays[0]
        cls.__holidays__.update(
            map(lambda d: convertors.to_datetime(d).date(), holidays)
        )

    @classmethod
    def add_businessdays(cls, *businessdays: List) -> None:
        """添加工作日"""
        if not businessdays:
            return
        if len(businessdays) == 1 and isinstance(businessdays[0], (list, tuple)):
            businessdays = businessdays[0]

        businessdays = sorted(
            map(lambda x: convertors.to_datetime(x).date(), businessdays)
        )
        start_date = businessdays[0]
        end_date = businessdays[-1]
        business_dates = cls.date_range(start_date, end_date, skip_holidays=False)
        holidays = set(business_dates) - set(businessdays)
        cls.__holidays__ = cls.__holidays__ - set(businessdays)
        cls.__holidays__.update(holidays)


if __name__ == "__main__":
    print(vxtime.now("%Y-%m-%d %H:%M:%S"))
