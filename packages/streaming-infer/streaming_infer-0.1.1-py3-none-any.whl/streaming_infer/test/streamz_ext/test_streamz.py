#!/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
@Time    :   2023/06/08 17:26:28
@Author  :   qiupengfei 
@Contact :   qiupengfei@baidu.com
@Desc    :   
"""
import logging
import time
import unittest
import uuid
from unittest import IsolatedAsyncioTestCase

from nats.aio.client import Client as NATS

from streaming_infer.streamz_ext.sources.jetstream import from_jetstream

logging.basicConfig(level=logging.INFO)


#class TestStreamz(TestCase):
class TestStreamz(IsolatedAsyncioTestCase):
    
    def setUp(self) -> None:
        self.NATS_URL="10.214.36.203:8221"
        self.SUBJECTS=[
            "thing.defaultDeviceProduct.test1.property.post",
            "thing.defaultDeviceProduct.test2.property.post"
        ]    
        self.nc = NATS()

    async def send_msg(self, nc, url, subject, msg):
        try:
            # 连接到NATS服务器
            await nc.connect(servers=[url])
            # 发送消息到指定主题
            await nc.publish(subject, msg.encode())
        except Exception as e:
            logging.exception(e)
        finally:
            # 关闭NATS连接
            await nc.close()
             
    async def test_streamz(self):
        """ 确保跑通，异步操作中难以断言，这里不进行断言
        """
        source = from_jetstream(
            self.NATS_URL,
            subjects=self.SUBJECTS,
            consumer_name=f"js-stream-test_{uuid.uuid1().hex[:8]}",
            asynchronous=True,
            start=True
        )

        def process_msg(msg):
            logging.info(msg.data)
            return msg.data
        stream = source.map(process_msg)
        await self.send_msg(self.nc, f"nats://{self.NATS_URL}", self.SUBJECTS[0], "test_send")
        time.sleep(10)


if __name__ == '__main__':
    unittest.main()
