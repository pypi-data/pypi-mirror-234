#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Time    :   2023/06/16 11:42:30
@Author  :   qiupengfei 
@Contact :   qiupengfei@baidu.com
@Desc    :   
"""

from argparse import ArgumentParser
import ray
from streaming_infer.config.job_config import JobConfig
from streaming_infer.supervisor import Supervisor
from streaming_infer.tasks.task_manager import TaskManager
# 注意：虽然这个代码没有被使用到，但是不可以删除， 因为有多个工厂函数依赖了获取类的所有子类， 
# 而子类如果没有被import到是无法获取的。这个设计方法提高了理解难度，单好处是在新增子类实现的时候不需要调整products目录以外的代码。
import streaming_infer.products

import time
import logging


def main(args):
    """ray driver入口函数"""
    # TODO： 添加namespace
    ray.init(local_mode=args.local_mode)

    job_config = JobConfig.parse_from_runtimeenv()

    actor = Supervisor.remote(
        job_config=job_config,
        task_manager=TaskManager.get_instance(job_config),
    )
    logging.info('supervisor actor created')
    try:
        while True:
            time.sleep(1)
            #print(ray.get(actor.get_report.remote()))
            # TODO: 检查supervisor的运行状态， 判断是否要退出job， 退出的处理工作可能与except中类似
    except KeyboardInterrupt:
        # TODO：正常退出，清理所有的task, 可能需要用at_exit来注册，需要测试一下
        pass

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--local_mode', help='local_mode', default=False)
    args = parser.parse_args()
    main(args)