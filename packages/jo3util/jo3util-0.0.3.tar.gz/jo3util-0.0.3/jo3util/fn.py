#! /usr/bin/env python3
# vim:fenc=utf-8

from functools import reduce



def compose(*func):
    """Create a single function out of multiple functions."""

    def compose_(f, g):
        return lambda *args, **kwargs: f(g(*args, **kwargs))

    return reduce(compose_, func, lambda out: out)
if __name__ == "__main__":

    def fn0(x):
        print("fn0", x + 1)
        return x + 1

    def fn1(x):
        print("fn1", -x)
        return -x

    fn2 = compose(fn1, fn0)
    assert fn2(5) == -6
