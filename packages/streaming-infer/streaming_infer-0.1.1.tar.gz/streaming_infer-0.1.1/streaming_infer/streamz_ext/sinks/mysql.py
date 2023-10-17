#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Time    :   2023/06/20 17:37:22
@Author  :   qiupengfei 
@Contact :   qiupengfei@baidu.com
@Desc    :   
"""

from streamz.sinks import Sink, Stream
from sqlalchemy.sql.expression import insert
from streaming_infer.streamz_ext.sqlalchemy_connection import SQLAlchemyConnection
import sqlalchemy
import logging

class OnDuplicateOption:
    """插入重复时候的处理方案
    """
    # 主键重复时忽略
    ON_DUPLICATE_IGNORE = 'ignore'
    # 主键重复时更新
    ON_DUPLICATE_UPDATE = 'update'
    # 主键重复时报错
    ON_DUPLICATE_ERROR = 'error'


@Stream.register_api()
class sink_to_mysql(Sink):
    """写入mysql的类
    """

    def __init__(self, upstream, mysql_url: str, database: str, table: str, field_map: dict, on_duplicate=OnDuplicateOption.ON_DUPLICATE_UPDATE, **kwargs):
        super().__init__(upstream, **kwargs)

        # mysql的sqlalchemy url
        self.mysql_url = mysql_url
        self.database = database
        self.table = table 
        # 字段映射关系
        self.field_map = field_map
        # 主键重复处理策略
        self.on_duplicate = on_duplicate

        # 初始化mysql连接
        url = SQLAlchemyConnection.get_url(mysql_url, database=database)
        self.conn = SQLAlchemyConnection(url, reflect_tables=[table])
        self.table_obj = self.conn[self.table]

    def update(self, x, who=None, metadata=None):
        """写入数据到mysql, 如果是批量写，则需要添加缓存，处理metadata的引用计数，暂时只支持单条数据插入和删除，所以不需要处理
        """
        with self.conn.session() as session:
            row = {}
            for k, v in self.field_map.items():
                # key不存在
                if k not in x:
                    continue
                # 如果存在， 优先用mapping后的key， 如果没有写mapping， 那么用原始的key
                key = v or k
                row[key] = x[k]

            self.insert_one(session, self.table_obj, row, on_duplicate=self.on_duplicate)
    
    def insert_one(self, session, table, row: dict, on_duplicate=OnDuplicateOption.ON_DUPLICATE_ERROR) -> bool:
        """插入一条数据

        Args:
            table: 要插入的表对象
            row (dict): 要插入的一个json
            on_duplicate (str, optional): 主键重复时候的处理策略. Defaults to 'error'.
        
        Returns:
            bool: 是否插入成功
        """
        try:
            columns = {c.name for c in table.__table__.columns}
            fixed_row = {k: v for k, v in row.items() if k in (
                row.keys() & columns)}
            session.execute(insert(table).values(**fixed_row))
            session.commit()
            return True
        except sqlalchemy.exc.IntegrityError as e:
            # 发现重复， 此错误只针对mysql
            if e.orig and e.orig.args and e.orig.args[0] == 1062:
                message = e.orig.args[1]
                if on_duplicate == OnDuplicateOption.ON_DUPLICATE_ERROR:
                    raise e
                elif on_duplicate == OnDuplicateOption.ON_DUPLICATE_UPDATE:
                    r = table(**fixed_row)  # type: ignore
                    session.merge(r, load=True)
                    session.commit()
                    return True
                elif on_duplicate == OnDuplicateOption.ON_DUPLICATE_IGNORE:
                    logging.warning('%s: %s', table.__table__.name, message)
            return False