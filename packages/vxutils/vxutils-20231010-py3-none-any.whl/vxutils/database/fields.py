"""字段定义"""

import uuid
import time
import datetime
import re
from typing import Any, Callable, Type
from abc import ABC
from enum import Enum
from vxutils.convertors import to_binary

# from vxutils import logger

__all__ = [
    "vxFieldBase",
    "vxUUIDField",
    "vxEnumField",
    "vxIntField",
    "vxFloatField",
    "vxPropertyField",
    "vxDatetimeField",
    "vxBoolField",
    "vxBytesField",
]


_NOTSET = object()


class DBTypes(Enum):
    """数据库类型"""

    INTERGETE = 0
    LONG = 1
    FLOAT = 2
    DOUBLE = 3
    STRING = 4
    VARCHAR = 5
    BOOLEAN = 6
    DATETIME = 7
    ENUM = 8
    BYTES = 9


class vxFieldBase(ABC):
    "字段基类"
    __dbtype__ = DBTypes.VARCHAR

    def __init__(
        self,
        doc: str = None,
        default_factory: Callable = None,
        formatter: Callable = None,
    ):
        self._formatter: Callable = formatter if callable(formatter) else None
        self._fdefault: Callable = (
            default_factory if callable(default_factory) else None
        )
        self._value = _NOTSET
        self.__doc__ = doc
        self._name = ""
        self._owner = None

    def __set_name__(self, owner: Any, name: str) -> None:
        self._name = name
        self._owner = owner
        if not hasattr(owner, "_data"):
            owner._data = {}

    def set_default(self) -> Any:
        if callable(self._fdefault):
            return self._fdefault()
        return None

    def formatter(self, value: Any = _NOTSET) -> Any:
        """格式化输出"""
        value = self.set_default() if value is _NOTSET else value
        return self._formatter(value) if callable(self._formatter) else value

    def __get__(self, obj: Any, objtype: Type = None) -> Any:
        if obj is None:
            return self

        return obj._data.setdefault(self._name, self.set_default())

    def __set__(self, obj: Any, value: Any) -> None:
        try:
            obj._data[self._name] = self.convert(obj, value)
        except Exception:
            obj._data[self._name] = self.set_default()

    def convert(self, obj: Any, value: Any) -> Any:
        """转换数据类型"""
        return value


class vxUUIDField(vxFieldBase):
    """UUID类型"""

    __dbtype__ = DBTypes.STRING

    def __init__(
        self,
        doc: str = None,
        prefix: str = "",
        auto: bool = True,
    ):
        self._prefix = prefix

        def default_factory():
            return f"{self._prefix}_{uuid.uuid4().hex if auto else ''}"

        super().__init__(doc, default_factory)

    # def convert(self, obj: Any, value: Any) -> Any:
    #    if isinstance(value, (str)):
    #        return (
    #            value if value.startswith(self._prefix) else f"{self._prefix}_{value}"
    #        )
    #    return str(value)


class vxEnumField(vxFieldBase):
    """枚举类型"""

    __dbtype__ = DBTypes.ENUM

    def __init__(
        self,
        doc: str = None,
        default: Enum = None,
        formatter: Callable = None,
    ):
        def default_factory():
            return default

        formatter = formatter if callable(formatter) else lambda value: value.name

        self._enumcls = default.__class__
        super().__init__(doc, default_factory, formatter)

    def convert(self, obj: Any, value: Any) -> Any:
        if isinstance(value, self._enumcls):
            return value
        elif value in self._enumcls._member_names_:
            return self._enumcls[value]
        return self._enumcls(value)


class vxBoolField(vxFieldBase):
    """布尔类型"""

    __dbtype__ = DBTypes.BOOLEAN

    def __init__(
        self,
        doc: str = None,
        default: bool = False,
        formatter: Callable = None,
    ):
        def default_factory():
            return bool(default)

        formatter = (
            formatter if callable(formatter) else lambda value: 1 if value else 0
        )

        super().__init__(doc, default_factory, formatter=formatter)

    def convert(self, obj: Any, value: Any) -> Any:
        return bool(value)


class vxIntField(vxFieldBase):
    """整型"""

    __dbtype__ = DBTypes.INTERGETE

    def __init__(
        self,
        doc: str = None,
        default: int = 0,
        upper_bound: float = float("inf"),
        lower_bound: float = float("-inf"),
        formatter: Callable = None,
    ):
        def default_factory():
            return default

        formatter = formatter if callable(formatter) else lambda value: f"{value:,.0f}"

        self.max = upper_bound
        self.min = lower_bound

        super().__init__(doc, default_factory, formatter)

    def convert(self, obj: Any, value: Any) -> Any:
        if isinstance(value, str):
            value = int(value.replace(",", ""))

        value = int(value)

        if not self.min <= value <= self.max:
            raise ValueError(f"{self._name} must between {self.min} to {self.max}")
        return value


