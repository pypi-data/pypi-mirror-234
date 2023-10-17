#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Time    :   2023/06/16 16:49:49
@Author  :   qiupengfei 
@Contact :   qiupengfei@baidu.com
@Desc    :   
"""
import logging
import traceback
from typing import List

from sqlalchemy.sql.expression import select

from .task import SoeTaskConfig
from streaming_infer.config.job_config import JobConfig
from streaming_infer.tasks.task_manager import TaskManager


class SoeTaskMonitor(TaskManager):
    """ SOE TaskMonitor
    """
    def __init__(self, job_config: JobConfig):
        super().__init__(job_config)
        self.table_list = ["task", "task_input", "task_model", "task_output", "task_stat"]

    def fetch_tasks(self) -> List[SoeTaskConfig]:
        """
        TODO 从数据库解析任务配置 解析task ... 等5张表

        Returns:
            List[SoeTaskConfig]: _description_
        """
        CONFIG_DB = self.job_config.get_conf("config_db")
        CONTROLLER_URL = self.job_config.get_conf("controller_url")
        MYSQL_URL = self.job_config.get_conf("mysql_url")
        NATS_URL = self.job_config.get_nats_url()

        input_span_type_to_seconds = {
            "second": 1,
            "minute": 60,
            "hour":  3600,
            "day":   86400,
            "week":  604800,
        }

        # 获取sql conn
        sql_conn = self.job_config.get_db(reflect_tables=self.table_list)

        with sql_conn.session() as session:
            # 批量查询数据
            table_task = sql_conn["task"]
            table_task_input = sql_conn["task_input"]
            table_task_output = sql_conn["task_output"]
            table_task_model = sql_conn["task_model"]
            task_rows = session.query(table_task).all()
            task_input = session.query(table_task_input).all()
            task_output = session.query(table_task_output).all()
            task_model = session.query(table_task_model).all()
            # 做配置关联
            tasks = []
            for task in task_rows:
                try:
                    if task.status != 'start': continue
                    # init
                    config = {}
                    inputs = list(filter(lambda x: x.task_id==task.id, task_input))
                    outputs = list(filter(lambda x: x.task_id==task.id, task_output))
                    models = list(filter(lambda x: x.task_id==task.id, task_model))
                    # model_config
                    config["model_config"] = {
                        "model_name": models[0].local_name,
                        "model_version": models[0].num_version,
                        "endpoint": models[0].endpoint,
                    }
                    # sources
                    config["sources"] = [{
                        "source_type": "jetstream",   # 只有这一个是必须的，其他的根据不同的source_type不一样
                        "nats_url": NATS_URL,
                        "subjects": list(set(
                            f"thing.{inp.nats_product_key}.{inp.nats_device_id}.property.post"
                            for inp in inputs
                        ))
                    }]
                    # sinks
                    config["sinks"] = [{
                        "sink_type": "http",
                        "url": CONTROLLER_URL + "/soe/opt/controller/cmd",
                    }]
                    # input_config
                    config["input_config"] = {
                        "input_type": task.input_type,
                        "input_span": task.input_span * input_span_type_to_seconds.get(task.input_span_type, 1),
                        "row_interval": task.row_interval,
                        "fields": [
                            {
                                "model_field": inp.field_name,
                                "model_field_type": inp.field_type,
                                "device_id": inp.nats_device_id,
                                "prop_id": inp.nats_data_point_id,
                                "field_type": inp.data_point_type,
                                "aggregate_strategy": inp.sample_policy,
                            } for inp in inputs
                        ]
                    }
                    # output_config
                    config["output_config"] = {
                        "fields": [
                            {
                                "model_field": outp.field_name,
                                "model_field_type": outp.field_type,
                                "device_id": outp.device_id,
                                "prop_id": outp.data_point_id,
                                "field_type": outp.data_point_type,
                            } for outp in outputs
                        ]
                    }
                    # trigger_config
                    config["trigger_config"] = {
                        "trigger_mode": task.trigger_mode,    # 事件触发、周期执行
                        "trigger_interval": task.trigger_interval,      # 周期执行的周期
                        "trigger_num":  task.trigger_num,          # 事件触发的触发数量
                        "trigger_device": task.nats_trigger_device_id,       # 事件触发的设备ID，可以为空。UI上选择的是模型输入字段，需要转换成实际设备点位。
                        "trigger_field": task.nats_trigger_field_id,        # 事件触发的触发点位，可以为空。
                    }
                    # Append to tasks
                    task_config = SoeTaskConfig(task.id, task.local_name, task.version, config)
                    tasks.append(task_config)
                except Exception as ex:
                    logging.error("task config decode err :")
                    logging.error(traceback.format_exc())
        return tasks
    
    @classmethod
    def get_task_type(self):
        return SoeTaskConfig.TASK_TYPE