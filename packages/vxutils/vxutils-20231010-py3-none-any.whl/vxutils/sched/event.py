"""消息类型"""

from heapq import heappush, heappop
from enum import Enum
from queue import Queue, Empty
from typing import Any
from vxutils.database.fields import (
    vxIntField,
    vxDatetimeField,
    vxFloatField,
    vxUUIDField,
    vxBoolField,
    vxPropertyField,
    vxStringField,
    DBTypes,
)
from datetime import timedelta
from vxutils import logger
from vxutils.time import vxtime
from vxutils.convertors import combine_datetime, to_timestring, to_timestamp
from vxutils.database.dataclass import vxDataClass


__all__ = ["vxEvent", "vxEventQueue", "vxTrigger", "TriggerStatus"]


class TriggerStatus(Enum):
    """触发器状态

    Pending : 未开始
    Running : 已开始
    Completed: 已完成
    """

    #  未开始
    Pending = 1
    #  已开始
    Running = 2
    #  已完成
    Completed = 3


def _trigger_status(trigger):
    if trigger.next() is None:
        return TriggerStatus.Completed
    elif trigger.trigger_dt is None:
        return TriggerStatus.Pending
    return TriggerStatus.Running


def _get_trigger_dt(trigger):
    return trigger._data.get("trigger_dt", None)


class vxTrigger(vxDataClass):
    __sortkeys__ = ("trigger_dt",)

    # 触发时间
    # trigger_dt = vxDatetimeField("触发事件")
    trigger_dt = vxPropertyField(
        "触发时间",
        fgetter=_get_trigger_dt,
        converter=lambda obj, value: to_timestamp(value) if value else None,
        formatter=lambda value: to_timestring(value) if value else None,
    )
    # 间隔 (单位：秒)
    interval = vxFloatField(
        "间隔(单位：秒)",
        default=1,
        ndigits=3,
        lower_bound=0.001,
        formatter=lambda value: timedelta(seconds=value),
    )
    # 是否跳过假期
    skip_holiday = vxBoolField("是否跳过假期", default=True)
    # 触发器状态
    status = vxPropertyField("触发器状态", fgetter=_trigger_status)
    # 开始时间
    start_dt = vxDatetimeField("起始时间")
    # 结束时间
    end_dt = vxDatetimeField("结束时间", default=float("inf"))

    def next(self):
        """获取下一个触发时间"""

        if self.trigger_dt is None or self.trigger_dt < self.start_dt:
            now = vxtime.now()
            trigger_dt = self.start_dt

            if now > self.end_dt:
                return None

            if now > self.start_dt:
                trigger_dt = (
                    self.start_dt
                    + (now - self.start_dt) // self.interval * self.interval
                    + self.interval
                )
        else:
            trigger_dt = self.trigger_dt + self.interval

        while (
            self.skip_holiday
            and trigger_dt <= self.end_dt
            and vxtime.is_holiday(trigger_dt)
        ):
            trigger_dt = (
                trigger_dt
                + (combine_datetime(trigger_dt, "23:59:59") - trigger_dt)
                // self.interval
                * self.interval
                + self.interval
            )

        return trigger_dt if trigger_dt <= self.end_dt else None

    def __iter__(self):
        return self

    def __next__(self) -> float:
        if self.next() is not None:
            self.trigger_dt = self.next()
            return self.trigger_dt

        raise StopIteration

    @staticmethod
    def once(trigger_dt):
        """创建一个一次性触发器"""
        return vxTrigger(
            start_dt=trigger_dt, end_dt=trigger_dt, interval=1, skip_holiday=False
        )

    @staticmethod
    def daily(run_time="00:00:00", freq=1, end_dt=None, skip_holiday=False):
        """创建一个每日触发器"""
        start_dt = vxtime.today(run_time)
        if start_dt < vxtime.now():
            start_dt += 24 * 60 * 60

        return vxTrigger(
            start_dt=start_dt,
            end_dt=end_dt,
            interval=int(freq) * 24 * 60 * 60,
            skip_holiday=skip_holiday,
        )

    @staticmethod
    def every(interval=1, start_dt=None, end_dt=None, skip_holiday=False):
        """创建一个固定间隔触发器"""
        return vxTrigger(
            start_dt=start_dt,
            end_dt=end_dt,
            interval=interval,
            skip_holiday=skip_holiday,
        )


