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
        "task_type": "example",
    }, ensure_ascii=False
)
'''


class ExampleTaskConfig(InferTaskConfig):
    """任务配置的示例"""

    TASK_TYPE = "example"

    def model_name(self) -> str:
        return "example_model"
    
    def endpoint(self) -> str:
        return "example_endpoint"
    
    
    



