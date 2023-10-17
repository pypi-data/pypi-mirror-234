#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Time    :   2023/06/15 15:30:33
@Author  :   qiupengfei 
@Contact :   qiupengfei@baidu.com
@Desc    :   
"""

import base64
import json
import logging
import os

import ray

from streaming_infer.streamz_ext.sqlalchemy_connection import \
    SQLAlchemyConnection


class JobConfig(object):
    """job的全局配置信息
    配置说明：
        - worker_capacity": 1 // 每个worker的最大容量
          task_type": "soe" // 任务的类型
          log_level": 20  // 默认INFO， CRITICAL = 50, ERROR = 40, WARNING = 30, INFO = 20, DEBUG = 10
          task_fetch_interval": 5   // 轮询发现任务的间隔
          nats_url": "10.31.76.16:8221" // NATS地址
          mysql_url": "mysql+pymysql://user:password@localhost:3306/" // 服务mysql库
          config_db": "default" // 配置相关的表 所在数据库的名字
          influxdb_url": "" // 时序数据表 v0.1不使用
          controller_url": "http://10.27.37.65:8080" // 控制服务地址
    """

    def __init__(self, config: dict):
        self.config = config

    def get_nats_url(self):
        return self.get_conf('nats_url', '10.214.36.203:8221')
    
    def get_windmill_client(self, endpoint):
        """获得windmill的client
        """
        raise NotImplementedError()
    
    @property
    def worker_capacity(self):
        """worker可以运行的task数量

        """
        return self.get_conf('worker_capacity', 1)
    
    def get_db(self, reflect_tables=None) -> SQLAlchemyConnection:
        """获取数据库连接
        """
        url = SQLAlchemyConnection.get_url(self.get_conf("mysql_url"), database=self.get_conf("config_db"))
        logging.info("connecting to %s, %s", url, self.get_conf("mysql_url"))
        conn = SQLAlchemyConnection(url, reflect_tables=reflect_tables)
        return conn
    
    @classmethod
    def parse_from_runtimeenv(cls):
        """解析runtimeenv中的全局配置信息
        """
        context = ray.get_runtime_context()
        env = context.runtime_env
        env_vars = env.get('env_vars', {})
        ray_params = env_vars.get('RAY_PARAMETERS', os.environ.get('RAY_PARAMETERS'))
        if ray_params:
            if not isinstance(ray_params, dict):
                try:
                    ray_params = base64.b64decode(ray_params)
                except Exception:
                    logging.info("RAY_PARAMETERS is not base64")
                ray_params = json.loads(ray_params)
            return cls(ray_params)
        else:
            return cls({})
        
    @classmethod
    def parse_from_yaml(cls, config_file):
        """从配置文件解析全局配置信息， 主要用于本地测试
        """
        import yaml
        with open(config_file) as df:
            ray_params = yaml.safe_load(df)
            if ray_params:
                return cls(ray_params)
            else:
                return cls({})
    
    @classmethod
    def parse_from_env(cls):
        """解析环境变量中的全局配置信息, 主要用于本地测试
        """
        ray_params = os.environ.get('RAY_PARAMETERS')
        if ray_params:
            return cls(json.loads(ray_params))
        else:
            return cls({})
    
    def get_task_type(self):
        """获取任务类型
        """
        return self.get_conf('task_type')
    
    def get_log_level(self):
        """日志输出级别
        """
        return self.get_conf('log_level', logging.INFO)

    def get_conf(self, key, default=None):
        """读取配置文件
        # TODO: key支持多级
        """
        return self.config.get(key, default)

    def get_namespace(self):
        """TODO: 获取ray job的namespace， 以此实现多租户, 不过job_config在ray.init()之前可能无法使用， 需要再研究一下
        """
        return self.get_conf('namespace')
