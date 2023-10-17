#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Time    :   2023/06/16 17:01:14
@Author  :   qiupengfei 
@Contact :   qiupengfei@baidu.com
@Desc    :   
"""

from streaming_infer.pipeline.pipeline import InferPipeline
from .task import ExampleTaskConfig
from nats.aio.msg import Msg
from streaming_infer.streamz_ext.core import long_time_window
import json
import arrow
import logging


class DataItem(object):
    """转换的内部对象
    """

    def __init__(self, body):
        try:
            self.body = json.loads(body)
        except  Exception as e:
            logging.exception(e)
            self.body = {}


class ExampleInferPipline(InferPipeline):
    """
    一个流水线的样例
    """

    @classmethod
    def get_task_type(cls):
        """获取任务类型"""
        return ExampleTaskConfig.TASK_TYPE
    
    def __exec__(self):
        """运行流水线
        """
        logging.info('example pipeline start')
        # 从配置文件中获取数据源
        source = self.get_merged_streamz_source()

        # 对消息进行转换， 这里一般是做数据结构的转换
        stream = source.map(lambda msg: DataItem(msg.data)).filter(lambda x: x.body)
        # 使用时间窗口
        # 窗口中只保留事件时间在60秒nei的数据， 毎10秒钟会触发一次计算将数据传递给下游
        stream = stream.long_time_window(evict_time=60, evict_by_event_time=True,
                                        event_time_func=lambda x: arrow.get(x.body.get('time')).to('+08:00'), trigger_interval=10
                                    )
        # 以下这几步没有实现， 直接输出了结果
        # 1. 用map算子将窗口得到的list转换成模型的输入
        # 2. 用map算子调用推理
        # 3. 输出推理结果
        stream.sink(print)
        