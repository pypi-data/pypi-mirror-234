#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Time    :   2023/06/09 09:40:22
@Author  :   qiupengfei 
@Contact :   qiupengfei@baidu.com
@Desc    :   
"""

from collections import defaultdict
import arrow
from streamz.core import Stream
from streamz.core import map as streamz_map
from typing import Any, Iterable, Tuple, Optional, Callable
from collections import deque

from queue import PriorityQueue
import concurrent.futures
import logging

def now():
    """当前北京时间"""
    return arrow.utcnow().to('+08:00')


class WindowElement:
    """对窗口中的元素进行的封装"""
    def __init__(self, value, metadata, event_time: arrow.Arrow, subject):
        # 上游传递过来的metadata
        self.metadata = metadata
        # 实际的上游传递过来的元素
        self.value = value
        # 从元素中提取事件时间
        self.event_time = event_time
        # 从元素中提取主题的函数，不提供则不提取
        self.subject = subject

    def __lt__(self, other: "WindowElement"):
        return self.event_time < other.event_time


class WindowEmitCollection:
    """窗口输出的数据集合
    """
    def __init__(self, window_start: arrow.Arrow, window_end: arrow.Arrow, elements: list):
        # 窗口开始时间
        self.window_start = window_start
        # 窗口结束时间
        self.window_end = window_end
        # 窗口中的元素
        self.elements = elements

    def iter_elements(self) -> Iterable:
        """窗口中的元素的迭代器"""
        yield from self.elements


@Stream.register_api()
class flatten_map(Stream):
    """ Apply a function to every element in the stream, and flatten the results.

    Parameters
    ----------
    func: callable
    *args :
        The arguments to pass to the function.
    **kwargs:
        Keyword arguments to pass to func

    Examples
    --------
    >>> source = Stream()
    >>> source.flatten_map(lambda x: [i * x for i in range(3)]).sink(print)
    >>> for i in range(3):
    ...     source.emit(i)
    0
    0
    0
    0
    1
    2
    0
    2
    4
    """
    def __init__(self, upstream, func, *args, **kwargs):
        self.func = func
        # this is one of a few stream specific kwargs
        stream_name = kwargs.pop('stream_name', None)
        self.kwargs = kwargs
        self.args = args

        Stream.__init__(self, upstream, stream_name=stream_name)

    def update(self, x, who=None, metadata=None):
        try:
            result = self.func(x, *self.args, **self.kwargs)
        except Exception as e:
            logging.exception(e)
            raise
        else:
            for ret in result:
                self._emit(ret, metadata=metadata)


class long_window(Stream):
    def __init__(self, upstream,
                 event_time_func: Optional[Callable]=None,
                 subject_key_func: Optional[Callable]=None,
                 trigger_subject: str="",
                 trigger_subject_count=0,
                 trigger_interval: int=0,
                 only_trigger_after_update=True,
                 start_trigger_after_new_event=True,
                 threaded=False,
                 **kwargs):
        # 提取事件时间的函数
        self.event_time_func: Optional[Callable] = event_time_func
        # 从消息中提取主题的函数
        self.subject_key_func: Optional[Callable] = subject_key_func
        # 基于时间触发的时候使用的时间间隔，单位是秒
        self.trigger_interval: int = trigger_interval
        # 基于条数触发的时候参考的主题，当不提供的时候就看全部条数。
        self.trigger_subject: str = trigger_subject
        # 按条数触发的时候，配置的主题的触发条数
        self.trigger_subject_count: int = trigger_subject_count

        # 仅在距离上次窗口触发后数据有更新的时候才会触发
        self.only_trigger_after_update: bool = only_trigger_after_update
        # 仅在收到事件时间大于任务启动时间的数据时才开始触发
        self.start_trigger_after_new_event: bool = start_trigger_after_new_event

        # 上次触发后最近一次数据到来的时间
        self._last_update_time: Optional[arrow.Arrow] = None
        # 上次触发后trigger_subject对应的新到元素的数量，如果trigger_subject为空，则是所有新到元素的数量
        self._new_subject_count: int = 0
        # 上次触发窗口计算时间
        self._last_trigger_time: Optional[arrow.Arrow] = arrow.get(0)
        # 最近发送出去的数据
        self._emited = []
        # 在线程中执行_emit，这样允许下游执行计算密集型任务
        self.threaded = threaded
        # 最新数据时间
        self._latest_event_time = arrow.get(0)
        # 任务启动时间
        self._task_start_time = now()

        super().__init__(upstream, **kwargs)
    
    def get_element(self, x, metadata=None) -> WindowElement:
        """工厂函数， 构造一个element"""
        # print(self.event_time_func)
        return WindowElement(
            value=x,
            metadata=metadata,
            event_time=self.event_time_func(x) if self.event_time_func else arrow.utcnow().to('+08:00'),
            subject=self.subject_key_func(x) if self.subject_key_func else x
        )
    

    def _evict(self) -> Iterable[WindowElement]:
        """对buffer进行检查， 判断是否要移除元素， 并返回要移除的元素
        """
        raise NotImplementedError()
    
    def _append(self, element: WindowElement):
        """将元素加入到buffer
        """
        raise NotImplementedError()
    
    def _iter_elements(self)-> Iterable[WindowElement]:
        """遍历buffer，返回元素
        """
        raise NotImplementedError()
    
     
    def update(self, x, who=None, metadata=None):
        """上游输出数据的时候会调用此函数来传递数据
        """
        self._retain_refs(metadata)

        element = self.get_element(x, metadata)
        # 加入缓冲区
        self._append(element)

        # 尝试从窗口中剔除元素
        for e in self._evict():
            self._release_refs(e.metadata)

        self._last_update_time = now()
        self._latest_event_time = element.event_time
        if self.trigger_subject:
            if element.subject == self.trigger_subject:
                self._new_subject_count += 1
        else:
            self._new_subject_count += 1

        # 判断是否要触
        self.loop.add_callback(self.trigger)

        # 返回_emit出去的数据
        tmp = self._emited
        self._emited = []
        #logging.info(self._emited)
        return tmp
        
    async def trigger(self):
        """判断是否要触发窗口计算
        """
        logging.debug('trigger called')
        # 只在有新数据的时候才更新
        if self.only_trigger_after_update and self._last_update_time is None:
            logging.debug('only trigger after update')
            return
        # 仅在收到启动时间之后的数据时才触发，为了解决回放数据的问题
        if self.start_trigger_after_new_event and self._latest_event_time < self._task_start_time:
            #logging.info('start trigger after new event, %s, %s', self._task_start_time, self._latest_event_time)
            return
        n = now()
        # 按时间触发
        if self.trigger_interval:
            # 到达计划触发时间
            expect_time = self._last_trigger_time.shift(seconds=self.trigger_interval)
            if n.timestamp() >= expect_time.timestamp():
                self.loop.add_callback(self.cb)
                #await self.cb()
                self._last_trigger_time = n
                logging.info("triggered %s, expect %s, now: %s", str(self.trigger_interval), expect_time, n)
            else:
                logging.debug("trigger not reach, interval %s, expect %s, now: %s", str(self.trigger_interval), expect_time, n)
            # 调度下次触发时间
            self.loop.call_later(self.trigger_interval, self.trigger)
        elif self.trigger_subject_count > 0:
            # 按条数触发
            if self._new_subject_count > self.trigger_subject_count:
                self.loop.add_callback(self.cb)
                #await self.cb()
                self._last_trigger_time = n
            # 按条数触发只会发生在新数据到来的时候， 所以不需要定时
            
    def get_emit_data(self):
        """获取要窗口要输出的数据
        """
        result = [x.value for x in self._iter_elements()]
        metadata = [x.metadata for x in self._iter_elements()]

        # 清空数据更新时间
        self._last_update_time = None
        self._new_subject_count = 0
        self._emited.extend(result)
        logging.info('emit %s item', len(result))
        return result, metadata

    async def cb(self):
        """窗口输出函数， 输出是一个集合"""
        result, metadata = self.get_emit_data()
        self._emit(result, metadata=metadata)


@Stream.register_api()
class long_time_window(long_window):
    """类似于基于时间的滑动窗口， 不同的地方在于：
    1. 支持事件时间，可以从元素中提取事件时间。 不提供时间时间则使用摄入时间（算子接收到元素的时间）
    2. 可以基于时间触发，也可以基于新数据条数触发。 基于新数据条数触发时还可以按照提取的subject统计对应subject的条数来触发。
    3. 在没有新元素进入的时候可以不触发窗口计算
    4. 元素的移除和触发器是分开的，没有触发计算也可以移除元素。
    
    """

    def __init__(self, upstream, evict_time: int, evict_by_event_time=False,
                 event_time_func: Optional[Callable[..., Any]] = None, 
                 subject_key_func: Optional[Callable[..., Any]] = None, 
                 trigger_subject: str = "", trigger_subject_count=0, trigger_interval: int = 0, 
                 only_trigger_after_update=True, **kwargs):
        super().__init__(upstream, 
                         event_time_func=event_time_func, 
                         subject_key_func=subject_key_func, 
                         trigger_subject=trigger_subject, 
                         trigger_subject_count=trigger_subject_count, 
                         trigger_interval=trigger_interval, 
                         only_trigger_after_update=only_trigger_after_update, **kwargs)
        # 淘汰时间，单位秒
        self.evict_time = evict_time
        # 基于最新事件时间来淘汰数据
        self.evict_by_event_time = evict_by_event_time
        # 当前窗口结束时间，数据源时钟不正常时可能与_latest_event_time不一致
        self._window_end_time = arrow.get(0)
        # 数据缓存
        self._buffer = PriorityQueue()
    
    def _append(self, element: WindowElement):
        """添加元素到buffer
        """
        # priority_queue默认是小顶堆
        #self._buffer.put((-element.event_time.timestamp(), element))
        self._buffer.put(element)
    
    def _evict(self) -> Iterable[WindowElement]:
        """淘汰元素
        """
        curr_time = now()
        if not self.evict_by_event_time:
            base_time = curr_time
        else:
            # 基于事件时间来淘汰元素。这里不是严谨的事件窗口，没有处理迟到数据、watermark等，假设了数据的事件时间是单调递增的
            base_time = self._latest_event_time
            # 防止事件时间出错收到未来的数据, 这种数据在_emit的时候不会传给下游
            if base_time > curr_time:
                base_time = curr_time
        # 当前窗口结束时间
        self._window_end_time = base_time

        oldest_time = base_time.shift(seconds=-self.evict_time)
        while not self._buffer.empty():
            elem = self._buffer.queue[0]
            if elem.event_time < oldest_time:
                _ = self._buffer.get()
                logging.info('evict data, event time: %s, window_end_time: %s', elem.event_time, self._window_end_time)
                yield elem
            else:
                break

    def _iter_elements(self) -> Iterable[WindowElement]:
        for item in self._buffer.queue:
            # 注意： 超出当前窗口截止时间的数据不会被输出。数据源必须是真实时间，不能有未来时间的数据。如果时钟不一致可能会导致消息输出延迟
            if item.event_time > self._window_end_time:
                logging.info('data ignored because of a future event time: %s', item.event_time)
                continue
            yield item

    def cb(self):
        """窗口输出函数， 输出是一个集合
        """
        result, metadata = self.get_emit_data()
        col = WindowEmitCollection(
            window_start=self._window_end_time.shift(seconds=-self.evict_time),
            window_end=self._window_end_time,
            elements=result)
        self._emit(col, metadata=metadata)


@Stream.register_api()
class long_count_window(long_window):
    """类似于long_time_window, 只是淘汰是基于subject的条数来淘汰的
    """

    def __init__(self, upstream, evict_count: int, event_time_func: Optional[Callable[..., Any]] = None, subject_key_func: Optional[Callable[..., Any]] = None, trigger_subject: str = "", trigger_subject_count=0, trigger_interval: int = 0, only_trigger_after_update=True, **kwargs):
        super().__init__(upstream, event_time_func, subject_key_func, trigger_subject, trigger_subject_count, trigger_interval, only_trigger_after_update, **kwargs)
        self.evict_count = evict_count

        # 数据缓存
        # TODO: 可能每个subject也得存在优先队列中才能保证淘汰的时候按照事件时间淘汰
        self._buffer = defaultdict(deque)
    
    def _evict(self) -> Iterable[WindowElement]:
        """每个subject只保留最多evict_count个元素"""
        for _, queue in self._buffer.items():
            while len(queue) > self.evict_count:
                elem = queue.popleft()
                logging.info('evict data, event time: %s', elem.event_time)
                yield elem
        
    def _iter_elements(self) -> Iterable[WindowElement]:
        """目前是按照subject去迭代的，因为每个subject的队列是有序的，所以也可以返回时间有序的结果
        """
        for _, queue in self._buffer.items():
            yield from queue

    def _append(self, element: WindowElement):
        self._buffer[element.subject].append(element)


@Stream.register_api()
class threaded_map(streamz_map):
    """在线程中运行map函数， 以避免主线程阻塞, TODO: 仍不可用
    """

    def __init__(self, upstream, func, *args, **kwargs):
        super().__init__(upstream, func, *args, **kwargs)
        self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    def update(self, x, who=None, metadata=None):
        streamz_map.update(self, x, who, metadata)
        #self.loop.run_in_executor(self.pool, streamz_map.update, self, x, who, metadata)

