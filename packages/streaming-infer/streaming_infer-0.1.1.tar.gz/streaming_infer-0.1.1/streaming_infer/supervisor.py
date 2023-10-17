#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Time    :   2023/06/15 09:00:43
@Author  :   qiupengfei 
@Contact :   qiupengfei@baidu.com
@Desc    :   
"""
import json
import logging
import ray
import threading
import time
from typing import Dict, List, Tuple, Any, Iterable

from .tasks.task_config import InferTaskConfig
from streaming_infer.tasks.task_manager import TaskManager
from streaming_infer.config.job_config import JobConfig
from streaming_infer.worker import WorkerActor


@ray.remote
class Supervisor:

    def __init__(self, job_config: JobConfig, task_manager: TaskManager):
        logging.basicConfig(level=job_config.get_log_level(),
                            format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s', 
                            datefmt='%m-%d %H:%M:%S')
        # 任务工厂类
        self.task_manager = task_manager
        # 全局任务配置
        self.job_config = job_config
        # 所有的worker
        self.workers = []
        # 任务id与任务配置的对应关系
        self.tasks: Dict[str, InferTaskConfig] = {}
        # 任务id与worker的对应关系
        self.task_workers: Dict[str, WorkerActor] = {}
        # 每个worker可以分配几个任务
        self.worker_capacity = job_config.worker_capacity

        # 新启动的时候接管worker的状态
        self.find_orphan_workers()

        # 启动线程周期性获取worker的报告
        self.task_fetcher_thread = threading.Thread(target=self._task_fetcher_thread_func)
        self.task_fetcher_thread.setDaemon(True)
        self.task_fetcher_thread.start()

        # TODO: 启动线程周期性获取报告，注意要添加超时机制

    def remove_task(self, task_id):
        worker = self.task_workers[task_id]
        ret = ray.get(worker.remove_task.remote(task_id))
        if not ret:
            logging.error("remove task failed, task_id: %s", task_id)
        else:
            logging.debug("remove task success, task_id: %s", task_id)
            if task_id in self.tasks:
                del self.tasks[task_id]
            if task_id in self.task_workers:
                del self.task_workers[task_id]

    def update_task(self, task: InferTaskConfig):
        """更新任务
        """
        self.remove_task(task.id)
        self.add_task(task)
    
    def stop_all(self):
        """回收所有的worker， 停止任务
        """
        for worker in self.workers:
            ray.kill(worker)
    
    def add_task(self, task: InferTaskConfig):
        """新增任务
        """
        for worker in self.task_workers.values():
            ret = ray.get(worker.has_avaliable_slot.remote())
            if ret:
                logging.info('find available slot for task: %s', task.id)
                worker.add_task.remote(task)
                self.tasks[task.id] = task
                self.task_workers[task.id] = worker
                return 
        worker = WorkerActor.remote(job_config=self.job_config)
        worker.add_task.remote(task)
        self.tasks[task.id] = task
        self.task_workers[task.id] = worker
        self.workers.append(worker)
        logging.info('worker created for task %s', task.id)      
    
    def _task_fetcher_thread_func(self):
        """周期性监控任务更新
        """
        while True:
            self.fetch_tasks()

            # 休眠一会继续扫描
            time.sleep(self.job_config.get_conf('task_fetch_interval', 60))
    
    def fetch_tasks(self):
        """监控任务更新
        """
        logging.info('begin to fetch tasks')
        # 新的任务
        tasks = self.task_manager.fetch_tasks()
        for task in tasks: logging.info(task.__dict__)
        # 当前的任务ID列表
        current_taskids = set(self.tasks.keys())
        # 先找到已经停止的任务
        new_taskids = set([t.id for t in tasks])
        removed_taskids = current_taskids - new_taskids
        # 停止所有的任务
        for task_id in removed_taskids:
            self.remove_task(task_id)
        
        # 添加或更新任务
        for task in tasks:
            if task.id not in self.tasks:
                # 新任务
                self.add_task(task)
            else:
                old_task = self.tasks[task.id]
                if task.version != old_task.version:
                    # 任务更新
                    self.update_task(task)

    def find_orphan_workers(self):
        """找到ray集群中失联的worker， 仅在supervisor启动时执行
           worker的命名使用固定模式加序号，这样可以简单的顺序扫描来找到所有的worker。
           程序启动的时候对于排序靠后的worker如果没有被任务使用，会释放掉，但保证前面连续的序号都有worker
        """
        # TODO:
        pass
        #raise NotImplementedError()
    
    def get_report(self):
        """获取任务执行报告信息。
        1. 遍历所有的worker， 获取所有任务的报告信息
        """
        # raise NotImplementedError()
        return ''
