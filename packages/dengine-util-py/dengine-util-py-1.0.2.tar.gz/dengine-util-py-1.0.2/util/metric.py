import atexit
import os
import socket
import time

from util.log import logger

SERVER_LIST_FILE = '/home/xiaoju/statsd-client/server-list.txt'
FILE_EXPIRE_TIME = 10  # 10s

_server_list = []
_metric_socket = None
_namespace = None
_last_cache_time = 0.0
_file_mtime = 0.0


def log_fail(reason):
    logger.warning(reason)


def load_server_list():
    global _last_cache_time, _file_mtime, _server_list
    now = time.time()
    if now - _last_cache_time <= FILE_EXPIRE_TIME:
        return

    _last_cache_time = now

    if not os.path.exists(SERVER_LIST_FILE):
        return

    mtime = os.stat(SERVER_LIST_FILE).st_mtime
    if _file_mtime == mtime:
        return
    _file_mtime = mtime
    _server_list = []

    with open(SERVER_LIST_FILE) as conf:
        for line in conf:
            line = line.strip()
            if not line:
                continue

            addr, port = line.split(':', 1)

            try:
                port = int(port)
            except ValueError:
                continue

            _server_list.append((addr, port))


def set_namespace(ns):
    global _namespace
    _namespace = ns


def load_udp_socket():
    global _metric_socket
    if _metric_socket is not None:
        return

    _metric_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    atexit.register(_metric_socket.close)


def build_message(aggregator, metric, values, tags):
    if aggregator is None:
        log_fail('failed to send metric: aggregator is empty')
        return

    if aggregator == 'c' and not values:
        values = ['1']

    if not values:
        log_fail('failed to send metric: values is empty')
        return

    if metric is None:
        log_fail('failed to send metric: metric is empty')
        return

    if _namespace and '/' not in metric:
        metric = '{0}/{1}'.format(_namespace, metric)

    value_line = ','.join([str(v) for v in values])
    lines = [value_line, metric]

    if tags:
        lines += ['{0}={1}'.format(k, v) for k, v in tags.items()]

    lines.append(aggregator)
    return '\n'.join(lines).encode('utf8')


def send_metric(aggregator, metric, values=None, tags=None):
    """
    `aggregator` Aggregators:
       c        counter
       r,rt     ratio
       uc       unique counter
       pN       percentile N is [1~99]
       tN       percentile N is [5, 10, 20]
       rpc      rpc
    `values` is list
    `tags` is dict

    eg:.

    import metric
    metric.send_metric('p95,p99,p75,p50,p25,p5,p1', 'service.py.latency', [0.35])
    metric.send_metric('t5', 'user.purchase_sum', [13810302515, 30])
    metric.send_metric('rpc', 'rpc', [0.53, 'error'], {
                'caller':'/some-api',
                'callee':'http://10.10.10.10/another-api'
                }, 'ns')
    """
    data = build_message(aggregator, metric, values, tags)
    if not data:
        return

    load_server_list()

    if not _server_list:
        log_fail('statsd_server_list is empty')
        return

    hash_val = sum([ord(c) for c in metric])
    server_addr = _server_list[hash_val % len(_server_list)]

    load_udp_socket()
    _metric_socket.sendto(data, server_addr)

def count(name, counter, tags=None):
    send_metric('c', name, [counter], tags)

def gauge(name, counter, tags=None):
    send_metric('uc', name, [counter], tags)

def rpc(name, latency, tags=None):
    send_metric('p95,p99,p75,p50,p25,p5,p1', name, [latency], tags)
