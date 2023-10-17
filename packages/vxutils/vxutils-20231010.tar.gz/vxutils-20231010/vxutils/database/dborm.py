"""数据库ORM抽象"""


import contextlib
from enum import Enum
from typing import Iterator, List, Optional, Type, Union, Dict, Tuple, Any
from multiprocessing import Lock
import sqlite3
from sqlalchemy import (
    create_engine,
    Connection,
    MetaData,
    Table,
    Column,
    Boolean,
    Float,
    Integer,
    LargeBinary,
    NUMERIC,
    Text,
    text,
)
from vxutils.database.dataclass import vxDataClass
from vxutils.database.fields import DBTypes


__columns_mapping__ = {
    DBTypes.STRING: Text(256),
    DBTypes.FLOAT: Float,
    DBTypes.INTERGETE: Integer,
    DBTypes.BOOLEAN: Boolean,
    DBTypes.BYTES: LargeBinary,
    DBTypes.ENUM: Text(256),
    DBTypes.DATETIME: Float,
    DBTypes.LONG: NUMERIC,
    DBTypes.VARCHAR: Text(256),
}

SHARED_MEMORY_DATABASE = "file:vxquantdb?mode=memory&cache=shared"


def _normalize(value: Any) -> Any:
    """标准化处理数据库数值"""

    if value is None:
        return ""
    elif value is False:
        return 0
    elif value is True:
        return 1
    elif isinstance(value, Enum):
        return value.name
    else:
        return value


def creator():
    return sqlite3.connect(SHARED_MEMORY_DATABASE, uri=True)


class vxDataBase:
    """基于vxDataClass 数据管理"""

    def __init__(self, db_uri: str = None, **kwargs) -> None:
        if not db_uri:
            kwargs["creator"] = creator
            db_uri = "sqlite:///:memory:"

        self._dbengine = create_engine(db_uri, **kwargs)
        self._metadata = MetaData()
        self._tblmapping = {}
        self._lock = Lock()

    @classmethod
    def connect(cls, db_uri: str = None, **kwargs) -> "vxDataBase":
        """连接数据库"""
        return cls(db_uri, **kwargs)

    def create_table(
        self,
        table_name: str,
        primary_keys: List[str],
        vxdatacls: Type[vxDataClass],
        if_exists: str = "ignore",
    ) -> "vxDataBase":
        """创建数据表

        Arguments:
            table_name {str} -- 数据表名称
            primary_keys {List[str]} -- 表格主键
            vxdatacls {_type_} -- 表格数据格式
            if_exists {str} -- 如果table已经存在，若参数为ignore ，则忽略；若参数为 replace，则replace掉已经存在的表格，然后再重新创建

        Returns:
            vxDataBase -- 返回数据表格实例
        """
        column_defs = [
            Column(
                name,
                __columns_mapping__.get(vxfield.__dbtype__, Text(256)),
                primary_key=(name in primary_keys),
                nullable=(name in primary_keys),
            )
            for name, vxfield in vxdatacls.__vxfields__.items()
        ]
        tbl = Table(table_name, self._metadata, *column_defs)

        self._tblmapping[table_name] = (tbl, vxdatacls, primary_keys)

        if if_exists == "replace":
            tbl.drop(bind=self._dbengine, checkfirst=True)
        tbl.create(bind=self._dbengine, checkfirst=True)
        return self

    def drop_table(self, table_name: str) -> "vxDataBase":
        """删除数据表

        Arguments:
            table_name {str} -- 数据表名称
        """
        if table_name in self._tblmapping:
            tbl, _, _ = self._tblmapping.pop(table_name)
            tbl.drop(bind=self._dbengine, checkfirst=True)
        return self

    def truncate(self, table_name: str) -> "vxDataBase":
        """清空表格

        Arguments:
            table_name {str} -- 待清空的表格名称
        """
        if table_name in self._tblmapping:
            tbl, _, _ = self._tblmapping.pop(table_name)

            with self._dbengine.begin() as conn:
                conn.execute(tbl.delete())
        return self

    @contextlib.contextmanager
    def start_session(self, with_lock=True):
        """开始session，锁定python线程加锁，保障一致性"""
        if with_lock:
            with self._lock, self._dbengine.begin() as conn:
                yield vxDBSession(conn, self._tblmapping)
        else:
            with self._dbengine.begin() as conn:
                yield vxDBSession(conn, self._tblmapping)

    def get_dbsession(self):
        """获取一个session"""
        return vxDBSession(self._dbengine.connect(), self._tblmapping)


