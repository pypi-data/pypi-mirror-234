import os

import pytest

from barbuilder import Menu
from barbuilder.utils import deserialize_callback, serialize_callback


def dummy1():
    return True

def dummy2(*args):
    args_list = sorted([*args])
    return args_list

def dummy3(*args, **kwargs):
    args_list = []
    kwargs_list = []
    for arg in args:
        args_list.append(arg)
    for key, value in kwargs.items():
        kwargs_list.append((key, value))
    args_list.reverse()
    kwargs_list.reverse()
    return args_list, kwargs_list

dummy_callbacks = [
    [dummy1,    (),             {},                 True],
    [dummy2,    (3,1,2),        {},                 [1,2,3]],
    [dummy3,    ('a', 'b'),     {'x': 1, 'y': 2},   (['b', 'a'], [('y', 2), ('x', 1)])]
]


@pytest.mark.parametrize('in_func, in_args, in_kwargs, expected', dummy_callbacks)
def test_serialization(in_func, in_args, in_kwargs, expected):
    serialized = serialize_callback(in_func, *in_args, **in_kwargs)
    assert isinstance(serialized, str)

    func, args, kwargs = deserialize_callback(serialized)
    assert callable(func)
    assert isinstance(args, tuple)
    assert isinstance(kwargs, dict)
    assert args == in_args
    assert kwargs == in_kwargs

    result = func(*args, **kwargs)
    assert result == expected


@pytest.mark.parametrize('in_func, in_args, in_kwargs, expected', dummy_callbacks)
def test_add_callback(in_func, in_args, in_kwargs, expected, script_path):
    menu = Menu('menu')
    item = menu.add_item('option')
    item.add_callback(in_func, *in_args, **in_kwargs)
    out = str(menu)
    assert out == f"""\
menu
---
option | shell=/path/to/script.py param0=--script-callbacks param1={item._callbacks[0]} terminal=False
"""
