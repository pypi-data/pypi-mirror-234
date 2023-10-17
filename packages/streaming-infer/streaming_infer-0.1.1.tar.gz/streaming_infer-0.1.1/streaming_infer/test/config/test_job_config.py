#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Author: liuzixiang
Date: 2023-07-21 18:35:34
LastEditors: liuzixiang
LastEditTime: 2023-07-21 18:45:52
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



class TestJobConfig(TestCase):
    """TestJobConfig"""

    @classmethod
    def setUpClass(cls) -> None:
        job_config_dict = {
            "task_type": "soe",
            "nats_url": "10.214.36.203:8221",
            "controller_url": "http://10.68.114.166:8271",
            "mysql_url": "mysql+pymysql://root:5HchceAzKWUS3ks@10.27.240.57:8436/",
            "config_db":"soe_process_optimization_ray",
            "task_fetch_interval":60,
            "log_level":20
        }

        ray.init(num_cpus=4, num_gpus=0, runtime_env={
                'env_vars': {
                    'RAY_PARAMETERS': json.dumps(job_config_dict)
                }
            }
        )

    @classmethod
    def tearDownClass(cls) -> None:
        ray.shutdown()

    def setUp(self) -> None:
        self.job_config_dict = {
            "task_type": "soe",
            "nats_url": "10.214.36.203:8221",
            "controller_url": "http://10.68.114.166:8271",
            "mysql_url": "mysql+pymysql://root:5HchceAzKWUS3ks@10.27.240.57:8436/",
            "config_db":"soe_process_optimization_ray",
            "task_fetch_interval":60,
            "log_level":20
        }

    def test_parse_from_runtimeenv(self):
        self.job_config = JobConfig.parse_from_runtimeenv()

    def test_parse_from_env(self):
        os.environ["RAY_PARAMETERS"]=json.dumps(self.job_config_dict)
        self.job_config = JobConfig.parse_from_env()