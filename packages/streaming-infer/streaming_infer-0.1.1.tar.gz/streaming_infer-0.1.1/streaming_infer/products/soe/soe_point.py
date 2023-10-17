#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Author: liuzixiang
Date: 2023-07-12 16:23:18
LastEditors: liuzixiang
LastEditTime: 2023-07-19 16:47:29
Description: 
"""
import json
import logging
import sys
from abc import ABCMeta, abstractmethod
from datetime import datetime

import pandas as pd

from streamz.core import Stream


@Stream.register_api()
class to_soe_point(Stream):
    """ 转换LowPoint/HighPoint
    """
    def __init__(self, upstream, *args, **kwargs):
        super().__init__(upstream, *args, **kwargs)

    def _point_iter(self, body):
        data_speed = 'low' if body['kind'] == 'deviceReport' else 'high'
        if data_speed == 'low':
            # 低速数据格式化
            for k, v in body['content']['blink']['properties'].items():
                yield SOELowPoint(
                    device_id=body['meta']['device'],
                    timestamp=body['content']['blink']['timestamp'],
                    prop_id=k,
                    value=v,
                )
        elif data_speed == 'high':
            # 高速数据格式化
            properties = body['content']['blink']['properties']
            yield SOEHighPoint(
                storage_type=properties['storage_type'],
                storage_path=properties['storage_path'],
                device_id=properties['device_id'],
                prop_id=properties['prop_id'],
                start_timestamp=properties['start_timestamp'],
                end_timestamp=properties['end_timestamp'],
            )
        else:
            raise ValueError(
                "please check data_speed, need 'low' or 'high', find {}".format(data_speed)
            )

    def update(self, x, who=None, metadata=None):
        body = json.loads(x.data)
        logging.debug(body)
        for result in self._point_iter(body):
            self._emit(result, metadata=metadata)


class SOEPointData(object):
    """
    description: SOEPointData
    param {str} key
    param {any} value
    param {Timestamp} timestamp
    """
    def __init__(
        self,
        timestamp: datetime,
        key: str,
        value: any,
    ) -> None:
        self.timestamp = timestamp
        self.key = key
        self.value = value

    def to_dict(self) -> dict:
        """
        description: transform to dict
        param {*} self
        """
        return {
            "timestamp": self.timestamp,
            self.key: self.value,
        }

    def to_dataframe(self) -> pd.DataFrame:
        """
        description: transform to pd.DataFrame
        return {list, list} (columns, values)
        """
        return pd.DataFrame(
            data = [
                [self.timestamp, self.value]
            ],
            columns = ["timestamp", self.key]
        )


class SOEPoint(metaclass=ABCMeta):
    """
    description: SOE 缓存点位 基类
    param {str} mode
    param {float} timestamp
    param {int} unit
    """
    def __init__(
        self,
        name: str = None,
        timestamp: float = None,
        unit: str = 'ms',
    ) -> None:
        self.name = name
        time_div = 1
        if unit == 'ms': time_div = 1000.0
        self.timestamp = datetime.fromtimestamp(timestamp / time_div)

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError()

    def set_name(self, name):
        self.name = name

    @abstractmethod
    def microseconds_from(self, target_block: 'SOEPoint') -> int:
        """
        description: 计算时间差 (ms)
        param {SOEPoint} target_block
        return {int}
        """
        raise NotImplementedError()

    @abstractmethod
    def get_data(self, storage_dict: dict = {}) -> list[SOEPointData]:
        """
        description: 解析返回点位数据列表
        param {dict} storage_dict
        return {list[SOEPointData]}
        """
        raise NotImplementedError()


class SOELowPoint(SOEPoint):
    """
    description:  LowSOEPoint
    param {str} device_id
    param {str} prop_id
    param {any} value
    param {float} timestamp
    """
    def __init__(
        self,
        device_id: str,
        prop_id: str,
        value: any,
        name: str = None,
        timestamp: float = None,
        unit: str = 'ms',
    ) -> None:
        self.device_id = device_id
        self.prop_id = prop_id
        self.value = value
        super().__init__(
            '#'.join([self.device_id, self.prop_id]) \
                if name is None else name,
            timestamp,
            unit,
        )

    @property
    def start_timestamp(self) -> int:
        return self.timestamp

    @property
    def end_timestamp(self) -> int:
        return self.timestamp

    def __len__(self) -> int:
        return 1

    def __str__(self) -> str:
        return f"{__class__}: {self.device_id}::{self.prop_id}::{self.value}::{self.timestamp}"

    def get_key(self) -> str:
        return str(self.device_id) + str(self.prop_id)

    def microseconds_from(self, target_block: 'SOEPoint') -> int:
        """
        description: 计算时间差 (ms)
        param {SOEPoint} target_block
        return {int}
        """
        return 1000 * (target_block.timestamp - self.timestamp).total_seconds() # ms

    def get_data(self, storage_dict: dict = {}) -> list[SOEPointData]:
        """
        description: 解析返回点位数据列表
        param {dict} storage_dict
        return {list[SOEPointData]}
        """
        return [
            SOEPointData(
                timestamp=self.timestamp,
                key=self.name,
                value=self.value,
            )
        ]


class SOEHighPoint(SOEPoint):
    """
    TODO
    description: HighSOEPoint
    param {int} timestamp
    """
    def __init__(
        self,
        storage_type: str,
        storage_path: str,
        device_id: str,
        prop_id: str,
        name: str = None,
        start_timestamp: int = None,
        end_timestamp: int = None,
        unit: str = 'ms',
    ) -> None:
        self.storage_type = storage_type
        self.storage_path = storage_path
        self.device_id = device_id
        self.prop_id = prop_id
        self._start_timestamp = start_timestamp
        super().__init__(
            '#'.join([self.device_id, self.prop_id]) \
                if name is None else name,
            end_timestamp,
            unit,
        )

    @property
    def start_timestamp(self) -> int:
        return self._start_timestamp

    @property
    def end_timestamp(self) -> int:
        return self.timestamp

    def __len__(self) -> int:
        return 1

    def __str__(self) -> str:
        return f"{__class__}: {self.storage_type}::{self.storage_path}::{self.device_id}::" \
            f"{self.prop_id}::{self.start_timestamp}::{self.end_timestamp}"

    def get_key(self) -> str:
        return str(self.device_id) + str(self.prop_id)

    def microseconds_from(self, target_block: 'SOEPoint') -> int:
        """
        description: 计算时间差 (ms)
        param {SOEPoint} target_block
        return {int}
        """
        return 1000 * (target_block.timestamp - self.timestamp).total_seconds() # ms

    def get_data(self, storage_dict: dict = {}) -> list[SOEPointData]:
        """
        description: 解析返回点位数据列表
        param {dict} storage_dict
        return {list[SOEPointData]}
        """
        storage_obj = storage_dict[self.storage_type]
        if not storage_obj.is_connected(): storage_obj.connect()
        value = storage_obj.read_file(self.storage_path)
        p_list = [
            SOEPointData(
                timestamp=self.timestamp,
                key=self.name,
                value=value,
            )
        ]
        logging.debug('sizeof(value) = %d', sys.getsizeof(value))
        del value
        return p_list

