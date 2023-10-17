"""缓存

支持

"""

import pickle
import inspect
import hashlib
from pathlib import Path
from typing import Any, Dict, Callable, List
from functools import wraps
from vxutils import vxtime
from vxutils.convertors import to_timestamp, to_json
from vxutils.database.dborm import vxDataBase, vxDBSession
from vxutils.database.dataclass import vxDataClass
from vxutils.database.fields import (
    vxUUIDField,
    vxDatetimeField,
    vxBytesField,
)

__all__ = ["MissingCache", "vxCache", "diskcache", "memcache"]


_ENDOFTIME = to_timestamp("2199-12-31 23:59:59")


class MissingCache(Exception):
    pass


class _CacheUnit(vxDataClass):
    key: str = vxUUIDField(False)
    value: Any = vxBytesField()
    expired_dt: float = vxDatetimeField()


class vxCache:
    """Cache缓存"""

    def __init__(self, db_uri: str = None) -> None:
        if db_uri and (not db_uri.startswith("sqlite:///")):
            db_uri = f"sqlite:///{db_uri}"

        self._conn = vxDataBase(db_uri)
        self._conn.create_table("__cache__", ["key"], _CacheUnit)
        self._last_remove_expired_dt = 0
        with self._conn.start_session() as session:
            self._remove_expired(session)

    def __contains__(self, key) -> bool:
        with self._conn.start_session() as session:
            self._remove_expired(session)
            cache_unit = session.findone(
                "__cache__", f"expired_dt> {vxtime.now()}", key=key
            )
            return bool(cache_unit)

    def __len__(self) -> int:
        with self._conn.start_session() as session:
            self._remove_expired(session)
            return len(session.distinct("__cache__", "key"))

    def __getitem__(self, key) -> Any:
        if not key:
            raise ValueError("key can't be empty")
        with self._conn.start_session() as session:
            self._remove_expired(session)
            cache_unit = session.findone(
                "__cache__", f"""expired_dt > {vxtime.now()}""", key=key
            )
            if cache_unit is None:
                raise MissingCache(key)
            return pickle.loads(cache_unit.value)

    def get(self, key: str, default: Any = None) -> Any:
        """获取缓存内容

        Arguments:
            key {str} -- 缓存key
            default {Any} -- 默认值 {default=None}, 如果缓存不存在，返回默认值

        Returns:
            Any -- 缓存内容
        """
        if not key:
            raise ValueError("key can't be empty")

        with self._conn.start_session() as session:
            self._remove_expired(session)
            cache_unit = session.findone(
                "__cache__", f"""expired_dt > {vxtime.now()}""", key=key
            )
            return pickle.loads(cache_unit.value) if cache_unit else default

    def get_many(self, *keys: List[str]) -> Dict:
        """获取缓存内容

        Returns:
            Dict -- 缓存内容
        """
        if not keys:
            raise ValueError("keys can't be empty")

        if len(keys) == 1 and isinstance(keys[0], (tuple, list)):
            keys = keys[0]

        with self._conn.start_session() as session:
            self._remove_expired(session)
            conditions = [
                f"""key in ('{"', '".join(keys)}')""",
                f"""expired_dt > {vxtime.now()}""",
            ]
            cur = session.find("__cache__", *conditions)
            return {
                cache_unit.key: pickle.loads(cache_unit.value) for cache_unit in cur
            }

    def set(self, expired_dt: float = None, ttl: float = None, **cacheobjs) -> None:
        """设置缓存内容

        Arguments:
            cacheobjs {Dict} -- 缓存内容
            expired_dt {float} -- 超时时间 (default: {None})
            ttl {float} -- 生命周期，单位：s (default: {None})
        """
        if ttl:
            expired_dt = vxtime.now() + ttl

        if expired_dt is None:
            expired_dt = _ENDOFTIME

        cache_units = [
            _CacheUnit(key=key, value=pickle.dumps(value), expired_dt=expired_dt)
            for key, value in cacheobjs.items()
        ]
        with self._conn.start_session() as session:
            self._remove_expired(session)
            session.save("__cache__", *cache_units)

    def pop(self, key: str, default: Any = None) -> Any:
        """弹出缓存内容

        Arguments:
            key {str} -- 缓存key
            default {Any} -- 缺省值 (default: {None})

        Returns:
            Any -- 缓存内容
        """
        if not key:
            raise ValueError("key can't be empty")

        with self._conn.start_session() as session:
            self._remove_expired(session)
            cache_unit = session.findone(
                "__cache__", f"""expired_dt > {vxtime.now()}""", key=key
            )
            if cache_unit:
                session.delete("__cache__", key=key)
                return pickle.loads(cache_unit.value)
            return default

    def _remove_expired(self, session: vxDBSession) -> Any:
        """删除超时内容"""
        now = vxtime.now()
        if self._last_remove_expired_dt + 60 > now:
            return
        self._last_remove_expired_dt = now
        session.delete("__cache__", f"expired_dt < {self._last_remove_expired_dt}")

    def update(
        self, cacheobjs: Dict, expired_dt: float = None, ttl: float = None
    ) -> None:
        """批量更新

        Keyword Arguments:
            expired_dt {float} -- 超时时间 (default: {None})
            cacheobjs {dict} -- 缓存内容
        """
        if not cacheobjs:
            return

        if ttl:
            expired_dt = vxtime.now() + ttl
        elif expired_dt is None or expired_dt > _ENDOFTIME:
            expired_dt = _ENDOFTIME

        cache_units = [
            _CacheUnit(key=key, value=pickle.dumps(value), expired_dt=expired_dt)
            for key, value in cacheobjs.items()
        ]
        with self._conn.start_session() as session:
            self._remove_expired(session)
            session.save("__cache__", cache_units)

    def clear(self) -> None:
        """清空所有缓存内容"""
        with self._conn.start_session() as session:
            session.delete("__cache__")

    def keys(self) -> List[str]:
        """获取所有key"""
        with self._conn.start_session() as session:
            return session.distinct("__cache__", "key", f"expired_dt > {vxtime.now()}")

    def hash_keys(self, obj: Any) -> str:
        """将keys进行hash

        Arguments:
            obj {Any} -- 需要hash的对象

        Returns:
            str -- hash后的keys
        """
        try:
            return hash(obj)
        except TypeError:
            return hash(to_json(obj.__dict__, sort_keys=True, default=str))

    def __call__(self, ttl: float = None) -> Any:
        def deco(func: Callable) -> Callable:
            @wraps(func)
            def wapper(*args, **kwargs):
                try:
                    ba = inspect.signature(func).bind(*args, **kwargs)
                    ba.apply_defaults()
                    string = to_json(ba.arguments, sort_keys=True, default=str)
                    key = hashlib.md5(string.encode()).hexdigest()
                    retval = self[key]
                except MissingCache:
                    retval = func(*args, **kwargs)
                    self.set(key, retval, ttl=ttl)

                return retval

            return wapper

        return deco


_cache_path = Path.home().joinpath(".cache")
_cache_path.mkdir(parents=True, exist_ok=True)
diskcache = vxCache(str(_cache_path.joinpath("vxcache.db").absolute()))
memcache = vxCache()

if __name__ == "__main__":
    from vxutils import logger

    logger.info("starting")
    memcache.set(test=1, test2=3)
    logger.info(memcache["test2"])
