#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Time    :   2023/06/16 17:44:34
@Author  :   qiupengfei 
@Contact :   qiupengfei@baidu.com
@Desc    :   
"""


class SinkConfig:
    """数据汇配置
    """

    def get_streamz_sink(self, **kwargs):
        """生成一个streamz的sink, 输入的参数是额外传递给streamz的参数
        """
        raise NotImplementedError()
    
    @classmethod
    def get_all_subclasses(cls):
        """获取所有子类, 注意一定要确保在运行此函数的时候，子类已经被import到

        """
        all_subclasses = {}

        for subclass in cls.__subclasses__():
            all_subclasses[subclass.SINK_TYPE] = subclass
            all_subclasses.update(subclass.get_all_subclasses())

        return all_subclasses
    
    @classmethod
    def get_instance(cls, **kwargs):
        """
        获取实例
        """
        sub_cls = cls.get_all_subclasses().get(kwargs['sink_type'])
        return sub_cls(**kwargs)


class HttpSinkConfig(SinkConfig):

    SINK_TYPE = "http"

    def __init__(
        self, 
        url: str, 
        **kwargs
    ):
        # 控制器URL
        self.url = url