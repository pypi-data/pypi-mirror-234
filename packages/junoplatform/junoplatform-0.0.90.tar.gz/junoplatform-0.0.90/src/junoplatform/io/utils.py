"""junoplatform.io.utils.py: implements helper tools"""
from collections import UserDict
import os
from decouple import config as dcfg
import json
import redis
import yaml
from clickhouse_connect.driver import Client as CHClient
from urllib.parse import urlparse
import logging
import uuid
import pulsar
from itertools import islice
import oss2
from questdb.ingress import Sender, IngressError, TimestampNanos, TimestampMicros
import pymongo
import clickhouse_connect
from elasticsearch import Elasticsearch
from datetime import datetime

__author__ = "Bruce.Lu"
__email__ = "lzbgt@icloud.com"
__time__ = "2023/07/20"


def get_package_path(cfg: dict, package_id: str):
    plant = cfg['plant']
    module = cfg['module']

    return f"dist/{plant}-{module}-{package_id}.zip"


class JunoConfig(UserDict):
    def __init__(self):
        super(JunoConfig, self).__init__()
        self.data = {}
        if os.path.exists('project.yml'):
            with open('project.yml', 'r', encoding='utf-8') as f:
                self.data.update(yaml.safe_load(f))

        if os.path.exists('project-ext.yml'):
            with open('project-ext.yml', 'r', encoding='utf-8') as f:
                ext = yaml.safe_load(f)
                if ext and len(ext) > 0:
                    self.data.update()

        if "cloud" in self.data and "token" in self.data["cloud"]:
            pass
        else:
            jf = os.path.expanduser('~') + '/.juno/config.yaml'
            if os.path.exists(jf):
                with open(jf, 'r', encoding='utf-8') as f:
                    jc = yaml.safe_load(f)
                    self.data["cloud"] = jc
            else:
                self.data["cloud"] = {
                    "api": "http://192.168.101.158:/8823/api"}

        if "redis" not in self.data:
            self.data["redis"] = {
                "host": "192.168.101.158",
                "port": 6379,
                "password": "myredis"
            }
        if "pulsar" not in self.data:
            self.data["pulsar"] = {
                "url": "pulsar://192.168.101.158:6650"
            }

        try:
            if dcfg("instance_id", ""):
                self.data["instance_id"] = instance_id = dcfg("instance_id")
                self.data["env_dev"] = False
            else:
                self.data["instance_id"] = self.data['plant'] + \
                    '-' + self.data['module'] + '.' + uuid.uuid4().hex + \
                    '.' + datetime.now().strftime("%Y%m%d%H%M%S") + ".dev"
                self.data["env_dev"] = True
        except:
            pass
        self.data["input_cfg"] = {}
        try:
            with open('input.json', 'r', encoding='utf-8') as f:
                self.data["input_cfg"] = json.load(f)
        except:
            pass

        self.data["algo_cfg"] = {}
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                self.data["algo_cfg"] = json.load(f)
        except:
            pass

        if dcfg("cloud_api", ""):
            if "cloud" in self.data:
                self.data["cloud"]["api"] = dcfg("cloud_api")
            else:
                self.data["cloud"] = {"api": dcfg("cloud_api")}

    def __getitem__(self, key):
        try:
            return self.data[key]
        except KeyError:
            pass

        raise KeyError(key)

    def __setitem__(self, key, value):
        self.data[key] = value


junoconfig = JunoConfig()


def redis_cli(host: str, port: int, password: str, db: int = 0, socket_timeout=3):
    logging.debug(f"local redis: {host}:{port} {db} {password}")
    return redis.Redis(host, port, db, password, socket_timeout=socket_timeout)


def pulsar_cli(url: str, shared: bool = False, ca: str = "certs/ca.cert.pem",
               cert: str = "certs/client.cert.pem", key: str = "certs/client.key-pk8.pem"):
    client: pulsar.Client
    if 'ssl' in url:
        auth = pulsar.AuthenticationTLS(cert, key)
        client = pulsar.Client(url,
                               tls_trust_certs_file_path=ca,
                               tls_allow_insecure_connection=False,
                               authentication=auth)
    else:
        client = pulsar.Client(url)

    return client


def es_cli(url: str, ca: str, user: str, password: str):
    # cfg['elastic']['url'], ca_certs=cfg['elastic']['ca'],
    # basic_auth=(cfg['elastic']['user'], cfg['elastic']['password'])
    return Elasticsearch(url, ca_certs=ca, basic_auth=(user, password))


def clickhouse_cli(url: str):
    p = urlparse(url)
    schema = p.scheme
    if schema != 'ch':
        raise Exception(f'invalid schema in dbs.clickhouse.url: {url}')
    user = p.username
    password = p.password
    host = p.hostname
    port = p.port
    return clickhouse_connect.get_client(host=host, username=user,
                                         password=password, port=port)

# auth = ("pulsar", "KA6oqjb0s5OP49WHfKLabO8ef42ArV_9q9NznHNKUJ8", "_lTCuKKqtRWVDyb9d5545s99VwXVkJjs-HhCtPxPaTQ", "afh08JDKKYUxPYuHCWsytHQ7LgUZ63s-CTvTFaWFVE4")


def qdb_cli(host: str, port: str, auth: str, tls: bool, auto_flush: bool, **kwargs):
    auth_t = tuple(auth.split(' '))
    s = Sender(host, port, auth=auth_t, tls=tls, auto_flush=auto_flush)
    s.connect()
    return s


def mongo_cli(url: str):
    return pymongo.MongoClient(url)


def oss_cli(key: str, sec: str, endpoint: str, bucket: str):
    auth = oss2.Auth(key, sec)
    endpoint = endpoint
    r = oss2.Bucket(auth, endpoint, bucket, connect_timeout=5)
    # for b in islice(oss2.ObjectIterator(r), 10):
    #     print(b.key)
    return r
