"""junoplatform.io: implements io spec and common tools for algo"""
import inspect
import logging
from junoplatform.io.utils import junoconfig
from junoplatform.io._driver import Pulsar as Pulsar, Opc as Opc, junoconfig, Redis, Clickhouse, RDLock, Singleton
import numpy as np
from typing import Optional, Any, List
import datetime as datetime
from pydantic import BaseModel, Field, model_validator, NonNegativeInt

import threading

__author__ = "Bruce.Lu"
__email__ = "lzbgt@icloud.com"
__time__ = "2023/07/20"

__all__ = [
    'Storage',
    'InputConfig',
]


class InputConfig(BaseModel):
    ''' InputConfig spec for JunoPlatform Runtime
    tags: OPC tags
    minutes: last n minutes of data
    items: last n records of data
    sched_interval: algo schedule interval in seconds
    '''
    tags: List[str]
    minutes: Optional[NonNegativeInt] = Field(
        default=None, description='input data of last n minutes')
    items: Optional[NonNegativeInt] = Field(
        default=None, description='input data of last n items')
    sched_interval: NonNegativeInt = Field(
        description='schedule interval in seconds')

    @model_validator(mode="before")
    def atleast_one(cls, values: 'dict[str, Any]') -> 'dict[str, Any]':
        if not values.get('minutes') and not values.get('items'):
            raise ValueError("field 'minutes' or 'items' must be given")
        return values


class DataSet(object):
    def __del__(self):
        if hasattr(self, "io"):
            if hasattr(self.io, "io"):
                self.io.io.close()

    def __init__(self) -> None:

        if 'clickhouse' in junoconfig:
            self.url = junoconfig['clickhouse']['url']
        else:
            devcfg = {'gangqu': 'ch://sf_read1:reader@123.@192.168.101.101:7000',
                      'yudai': 'ch://default:L0veclickhouse@192.168.101.101:8123',
                      'yulin': 'ch://sf_read1:reader@123.@192.168.101.101:7010'}
            self.url = devcfg[junoconfig["plant"]]
        self.io: Clickhouse = Clickhouse(url=self.url)
        self.tbl_c = f'{junoconfig["plant"]}_data.running'
        self.tbl_w = f'{junoconfig["plant"]}_data.running_today'

    def fetch(self, num: int = 0, tags: List[str] = "", time_from=None):
        if num > 0:
            data, timestamps, names = self.io.read(
                self.tbl_w, tskey='time', tags=tags, num=num, time_from=None)
            num = num - len(timestamps)
            if num > 0:
                nd, nt, _ = self.io.read(
                    self.tbl_c, tskey='time', tags=tags, num=num, time_from=None)
                return np.concatenate((nd, data), axis=0), nt + timestamps, names
            return data, timestamps, names
        if time_from:
            data, timestamps, names = self.io.read(
                self.tbl_w, tskey='time', tags=tags, num=0, time_from=time_from)
            if timestamps[0].utcnow() > time_from.utcnow():
                nd, nt, _ = self.io.read(
                    self.tbl_c, tskey='time', tags=tags, num=0, time_from=time_from)
                return np.concatenate((nd, data), axis=0), nt + timestamps, names
            return data, timestamps, names


def print_call_frame():
    frames = inspect.stack()
    for frame_info in frames:
        frame = frame_info.frame
        frame_info = inspect.getframeinfo(frame)
        if "<frozen" in frame_info.filename:
            break
        logging.info(
            f"[inspect] file: {frame_info.filename}:{frame_info.lineno}, fun: {frame_info.function}")


class Storage(object):
    _lock = threading.Lock()
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._lock.acquire()
            if not cls._instance:
                cls._instance = super().__new__(cls)
            cls._lock.release()

        print_call_frame()
        logging.info(f"Storage: {cls._instance}")

        return cls._instance

    def __init__(self):
        super().__init__()
        _redis_cfg = junoconfig['redis']
        self._local = Redis(**_redis_cfg)
        self.lock = RDLock(self._local.io)
        self._cloud = None
        self._opc = None

    @property
    def cloud(self):
        if not self._cloud:
            self._lock.acquire()
            if not self._cloud:
                self._cloud: Pulsar = Pulsar(
                    **junoconfig['pulsar'], lock=self.lock)
            self._lock.release()
        return self._cloud

    @property
    def opc(self):
        if not self._opc:
            self._lock.acquire()
            if not self._opc:
                OpcWriter = Opc(lock=self.lock, rediscli=self._local.io)
                self._opc = OpcWriter
            self._lock.release()

        return self._opc

    @property
    def local(self):
        return self._local
