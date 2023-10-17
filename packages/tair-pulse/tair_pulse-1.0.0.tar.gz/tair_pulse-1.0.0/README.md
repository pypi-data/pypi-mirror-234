# TairPulse
TairPulse is a tool to visualize the latency and availability of Tair/Redis instances.

## Install

TairPulse requires `Python 3.6` or later.

Install with `pip` or your favorite PyPI package manager.

```bash
pip install tair-pulse
```

## Usage

1. Make sure the Redis instance is running.
2. Start tair_availability with:
```bash
tair_availability --host xxx.xxx.xxx.xxx --port xxxx
```
3. Do some operations on your redis, such as switch over, scale, resharding.
4. Make sure the above operation is over, stop tair_availability with `Ctrl+C`.
