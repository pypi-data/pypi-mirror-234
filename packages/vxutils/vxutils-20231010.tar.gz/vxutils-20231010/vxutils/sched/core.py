"""vxsched调度器 """

import contextlib
import importlib
import os
import time
from types import MappingProxyType
from collections import defaultdict, namedtuple
from collections.abc import MutableMapping, Mapping
from multiprocessing.dummy import Lock
from concurrent.futures import ThreadPoolExecutor as Executor, Future, as_completed
from pathlib import Path
from queue import Empty
from typing import Any, Callable, Union, Dict
from vxutils.sched.context import vxContext
from vxutils.sched.event import vxEvent, vxEventQueue, vxTrigger
from vxutils import logger, vxtime


__all__ = ["vxScheduler", "vxsched", "vxTask"]

_default_context = {}
ON_INIT_EVENT = "__init__"
ON_REPLY_EVENT = "__reply__"
ON_TASK_COMPLETE_EVENT = "__task_complete__"
ON_EXIT_EVENT = "__exit__"

vxTask = namedtuple("vxTask", ["handler", "time_limit", "lock"])


class vxScheduler:
    def __init__(self, workers: int = None, executor: Executor = None) -> None:
        if executor is None:
            executor = Executor(max_workers=workers)

        self._executor = executor
        self._tasks = defaultdict(set)
        self._queue = vxEventQueue()
        self._context = vxContext(_default_context)
        self._is_active = False

    @property
    def context(self) -> vxContext:
        """调度器上下文"""
        return self._context

    def set_context(self, context: Union[vxContext, MutableMapping, Mapping]):
        """设置调度器上下文"""
        self._context = context if context else vxContext()

    def is_active(self):
        """调度器是否在运行"""
        return self._is_active

    def add_task(
        self,
        event_type: vxEvent,
        handler: Callable,
        time_limit: float = 1.0,
        lock: Lock = None,
    ):
        """添加调度任务"""
        for task in self._tasks[event_type]:
            if task.handler == handler:
                logger.warning("任务 %s 已存在", handler)
                return

        task = vxTask(handler, time_limit, lock)
        self._tasks[event_type].add(task)
        logger.info("事件(%s) 添加任务 %s", event_type, handler)

    def remove_task(self, event_type: vxEvent, handler: Callable):
        """删除调度任务"""
        for task in self._tasks[event_type]:
            if task.handler == handler:
                self._tasks[event_type].remove(task)
                logger.info("删除任务 %s", handler)
                break

    def get_tasks(self):
        """获取调度任务列表"""
        return MappingProxyType(self._tasks)

    def run_task(self, task: vxTask, event: vxEvent):
        """运行任务"""
        start_time = time.perf_counter()
        try:
            if task.lock:
                task.lock.acquire()

            ret = task.handler(self.context, event)
            if (
                event.type not in (ON_TASK_COMPLETE_EVENT, ON_REPLY_EVENT)
                and event.reply_to
                and self._tasks[ON_REPLY_EVENT]
            ):
                self.trigger_event(ON_REPLY_EVENT, data=(task, event, ret))
            return ret

        finally:
            if task.lock:
                task.lock.release()

            cost_time = time.perf_counter() - start_time
            if cost_time > task.time_limit:
                logger.warning(
                    "%s 运行时间 %.2f ms> %.2f ms.  触发消息: %s, data: %s",
                    task.handler,
                    cost_time * 1000,
                    task.time_limit * 1000,
                    event.type,
                    event.data,
                )

            if (
                event.type not in (ON_TASK_COMPLETE_EVENT, ON_REPLY_EVENT)
                and self._tasks[ON_TASK_COMPLETE_EVENT]
            ):
                self.trigger_event(
                    ON_TASK_COMPLETE_EVENT, data=(task, event, cost_time)
                )

    def trigger_event(
        self,
        event: Union[vxEvent, str] = None,
        data: Any = None,
        trigger: vxTrigger = None,
        priority: int = 0,
        **kwargs,
    ):
        """触发事件"""
        events = {}
        if isinstance(event, str):
            t_event = vxEvent(
                type=event,
                data=data,
                trigger=trigger,
                priority=priority,
                **kwargs,
            )
            events[t_event.id] = t_event

        elif isinstance(event, vxEvent):
            t_event = event
            events[t_event.id] = t_event

        while not self._queue.empty():
            with contextlib.suppress(Empty):
                t_event = self._queue.get_nowait()
                events[t_event.id] = t_event

        fus = []
        for t_event in events.values():
            for task in self._tasks[t_event.type]:
                fu = self._executor.submit(self.run_task, task, t_event)
                fu.add_done_callback(self._handle_callback)
                fus.append(fu)

        return list(as_completed(fus))

    def submit_event(
        self,
        event: Union[vxEvent, str],
        data: Any = None,
        trigger: vxTrigger = None,
        priority: int = 0,
        **kwargs,
    ):
        """提交一个消息"""

        if isinstance(event, str):
            send_event = vxEvent(
                type=event,
                data=data,
                trigger=trigger,
                priority=priority,
                **kwargs,
            )

        elif isinstance(event, vxEvent):
            send_event = event
        else:
            raise ValueError(f"{self} event 类型{type(event)}错误，请检查: {event}")

        logger.debug("提交消息: %s", send_event)
        self._queue.put_nowait(send_event)

    def run(self):
        """运行调度器"""
        if self._is_active:
            logger.warning("调度器已经在运行")
            return

        self._is_active = True
        logger.info("vxSched(id=%s) 执行初始化", id(self))
        self.trigger_event(ON_INIT_EVENT)
        logger.info("vxSched(id=%s) 调度器启动....", id(self))
        try:
            while self.is_active():
                with contextlib.suppress(Empty):
                    event = self._queue.get(timeout=1)
                    for task in self._tasks[event.type]:
                        fu = self._executor.submit(self.run_task, task, event)
                        fu.add_done_callback(self._handle_callback)
                    logger.debug("处理消息: %s", event)
        finally:
            self.trigger_event(ON_EXIT_EVENT)
            self.stop()

    def _handle_callback(self, fn: Future):
        """处理回调"""
        if fn.exception():
            logger.error(fn.exception(), exc_info=True, stack_info=True)

    def start(self, blocking=False):
        """启动调度器"""
        if blocking:
            self.run()
        else:
            self._executor.submit(self.run)

    def stop(self):
        """停止调度器"""
        self._is_active = False
        self._executor.shutdown(wait=True)
        logger.info("vxSched(id=%s) 调度器停止....", id(self))

    def server_forerver(
        self, config: Union[Path, str, Dict] = None, mod_path: Union[Path, str] = None
    ):
        """启动调度器"""

        if config and Path(config).is_file():
            logger.info(f"loading config file: {config}")
            context = vxContext.load_json(config)
        elif isinstance(config, dict):
            context = vxContext(**config)
        else:
            context = vxContext()

        self.set_context(context)
        if mod_path:
            self.load_modules(mod_path)
        self.run()

    def register(
        self, event_type: str, time_limit: int = 1.0, lock: Lock = None
    ) -> Callable:
        """事件任务"""

        def deco(handler):
            self.add_task(event_type, handler, time_limit, lock)
            return handler

        return deco

    @classmethod
    def load_modules(cls, mod_path: Union[str, Path]) -> Any:
        """加载策略目录"""
        if not os.path.exists(mod_path):
            logger.warning(msg=f"{mod_path} is not exists")
            return

        modules = os.listdir(mod_path)
        logger.info(f"loading strategy dir: {mod_path}.")
        logger.info("=" * 80)
        for mod in modules:
            if (not mod.startswith("__")) and mod.endswith(".py"):
                try:
                    loader = importlib.machinery.SourceFileLoader(
                        mod, os.path.join(mod_path, mod)
                    )
                    spec = importlib.util.spec_from_loader(loader.name, loader)
                    strategy_mod = importlib.util.module_from_spec(spec)
                    loader.exec_module(strategy_mod)
                    logger.info(f"Load Module: {strategy_mod} Sucess.")
                    logger.info("+" * 80)
                except Exception as err:
                    logger.error(f"Load Module: {mod} Failed. {err}", exc_info=True)
                    logger.error("-" * 80)


vxsched = vxScheduler()

if __name__ == "__main__":
    sched = vxScheduler(3)

    @sched.register("__init__")
    def on_init(context, event):
        logger.warning("=====================on_init=====================")

    @sched.register("test", 0)
    def test(context, event):
        logger.warning(event)
        return 3

    @sched.register(ON_REPLY_EVENT)
    def on_reply(context, event):
        logger.critical(event)
        # raise ValueError("test")

    logger.info(f"{sched.get_tasks()}")

    sched.submit_event(
        "test",
        data=1,
        reply_to="333",
        trigger=vxTrigger.once(trigger_dt=vxtime.now() + 3),
    )
    vxtime.sleep(0.1)
    sched.server_forerver()
