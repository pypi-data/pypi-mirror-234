#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Time    :   2023/06/15 09:17:06
@Author  :   qiupengfei 
@Contact :   qiupengfei@baidu.com
@Desc    :   
"""
from .tasks.task_config import InferTaskConfig
from typing import Dict, Iterable, Any, List
from threading import Thread
from streaming_infer.pipeline.factory import PipelineFactory
from streaming_infer.pipeline.pipeline import InferPipeline
import logging
from streaming_infer.config.job_config import JobConfig
import ray
import logging
logging.basicConfig(level=logging.INFO, 
                    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s', 
                    datefmt='%m-%d %H:%M:%S')

@ray.remote
class WorkerActor:

    def __init__(self, job_config: JobConfig):
        logging.basicConfig(level=job_config.get_log_level(), 
                            format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s', 
                            datefmt='%m-%d %H:%M:%S')

        # 已经使用的槽位数
        self.used_slots = 0

        # 任务配置
        self.tasks: Dict[str, InferTaskConfig] = {}
        # 任务运行的线程
        self.pipelines: Dict[str, InferPipeline] = {}

        # 作业级别的配置
        self.job_config = job_config
    
    @property
    def capacity(self) -> int:
        """
        获取允许运行多少个任务
        """
        return self.job_config.worker_capacity

    def has_avaliable_slot(self) -> bool:
        """是否还可以容纳更多的任务
        """
        return self.used_slots < self.capacity

    def add_task(self, task: InferTaskConfig):
        """添加一个任务

        Args:
            task (InferTaskConfig): _description_
        """
        if not self.has_avaliable_slot():
            raise ValueError(
                "no slots avaliable"
            )
        self.tasks[task.id] = task
        ppl = PipelineFactory.get_pipeline(task, self.job_config)
        self.pipelines[task.id] = ppl
        ppl.start()

    def get_pipeline(self, task_id) -> InferPipeline:
        return self.pipelines[task_id]

    def remove_task(self, task_id: str) -> bool:
        """移除一个任务
        """
        # 尝试停止pipeline
        try:
            pipeline = self.get_pipeline(task_id)
            pipeline.stop()
        except Exception as e:
            logging.exception(e)
            return False
        else:
            self.pipelines.pop(task_id)
            self.tasks.pop(task_id)
            return True
        
    def set_concurrency(self, task_id, concurrency: float):
        """设置一个任务的并发度
        """
        ppl = self.get_pipeline(task_id)
        ppl.set_concurrency(concurrency=concurrency)

    def get_report(self) -> List[Any]:
        """获取所有的任务的report
        """
        return [
            ppl.get_report() for ppl in self.pipelines.values()
        ]
