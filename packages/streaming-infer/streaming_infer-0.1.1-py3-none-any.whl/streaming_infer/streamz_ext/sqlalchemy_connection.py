#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Time    :   2023/06/20 18:02:44
@Author  :   qiupengfei 
@Contact :   qiupengfei@baidu.com
@Desc    :   
"""


import logging
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy.sql.schema import MetaData
from sqlalchemy_utils import database_exists, create_database


class CharsetBase(object):
    """设置数据库的编码方式
    """

    __table_args__ = {
        "mysql_default_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_0900_ai_ci",
    }


Base = declarative_base(cls=CharsetBase)
metadata = Base.metadata


class SQLAlchemyConnection(object):
    """封装sqlalchemy以方便使用
    """

    def __init__(self, url, create_if_not_exists=False, reflect_tables=None, declare_tables=None, pool_size=100,
                 autocommit=False, pool_pre_ping=True, **kwargs):
        """

        Args:
            url (str): 对应的sqlalchemy url
            createIfNotExists (bool): 如果database不存在是否创建
            reflectTables (list):  要反射的数据库中已存在的表名, 指定其他项目中创建的表
            declareTables (list):  新定义的表, 指定当前项目管理的表, 需要继承本文件中定义的Base
        """
        reflect_tables = reflect_tables or []
        declare_tables = declare_tables or []
        self.url = url
        self.engine = create_engine(self.url, max_overflow=-1, pool_size=pool_size, 
                                    pool_pre_ping=pool_pre_ping, **kwargs)
        if create_if_not_exists:
            if not database_exists(self.engine.url):
                logging.info('Database[%s] not exists, create it', url)
                create_database(self.engine.url)
                self.engine.connect()
            else:
                logging.info('Database[%s] is already existing', url)
                self.engine.connect()
        else:
            logging.info('Database[%s] is already existing', url)
            self.engine.connect()

        self._autocommit = autocommit
        self._Session = sessionmaker(bind=self.engine, autocommit=autocommit)
        self._tables = {}

        self.autoMapMetaData = MetaData()
        self.AutoMapBase = automap_base(metadata=self.autoMapMetaData)
        self.reflect_tables(*reflect_tables)

        for table in declare_tables:
            #print(dir(table))
            if hasattr(table, '__tablename__'):
                self._tables[table.__tablename__] = table
            else:
                self._tables[table.name] = table

    def reflect_tables(self, *tables):
        """反射获得表的信息
        """
        if not tables:
            return
        self.autoMapMetaData.reflect(self.engine, only=tables, views=True)
        self.AutoMapBase.prepare()
        for table_name in tables:
            try:
                tcls = getattr(self.AutoMapBase.classes, table_name)
                self._tables[table_name] = tcls
            except AttributeError:
                if self.autoMapMetaData.tables and table_name in self.autoMapMetaData.tables:
                    self._tables[table_name] = self.autoMapMetaData.tables[table_name]
                else:
                    logging.error('table %s not found', table_name)
        
    def __getitem__(self, tablename):
        """获得table对应的表
        """
        return self._tables[tablename]

    @contextmanager
    def session(self, autocommit=False):
        """
            单纯读的查询可以将autocommit设置为True, 以减少锁表的概率
        """
        # session = self._Session()
        Session = sessionmaker(bind=self.engine, autocommit=autocommit or self._autocommit)
        session = Session()
        try:
            yield session
            session.commit()
        except Exception as e: 
            session.rollback()
            raise e
        finally:
            session.close()

    def create_table(self):
        """创建所有表
        """
        metadata.create_all(self.engine)

    def execute(self, sql, **kwargs):
        """执行sql语句"""
        if kwargs:
            sql = text(sql)
            rs = self.engine.execute(sql, **kwargs)
        else:
            rs = self.engine.execute(sql)
        return rs

    def iter_result(self, sql, lowerCase=True, **kwargs):
        """执行sql并将结果返回, 返回的结果是dict

        Args:
            sql (str): 可以是包含:param的格式, 但这种情况下必须提供kwargs. 如果不提供kwargs, 则当做普通sql执行

        Yields:
            dict: 每一行数据, 返回字典
        """
        rs = self.execute(sql, **kwargs)
        for row in rs:
            yield {
                column.lower() if lowerCase else column: value
                for column, value in row.items()
            }

    def first(self, sql, lowerCase=True, **kwargs):
        """执行sql并返回第一条结果, 如果没有结果则返回None
        Args:
            sql (str): 可以是包含:param的格式, 但这种情况下必须提供kwargs. 如果不提供kwargs, 则当做普通sql执行

        Returns:
            dict: 每一行数据, 返回字典
        """
        for item in self.iterResult(sql, lowerCase=lowerCase, **kwargs):
            return item
        return None

    @classmethod
    def get_url(self, url, drivername=None, username=None, password=None, host=None, port=None, database=None):
        """获取一个新的url, 可以同时替换一些参数
        """
        url = make_url(url)
        if drivername:
            url = url.set(drivername=drivername)
        if username:
            url = url.set(username=username)
        if password:
            url = url.set(password=password)
        if host:
            url = url.set(host=host)
        if port:
            url = url.set(port=port)
        if database:
            url = url.set(database=database)
        return url

