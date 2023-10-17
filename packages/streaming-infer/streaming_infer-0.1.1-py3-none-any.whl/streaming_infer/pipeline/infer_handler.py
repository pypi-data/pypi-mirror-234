#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Time    :   2023/06/15 09:44:33
@Author  :   qiupengfei
@Contact :   qiupengfei@baidu.com
@Desc    :
"""
import inspect
from tornado.queues import Queue
import logging
import time
import asyncio
from tritonv2.client_factory import TritonClientFactory
from tritonv2.client_factory import TritonHTTPClient
from streaming_infer.pipeline.infer_report import InferReport
from streamz.core import Stream


class InferRequest:
    """一个推理请求
    """

    def __init__(self, callback=None, on_error=None, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        # 推理服务调用成功的回调函数，输入参数是推理client的返回
        self.callback = callback
        # 推理服务调用失败的回调, on_error的签名是
        # def on_error(request, exception):
        self.on_error = on_error


class InferHandler:
    """推理调用管理， 通过async来调用推理服务
    """

    def __init__(self, model_name: str, model_version: str, endpoint: str, ioloop=None, concurrency: int=10,
                    retry_delay: float=3, retry_times: int = 3,
                    min_delay = 0.01, max_delay = 60.0):
        # 模型名称
        self.model_name = model_name
        # 模型版本
        self.model_version = model_version
        # 模型对应的endpoint名称
        self.endpoint = endpoint
        # 最大并发量
        self.concurrency = concurrency
        # retry次数
        self.retry_times = retry_times if retry_times > 0 else 0
        # 重试间隔
        self.retry_delay =  retry_delay if retry_delay > 0 else 0

        # event loop
        self.ioloop = ioloop
        # 缓冲队列， 目前队列大小设置的1， 只有前一个请求发出去了，下一个请求才能进来
        self._queue = Queue(maxsize=1)

        # 推理的client
        self._client = self.get_client(self.model_name, self.endpoint)
        # 初始延迟0
        self.delay = 0
        # 两次请求最小延迟
        self.min_delay = min_delay
        # 两次请求的最大延迟
        self.max_delay = max_delay

        # 推理请求报告信息
        self.report =  InferReport()
        self.ioloop.add_callback(self._run_infer_loop)

    def get_and_pop_report(self) -> InferReport:
        """获取推理报告, 并生成一个新的推理报告
        """
        old_report = self.report
        self.report = InferReport()
        return old_report

    def get_client(self, model_name: str, endpoint: str):
        """获取推理client, 这里的实现方式是调用windmill的sdk去获取推理client。 假设已经有endpoint url了。
           或许以后还要传入endpoint的类型，才能确定要启动哪种client.
           # TODO 根据不同类型，获取不同的client
        """
        return TritonClientFactory.create_http_client(server_url=endpoint)

    def get_inputs_and_outputs_detail(self):
        """ 获取模型描述
        """
        return self._client.get_inputs_and_outputs_detail(
            model_name=self.model_name,
            model_version=self.model_version
        )

    async def infer(self, _callback=None, on_error=None, *args, **kwargs):
        """infer的async版本, 在推理完成后会调用callback
            推理调用入口，根据输入的参数调用推理服务，还没有想好要不要在这里进行输入输出的处理
        """
        await self._queue.put(InferRequest(_callback, on_error, *args, **kwargs))
    
    async def _run_infer_loop(self):
        while True:
            request = await self._queue.get()
            self.ioloop.add_callback(self._do_infer, request)

            # 等待一个延迟再发送下一个请求
            await asyncio.sleep(self.delay)

    async def _do_infer(self, request: InferRequest):
        """调用推理服务

        Args:
            request (InferRequest): _description_
        """
        latency = 0
        # 请求失败
        failed = False
        infer_result = None
        try:
            start_time = time.time()
            if inspect.iscoroutinefunction(self._client.model_infer):
                infer_result = await self._client.model_infer(
                    self.model_name, *request.args,
                    model_version=self.model_version, **request.kwargs
                )
            else:
                infer_result = self._client.model_infer(
                    self.model_name, *request.args,
                    model_version=self.model_version, **request.kwargs
                )
            # 执行推理的回调函数
            end_time = time.time()
            latency = end_time - start_time
            self.report.record_request(self.model_name, self.endpoint, latency, status_code=200)
        except Exception as e:
            logging.exception(e)
            failed = True
            # TODO: 获取真实错误代码
            self.report.record_request(self.model_name, self.endpoint, latency, status_code=500)
            # 错误处理回调
            if callable(request.on_error):
                self.ioloop.add_callback(request.on_error, request, e)
        finally:
            self.ioloop.add_callback(request.callback, infer_result)
        # 调整推理的调用间隔
        self.delay = self._adjust_delay(self.delay, latency, failed)

    def _adjust_delay(self, delay, latency, failed):
        """获取下一次发送请求的延迟
        参考scrapy的设计： https://github.com/scrapy/scrapy/blob/master/scrapy/extensions/throttle.py
        """
        if failed:
            # 请求失败, 不调整延迟， 因为请求失败的时候通常延迟很小，如果调整可能会导致并发增加。
            # 这时候可能不仅不能调低延迟，还需要调高延迟
            return delay
        # 目标延迟计算
        # If a server needs `latency` seconds to respond then
        # we should send a request each `latency/N` seconds
        # to have N requests processed in parallel
        target_delay = latency / self.concurrency

        # Adjust the delay to make it closer to target_delay
        new_delay = (delay + target_delay) / 2.0

        # If target delay is bigger than old delay, then use it instead of mean.
        # It works better with problematic sites.
        new_delay = max(target_delay, new_delay)

        # Make sure self.mindelay <= new_delay <= self.max_delay
        new_delay = min(max(self.min_delay, new_delay), self.max_delay)

        delay = new_delay
        return delay


@Stream.register_api()
class async_infer(Stream):
    """异步执行推理任务的算子

    Example:
        # 上游的算子输出的元素是InferHandler.infer的参数， 是一个tuple (args, kwargs, ext)
        stream = stream.async_infer(self.infer_handler)
    """
    def __init__(self, upstream, handler: InferHandler, on_error=None, **kwargs):
        self.handler = handler
        self.on_error = on_error
        # this is one of a few stream specific kwargs
        self._emited = []

        Stream.__init__(self, upstream, **kwargs)

    def update(self, x, who=None, metadata=None):
        args, kwargs = x
        kwargs = kwargs or {}
        self._retain_refs(metadata)

        def cb(metadata):
            def f(result):
                if result is not None:
                    tmp = self._emit(result, metadata=metadata)
                    self._emited.extend(tmp)
                self._release_refs(metadata)
            return f
        try:
            kwargs['_callback'] = cb(metadata)
            if self.on_error:
                kwargs['on_error'] = self.on_error
            self.loop.add_callback(self.handler.infer, *args, **kwargs)
        except Exception as e:
            raise
        else:
            tmp = self._emited
            self._emited = []
            return tmp



