#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Time    :   2023/06/15 09:28:40
@Author  :   qiupengfei 
@Contact :   qiupengfei@baidu.com
@Desc    :   
"""

import threading
from abc import ABC
from typing import Any
from threading import Thread, Event
import asyncio
from tornado.platform.asyncio import AsyncIOMainLoop
from tornado.ioloop import IOLoop
import time
import logging

from streaming_infer.tasks.task_config import InferTaskConfig
from streaming_infer.pipeline.infer_report import InferReport
from streaming_infer.pipeline.infer_handler import InferHandler
from streaming_infer.config.job_config import JobConfig

AsyncIOMainLoop().install()


class InferPipeline(ABC, Thread):
    """一个推理pipeline的基类
    """

    def __init__(self, task: InferTaskConfig, job_config: JobConfig):
        Thread.__init__(self)
        # 任务配置
        self.task =  task
        # 用于控制线程退出
        self.stop_event = Event()
        # ioloop创建，不同pipline之间隔离
        self.loop = IOLoop()
        # 推理服务调用封装
        self.infer_handler = InferHandler(
            self.task.model_config.model_name,
            self.task.model_config.model_version,
            self.task.model_config.endpoint,
            self.loop
        )
        # 作业级别的配置
        self.job_config = job_config

    def stop(self, timeout=10):
        """停止pipeline
        """
        self.stop_event.set()
    
    def start(self):
        """启动线程执行
        """
        self.setDaemon(True)
        Thread.start(self)
    
    def set_concurrency(self, concurrency: int):
        """设置并发度
        """
        self.infer_handler.concurrency = concurrency

    def get_concurrency(self):
        """获取并发度
        """
        return self.infer_handler.concurrency
    
    def run_asyncio_loop(self):
        thread = threading.Thread(target=self.loop.start)
        thread.daemon = True
        thread.start()
        try:
            while not self.stop_event.is_set():
                time.sleep(1)
        except KeyboardInterrupt:
            logging.warning("received keyboard interrupt")
        self.loop.stop()
        logging.warning("pipeline exit, Task id: %s", self.task.id)

    def run(self):
        """"启动线程执行
        """
        try:
            self.__exec__()
        except Exception as e:
            logging.exception(e)
            logging.error("start pipeline failed, Task id: %s", self.task.id)
            return
        self.run_asyncio_loop()
    
    @classmethod
    def get_all_subclasses(cls):
        """获取所有子类, 注意一定要确保在运行此函数的时候，子类已经被import到

        """
        all_subclasses = {}

        for subclass in cls.__subclasses__():
            all_subclasses[subclass.get_task_type()] = subclass
            all_subclasses.update(subclass.get_all_subclasses())

        return all_subclasses
        
    def get_merged_streamz_source(self, **kwargs):
        """生成streamz的source， 多个source会union成一个Stream
        """
        # 组合source
        source = None
        # 流默认启动
        if 'start' not in kwargs:
            kwargs['start'] = True
        if 'asynchronous' not in kwargs:
            kwargs['asynchronous'] = True
        if 'loop' not in kwargs:
            kwargs['loop'] = self.loop

        for s_conf in self.task.get_sources():
            logging.info(s_conf)
            # 这里可以判断s的类型， 以便调整get_streamz_source的参考
            # 注意consumer_name不能包含*,>,.
            ts = s_conf.get_streamz_source(consumer_name=f"streaming_infer_{str(self.task.id).replace('.', '_').replace('>', '_').replace('*', '_')}", **kwargs)
            if not source:
                source = ts
            else:
                source = source.union(ts)
        return source
    

    ### 以下为抽象方法

    def __exec__(self):
        """构建和启动pipeline， pipeline是streamz中的async协程，因此此函数只是向loop注册了事件处理函数，会直接退出。
        """
        raise NotImplementedError()

    def get_report(self) -> InferReport:
        """"获取当前pipeline的报告
        """
        raise NotImplementedError()
    
    @classmethod
    def get_task_type(cls):
        """获取任务类型
        """
        raise NotImplementedError('get_task_type is not implemented')
    