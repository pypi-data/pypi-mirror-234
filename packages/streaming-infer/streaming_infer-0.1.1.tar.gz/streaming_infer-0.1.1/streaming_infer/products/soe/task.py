#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Time    :   2023/06/16 16:44:09
@Author  :   qiupengfei 
@Contact :   qiupengfei@baidu.com
@Desc    :   
"""

from streaming_infer.tasks.task_config import InferTaskConfig

# hack默认的ray job 配置
import os
import json

'''
os.environ['RAY_PARAMETERS'] = json.dumps(
    {
        "task_type": "soe",
        "nats_url": "10.31.76.16:8221", 
        "controller_url": "10.27.37.65:8080"
    }, ensure_ascii=False
)
'''


class InputFieldConfig(object):
    """ 输入字段配置 """

    def __init__(self, model_field: str, model_field_type: str, device_id: str, prop_id: str, field_type: str, aggregate_strategy: str, fill_strategy: str='none'):
        self.model_field = model_field
        self.model_field_type = model_field_type
        self.device_id = device_id
        self.prop_id = prop_id
        self.field_type = field_type
        self.aggregate_strategy = aggregate_strategy
        self.fill_strategy = fill_strategy

    @property
    def key(self):
        return str(self.device_id) + str(self.prop_id)


class InputConfig(object):
    """ 输入配置 """

    def __init__(
        self,
        input_type: str,
        input_span: int,
        row_interval: int,
        fields: dict
    ):
        self.input_type = input_type
        self.input_span = input_span
        self.row_interval = row_interval
        self.fields = [ InputFieldConfig(**field) for field in fields ] 


class OutputFieldConfig(object):
    """ 输出字段配置 """

    def __init__(self,  model_field: str, model_field_type: str, device_id: str, prop_id: str, field_type: str):
        self.model_field = model_field
        self.model_field_type = model_field_type
        self.device_id = device_id
        self.prop_id = prop_id
        self.field_type = field_type


class OutputConfig(object):
    """ 输出配置 """

    def __init__(
        self,
        fields: dict
    ):
        self.fields = [ OutputFieldConfig(**field) for field in fields ]


class SoeTaskConfig(InferTaskConfig):
    """任务配置的示例"""

    TASK_TYPE = "soe"

    def __init__(
        self,
        id: str,
        name: str,
        version: str,
        config: dict
    ):
        super().__init__(id, version, config)
        self.name = name

    def model_name(self) -> str:
        return self.model_config.model_name
    
    def endpoint(self) -> str:
        return self.model_config.endpoint
    
    def get_input_config(self) -> InputConfig:
        """获取输入配置
        """
        return InputConfig(**self.config["input_config"])

    def get_output_config(self) -> InputConfig:
        """获取输入配置
        """
        return OutputConfig(**self.config["output_config"])
    
    
    



