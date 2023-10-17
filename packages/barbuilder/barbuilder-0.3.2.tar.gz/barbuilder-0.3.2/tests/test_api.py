import os
import pathlib
from urllib.parse import urlencode

import pytest

from barbuilder.utils import (disableplugin, enableplugin, notify, open_url,
                              refreshallplugins, refreshplugin, toggleplugin)


script_path = pathlib.Path(os.environ['SWIFTBAR_PLUGIN_PATH'])

def test_open_url(mock_subprocess):
    subp_args, subp_kwargs = open_url('swiftbar://notify', name='hello.py', title='test')
    assert subp_args == ( ['open', '-g', 'swiftbar://notify?name=hello.py&title=test'], )
    assert subp_kwargs == {'capture_output': True, 'check': True}



@pytest.mark.parametrize('method, in_args, in_kwargs, expected_args, expected_kwargs', [
    (
        notify,
        (),
        dict(title='title text', subtitle='subtitle text', body='body text', href='https://github.com/swiftbar/SwiftBar'),
        ( ['open', '-g', f'swiftbar://notify?name={script_path.name}&title=title+text&subtitle=subtitle+text&body=body+text&href=https%3A%2F%2Fgithub.com%2Fswiftbar%2FSwiftBar'], ),
        {'capture_output': True, 'check': True}
    ),
    (
        refreshplugin,
        (),
        {},
        ( ['open', '-g', f'swiftbar://refreshplugin?name={script_path.name}'], ),
        {'capture_output': True, 'check': True}
    ),
    (
        refreshallplugins,
        (),
        {},
        ( ['open', '-g', f'swiftbar://refreshallplugins'], ),
        {'capture_output': True, 'check': True}
    ),
    (
        enableplugin,
        (),
        {},
        ( ['open', '-g', f'swiftbar://enableplugin?name={script_path.name}'], ),
        {'capture_output': True, 'check': True}
    ),
    (
        disableplugin,
        (),
        {},
        ( ['open', '-g', f'swiftbar://disableplugin?name={script_path.name}'], ),
        {'capture_output': True, 'check': True}
    ),
    (
        toggleplugin,
        (),
        {},
        ( ['open', '-g', f'swiftbar://toggleplugin?name={script_path.name}'], ),
        {'capture_output': True, 'check': True}
    ),

])
def test_api_methods(method, in_args, in_kwargs, expected_args,
                     expected_kwargs, mock_subprocess, script_path):

    subp_args, subp_kwargs = method(*in_args, **in_kwargs)
    assert subp_args == expected_args
    assert subp_kwargs == expected_kwargs
