#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Time    :   2023/06/15 11:02:25
@Author  :   qiupengfei 
@Contact :   qiupengfei@baidu.com
@Desc    :   
"""


class InferReport:
    """推理服务调用报告
    """

    def record_request(self, model_name: str, endpoint: str, duration: float, status_code: int = 200):
        """记录一个请求的信息
        """
        pass