#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Time    :   2023/06/15 09:07:00
@Author  :   qiupengfei 
@Contact :   qiupengfei@baidu.com
@Desc    :   
"""

import logging
from abc import ABC
from typing import List

from .source_config import SourceConfig
from .sink_config import SinkConfig

class ModelConfig(object):
    """模型配置"""

    def __init__(self, model_name: str, model_version: str, endpoint: str = '', deploy=''):
        self.model_name =  model_name
        self.model_version =  model_version
        self.endpoint = endpoint
        self.deploy =  deploy


class TriggerConfig(object):
    """调度配置"""

    def __init__(
        self,
        trigger_mode: str,
        trigger_interval: int = None,
        trigger_num: str = None,
        trigger_device: str = None,
        trigger_field: str = None
    ):
        self.trigger_mode =  trigger_mode
        self.trigger_interval =  trigger_interval
        self.trigger_num =  trigger_num
        self.trigger_device =  trigger_device
        self.trigger_field =  trigger_field


class InferTaskConfig(ABC):
    """一个任务的配置信息. 配置文件的默认格式为：
    task_type: "任务类型，对应InferTaskConfig.task_type"
    sources: # 可以有多个数据源
        - source_type: jetstream   # 只有这一个是必须的，其他的根据不同的source_type不一样
          nats_url: xxx
          subjects:
            - subj1
            - subj2
    sinks: # 可以有多个sink
        - sink_type: mysql
          url:  mysql://localhost:3306/test
    model_config:
        model_name: "模型名称"
        endpoint: "endpoint url"
        deploy: "模型服务配置"
    # 其他配置可以自由定义

    """
    # 任务类型， 用来生成不同的任务对象
    TASK_TYPE = "infer_base"

    def __init__(self, id: str, version: str, config: dict):
        # 任务的唯一ID
        self.id = id
        # 任务的版本号
        self.version = version
        # 任务的配置
        self.config = config

    @property
    def model_config(self) -> ModelConfig:
        """获取模型配置"""
        return ModelConfig(**self.config["model_config"])

    @property
    def trigger_config(self) -> TriggerConfig:
        """获取调度配置
        """
        return TriggerConfig(**self.config["trigger_config"])

    def get_sources(self) -> List[SourceConfig]:
        """获取任务的sources
        """
        sources = []
        for cfg in self.config.get('sources', []):
            logging.info(cfg)
            sources.append(SourceConfig.get_instance(**cfg))
        return sources
    
    def get_sinks(self) -> List[SinkConfig]:
        """获取任务的sinks
        """
        sinks = []
        for cfg in self.config.get('sinks', []):
            sinks.append(SinkConfig.get_instance(**cfg))
        return sinks 
    
