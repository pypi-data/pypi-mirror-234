import time
import pickle
import zlib
from collections import OrderedDict
from collections.abc import Mapping, MutableMapping
from typing import Dict, Tuple, Type, Any, Iterable
from vxutils import logger
from vxutils.convertors import to_json, vxJSONEncoder
from vxutils.database.fields import vxFieldBase, vxDatetimeField


__all__ = ["vxDataMeta", "vxDataClass"]


def _is_lower_than(self, other: "vxDataClass") -> bool:
    """< 根据sortkeys的顺序一次对比"""
    for attr in self.__sortkeys__:
        if getattr(self, attr) < getattr(other, attr):
            return True
        elif getattr(self, attr) > getattr(other, attr):
            return False
    return False


def _is_greater_than(self, other: "vxDataClass") -> bool:
    """> 根据sortkeys的顺序一次对比"""
    for attr in self.__sortkeys__:
        if getattr(self, attr) < getattr(other, attr):
            return False
        elif getattr(self, attr) > getattr(other, attr):
            return True
    return False


class vxDataMeta(type):
    """data 元类"""

    def __new__(cls, name: str, bases: Tuple, attrs: Dict) -> Type:
        attrs["__vxfields__"] = OrderedDict()

        for base_cls in bases:
            if hasattr(base_cls, "__vxfields__"):
                attrs["__vxfields__"].update(**base_cls.__vxfields__)

        attrs["__vxfields__"].update(
            (name, field)
            for name, field in attrs.items()
            if isinstance(field, vxFieldBase)
        )

        attrs["__vxfields__"].move_to_end("created_dt")
        attrs["__vxfields__"].move_to_end("updated_dt")

        if "__sortkeys__" in attrs and len(attrs["__sortkeys__"]) > 0:
            attrs["__lt__"] = _is_lower_than
            attrs["__gt__"] = _is_greater_than

        return type.__new__(cls, name, bases, attrs)

    def __call__(cls, *args, **kwds) -> Any:
        created_dt = kwds.pop("created_dt", None)
        updated_dt = kwds.pop("updated_dt", created_dt)

        instance = super().__call__(*args, **kwds)

        if created_dt is None:
            created_dt = updated_dt = time.time()

        instance.created_dt = created_dt
        instance.updated_dt = updated_dt

        return instance


class vxDataClass(metaclass=vxDataMeta):
    """数据基类"""

    __sortkeys__ = []
    __vxfields__ = OrderedDict()
    created_dt = vxDatetimeField()
    updated_dt = vxDatetimeField()

    def __init__(self, *args, **kwargs) -> None:
        if args:
            if isinstance(args[0], self.__class__):
                kwargs.update(**args[0].to_dict())
            elif isinstance(args[0], Mapping):
                kwargs |= args[0]
            else:
                kwargs |= zip(self.__vxfields__, args)

        self._data = {}

        for attr, field in self.__vxfields__.items():
            if attr in ("created_dt", "updated_dt"):
                continue
            if attr in kwargs:
                setattr(self, attr, kwargs[attr])
            else:
                setattr(self, attr, field.set_default())

    def __setattr__(self, __name: str, __value: Any) -> None:
        super(vxDataClass, self).__setattr__(__name, __value)
        if __name in self.__vxfields__ and __name != "updated_dt":
            self.updated_dt = time.time()

    def __setitem__(self, __name: str, __value: Any) -> None:
        try:
            self.__setattr__(__name, __value)
        except AttributeError as err:
            raise KeyError(f"{__name} not find.") from err

    def __getitem__(self, __name: str) -> Any:
        return getattr(self, __name)

    def __str__(self) -> str:
        message = dict(
            map(
                lambda item: (item[0], item[1].formatter(getattr(self, item[0]))),
                self.__vxfields__.items(),
            )
        )
        return f"<{self.__class__.__name__}({id(self)}):{to_json(message)}>"

    def __repr__(self) -> str:
        message = dict(
            map(
                lambda item: (item[0], item[1].formatter(getattr(self, item[0]))),
                self.__vxfields__.items(),
            )
        )
        return f"<{self.__class__.__name__}({id(self)}):{to_json(message)}>"

    @property
    def message(self):
        """消息"""

        return dict(
            map(lambda key: (key, getattr(self, key)), self.__vxfields__.keys())
        )

    def keys(self) -> Iterable[str]:
        """keys"""
        return self.__vxfields__.keys()

    def values(self) -> Iterable[Any]:
        """值"""
        return iter(getattr(self, __name) for __name in self.__vxfields__.keys())

    def items(self) -> Iterable[Tuple[str, Any]]:
        """获取 key,value 对"""
        return iter(
            (__name, getattr(self, __name)) for __name in self.__vxfields__.keys()
        )

    def get(self, key: str, default: Any = None) -> Any:
        """获取 key 对应的值"""
        return getattr(self, key, default)

    def update(self, **kwargs) -> None:
        """更新数据"""
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def loads(cls, pickle_obj: bytes) -> "vxDataClass":
        """从文件中获取"""
        pickled = zlib.decompress(pickle_obj)
        return pickle.loads(pickled)

    def dumps(self) -> bytes:
        """序列化"""
        pickled = pickle.dumps(self)
        return zlib.compress(pickled)

    def __setstate__(self, state: dict):
        self.__init__(**state)

    def __getstate__(self):
        return self.message

    def __iter__(self):
        return next(self)

    def __next__(self):
        yield from self.keys()

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, __o: "vxDataClass") -> bool:
        return all(v == __o[k] for k, v in self.items())

    def __contains__(self, item: str) -> bool:
        return item in self.keys()

    def clear(self) -> None:
        """恢复原始状态"""
        now = time.time()
        for attr, field in self.__vxfields__.items():
            if attr in ("created_dt", "updated_dt"):
                setattr(self, attr, now)
            else:
                setattr(self, attr, field.set_default())


@vxJSONEncoder.register(vxDataClass)
def _(obj):
    message = {}

    for attr, vxfield in obj.__vxfields__.items():
        value = getattr(obj, attr)
        if isinstance(value, vxDataClass):
            value = value.to_dict()
        else:
            value = vxfield.formatter(value)

        message[attr] = value

    return message


Mapping.register(vxDataClass)
MutableMapping.register(vxDataClass)


if __name__ == "__main__":
    from vxutils.database.fields import (
        vxUUIDField,
        vxStringField,
        vxBoolField,
    )

    class vxOrder(vxDataClass):
        id = vxUUIDField("order id", prefix="orderid", auto=True)
        c = vxStringField()
        a = vxBoolField(formatter=lambda value: 1 if value else 0)
        b = vxStringField()

    # a = 3
    data = vxOrder(
        1,
        2,
        3,
        4,
        5,
        6,
        7,
    )
    data2 = vxOrder("a", "b", "c")
    data3 = vxOrder()

    # data.c = 3

    # data.update(c=3, created_dt=123)
    # data2.a = "this is a "

    # for k, v in data._data.items():
    #    logger.info("%s %s", k, v)
    logger.info(data3.message)
    logger.info(data2.message)
    logger.info("data2: %s", data2)
    logger.info(isinstance(data, Mapping))
    logger.info(isinstance(data, dict))
    logger.info(data2.message)

    # logger.info(data.b)
    # logger.info(data.c)
