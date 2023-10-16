#! /usr/bin/env python3
# vim:fenc=utf-8
from time import time

class ReportTime:
    def __init__(self):
        self.i = 0
        self.last_t = time()
        self.t = {}

    def __call__(self, name=None):
        t = time()
        name = self.i if name is None else name
        self.t[name] = [t - self.last_t]
        self.i += 1
        self.last_t = time()

    def next(self):
        self.i = 0
        self.__call__ = self.call_next

    def call_next(self, name=None):
        t = time()
        name = self.i if name is None else name
        self.t[name].append(t - self.last_t)
        self.i += 1
        self.last_t = time()

    def __repr__(self):
        out = []
        for i, t in self.t.items():
            t = sum(t) / len(t)
            out.append(f"{i}={t:.4f}")
        return "\n".join(out)

