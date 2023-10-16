"""junoplatform.io._driver.py: implements DB adaptor classes"""
import inspect
import redis
from junoplatform.api.local import write as connector_write
import numpy as np
import dateparser
from typing import List
from datetime import datetime
import json
from pulsar import Client, AuthenticationTLS, ConsumerType, InitialPosition, schema, Producer, Consumer
from typing import Dict
import logging
from junoplatform.io.utils import *
import hashlib
import threading
from abc import ABC, abstractmethod

__author__ = "Bruce.Lu"
__email__ = "lzbgt@icloud.com"
__time__ = "2023/07/20"


class IWriter(ABC):
    @abstractmethod
    def write(self, **kwargs):
        pass


class IReader(ABC):
    @abstractmethod
    def read(self, **kwargs):
        pass


class ALock(ABC):
    @abstractmethod
    def aquire(self, key: str, ex: int):
        pass


class RDLock(ALock):
    def __init__(self, redis: redis.Redis):
        super(RDLock, self).__init__
        self.redis = redis
        self.key = f"{junoconfig['plant']}.{junoconfig['module']}.rdlock"
        if junoconfig["env_dev"]:
            self.key = f"{junoconfig['plant']}.{junoconfig['module']}.rdlock.dev"
        self.ex = 60
        try:
            self.ex = int(junoconfig['input_cfg']["sched_interval"])
            self.ex += int(self.ex/3)
        except:
            pass
        self.uid: str = junoconfig['instance_id']

    def aquire(self):
        try:
            if junoconfig["env_dev"]:
                return True

            r = self.redis.setnx(self.key, self.uid)
            if not r:
                v = self.redis.get(self.key)
                if v.decode() != self.uid:
                    return False
            self.redis.expire(self.key, self.ex)
            return True
        except Exception as e:
            logging.error({e})
            return False


class Opc(IWriter, IReader):
    def __init__(self, lock: ALock = None, rediscli=None, **kwargs,):
        super(Opc, self).__init__()
        self.io = kwargs
        self.lock = lock
        self.redis: redis.Redis = rediscli

    def write(self, data: list[dict], **kwargs):
        if self.lock:
            if not self.lock.aquire():
                logging.warn("holding no lock, skip opc write")
                return
        ret = ""
        logging.info(junoconfig["instance_id"])
        if junoconfig["instance_id"].rfind(".dev") > 0:
            logging.warn("test env, skip opc write")
        else:
            try:
                ret = connector_write(data)
            except Exception as e:
                logging.error(f"failed to write opc: {e}")
                return ret

        logging.info(f"write opc data: {data}")

        if self.redis and "algo_system_spec" in junoconfig["algo_cfg"] and "MSET_aliases" in junoconfig["algo_cfg"]["algo_system_spec"]:
            aliases = junoconfig["algo_cfg"]["algo_system_spec"]["MSET_aliases"]
            day = datetime.now().strftime("%Y%m%d")
            lkey = f"system.ai.operations.{junoconfig['plant']}.{junoconfig['module']}.{day}"
            for x in data:
                k = x["key"]
                if k in aliases:
                    v = x["value"]
                    alias = aliases[k]
                    record = {
                        "key": k,
                        "value": v,
                        "alias": alias,
                        "et": datetime.now().timestamp()*1000
                    }
                    logging.info(
                        f"write local with ai operation record: {record}")
                    self.redis.lpush(
                        lkey, json.dumps(record, ensure_ascii=False).encode("utf-8"))

        return ret

    def read(self, **kwargs):
        pass


class Singleton(object):
    _instance = {}
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._lock.acquire()
            if not cls._instance:
                cls._instance = super().__new__(cls)
            cls._lock.release()

        return cls._instance

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            Singleton._lock.acquire()
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
            Singleton._lock.release()

        logging.info(f"singleton: {cls._instances}")
        return cls._instances[cls]


