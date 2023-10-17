from __future__ import annotations

import json
import re
import shlex
from base64 import b64encode
from collections.abc import Callable
from pathlib import Path
from textwrap import indent
from typing import Any, Iterator, Union


from.utils import serialize_callback, PLUGIN_PATH, P


Params = Union[str, int, bool, Path]
ParamsDict = dict[str, Params]



valid_params_re = re.compile('|'.join([
    'alternate', 'ansi', 'bash', 'checked', 'color', 'dropdown', 'emojize', 'font',
    'href', 'image', 'length', 'md', 'param[0-9]+', 'refresh', 'sfcolor([1-9]|10)?',
    'sfconfig', 'sfimage', 'sfsize', 'shell', 'shortcut', 'size', 'symbolize',
    'templateImage', 'terminal', 'tooltip', 'trim',  'webView', 'webViewHeight',
    'webViewWidth'
]), re.IGNORECASE)


class Item:
    title: str = ''

    def __str__(self) -> str:
        return self.title


class ConfigurableItem(Item):

    def __init__(self, title: str = '', **params: Params) -> None:
        super().__init__()
        self.title = title
        self._alternate: Item | None = None
        self._callbacks: list[str] = []
        self.params = params

    def __setattr__(self, name: str, value: Any) -> None:
        if valid_params_re.fullmatch(name):
            if name == 'sfconfig' and isinstance(value, dict):
                serialized = json.dumps(value).encode()
                encoded = b64encode(serialized).decode()
                self.params[name] = encoded
            else:
                self.params[name] = value
        else:
            self.__dict__[name] = value

    def __getattr__(self, name: str) -> Any:
        if valid_params_re.fullmatch(name):
            return self.params[name]
        if name not in self.__dict__:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )
        return self.__dict__[name]

    def __str__(self) -> str:
        return self._render_line()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.title}")'

    def _render_line(self) -> str:
        line = self.title.replace('|', chr(9474)) # melonamin is a smartass
        params = ' '.join(self._encode_params())
        if params:
            line = f'{line} | {params}'
        line = line.replace('\n', '\\n')
        return line

    def _encode_params(self) -> Iterator[str]:
        params = self.params
        if self._callbacks:
            params = params.copy()
            for key in self.params:
                if key in ['bash', 'shell', 'terminal'] or key.startswith('param'):
                    del params[key]
            params['shell'] = PLUGIN_PATH
            params['param0'] = '--script-callbacks'
            for i, callback in enumerate(self._callbacks, start=1):
                params[f'param{i}'] = callback
            params['terminal'] = False
        for key, value in params.items():
            yield f'{key}={shlex.quote(str(value))}'

    def add_callback(self, func: Callable[P, object], *args: P.args, **kwargs: P.kwargs) -> None:
        callback = serialize_callback(func, *args, **kwargs)
        self._callbacks.append(callback)

    def set_alternate(self, title: str, **params: Params) -> Item:
        cls = self.__class__
        params['alternate'] = True
        self._alternate = cls(title, **params)
        return self._alternate

    def clear(self) -> None:
        self.title = ''
        self._alternate = None
        self._callbacks.clear()
        self.params.clear()


class NestableItem(ConfigurableItem):

    def __init__(self, title: str = '', **params: Params) -> None:
        super().__init__(title, **params)
        self.children: list[Item] = []

    def __str__(self) -> str:
        lines = [self._render_line()]
        for item in self.children:
            lines.append(indent(str(item), '--'))
        if self._alternate is not None:
            lines.append(str(self._alternate))
        return '\n'.join(lines)

    def __repr__(self) -> str:
        children = ", ".join(repr(i) for i in self.children)
        return f'{self.__class__.__name__}("{self.title}", [{children}])'

    def clear(self) -> None:
        super().clear()
        self.children.clear()
