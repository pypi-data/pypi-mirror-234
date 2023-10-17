"""类型集合"""
import contextlib
from typing import Any, Type
from collections.abc import MutableMapping, Sequence, Mapping
from vxutils.convertors import vxJSONEncoder, to_json
from vxutils.database.dataclass import vxDataClass

try:
    import simplejson as json
except ImportError:
    import json


class vxDict(dict):
    """引擎上下文context类"""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            super().__setitem__(k, _to_vxdict(v, self.__class__))

    def __setitem__(self, key: Any, item: Any) -> None:
        return super().__setitem__(key, _to_vxdict(item, self.__class__))

    def __setattr__(self, attr: str, value: Any) -> Any:
        return super().__setitem__(attr, _to_vxdict(value, self.__class__))

    def __getattr__(self, attr: str) -> Any:
        try:
            return super().__getitem__(attr)
        except KeyError:
            raise AttributeError(f"{self.__class__.__name__} has no attribute {attr}")

    def __eq__(self, __o: MutableMapping) -> bool:
        if len(self) == len(__o):
            with contextlib.suppress(Exception):
                return all(v == __o[k] for k, v in self.items())
        return False

    def __setstate__(self, state) -> None:
        self.__init__(**state)

    def __getstate__(self) -> dict:
        return self.data

    def __str__(self):
        try:
            return f"< {self.__class__.__name__}(id-{id(self)}) : {to_json(self)} >"
        except (TypeError, KeyError) as err:
            logger.info(err)

    def to_dict(self):
        return {k: v.to_dict() if isinstance(v, vxDict) else v for k, v in self.items()}


def _to_vxdict(value: Any, vxdict_cls: Type[vxDict]) -> Any:
    if isinstance(value, vxDataClass):
        return value
    if isinstance(value, (Mapping, MutableMapping)):
        return vxdict_cls(**value)
    elif isinstance(value, Sequence) and not isinstance(value, str):
        return [_to_vxdict(v, vxdict_cls) for v in value]
    else:
        return value


@vxJSONEncoder.register(vxDict)
def _(obj):
    return obj.to_dict()


Mapping.register(vxDict)
MutableMapping.register(vxDict)


if __name__ == "__main__":
    __default_settings__ = {
        "mdapi": {"class": "vxquant.mdapi.vxMdAPI", "params": {}},
        "tdapis": {},
        "notify": {},
        "preset_events": {
            "before_trade": "09:15:00",
            "on_trade": "09:30:00",
            "noon_break_start": "11:30:00",
            "noon_break_end": "13:00:00",
            "before_close": "14:45:00",
            "on_close": "14:55:00",
            "after_close": "15:30:00",
            "on_settle": "16:30:00",
        },
    }

    from vxutils import logger

    d = vxDict(settings=__default_settings__)
    print(d.settings.mdapi)
    print(isinstance(d, dict))
    print(dir(d))
    print(d.__dict__)
    # logger.info(d)
    # d.a = {}
    # d.settings.mdapi = 33
    # d.update(**{"a1": 2, "b1": {"e": 5, "f": 6}, "c1": 4})
    # logger.info(d)
    # logger.info(__default_settings__)

    # logger.info(d.to_dict())
    # logger.info("e" in d.keys())
    # logger.info(isinstance(d, dict))
    # d.update({"a1": 2, "b1": {"e": 5, "f": 6}, "c1": 4})
    # logger.info(d)
    # logger.info(d.keys())
    # logger.info(d.a1)
    # logger.info(d.b1.e)
    # logger.info(isinstance(d, UserDict))
    # logger.info(f"{round(400000 / 680)*1000*11.50*0.5:,.2f}")