class vxDBSession:
    def __init__(
        self, conn: Connection, tblmapping: Dict[str, Tuple[Table, Type[vxDataClass]]]
    ) -> None:
        self._conn = conn
        self._tblmapping = tblmapping

    def save(self, table_name: str, *vxdataobjs) -> None:
        """保存vxdataclass的objects

        Arguments:
            table_name {str} -- 数据表名称
            vxdataobjs [vxdataobj] -- 需要保存的vxdataclass objects
        """
        if len(vxdataobjs) == 1 and isinstance(vxdataobjs[0], (list, tuple)):
            vxdataobjs = vxdataobjs[0]
        if table_name not in self._tblmapping:
            raise KeyError(f"{table_name} is not in tblmapping.")

        _, vxdatacls, _ = self._tblmapping[table_name]
        fields = list(vxdatacls.__vxfields__.keys())
        cols = " , ".join(fields)
        col_ids = " , ".join([f":{f}" for f in fields])
        sql = text(f"""INSERT OR REPLACE INTO `{table_name}`
            ({cols})
            VALUES ({col_ids})""")

        datas = [
            {col: _normalize(getattr(obj, col)) for col in fields}
            for obj in vxdataobjs
            if isinstance(obj, vxDataClass)
        ]

        self._conn.execute(sql, datas)
        return self

    def find(self, table_name: str, *conditions, **query) -> Iterator:
        """查询数据

        Arguments:
            table_name {str} -- 数据表名称
            conditions [list[str]] -- 查询条件
            query {str} -- 查询条件
        """
        sql = f"""SELECT * FROM `{table_name}`"""
        query_conditions = list(conditions)
        _, vxdatacls, _ = self._tblmapping[table_name]
        if query:
            query_conditions.extend(
                [f"{key}='{value or ''}'" for key, value in query.items()]
            )
        if query_conditions:
            sql += f""" WHERE {' and '.join(query_conditions)}"""
        sql += ";"

        for row in self._conn.execute(text(sql)):
            yield vxdatacls(**row._mapping)

    def findone(self, table_name: str, *conditions, **query) -> Optional[vxDataClass]:
        """查询数据

        Arguments:
            table_name {str} -- 数据表名称
            conditions [list[str]] -- 查询条件
            query {str} -- 查询条件
        """
        sql = f"""SELECT * FROM `{table_name}`"""
        query_conditions = list(conditions)
        _, vxdatacls, _ = self._tblmapping[table_name]
        if query:
            query_conditions.extend(
                [f"{key}='{value or ''}'" for key, value in query.items()]
            )
        if query_conditions:
            sql += f""" WHERE {' and '.join(query_conditions)}"""
        sql += ";"

        row = self._conn.execute(text(sql)).fetchone()
        return vxdatacls(**row._mapping) if row else None

    def remove(self, table_name: str, *vxdataobjs) -> None:
        """删除数据vxdataclass objects

        Arguments:
            table_name {str} -- 数据表名称
            vxdataobjs {vxdatacls_obj} -- 待删除的objects

        """
        if len(vxdataobjs) == 1 and isinstance(vxdataobjs[0], (list, tuple)):
            vxdataobjs = vxdataobjs[0]

        if table_name not in self._tblmapping:
            raise KeyError(f"{table_name} is not in tblmapping.")

        _, vxdatacls, primary_keys = self._tblmapping[table_name]

        if not primary_keys:
            primary_keys = vxdatacls.__vxfields__
            primary_keys.pop("created_dt")
            primary_keys.pop("updated_dt")

        query_str = " and ".join([f"{key} =:{key}" for key in primary_keys])
        sql = f"DELETE FROM `{table_name}` WHERE {query_str}"

        datas = [
            {key: _normalize(getattr(vxdataobj, key)) for key in primary_keys}
            for vxdataobj in vxdataobjs
        ]
        self._conn.execute(text(sql), datas)

    def delete(self, table_name: str, *conditions, **query) -> None:
        """批量删除

        Arguments:
            table_name {str} -- 数据表名称
            conditions [list(str)] -- 查询条件
            query {str} -- 查询条件
        """
        sql = f"""DELETE FROM `{table_name}`"""
        query_conditions = list(conditions)

        if query:
            query_conditions.extend(
                [f"{key}='{value or ''}'" for key, value in query.items()]
            )
        if query_conditions:
            sql += f""" WHERE {' and '.join(query_conditions)}"""
        sql += ";"
        self._conn.execute(text(sql))

    def insert(self, table_name: str, vxdataobj: vxDataClass) -> None:
        """插入数据vxdataclass object

        Arguments:
            table_name {str} -- 数据表格名称
            vxdataobj [vxDataClass] -- 被插入对象

        Raises:
            Valueerror -- 若插入对象以存在数据库时，抛出异常
        """
        _, vxdatacls, primary_keys = self._tblmapping[table_name]
        if not isinstance(vxdataobj, (vxDataClass, vxdatacls)):
            raise TypeError(f"vxdataobj 类型{type(vxdataobj)}非{vxdatacls.__name__}")

        col_names = []
        values = []
        update_string = []

        for col, value in vxdataobj.items():
            col_names.append(f"'{col}'")
            values.append(f"'{_normalize(value)}'")
            if col not in primary_keys:
                update_string.append(f"{col}=excluded.{col}")

            sql = f"""INSERT INTO {table_name}
                    ({','.join(col_names)}) \n\tVALUES ({','.join(values)})"""

        self._conn.execute(text(sql))

    def distinct(self, table_name: str, col: str, *conditions, **query) -> List:
        """去重

        Arguments:
            table_name {str} -- 数据表格名称
            col {str} -- 字段名称
            conditions / query -- 查询条件

        Returns:
            List -- _description_
        """
        sql = f"""SELECT DISTINCT `{col}` FROM `{table_name}`"""
        query_conditions = list(conditions)

        if query:
            query_conditions.extend(
                [f"{key}='{value or ''}'" for key, value in query.items()]
            )
        if query_conditions:
            sql += f""" WHERE {' and '.join(query_conditions)}"""
        sql += ";"
        return [row[0] for row in self._conn.execute(text(sql))]

    def count(self, table_name: str, *conditions, **query) -> int:
        """返回数据表格中的数据条数

        Arguments:
            table_name {str} -- 数据表格名称
            conditions {List[str]} -- 查询条件
            query {Dict[str,str]} -- 查询条件

        Returns:
            int -- 返回数据条数
        """
        sql = f"""SELECT COUNT(1) AS cnt FROM `{table_name}`"""
        query_conditions = list(conditions)

        if query:
            query_conditions.extend(
                [f"{key}='{value or ''}'" for key, value in query.items()]
            )
        if query_conditions:
            sql += f""" WHERE {' and '.join(query_conditions)}"""
        sql += ";"
        return self._conn.execute(text(sql)).fetchone()[0]

    def max(self, table_name: str, col: str, *conditions, **query) -> Union[int, float]:
        """获取数据表格中的最大值

        Arguments:
            table_name {str} -- 数据表格名称
            col {str} -- 字段名称
            conditions {List[str]} -- 查询条件
            query {Dict[str,str]} -- 查询条件
        Returns:
            Union[int, float] -- 最大值
        """
        sql = f"""SELECT MAX(`{col}`) AS col_max FROM `{table_name}`"""
        query_conditions = list(conditions)

        if query:
            query_conditions.extend(
                [f"{key}='{value or ''}'" for key, value in query.items()]
            )
        if query_conditions:
            sql += f""" WHERE {' and '.join(query_conditions)}"""
        sql += ";"
        return self._conn.execute(text(sql)).fetchone()[0]

    def min(self, table_name: str, col: str, *conditions, **query) -> Union[int, float]:
        """获取数据表格中的最小值

        Arguments:
            table_name {str} -- 数据表格名称
            col {str} -- 字段名称
            conditions {List[str]} -- 查询条件
            query {Dict[str,str]} -- 查询条件
        Returns:
            Union[int, float] -- 最小值
        """
        sql = f"""SELECT MIN(`{col}`) AS col_min FROM `{table_name}`"""
        query_conditions = list(conditions)

        if query:
            query_conditions.extend(
                [f"{key}='{value or ''}'" for key, value in query.items()]
            )
        if query_conditions:
            sql += f""" WHERE {' and '.join(query_conditions)}"""
        sql += ";"
        return self._conn.execute(text(sql)).fetchone()[0]

    def execute(self, sql: str, params: Union[Tuple, Dict, List] = None) -> Any:
        return self._conn.execute(text(sql), params)

    def commit(self) -> None:
        return self._conn.commit()

    def rollback(self) -> None:
        return self._conn.rollback()

    def __enter__(self) -> None:
        pass

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_tb and exc_type and exc_val:
            self._conn.rollback()
        else:
            self._conn.commit()


