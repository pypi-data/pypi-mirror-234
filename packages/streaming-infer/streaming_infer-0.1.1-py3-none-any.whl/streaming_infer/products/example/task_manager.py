#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Time    :   2023/06/16 16:49:49
@Author  :   qiupengfei 
@Contact :   qiupengfei@baidu.com
@Desc    :   
"""

from typing import List
from streaming_infer.tasks.task_manager import TaskManager
from .task import ExampleTaskConfig


class ExampleTaskMonitor(TaskManager):
    """一个示例
    """

    def fetch_tasks(self) -> List[ExampleTaskConfig]:
        """

        Returns:
            List[ExampleTaskConfig]: _description_
        """
        return [
            ExampleTaskConfig("ex_1", "v1", {
                'model_config': {
                    "model_name": "example_1",
                },
                "sources": [
                    {
                        "source_type": "jetstream",   # 只有这一个是必须的，其他的根据不同的source_type不一样
                        "nats_url": self.job_config.get_nats_url(),
                        "subjects": ["js-test-7"],
                        'replay_seconds': 86400*10
                    }
                ]
            }),
            ExampleTaskConfig("ex_2", "v1", {

                'model_config': {
                    "model_name": "example_2",
                },
                "sources": [
                    {
                        "source_type": "jetstream",   # 只有这一个是必须的，其他的根据不同的source_type不一样
                        "nats_url": self.job_config.get_nats_url(),
                        "subjects": ["js-test-7"]
                    }
                ]
            })
        ]
    
    @classmethod
    def get_task_type(self):
        return ExampleTaskConfig.TASK_TYPE