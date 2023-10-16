#! /usr/bin/env python3
# vim:fenc=utf-8

"""
This code is copied from https://stackoverflow.com/questions/366682/how-to-limit-execution-time-of-a-function-call/601168#601168
"""

import signal
from contextlib import contextmanager


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    """
    ## Usage
    try:
        with time_limit(10):
            long_function_call()
    except TimeoutException as e:
        print("Timed out!")
    """
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

