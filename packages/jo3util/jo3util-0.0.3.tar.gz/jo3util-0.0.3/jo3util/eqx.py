#! /usr/bin/env python3

from typing import Callable, Optional

import equinox as eqx

from .fn import compose


def create_hook(
    fwd_pre: Callable = lambda *arg, **kwarg: None,
    fwd_post: Callable = lambda *arg, **kwarg: None,
    bwd_pre: Callable = lambda *arg, **kwarg: None,
    bwd_post: Callable = lambda *arg, **kwarg: None,
) -> Callable:
    def _create_hook(node: eqx.Module) -> eqx.Module:
        node_call = type(node).__call__

        @eqx.filter_custom_jvp
        def fwd(hook, *args, **kwargs):
            fwd_pre(*args, **kwargs)
            out = node_call(hook, *args, **kwargs)
            fwd_post(out)
            return out

        @fwd.def_jvp
        def bwd(primals, tangents):
            bwd_pre(*primals, *tangents)
            primals_out, tangents_out = eqx.filter_jvp(
                node_call, primals, tangents
            )
            bwd_post(primals_out, tangents_out)
            return primals_out, tangents_out

        class Hook(type(node)):
            def __init__(self, node):
                self.__dict__.update(node.__dict__)

            def __call__(self, *args, **kwargs):
                return fwd(self, *args, **kwargs)

        return Hook(node)

    return _create_hook
