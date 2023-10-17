#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Time    :   2023/06/15 09:25:24
@Author  :   qiupengfei 
@Contact :   qiupengfei@baidu.com
@Desc    :   
"""

from streaming_infer.tasks.task_config import InferTaskConfig
from streaming_infer.pipeline.pipeline import InferPipeline
from streaming_infer.config.job_config import JobConfig


class PipelineFactory:

    @classmethod
    def get_pipeline(cls, task: InferTaskConfig, job_config: JobConfig) -> InferPipeline:
        """根据任务类型生成对应的pipeline

        Args:
            task (InferTaskConfig): _description_
            job_config (JobConfig): 作业级别的配置信息
        """
        return InferPipeline.get_all_subclasses()[task.TASK_TYPE](task, job_config)