import argparse
import datetime
import gc
import random
import signal
import time
from typing import Union

import plotly.graph_objects as go
import redis
from plotly_resampler import FigureResampler

from pulse.keys import SLOT2KEY

# args
EXAMPLES = """
Examples:

 Run the TairPulse with the default configuration against 127.0.0.1:6379:
   $ tair-pulse

 Test Aliyun Tair instance without password:
   $ tair-pulse --host r-bp1qf8wio5zkp01pzt.redis.rds.aliyuncs.com
 Test Cluster instance with password, one of the nodes is 192.168.10.1:7000:
   $ tair-pulse --host 192.168.10.1 --port 7000 --password 123456 --cluster
"""
parser = argparse.ArgumentParser(prog="tair-pulse",
                                 description="TairPulse is a tool to visualize Tair/Redis latency and availability.",
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=EXAMPLES)
parser.add_argument("--host", default="127.0.0.1", help="server hostname (default 127.0.0.1)")
parser.add_argument("--port", default=6379, help="server port (default 6379)")
parser.add_argument("--password", default="", help="password for Tair/Redis auth")
parser.add_argument("--cluster", default=False, action="store_true", help="server is a node of the Tair/Redis cluster")
parser.add_argument("--max-rt", default=0, type=float, help="print the key that exceeds the max-rt (default 0)")
g_args = parser.parse_args()

TYPE_CLIENT = Union[redis.RedisCluster, redis.Redis]
KEY_PREFIX = "tair_pulse_"

stopped = False
# data
data_dict = {}
# latency
datetime_array = []
latency_array = []
# error
error_dict = {}

TIMEOUT_SECONDS = 3


class ErrorPair:
    def __init__(self):
        self.array = []
        self.start_datetime = None


KEYS = [f"tair_pulse_{SLOT2KEY[i]}" for i in range(16384)]
g_stopped = False
g_error: [ErrorPair] = {}


class LatencySegment:
    def __init__(self):
        self.latency = []

    def add(self, latency):
        self.latency.append(latency)

    def __str__(self):
        length = len(self.latency)

        if length == 0:
            return "0"
        self.latency.sort()
        return f"avg: {sum(self.latency) / length:.1f}ms, min: {self.latency[0]:.1f}ms, max: {self.latency[-1]:.1f}ms"

    def clear(self):
        self.latency.clear()


def latency_normalization(latency: float):  # in ms
    return round(latency, 0)


def check_keys():
    try:
        r = create_client()
        for key in KEYS:
            ret = r.get(key)
            if ret is None:
                print(f"{key} should not be None")
                return
            ret = int(ret)
            if ret != data_dict[key]:
                print(f"{key} should be [{data_dict[key]}], but got [{ret}]")
                return
    except redis.exceptions.RedisError as e:
        print(f"error occurred when check keys: {e}")
        return


def clean_keys():
    try:
        r = create_client()
        for key in KEYS:
            r.delete(key)
    except redis.exceptions.RedisError as e:
        print(f"error occurred when cleaning up keys: {e}")
        return


def clear_all_errors():
    for error in error_dict.values():
        if error.start_datetime is not None:
            error.array.append((error.start_datetime, datetime.datetime.now()))
            error.start_datetime = None


def init_database():
    try:
        r = create_client()
        for i in range(16384):
            assert r.set(f"{KEY_PREFIX}{SLOT2KEY[i]}", i)
            data_dict[f"{KEY_PREFIX}{SLOT2KEY[i]}"] = i
    except redis.exceptions.RedisError as e:
        print(f"error occurred when init database: {e}")
        exit(0)