class Pulsar(IWriter, IReader):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._lock.acquire()
            if not cls._instance:
                cls._instance = super().__new__(cls)
            cls._lock.release()

        logging.info(f"called __new__: {cls._instance}")
        return cls._instance

    def __init__(self, lock: ALock = None, **kwargs):
        logging.info(f"called __init__: {self}")
        super().__init__()
        md5 = hashlib.md5()
        md5.update(json.dumps(kwargs, sort_keys=True).encode())
        key = md5.hexdigest()
        self.io = pulsar_cli(**kwargs)
        msg = f"pulsar args: {kwargs}"
        logging.info(msg)
        print(msg)

        self.producers: Dict[str, Producer] = {}
        self.consumers: Dict[str, Consumer] = {}
        self.plant = junoconfig["plant"]
        self.module = junoconfig["module"]
        self.instance_id = junoconfig["instance_id"]
        # prevent multipule instance issue
        self.name = f"{self.instance_id}"
        self.lock = lock

    def write(self, table: str, data: dict, **kwargs):
        if self.lock:
            if not self.lock.aquire():
                logging.warn("holding no lock, skip pulsar write")
                return

        topic = f'up-{self.plant}-{self.module}_{table}'
        if not (topic in self.producers):
            self.producers[topic] = self.io.create_producer(topic)
        try:
            self.producers[topic].send(json.dumps(data).encode('utf-8'))
            logging.info(f'write cloud: sent {data} to {topic}')
        except Exception as e:
            logging.error(f"failed to write cloud pulsar: {e}")

    def read(self, topic: str, shared: bool = False):
        #   if self.lock:
        #         if not self.lock.aquire():
        #             logging.warn("holding no lock, skip pulsar read")
        #             return

        subtype = ConsumerType.Shared
        if not shared:
            subtype = ConsumerType.Exclusive

        if topic not in self.consumers:

            self.consumers[topic] = self.io.subscribe(topic, self.name,
                                                      consumer_type=subtype, initial_position=InitialPosition.Latest,
                                                      schema=schema.BytesSchema(), pattern_auto_discovery_period=1, broker_consumer_stats_cache_time_ms=1500)
        try:
            return self.consumers[topic].receive()
        except Exception as e:
            logging.error(f"failed to read opc: {e}")
            return None


class Mongo(IWriter, IReader):
    def __init__(self, **kwargs):
        super(Mongo, self).__init__()
        self.url = kwargs['url']
        self.io = mongo_cli(self.url)

    def write(self, table: str, data: dict, **kwargs):
        ''' write to mongodb
            table: str, collection name
            data: dict, document to store
        database is derived from runtime environment
        '''
        logging.info(junoconfig)

        plant = junoconfig['plant']
        module = junoconfig['module']
        self.io[plant][f'{module}_{table}'].insert_one(data)

    def read(self, **kwargs):
        pass


class Redis(IWriter, IReader):
    def __init__(self, **kwargs):
        super(Redis, self).__init__()
        self.io = redis_cli(**kwargs)
        self.lock = RDLock(self.io)

    def write(self, key: str, value: dict | bytes | float | int | str, **kwargs):
        if not self.lock.aquire():
            logging.warn("holding no lock, skip redis write")
            return

        if isinstance(value, dict):
            logging.info(f"write local:  {key} -> {value}")
            self.io.json().set(key, '$', value)
        else:
            self.io.set(key, value)

    def read(self, key: str, cast=dict, **kwargs):
        if cast == dict:
            return self.io.json().get(key)
        r = self.io.get(key)
        if not r:
            return None

        return cast(r)

# class Elastic(IWriter, IReader):
#     def __init__(self, **kwargs):
#         super(Elastic, self).__init__()
#         self.url = kwargs['url']
#         self.ca = kwargs['ca']
#         self.user=kwargs['user']
#         self.password=kwargs['password']
#         self.io:Elasticsearch=es_cli(self.url, ca=self.ca,user=self.user, password=self.password)

