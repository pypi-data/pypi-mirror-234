#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Time    :   2023/06/21 10:00:32
@Author  :   qiupengfei 
@Contact :   qiupengfei@baidu.com
@Desc    :   
"""
from streaming_infer.config.job_config import JobConfig
from streaming_infer.tasks.task_manager import TaskManager
from argparse import ArgumentParser
from streaming_infer.pipeline.factory import PipelineFactory
# 同main.py，这一行代码虽然没有被使用， 但是不可以删除
import streaming_infer.products
import logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s', 
                    datefmt='%m-%d %H:%M:%S')

def get_args():
    """命令行参数解析
    """
    parser = ArgumentParser()
    parser.add_argument('--id', help='task id', required=True)
    parser.add_argument('--job-config', dest='job_config_file', help='作业配置文件， 如果不提供则从环境变量获取')
    return parser.parse_args()


def main():
    """本地测试的入口函数
    """
    args = get_args()
    if args.job_config_file:
        job_config = JobConfig.parse_from_yaml(args.job_config_file)
    else:
        job_config = JobConfig.parse_from_env()

    # 找到指定的task
    task_manager = TaskManager.get_instance(job_config)
    tasks = task_manager.fetch_tasks()
    task = None 
    for t in tasks:
        if t.id == args.id:
            task = t
            break
    if not task:
        raise ValueError('task not found')

    # 直接创建pipeline
    ppl = PipelineFactory.get_pipeline(task, job_config)
    ppl.start()

    ppl.join()

if __name__ == '__main__':
    main()

