from __future__ import annotations

import sys
import traceback
from argparse import ArgumentParser
from collections.abc import Callable
from functools import wraps
from time import sleep
from typing import TypeVar, Union

from .base import ConfigurableItem, Item, NestableItem, Params
from .utils import (PLUGIN_PATH, P, copy_to_clipboard, deserialize_callback,
                    refreshplugin)


R = TypeVar('R')
MetaDecorator = Union[
    Callable[..., None],
    Callable[[Callable[..., R]], Callable[..., None]]
]


class Divider(Item):
    title = '---'


class HeaderItem(ConfigurableItem):
    pass


class MenuItem(NestableItem):

    def add_item(self, title: str = '', **params: Params) -> MenuItem:
        item = MenuItem(title, **params)
        self.children.append(item)
        return item

    def add_divider(self) -> Item:
        item = Divider()
        self.children.append(item)
        return item


class Menu(MenuItem):
    def __init__(self, title: str = '', **params: Params) -> None:
        super().__init__(title, **params)
        self.headers: list[Item] = []
        self.body: list[Item] = []
        self._main: Callable[..., None] | None = None

    def __str__(self) -> str:
        lines = [self._render_line()]
        if self._alternate is not None:
            lines.append(str(self._alternate))
        for item in self.headers:
            lines.append(str(item))
        lines.append(str(Divider()))
        for item in self.children:
            lines.append(str(item))
        return '\n'.join(lines) + '\n'

    def _run_callbacks(self, callbacks: list[str]) -> None:
        for callback in callbacks:
            func: Callable[..., object]
            args: P.args
            kwargs: P.kwargs
            func, args, kwargs = deserialize_callback(callback)
            func(*args, **kwargs)

    def add_header(self, title: str, **params: Params) -> Item:
        item = HeaderItem(title, **params)
        self.headers.append(item)
        return item

    def clear(self) -> None:
        super().clear()
        self.headers.clear()

    def reset(self) -> None:
        print('\u001B[2J\u001B[0;0f')
        print('~~~')

    def error(self, message: str) -> None:
        self.clear()
        self.title = f':exclamationmark.triangle.fill: {PLUGIN_PATH.name}'
        self.params['sfcolor'] = 'yellow'
        error = self.add_item('Error running plugin')
        error.add_item('Traceback')
        error.add_divider()
        error.add_item(
            message, size=12, font='courier',
            tooltip='Copy error to clipboard'
        ).add_callback(copy_to_clipboard, message)
        self.add_divider()
        self.add_item(
            'Refresh', sfimage='arrow.clockwise'
        ).add_callback(refreshplugin)

    def runner(
        self, func: Callable[..., R] | None = None, *, clear: bool = False
    ) -> MetaDecorator[R]:

        def wrapperfactory(inner_func: Callable[P, R]) -> Callable[..., None]:
            @wraps(inner_func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
                if clear:
                    self.clear()
                try:
                    inner_func(*args, **kwargs)
                except: # pylint: disable=bare-except
                    exc_info = sys.exc_info()
                    traceback_text = ''.join(traceback.format_exception(*exc_info)).strip()
                    self.error(traceback_text)
            return wrapper

        def decorator(inner_func: Callable[..., R]) -> Callable[..., None]:
            self._main = wrapperfactory(inner_func)
            return self._main

        if func is None:
            return decorator
        self._main = wrapperfactory(func)
        return self._main

    def run(self, repeat_interval: float | Callable[[], float] | None = None) -> None:
        parser = ArgumentParser(add_help=False)
        parser.add_argument('--script-callbacks', nargs='+')
        args = parser.parse_args()
        if args.script_callbacks is not None:
            self._run_callbacks(args.script_callbacks)
            return
        if self._main is None:
            raise RuntimeError('no main function specified')
        if repeat_interval is None:
            self._main()
            print(self)
            return

        while True:
            self._main()
            self.reset()
            print(self, flush=True)
            if callable(repeat_interval):
                sleep(repeat_interval())
            else:
                sleep(repeat_interval)