class vxFloatField(vxFieldBase):
    """浮点数字类型"""

    __dbtype__ = DBTypes.FLOAT

    def __init__(
        self,
        doc=None,
        default: float = 0.0,
        ndigits: int = 2,
        upper_bound: float = float("inf"),
        lower_bound: float = float("-inf"),
        formatter: Callable = None,
    ):
        def default_factory():
            return default

        formatter = (
            formatter if callable(formatter) else lambda value: f"{value:,.{ndigits}f}"
        )

        self.max = upper_bound
        self.min = lower_bound

        super().__init__(doc, default_factory, formatter)

    def convert(self, obj: Any, value: Any) -> Any:
        if isinstance(value, str):
            value = float(value.replace(",", ""))
        elif value is None:
            value = 0.0
        value = float(value)
        if not self.min <= value <= self.max:
            raise ValueError(f"{self._name} must between {self.min} to {self.max}")
        return value


class vxDatetimeField(vxFieldBase):
    """日期时间类型"""

    __dbtype__ = DBTypes.DATETIME

    def __init__(
        self,
        doc: str = None,
        default: Any = _NOTSET,
        default_factory: Callable[..., Any] = None,
        fmt_string: Callable[..., Any] = "%F %H:%M:%S.%f",
    ):
        def formatter(value):
            return (
                datetime.datetime.fromtimestamp(value).strftime(fmt_string)
                if value
                else ""
            )

        if default is _NOTSET:
            super().__init__(doc, default_factory or time.time, formatter)
        else:
            super().__init__(doc, lambda: default, formatter)

    def convert(self, obj: Any, value: Any) -> Any:
        from vxutils.convertors import to_timestamp

        try:
            return to_timestamp(value)
        except Exception:
            return self.set_default()


class vxStringField(vxFieldBase):
    """字符串字段"""

    __dbtype__ = DBTypes.VARCHAR

    def __init__(
        self,
        doc=None,
        default: str = "",
        regex: str = None,
        normalizer: Callable = None,
        formatter: Callable = None,
    ):
        def default_factory():
            return default

        self._pattern = re.compile(regex) if regex else None
        self._normalizer = normalizer if callable(normalizer) else None

        super().__init__(doc, default_factory)

    def convert(self, obj: Any, value: Any) -> Any:
        if callable(self._normalizer):
            value = self._normalizer(value)

        if self._pattern and not self._pattern.match(value):
            raise ValueError(f"{self._name} must match {self._pattern.pattern}")

        return value


class vxBytesField(vxFieldBase):
    """二进制字段"""

    def __init__(
        self,
        doc: str = None,
        default: bytes = None,
        formatter: Callable = None,
    ):
        formatter = (
            formatter
            if callable(formatter)
            else lambda value: f"Bytes(id-{id(value)}),size:{len(value):,.2f}bits"
        )

        def default_factory():
            return default

        super().__init__(doc, default_factory, formatter)

    def convert(self, obj: Any, value: Any) -> Any:
        return to_binary(value)


class vxPropertyField(vxFieldBase):
    """属性字段"""

    __dbtype__ = DBTypes.VARCHAR

    def __init__(
        self,
        doc: str = None,
        fgetter: Callable = None,
        converter: Callable = None,
        formatter: Callable = None,
        dbtyupe: DBTypes = DBTypes.VARCHAR,
    ):
        def default_factory():
            return None

        self._fgetter = fgetter
        self._converter = converter
        self.__dbtype__ = dbtyupe

        super().__init__(doc, default_factory, formatter)

    def __get__(self, obj: Any, objtype: Type = None) -> Any:
        if callable(self._fgetter):
            return self._fgetter(obj)

        if self._name in obj._data:
            return obj._data[self._name]
        else:
            return obj._data.setdefault(self._name, self.set_default())


if __name__ == "__main__":

    def getter(obj):
        return obj.age * obj.score

    class vxTest:
        id = vxUUIDField("Test ID", prefix="vxorder", auto=True)
        name = vxStringField(
            "姓名", regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        )  # r"^1[3-9]\d{9}$")
        age = vxIntField("年龄", default=1000, upper_bound=1000, lower_bound=0)
        score = vxFloatField("分数", default=20000.0, lower_bound=0.0)
        level = vxEnumField("等级", default=DBTypes.VARCHAR)
        is_true = vxBoolField("bool", default=False)
        test = vxPropertyField("测试", fgetter=getter, formatter=lambda x: f"{x:,.0f}")
        created_dt = vxDatetimeField("创建时间", default_factory=time.time)
        updated_dt = vxDatetimeField("更新时间", default_factory=time.time)

    t = vxTest()
    print(t.id)
    t.id = "123"
    # t.name = "18007558228@qq.com"
    # t.score = f"{3000:,.0f}"
    # t.level = 0
    # print(t.level)
    print("test", t.id)
    print(t.is_true)

    # for key, formatter in t.__formatters__.items():
    #    print(key, formatter())
