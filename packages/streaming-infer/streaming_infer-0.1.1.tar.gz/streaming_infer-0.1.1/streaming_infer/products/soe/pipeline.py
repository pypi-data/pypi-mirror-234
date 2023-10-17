#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Time    :   2023/06/16 17:01:14
@Author  :   qiupengfei 
@Contact :   qiupengfei@baidu.com
@Desc    :   
"""

import json
import logging
import math
import uuid
from datetime import datetime
from statistics import mean

import arrow
import pandas as pd
import tritonclient.http as http_client
from sqlalchemy.sql.expression import insert, select, update
from tritonclient.utils import triton_to_np_dtype

from .soe_point import SOEHighPoint, SOELowPoint, to_soe_point
from .task import SoeTaskConfig
from streaming_infer.config.job_config import JobConfig
from streaming_infer.pipeline.infer_handler import InferHandler, async_infer
from streaming_infer.pipeline.pipeline import InferPipeline
from streaming_infer.streamz_ext.core import WindowEmitCollection, flatten_map, long_time_window
from streaming_infer.streamz_ext.sinks.http import sink_to_http
from streaming_infer.tasks.task_config import InferTaskConfig
from streamz.core import Stream


class SinkObject(object):
    """ sink 请求体
    """
    def __init__(
        self,
        device_id: str,
        prop_id: str,
        value: str,
    ):
        self.device_id = device_id
        self.prop_id = prop_id
        self.value = value

    @property
    def req_body(self):
        return json.dumps({
            'deviceId': str(self.device_id),
            'propId': str(self.prop_id),
            'value': str(self.value)
        })


class AlignAndResample:
    """ 时间对齐、重采样、缺失值补全
    """

    def __init__(
        self,
        row_interval: int,
        point_key_to_config: dict,
        on_error: callable=None,
        **kwargs
    ):
        # 目标采样频率
        self.row_interval = row_interval
        # 点位key: input_config
        self.point_key_to_config = point_key_to_config
        # 点位key: 模型fields
        self.point_key_to_model_field = {
            k: inp_conf.model_field
            for k, inp_conf in self.point_key_to_config.items()
        }
        # 用到的点位key集合，用于过滤
        self.inused_point_keys = set(self.point_key_to_config.keys())
        self.on_error = on_error

    def _aggr(self, time_block, aggr_strategy, fill_strategy):
        time_block = [self._fill_empty(fill_strategy) if v is None else v for v in time_block]
        if aggr_strategy == 'mean':
            return mean([p.value for p in time_block])
        elif aggr_strategy == 'first':
            return time_block[0].value
        elif aggr_strategy == 'last':
            return time_block[-1].value
        return mean([p.value for p in time_block])

    def _fill_empty(self, fill_strategy):
        if fill_strategy == 'none':
            return None
        elif fill_strategy == '0':
            return 0
        return None

    def __call__(self, x: WindowEmitCollection) -> list:
        try:
            groups = {}
            # 基础属性
            win_start_time = x.window_start
            win_end_time = x.window_end
            win_total_seconds = (win_end_time - win_start_time).total_seconds()
            time_block_num = int(win_total_seconds // self.row_interval) # 用row_interval对时间进行分区（左开右闭）
            # 按时间分组并对齐
            time_diff = [None] * time_block_num
            for point_data in x.iter_elements():
                subject = point_data.get_key()
                event_time = point_data.timestamp
                if subject not in self.inused_point_keys: continue # filter cols not in input_config
                if subject not in groups:
                    groups[subject] = [[] for i in range(time_block_num)]
                pos = max(math.ceil(
                    (event_time - win_start_time.naive).total_seconds() / self.row_interval
                ) - 1, 0) # 分组对应的时间戳：(0, 1], (1, 2], (2, 3]
                time_diff[pos] = (event_time - win_start_time.naive).total_seconds()
                groups[subject][pos].extend(point_data.get_data()) # 从SoePoint中提取PointData，并放入对应的分组
            # 聚合
            for sub, g in groups.items():
                for i, block in enumerate(g):
                    inp_conf = self.point_key_to_config[sub]
                    aggregate_strategy = inp_conf.aggregate_strategy
                    fill_strategy = inp_conf.fill_strategy
                    g[i] = self._aggr(block, aggregate_strategy, fill_strategy) if len(block) \
                        else self._fill_empty(fill_strategy)
            groups['timestamp'] = [
                win_start_time.shift(seconds=i * self.row_interval).timestamp()
                for i in range(1, time_block_num + 1)
            ] # 时间区间 左开右闭
            groups['time_diff'] = time_diff
            result = pd.DataFrame(groups)
            # 将NATS的点位命名，重命名为模型输入的字段名
            result = result.rename(columns=self.point_key_to_model_field)
            # 有可能整列缺失，用默认值补全
            for point_id, col in self.point_key_to_model_field.items():
                if col not in result.columns:
                    inp_conf = self.point_key_to_config[point_id]
                    result[col] = self._fill_empty(inp_conf.fill_strategy)
            return [result]
        except Exception as ex:
            logging.error(ex)
            if callable(self.on_error):
                self.on_error(ex)
            return []


class WindmillPreProcess:
    """ windmill client 前置处理
    """
    def __init__(
        self,
        infer_handler: InferHandler,
        on_error: callable=None,
        **kwargs
    ):
        self.infer_handler = infer_handler
        self.on_error = on_error

    def __call__(self, x: pd.DataFrame):
        try:
            # 获取模型字段配置文件
            input_metadata, output_metadata, batch_size = self.infer_handler.get_inputs_and_outputs_detail()
            logging.debug("windmill input_metadata: %s\noutput_metadata: %s", input_metadata, output_metadata)
            # 构造模型输入[np.array]
            input_data_list = [
                x[input_meta['name']].to_numpy(
                    # dtype=triton_to_np_dtype(input_meta['datatype'])).reshape(input_meta['shape']
                    dtype=triton_to_np_dtype(input_meta['datatype'])).resize(input_meta['shape'], refcheck=False
                )
                for input_meta in input_metadata
            ]
            # 生成InferInput
            inputs = [
                http_client.InferInput(input_meta["name"], input_data_list[i].shape, input_meta["datatype"])
                for i, input_meta in enumerate(input_metadata)
            ]
            for i, inp in enumerate(inputs):
                inp.set_data_from_numpy(input_data_list[i], binary_data=False)
            # 生成InferOutput
            outputs = [
                http_client.InferRequestedOutput(output_meta['name'], binary_data=True)
                for output_meta in output_metadata
            ]
            args = []
            kwargs = {
                "inputs": inputs,
                "outputs": outputs,
            }
            return [[args, kwargs]]
        except Exception as ex:
            logging.exception(ex)
            if callable(self.on_error):
                self.on_error(ex)
            return []


class WindmillPostProcess:
    """ windmill client 后处理
    """
    def __init__(
        self,
        infer_handler: InferHandler,
        on_error: callable=None,
        **kwargs
    ):
        self.infer_handler = infer_handler
        self.on_error = on_error

    def __call__(self, x: pd.DataFrame) -> list:
        try:
            input_metadata, output_metadata, batch_size = self.infer_handler.get_inputs_and_outputs_detail()
            result = pd.DataFrame({
                output_meta['name']: x.as_numpy(output_meta['name'])
                for output_meta in output_metadata
            })
            return [result]
        except Exception as ex:
            if callable(self.on_error):
                logging.error(ex)
            self.on_error(ex)
            return []


class LoggingToDb:
    """ 记录运行状态到数据库
    """
    def __init__(self, job_config, task_id) -> None:
        self.job_config = job_config
        self.task_id = task_id
        # 记录任务最后一次运行的状态
        self.last_status = self._get_task_status()
        # 记录上次异常信息，避免连续记录多条相同异常
        self.pre_err_msg = None

    def _update_task_status(self, session, table, status):
        row = session.query(table).filter_by(
            task_id=self.task_id,
            deleted_at=0
        ).first()
        row.status = status
        row.updated_at = datetime.now()
        session.commit()

    def _get_task_status(self):
        sql_conn = self.job_config.get_db(reflect_tables=['task_stat'])
        table = sql_conn['task_stat']
        try:
            with sql_conn.session() as session:
                task_stat_row = session.query(table).filter_by(
                    task_id=self.task_id,
                    deleted_at=0
                ).first()
                return task_stat_row.status
        except Exception as ex:
            logging.exception(ex)
        return None

    def _insert_exception(self, session, table, msg):
        if self.pre_err_msg is not None and str(msg) != '' \
                and str(msg) == str(self.pre_err_msg) and type(msg) == type(self.pre_err_msg):
            logging.info("same error: %s", msg)
            return
        self.pre_err_msg = msg
        now = datetime.now()
        row = table(
            id="log-" + uuid.uuid1().hex[:8],
            trace_id=self.task_id,
            message=msg,
            created_at=now,
            updated_at=now,
            deleted_at=0,
        )
        session.add(row)
        session.commit()

    def error(self, err_msg = None):
        # 获取sql conn
        sql_conn = self.job_config.get_db(reflect_tables=['task_stat', 'operation_log'])
        with sql_conn.session() as session:
            self._insert_exception(session, sql_conn['operation_log'], err_msg)
            self._update_task_status(session, sql_conn['task_stat'], 'error') # 异常状态每次都更新
            self.last_status = 'error'

    def normal(self):
        # 获取sql conn
        self.pre_err_msg = None
        sql_conn = self.job_config.get_db(reflect_tables=['task_stat', 'operation_log'])
        if self.last_status != 'normal':
            with sql_conn.session() as session:
                self._update_task_status(session, sql_conn['task_stat'], 'normal') # 正常状态只记录一次
        self.last_status = 'normal'


@Stream.register_api()
class SoeInferPipline(InferPipeline):
    """
    一个流水线的样例
    """
    def __init__(self, task: InferTaskConfig, job_config: JobConfig):
        super().__init__(task, job_config)
        # 数据库日志记录器
        self.logging_to_db = LoggingToDb(self.job_config, self.task.id)

    @classmethod
    def get_task_type(cls):
        """获取任务类型"""
        return SoeTaskConfig.TASK_TYPE

    def __exec__(self):
        """运行流水线
        """
        logging.info('soe pipeline start')
        # 输入配置
        input_config = self.task.get_input_config()
        # 输出配置
        output_config = self.task.get_output_config()
        model_output_to_device = {
            field.model_field: {
                'device_id': field.device_id,
                'prop_id': field.prop_id
            }
            for field in output_config.fields
        }
        # sink配置
        sinks = self.task.get_sinks()
        # 调度配置
        trigger_config = self.task.trigger_config
        # 模型配置
        model_config = self.task.model_config

        # 从配置文件中获取数据源
        source = self.get_merged_streamz_source()
        # 转换成SOE传输使用的点位数据对象
        stream = source.filter(lambda x: x.data).to_soe_point()
        # 使用时间窗口
        # 窗口中只保留事件时间在 ${input_span}秒 内的数据， 毎 ${trigger_interval}秒钟 会触发一次计算将数据传递给下游
        stream = stream.long_time_window(
            evict_time=input_config.input_span,
            event_time_func=lambda x: arrow.get(x.end_timestamp.timestamp()).to('+08:00'),
            subject_key_func=lambda x: x.get_key(),
            trigger_interval=trigger_config.trigger_interval
        )
        # 重采样、时间对齐并做合并
        data_preprocess_handler = AlignAndResample(
            row_interval=input_config.row_interval,
            point_key_to_config={
                input_config.key: input_config
                for input_config in input_config.fields
            },
            on_error=self.logging_to_db.error
        )
        stream = stream.flatten_map(data_preprocess_handler)
        # 调用windmill triton模型，前置处理
        windmill_preprocess_handler = WindmillPreProcess(
            self.infer_handler,
            on_error=self.logging_to_db.error
        )
        stream = stream.flatten_map(windmill_preprocess_handler)
        # 调用windmill triton模型（此处是为了实现异步模式）
        stream = stream.async_infer(
            handler=self.infer_handler,
            on_error=lambda req, e: self.logging_to_db.error(e)
        )
        # 调用windmill triton模型，后置处理
        windmill_postprocess_handler = WindmillPostProcess(
            self.infer_handler,
            on_error=self.logging_to_db.error
        )
        stream = stream.flatten_map(windmill_postprocess_handler)
        # 将推理结果转换成控制器所需的结果
        stream = stream.map(lambda df: [
            SinkObject(
                device_id=model_output_to_device[col]['device_id'],
                prop_id=model_output_to_device[col]['prop_id'],
                value=row[col],
            ).req_body
            for _, row in df.iterrows()
                for col in df.columns
        ])
        # 输出推理结果
        for sink in sinks:
            stream = stream.sink_to_http(
                "POST",
                sink.url,
                success_status_code=204,
                on_error=self.logging_to_db.error
            )
        # 任务完成，将数据库中任务状态更新为正常状态
        def set_task_status_normal_to_db(x):
            self.logging_to_db.normal()
            return x
        stream = stream.map(set_task_status_normal_to_db)
        # 打印
        stream.sink(logging.info)
        