class vxEvent(vxDataClass):
    """消息类型"""

    __sortkeys__ = ("trigger_dt", "priority")

    # 消息id
    id: str = vxUUIDField("消息id", prefix="event", auto=True)
    # 消息通道
    channel: str = vxStringField("消息通道", default="")
    # 消息类型
    type: str = vxStringField("消息类型", default="")
    # 消息内容
    data: Any = vxPropertyField("消息数据", dbtyupe=DBTypes.BOOLEAN)
    # 定时触发器
    trigger: vxTrigger = vxPropertyField("定期触发器", dbtyupe=DBTypes.DATETIME)
    # 触发时间
    trigger_dt: float = vxDatetimeField("触发时间")
    # 优先级
    priority: int = vxIntField("优先级", default=10)
    # rpc消息回复地址
    reply_to: str = vxStringField("rpc 消息回复地址")


class vxEventQueue(Queue):
    def _init(self, maxsize=0):
        self.queue = []
        self._event_ids = set()

    def _qsize(self):
        now = vxtime.now()
        return len([event for event in self.queue if event.trigger_dt <= now])

    def _put(self, event):
        if isinstance(event, str):
            event = vxEvent(type=event)
        elif not isinstance(event, vxEvent):
            raise ValueError(f"Not support type(event) : {type(event)}.")

        if event.id in self._event_ids:
            raise ValueError(f"event({event.id})重复入库. {event}")

        if event.trigger:
            if event.trigger.status.name == "Pending":
                event.trigger_dt = next(event.trigger, vxtime.now())
            elif event.trigger.status.name == "Completed":
                logger.warning("忽略已经完成的event。 %s", event)
                return

        heappush(self.queue, event)
        self._event_ids.add(event.id)

    def get(self, block=True, timeout=None):
        with self.not_empty:
            if not block:
                if not self._qsize():
                    raise Empty
            elif timeout is None:
                while not self._qsize():
                    remaining = 10
                    if len(self.queue) > 0:
                        remaining = self.queue[0].trigger_dt - vxtime.now()

                    if remaining > 0:
                        self.not_empty.wait(remaining)

            elif timeout < 0:
                raise ValueError("'timeout' must be a non-negative number")
            else:
                endtime = vxtime.now() + timeout
                while not self._qsize():
                    if len(self.queue) > 0:
                        min_endtime = min(endtime, self.queue[0].trigger_dt)
                    else:
                        min_endtime = endtime

                    remaining = min(min_endtime - vxtime.now(), 1)

                    if remaining <= 0.0:
                        raise Empty
                    self.not_empty.wait(remaining)
            event = self._get()
            self.not_full.notify()
            return event

    def _get(self):
        event = heappop(self.queue)
        # 获取的event都将trigger给去掉，以免trigger在其他地方再进行传递
        if not event.trigger or event.trigger.status.name == "Completed":
            self.unfinished_tasks -= 1
            self._event_ids.remove(event.id)
            event.trigger = ""
            return event

        reply_event = vxEvent(**event.message)
        reply_event.trigger = ""

        event.trigger_dt = next(event.trigger, None)
        heappush(self.queue, event)
        self.not_empty.notify()
        return reply_event


if __name__ == "__main__":
    from datetime import timedelta

    logger.info(timedelta(seconds=300))
    t1 = vxTrigger.daily(end_dt=vxtime.now() + 60 * 60 * 24 * 3)
    # t1 = vxTrigger.every(3, vxtime.now(), vxtime.now() + 60, True)
    logger.info(t1)
    for t in t1:
        logger.debug(t)
    logger.warning(t1)
    t = vxTrigger(**t1.message)
    logger.error(t.message)

    e1 = vxEvent(type="test", channel="channel1", data="data2", trigger=t)
    logger.critical(e1)
    logger.critical(e1.message)
