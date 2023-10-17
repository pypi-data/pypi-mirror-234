#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Time    :   2023/06/16 17:15:23
@Author  :   qiupengfei 
@Contact :   qiupengfei@baidu.com
@Desc    :   
"""
from streaming_infer.streamz_ext.sources.jetstream import from_jetstream
import json

class SourceConfig:
    """数据源配置
    """

    def get_streamz_source(self, **kwargs):
        """生成一个streamz的source, 输入的参数是额外传递给streamz的参数
        """
        raise NotImplementedError()
    
    @classmethod
    def get_all_subclasses(cls):
        """获取所有子类, 注意一定要确保在运行此函数的时候，子类已经被import到

        """
        all_subclasses = {}

        for subclass in cls.__subclasses__():
            all_subclasses[subclass.SOURCE_TYPE] = subclass
            all_subclasses.update(subclass.get_all_subclasses())

        return all_subclasses
    
    @classmethod
    def get_instance(cls, **kwargs):
        sub_cls = cls.get_all_subclasses().get(kwargs['source_type'])
        return sub_cls(**kwargs)



class JetStreamSourceConfig(SourceConfig):

    SOURCE_TYPE = "jetstream"

    def __init__(self, nats_url: str, subjects: list, 
                 retention_seconds=3600, 
                 replay_seconds=0,
                 manual_ack=False, 
                 **kwargs):
        # nats连接url， 认证方式不在这里配置，如果需要认证需要从job_config中获取
        self.nats_url = nats_url
        # 要监听的主题
        self.subjects =  subjects
        # 数据在消费者中保留的时间，已经消费的数据超过这个时间会被删除
        self.default_stream_retention_seconds = retention_seconds
        # 任务启动的时候要回放多长时间的数据
        self.replay_seconds = replay_seconds
        # 是否自动确认消息
        self.manual_ack = manual_ack
    
    def get_streamz_source(self, **kwargs):
       """生成一个streamz的source, 输入的参数是额外传递
       """
       return from_jetstream(
           nats_url=self.nats_url,
           subjects=self.subjects,
           default_stream_retention_seconds=self.default_stream_retention_seconds,
           replay_seconds=self.replay_seconds,
           manual_ack=self.manual_ack,
           **kwargs
       )
    
    def __str__(self) -> str:
        return json.dumps({
            "nats_url": self.nats_url,
            "subjects": self.subjects,
            "replay_seconds": self.replay_seconds,
            "manual_ack": self.manual_ack
        },  ensure_ascii=False)