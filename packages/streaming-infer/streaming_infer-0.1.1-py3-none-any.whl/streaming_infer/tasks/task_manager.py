#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Time    :   2023/06/15 09:05:11
@Author  :   qiupengfei 
@Contact :   qiupengfei@baidu.com
@Desc    :   
"""

from abc import ABC
from typing import List
from streaming_infer.tasks.task_config import InferTaskConfig
from streaming_infer.config.job_config import JobConfig

class TaskManager(ABC):
    """
    Task Manager用来处理如何从数据库或外部服务发现要运行的任务（可能会涉及某些任务要修改或停止），
    同时在Supervisor收集到任务的运行报告后，TaskManager可能会将报告的内容转化为任务执行报告为不同的应用所使用。
    TODO: 目前TaskManager只实现了发现任务这一个功能，未来还需要实现任务报告回写的功能。
    """

    def __init__(self, job_config: JobConfig):
        self.job_config = job_config

    def get_task_type(self):
        """对应的任务类型
        """
        raise NotImplementedError('task manager must implement get_task_type')

    def fetch_tasks(self) -> List[InferTaskConfig]:
        """
        获取任务列表
        :return:
        """
        raise NotImplementedError()
    
    @classmethod
    def get_instance(cls, job_config: JobConfig) -> "TaskManager":
        """
        获取任务工厂
        :param job_config:
        :return:
        """
        task_type = job_config.get_task_type()
        sub_cls = cls.get_all_subclasses()[task_type]
        return sub_cls(job_config)
    
    @classmethod
    def get_all_subclasses(cls):
        """获取所有子类, 注意一定要确保在运行此函数的时候，子类已经被import到

        """
        all_subclasses = {}

        for subclass in cls.__subclasses__():
            all_subclasses[subclass.get_task_type()] = subclass
            all_subclasses.update(subclass.get_all_subclasses())

        return all_subclasses