def run_write_cmd():
    r = create_client()
    gc.disable()

    print("start write test...")
    log_time = time.time()
    latency_segment = LatencySegment()
    while True:
        gc.collect()

        k = random.choice(SLOT2KEY)
        key = f"{KEY_PREFIX}{k}"
        if stopped:
            break

        start_date = datetime.datetime.now()
        error = None

        # latency
        start_time = time.time()
        try:
            ret = r.incr(key)
            data_dict[key] += 1
            assert ret == data_dict[key]
        except (redis.exceptions.RedisError, redis.exceptions.RedisClusterException) as e:
            error = str(e)
        latency = round((time.time() - start_time) * 1000, 1)

        if g_args.max_rt != 0 and latency > g_args.max_rt:
            print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]} latency is too high: {latency}, key:{key}")

        # error
        if error is not None:
            if error not in error_dict:
                error_dict[error] = ErrorPair()
            if error_dict[error].start_datetime is None:
                clear_all_errors()
                error_dict[error].start_datetime = start_date
                print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]} error occurred when writing data: {error}")
        else:
            clear_all_errors()
        # log
        latency_segment.add(latency)
        if start_time > log_time:
            log_time = start_time + 5
            print(f"{datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]} {latency_segment} {'' if error is None else 'error'}")
            latency_segment.clear()

        datetime_array.append(start_date)
        latency_array.append(round(latency, 1))

    clear_all_errors()
    gc.enable()


def signal_handler(sig, frame):
    global stopped
    if stopped:
        print("\nYou pressed Ctrl+C twice!")
        exit(0)
    print("\nYou pressed Ctrl+C!")
    stopped = True


def create_client() -> TYPE_CLIENT:
    if g_args.cluster:
        r = redis.RedisCluster(host=g_args.host, port=g_args.port, password=g_args.password,
                               cluster_error_retry_attempts=1,
                               socket_timeout=TIMEOUT_SECONDS,
                               socket_connect_timeout=TIMEOUT_SECONDS,
                               single_connection_client=True)

    else:
        r = redis.Redis(host=g_args.host, port=g_args.port, password=g_args.password,
                        socket_timeout=TIMEOUT_SECONDS,
                        socket_connect_timeout=TIMEOUT_SECONDS,
                        single_connection_client=True)
    return r


def dbsize() -> int:
    try:
        total_size = 0
        r = create_client()
        if g_args.cluster:
            redis_nodes = r.cluster_nodes()
            for node in redis_nodes:
                host, port = node.split(":")
                node_conn = redis.Redis(host=host, port=port, password=g_args.password)
                node_conn_size = node_conn.dbsize()
                total_size += node_conn_size
        else:
            total_size = r.dbsize()
    except redis.exceptions.RedisError as e:
        print(f"error occurred when get dbsize: {e}")
        return 0
    return total_size


def main():
    filename = f"pulse_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')}.html"
    signal.signal(signal.SIGINT, signal_handler)

    print("init database...")
    init_database()

    old_dbsize = dbsize()
    run_write_cmd()
    now_dbsize = dbsize()
    print(f"old dbsize: {old_dbsize}, new dbsize: {now_dbsize}, diff:{now_dbsize - old_dbsize}")

    print("Checking keys...")
    check_keys()

    print("Cleaning up...")
    clean_keys()

    print(f"Write data to latency.html... {len(datetime_array)}")
    fig = FigureResampler(go.Figure())
    fig.add_trace(go.Scattergl(name='latency', showlegend=False), hf_x=datetime_array, hf_y=latency_array)

    max_y = max(latency_array)
    for error_name, error in error_dict.items():
        x = [i[0] for i in error.array]
        y = [max_y for i in error.array]
        width = [(i[1] - i[0]).total_seconds() * 1000 for i in error.array]
        fig.add_trace(go.Bar(x=x, y=y, width=width, offset=0, name=error_name, opacity=0.7))
    fig.update_layout(
        title=f"TairPulse ({g_args.host}:{g_args.port})",
        yaxis_title="latency(ms)",
        height=500,
        legend=dict(yanchor="top", y=-0.2, xanchor="left", x=0)
    )
    fig.write_html(filename)
    print("Write finished.")

    fig.show_dash()
