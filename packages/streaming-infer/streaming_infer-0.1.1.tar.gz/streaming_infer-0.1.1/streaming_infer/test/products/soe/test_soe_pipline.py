#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Author: liuzixiang
Date: 2023-07-18 17:51:54
LastEditors: liuzixiang
LastEditTime: 2023-07-21 18:14:29
Description: 
"""

import json
import logging
import os
import re
import sqlite3
import unittest
from unittest import TestCase

import arrow
import ray

import streaming_infer.products
from streaming_infer.config.job_config import JobConfig
from streaming_infer.supervisor import Supervisor
from streaming_infer.tasks.source_config import SourceConfig
from streaming_infer.tasks.task_manager import TaskManager
from streamz.core import Stream
from streamz.sources import from_iterable

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
                    datefmt='%m-%d %H:%M:%S')

class TestJetStreamSourceConfig(SourceConfig):
    SOURCE_TYPE = "testjetstream"

    def __init__(self, nats_url: str, subjects: list, 
                 retention_seconds=3600, 
                 replay_seconds=0,
                 manual_ack=False, 
                 **kwargs):
        # nats连接url， 认证方式不在这里配置，如果需要认证需要从job_config中获取
        self.nats_url = nats_url
        # 要监听的主题
        self.subjects =  subjects
        # 数据在消费者中保留的时间，已经消费的数据超过这个时间会被删除
        self.default_stream_retention_seconds = retention_seconds
        # 任务启动的时候要回放多长时间的数据
        self.replay_seconds = replay_seconds
        # 是否自动确认消息
        self.manual_ack = manual_ack
    
    def get_streamz_source(self, **kwargs):
        """生成一个streamz的source, 输入的参数是额外传递
        """
        now_timestamp = int(arrow.utcnow().to('+08:00').timestamp() * 1000)
        mock_row_num = 20
        mock_interval = 5 # s
        return Stream.from_iterable([
            {
              "kind": "deviceReport",
              "meta": {
                "accessTemplate": "newinwater",
                "device": "test_device_in",
                "deviceProduct": "newinwatre",
                "node": "sewage-dosing-chengdu",
                "nodeProduct": "BIE-Product"
              },
              "content": {
                "blink": {
                  "reqId": "776c72bd-023b-4fac-bdbd-d9fcae009200",
                  "method": "thing.property.post",
                  "version": "1.0",
                  "timestamp": now_timestamp - (mock_row_num - 1 - i) * mock_interval,
                  "properties": {
                    "test_nats_in1": i,
                    "test_nats_in2": i * 100,
                    "test_nats_in3": i * 10000,
                    "test_nats_in4": i * 1000000
                  }
                }
              }
            }
            for i in range(mock_row_num)
        ])
    
    def __str__(self) -> str:
        return json.dumps({
            "nats_url": self.nats_url,
            "subjects": self.subjects,
            "replay_seconds": self.replay_seconds,
            "manual_ack": self.manual_ack
        },  ensure_ascii=False)


class TestSoePipeline(TestCase):
    """TestKafka"""

    @classmethod
    def setUpClass(cls):
        # Start it once for the entire test suite/module
        ray.init(num_cpus=4, num_gpus=0)
        path = os.path.abspath(os.curdir)
        init_sql_file_path = path + "/../products/soe/sql/init.sql"
        #init_sql_file_path = 'streaming_infer/products/soe/sql/init.sql'
        with open(init_sql_file_path, encoding='utf-8') as fp:
            sql_str = fp.read()
        # 数据表初始化
        cls._mysql_init(sql_str=sql_str)
        # jobconfig初始化
        job_config_dict = {
            "task_type": "soe",
            "nats_url": "10.214.36.203:8221",
            "controller_url": "http://10.68.114.166:8271",
            "mysql_url": "mysql+pymysql://root:5HchceAzKWUS3ks@10.27.240.57:8436/",
            "config_db":"soe_process_optimization_ray",
            "task_fetch_interval":60,
            "log_level":20
        }
        os.environ["RAY_PARAMETERS"]=json.dumps(job_config_dict)
        job_config = JobConfig.parse_from_env()
        # superviser初始化（无需执行）
        supervisor = Supervisor.remote(
            job_config=job_config,
            task_manager=TaskManager.get_instance(job_config),
        )
        supervisor.stop_all.remote()

    @classmethod
    def _mysql_init(cls, sql_str):
        conn = sqlite3.connect(':memory:')
        #conn.executescript(sql_str)
        sql_list = cls._sql_clean(sql_str)
        logging.debug(sql_list)
        for sql in sql_list:
            logging.debug(sql)
            conn.execute(sql)

    @classmethod
    def _sql_clean(cls, sql_str):
        sql_list = []
        var_mapping = {}
        for s in re.split(r"[;]", sql_str):
            if 'INSERT' in s \
                    or 'DROP' in s \
                    or 'CREATE' in s \
                    or 'ALTER' in s:
                for k, v in sorted(var_mapping.items(), reverse=True): # 字典倒序，防止前缀重合，导致被错误赋值
                    s = s.replace(k, v)
                sql_list.append(s)
            elif 'SET' in s:
                s = s.split('SET')[-1]
                s = s.strip().split()
                var_mapping[s[0]] = s[-1]
        logging.debug(var_mapping)
        return sql_list

    @classmethod
    def tearDownClass(cls):
        ray.shutdown()

    def setUp(self):
        """setup"""
        # jobconfig初始化
        job_config_dict = {
            "task_type": "soe",
            "nats_url": "10.214.36.203:8221",
            "controller_url": "http://10.68.114.166:8271",
            "mysql_url": "mysql+pymysql://root:5HchceAzKWUS3ks@10.27.240.57:8436/",
            "config_db":"soe_process_optimization_ray",
            "task_fetch_interval":60,
            "log_level":20
        }
        os.environ["RAY_PARAMETERS"]=json.dumps(job_config_dict)
        self.job_config = JobConfig.parse_from_env()
        self.task_manager = TaskManager.get_instance(self.job_config)
        # 目标任务配置信息
        self.target_task_conf = {
            "id": "1",
            "version": 4,
            "config": {
                "model_config": {
                    "model_name": "SoeMockProcess",
                    "model_version": "1",
                    "endpoint": "10.211.18.203:8951"
                },
                "sources": [
                    {
                        "source_type": "jetstream",
                        "nats_url": "10.214.36.203:8221",
                        "subjects": [
                            "thing.defaultDeviceProduct.test_device_in.property.post"
                        ]
                    }
                ],
                "sinks": [
                    {
                        "sink_type": "http",
                        "url": "http://10.68.114.166:8271/soe/opt/controller/cmd"
                    }
                ],
                "input_config": {
                    "input_type": "timeSeries",
                    "input_span": 30,
                    "row_interval": 5,
                    "fields": [
                        {
                            "model_field": "test_model_in1",
                            "model_field_type": "float",
                            "device_id": "test_device_in",
                            "prop_id": "test_nats_in1",
                            "field_type": "float",
                            "aggregate_strategy": "mean"
                        },
                        {
                            "model_field": "test_model_in2",
                            "model_field_type": "float",
                            "device_id": "test_device_in",
                            "prop_id": "test_nats_in2",
                            "field_type": "float",
                            "aggregate_strategy": "mean"
                        }
                    ]
                },
                "output_config": {
                    "fields": [
                        {
                            "model_field": "test_model_out1",
                            "model_field_type": "float",
                            "device_id": "1",
                            "prop_id": "1",
                            "field_type": "float"
                        },
                        {
                            "model_field": "test_model_out2",
                            "model_field_type": "float",
                            "device_id": "1",
                            "prop_id": "2",
                            "field_type": "float"
                        },
                        {
                            "model_field": "timestamp",
                            "model_field_type": "int",
                            "device_id": "1",
                            "prop_id": "4",
                            "field_type": "int"
                        }
                    ]
                },
                "trigger_config": {
                    "trigger_mode": "period",
                    "trigger_interval": 5,
                    "trigger_num": None,
                    "trigger_device": None,
                    "trigger_field": None
                }
            },
            "name": "soe_1"
        }
        '''
    def test_fetch_task(self):
        """ 任务解析测试
        """
        tasks = self.task_manager.fetch_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].__dict__, self.target_task_conf)


    def test_mock_source_run_pipline(self):
        """ mock source run pipline
        """
        tasks = self.task_manager.fetch_tasks()
        task = tasks[0]
        # 使用mock Source
        task.config['sources'] = [
            {
                **src,
                "source_type": "testjetstream"
            }
            for src in task.config['sources']
        ]
        # TODO 处理mockSource的数据，并assert
'''

if __name__ == '__main__':
    unittest.main()
