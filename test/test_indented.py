from pytest import fixture

from ..indented_struct import *


def test_convert():
    assert convert('3') == 3
    assert isinstance(convert('3.0'), float)
    assert convert('3.3') == 3.3
    assert convert('3,3') == '3,3'


@fixture
def test_str():
    return iter(('  structure mechanic',
                 '   structure laser',
                 " foo= 'a' ",
                 " bar =0.5",
                 "endstructure",
                 "endstructure"))


# noinspection PyShadowingNames
def test_read_line(test_str):
    assert read_line(test_str) == ('struct_start', 'mechanic', None)
    assert read_line(test_str) == ('struct_start', 'laser', None)
    assert read_line(test_str) == ('assignment', 'foo', 'a')
    assert read_line(test_str) == ('assignment', 'bar', 0.5)
    assert read_line(test_str) == ('struct_end', None, None)
    assert read_line(test_str) == ('struct_end', None, None)


# noinspection PyShadowingNames
def test_atom(test_str):
    assert atom(test_str, read_line(test_str)) == ('mechanic', {'laser': {'foo': 'a', 'bar': 0.5}})
