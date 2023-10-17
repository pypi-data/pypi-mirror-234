import pytest

from barbuilder import Menu


def test_render():
    m = Menu()
    m.title = 'title'
    m.add_item('option 1')
    m.add_header('title2', length=20)
    i = m.add_item('option 2', color='green')
    i.add_item('suboption1', sfimage='calendar')
    i.add_divider()
    s = i.add_item('suboption2')
    s.href = 'https://github.com/swiftbar/SwiftBar'
    i.set_alternate('alt')
    i.add_item('suboption3', shell='/some/command', param0='"this is text"; rm -rf /')
    out = str(m)
    assert out == """\
title
title2 | length=20
---
option 1
option 2 | color=green
--suboption1 | sfimage=calendar
-----
--suboption2 | href=https://github.com/swiftbar/SwiftBar
--suboption3 | shell=/some/command param0='"this is text"; rm -rf /'
alt | alternate=True
"""

def test_clear_menu():
    m = Menu('menu', sfimage='circle')
    m.add_header('header')
    i = m.add_item('ite', color='red')

    assert m.title == 'menu'
    assert len(m.params) == 1
    assert len(m.headers) == 1
    assert len(m.children) == 1

    m.clear()

    assert m.title == ''
    assert len(m.params) == 0
    assert len(m.children) == 0
    assert len(m.headers) == 0


def test_clear_menuitem():
    m = Menu('menu', sfimage='circle')
    i = m.add_item('item', color='red')
    i.add_callback(print, 'test')
    i.set_alternate('alt', color='green')
    i.add_item('subitem')

    assert i.title == 'item'
    assert i._alternate is not None
    assert len(i.params) == 1
    assert len(i.children) == 1
    assert len(i._callbacks) == 1
    assert m.title == 'menu'
    assert len(m.children) == 1

    i.clear()

    assert i.title == ''
    assert i._alternate is None
    assert len(i.params) == 0
    assert len(i.children) == 0
    assert len(i._callbacks) == 0
    assert m.title == 'menu'
    assert len(m.children) == 1


def test_sfencode():
    m = Menu('menu')
    i = m.add_item('item', sfimage='circle')
    i.sfconfig = {"renderingMode":"Palette", "colors":["red","blue"], "scale": "large", "weight": "bold"}
    assert i.sfconfig == 'eyJyZW5kZXJpbmdNb2RlIjogIlBhbGV0dGUiLCAiY29sb3JzIjogWyJyZWQiLCAiYmx1ZSJdLCAic2NhbGUiOiAibGFyZ2UiLCAid2VpZ2h0IjogImJvbGQifQ=='
