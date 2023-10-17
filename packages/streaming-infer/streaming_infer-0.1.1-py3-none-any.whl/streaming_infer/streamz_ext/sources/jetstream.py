#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Time    :   2023/06/08 14:53:20
@Author  :   qiupengfei 
@Contact :   qiupengfei@baidu.com
@Desc    :   
"""


from streamz.sources import Source, RefCounter
import nats
import nats.js.errors as jserrors
from nats.js.api import AckPolicy, DeliverPolicy, RetentionPolicy, ConsumerConfig
import nats.js.client as jsclient
import nats.js.errors as nats_errors
from typing import List, Optional
import logging
import tornado.gen as gen
import asyncio.exceptions
import datetime
import time

class from_jetstream(Source):
    """Fetch message from nats jetstream
    """
    def __init__(self, 
                 nats_url: str,
                 subjects: List[str],
                 consumer_name: str,
                 stream_name="__streamz", 
                 default_stream_retention_seconds=3600, 
                 ack_policy=AckPolicy.EXPLICIT,
                 replay_seconds=0,
                 ack_wait=3600*24,
                 manual_ack=True,
                 run_in_thread=False,
                 **kwargs):
        """初始化
        
        Args:
            nats_url (str): nats 地址
            subjects (List[str]): 需要订阅的主题列表
            consumername  (str): consumer名称, 不能重复. Defaults to "".
            stream_name  (str, optional): stream名称. Defaults to "".
            default_stream_retention_seconds (int, optional): 数据在stream中最多保存多长时间. Defaults to 3600.
            replay-seconds (int, optional): 消费者要回放多长时间的数据. Defaults to 0.
            ack_policy (str, optional): ack policy, 默认每条消息都要确认. Defaults to AckPolicy.EXPLICIT.
            ack_wait  (int, optional): 服务端在收不到ack重新发送消息的时间. Defaults to 3600*24.
            manual_ack (bool, optional): 是否需要手动ack，如果不用手动ack则消息发送给下游直接ack. Defaults to True.
        """
        self.nats_url = nats_url
        self.subjects = subjects
        # 流的名字， 注意：
        # 1. nats中stream有点类似database的概念，一个subject只能属于一个stream，因此stream一般不能在单个程序中创建，会导致出现'subjects overlap with an existing stream'的错误。
        # 2. 关于如何管理stream，可以参考https://github.com/nats-io/nats-server/issues/3935。 更推荐的方法应该是使用ncak来管理。 暂时为了不引入复杂度，可以手工在nats中创建一个接收全部subject的stream。 如果有拆分stream的需求，则需要手工指定stream
        self.stream_name = stream_name
        # jetstream连接
        self.js = None 
        # 消费者
        #self.consumers = []
        self.consumer_name = consumer_name
        self.consumers: List[jsclient.JetStreamContext.PullSubscription] = []
        self.default_stream_retention_seconds = default_stream_retention_seconds
        self.ack_policy = ack_policy
        self.replay_seconds = replay_seconds
        self.ack_wait = ack_wait

        # 将消费者放到线程中执行，防止cpu密集型消费者导致nats消费者阻塞
        self.run_in_thread = run_in_thread

        self.manual_ack = manual_ack

        # 消息接收和ack计数
        self._msg_received_count = 0
        self._msg_ack_count = 0

        super().__init__(**kwargs)
    
    async def upsert_stream(self, js: jsclient.JetStreamContext, stream: str, subject: str):
        """创建一个新的stream或将subject加入已有的stream订阅中
        """
        # 尝试获得已经存在的stream的config
        stream_info = None
        try:
            stream_info = await js.stream_info(stream)        
        except jserrors.NotFoundError:
            pass
        
        # stream不存在， 直接创建
        if not stream_info:
            await self.js.add_stream(name=self.stream_name, subjects=self.subjects, retention=RetentionPolicy.LIMITS, max_age=self.default_stream_retention_seconds)
        else:
            # 已经存在，将subject添加到stream中
            subjects = stream_info.config.subjects or []
            subjects.append(subject)
            await self.js.update_stream(name=self.stream_name, subjects=subjects, config=stream_info.config)

    async def connect(self):
        """连接jetstream
        """
        logging.info('Connect to nats jetstream')
        nc = await nats.connect(self.nats_url)
        self.js = nc.jetstream()
        # 1. 遍历所有的subject，每个subject是一个consumer
        # 2. 检查subject是否存在对应的stream，如果存在则直接创建消费者，否则若stream不为空，则创建对应的stream或将subject添加到已经存在的stream中。
        for subject in self.subjects:
            # 拉模式创建消费者，推模式的问题是不太好控制反压
            config = ConsumerConfig(
                ack_wait=self.ack_wait,
                ack_policy=self.ack_policy
            )
            # 先获取subject对应的stream
            try:
                stream_name = await self.js.find_stream_name_by_subject(subject)
                logging.info('found existed stream %s for subject %s', stream_name, subject)
            except:
                logging.info('subject %s not bounded to stream, bound it to %s', subject, self.stream_name)
                # stream不存在， 将subject加入到默认stream中
                await self.upsert_stream(self.js, self.stream_name, subject)
                stream_name = self.stream_name

            # 消费者和subject对应，一个subject只会有一个消费者
            consumer_name = f'{self.consumer_name}_{subject.replace(".", "_").replace(">", "#").replace("*", "x")}'
            # 如果设置了回放， 那么不需要创建持久化的消费者，否则需要创建持久化的消费者
            if self.replay_seconds > 0:
                config.deliver_policy = DeliverPolicy.BY_START_TIME
                # TODO: 没有考虑时区问题，不确定nats如何处理时区
                # 这里有个坑， opt_start_time声明的是int，实际上应该传入rfc3389格式
                config.opt_start_time = (datetime.datetime.utcnow() - datetime.timedelta(seconds=self.replay_seconds)).isoformat() + 'Z'
                #int(time.time() - self.replay_seconds) * 1000
                try:
                    res = await self.js.delete_consumer(stream_name, consumer_name)
                except jserrors.NotFoundError as e:
                    pass
                else:
                    logging.info('remove consumer %s from stream %s,  ret: %s', consumer_name, stream_name, res)
                consumer = await self.js.pull_subscribe(subject, stream=stream_name, durable=consumer_name, config=config)
            else:
                consumer = await self.js.pull_subscribe(subject, stream=stream_name, durable=consumer_name, config=config)
            logging.info('consumer created for %s', subject)
            self.consumers.append(consumer)
            self.loop.add_callback(self.consume, consumer)
    
    async def consume(self, consumer: jsclient.JetStreamContext.PullSubscription):
        """拉模式消费消息
        """
        while not self.stopped:
            try:
                msgs = await consumer.fetch(batch=1000, timeout=0.1)
                if msgs:
                    #logging.info('fetched %d', len(msgs))
                    for msg in msgs:
                        await self.on_message(msg)
                        if not self.manual_ack:
                            await self.ack(msg)
            except asyncio.exceptions.TimeoutError:
                #logging.info('no msg fetched')
                await gen.sleep(0.5)

    async def ack(self, msg: jsclient.Msg):
        """确认消息
        """
        await msg.ack()
        logging.debug("ack %s", msg.data)
        self._msg_ack_count += 1
        if self._msg_ack_count % 1000 == 0:
            logging.info('%d msg acked', self._msg_ack_count)

    async def on_message(self, msg: jsclient.Msg):
        """处理收到的消息
        """
        logging.debug('received msg: %s', msg.data)
        self._msg_received_count += 1
        if self._msg_received_count % 1000 == 0:
            logging.info('%d msg received', self._msg_received_count)
        if self.manual_ack:
            # 手动确认的时候在回调中增加ack， 自动确认的话不需要在这里执行ack（推模式自动ack， 拉模式在拉取的地方自动调用）
            ref = RefCounter(cb=lambda: self.ack(msg), loop=self.loop)
            #await self._emit(msg, [{"ref": ref}])
        else:
            ref = RefCounter(loop=self.loop)
        # TODO: 将后续处理运行在线程中， 还需要再测试一下
        if self.run_in_thread:
            await self.loop.run_in_executor(None, self._emit, msg,  [{"ref": ref}])
        else:
            self._emit(msg, [{"ref": ref}])

    def start(self):
        if self.stopped:
            self.stopped = False
            self.loop.add_callback(self.connect)

