#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Author: liuzixiang
Date: 2023-06-29 17:35:08
LastEditors: liuzixiang
LastEditTime: 2023-07-18 17:42:17
Description: 
"""
import logging

import requests
from streamz.sinks import Sink, Stream


@Stream.register_api()
class sink_to_http(Sink):
    """写入http的类 会在streamz中注册成函数 
    TODO 后续可能需要在构造函数中创建client，把认证的问题处理掉。
    """

    def __init__(
        self,
        upstream,
        method: str,
        url: str,
        success_status_code: int=200,
        params: str=None,
        headers: str=None,
        timeout: str=None,
        on_error: callable=None,
        **kwargs
    ):
        super().__init__(upstream, **kwargs)
        self.method = method
        self.url = url
        self.success_status_code = success_status_code
        self.params = params
        self.headers = headers
        self.timeout = timeout
        self.on_error = on_error


    def update(self, x: list, who=None, metadata=None):
        """发送数据到http
        """
        try:
            with requests.session() as session:
                for req_body in x:
                    logging.info("%s %s to %s", self.method, req_body, self.url)
                    res = session.request(
                        method=self.method,
                        url=self.url,
                        params=self.params,
                        data=req_body,
                        headers=self.headers,
                        timeout=self.timeout,
                    )
                    logging.info(res)
                    logging.info(res.text)
                    if res.status_code != self.success_status_code:
                        raise Exception(res.text)
            self._emit(x, metadata=metadata)
        except Exception as ex:
            logging.error(ex)
            if callable(self.on_error):
                self.on_error(ex)
        