memdb = vxDataBase()

if __name__ == "__main__":
    from vxutils import vxtime
    from vxutils.database.fields import (
        vxUUIDField,
        vxDatetimeField,
        vxStringField,
    )

    # from vxquant.model.exchange import vxCashPosition

    class Status(Enum):
        SUCCESS = 0
        FAILED = 1

    class vxTest(vxDataClass):
        id = vxUUIDField("学号", prefix="studentid", auto=True)
        name = vxStringField("姓名")
        dt = vxDatetimeField("修改时间")

    db = vxDataBase("sqlite:///./dist/test1.db")
    db.create_table("st", ["id"], vxTest, if_exists="replace")
    with db.start_session() as session, vxtime.timeit():
        t1 = vxTest()
        session.save("st", t1)
        objs = [vxTest(name=f"std_{i}", dt=vxtime.now() + i) for i in range(1, 10000)]
        session.save("st", objs)
        # obj = objs.pop(3)
        # for i in session.find("st"):
        #    print(i)
        #    break
        # session.remove("st", objs)
        # print(session.count("st"))
        # print(session.max("st", "age"))
        # print(session.min("st", "age"))
        # print(session.distinct("st", "age"))
        # print(obj)
        # session.insert("st", obj)

        # print(session.min("st", "age", "age>=500"))