#     def write(self, **kwargs):
#         topic=kwargs['topic']
#         data=kwargs['data']
#         id = ""

#         if "et" in data:
#             id = str(data["et"])

#         for x in ["time", "ts", "timestamp"]:
#             if id:
#                 break
#             if x in data:
#                 if isinstance(data[x], str):
#                     try:
#                         id = str(dateparser.parse(data[x]).timestamp()*1000)
#                     except:
#                         pass
#                 elif isinstance(data[x], datetime):
#                         id = str(data[x].timestamp()*1000)

#         if id:
#             self.io.index(index=topic, id=id, document=data)
#         else:
#             self.io.index(index=topic, document=data)

#     def read(self, **kwargs):
#         pass


class Clickhouse(IWriter, IReader):
    def __init__(self, *args, **kwargs):
        super(Clickhouse, self).__init__()
        self.url = kwargs['url']
        self.io: CHClient = clickhouse_cli(self.url)

    def write(self, **kwargs):
        pass

    def read(self, table: str,  tskey: str, tags: List[str] = [], num=0, time_from=None, time_to=None):
        cols = "*"
        if tags:
            if tskey not in tags:
                tags.append(tskey)
            tags = list(map(lambda x: f"`{x}`", tags))
            cols = ", ".join(tags)

        sql = f"select {cols} from {table}"
        for x in [time_from, time_to]:
            if isinstance(x, str) or isinstance(x, datetime) or x is None:
                pass
            else:
                raise Exception("invalid time_from or time_to")

        if not time_to and not time_from and not num:
            raise Exception("must provide time_from or time_to or num")
        else:
            s1 = ""
            s2 = ""
            if time_to:
                if isinstance(time_to, datetime):
                    time_to = time_to.strftime("%Y-%m-%d %H:%M:%S")
                s1 = f"{tskey} <= '{time_to}'"
            if time_from:
                if isinstance(time_from, datetime):
                    time_from = time_from.strftime("%Y-%m-%d %H:%M:%S")
                s2 = f"{tskey} > '{time_from}'"
            if s1 and s2:
                sql += f" where {s1} and {s2} "
            else:
                for x in [s1, s2]:
                    if x:
                        sql += f" where {x} "
        order = "asc"
        if num > 0:
            order = "desc"

        sql += f" order by {tskey} {order}"
        if num > 0:
            sql += f" limit {num}"

        logging.info(sql)
        try:
            r = self.io.query(sql)
            logging.info(f"got {len(r.result_rows)} records from dataset")
            data = list(map(lambda x: x[:-1], r.result_rows))
            timestamps = [x[-1] for x in r.result_rows]
            data = np.array(data, dtype=np.float32)
            column_names = r.column_names[:-1]

            if num > 0:
                timestamps.reverse()
                data = np.flip(data, 0)

            return data, timestamps, column_names
        except Exception as e:
            logging.error(f"exception: {e}")
            return None, None, None

# class Qdb(IWriter, IReader):
#     def __init__(self, *args, **kwargs):
#         super(Qdb, self).__init__()
#         self.init_kwargs=kwargs
#         self.io = qdb_cli(**self.init_kwargs)

#     def write(self, **kwargs):
#         topic=kwargs['topic']
#         data={k.translate(k.maketrans({'-':'_', '.': '_'})):v  for k,v in kwargs['data'].items()}
#         buff = self.io.new_buffer()
#         buff.row(topic, columns=data)
#         self.io.flush(buff)

#     def read(self, **kwargs):
#         pass


def MakeDB(kind: str, **kwargs):
    if kind == 'clickhouse':
        return Clickhouse(**kwargs)
    # elif kind == 'elastic':
    #     return Elastic(**kwargs)
    # elif kind == 'qdb':
    #     return Qdb(**kwargs)
    elif kind == 'mongo':
        return Mongo(**kwargs)
    else:
        raise Exception(f'unkown kind of db: {kind}')
