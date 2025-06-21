from typing import Dict
from trading_bot_mvp.shared.model import FieldMap


class CustomFieldMap(FieldMap):
    mapping: Dict[str, str] = {'foo': 'bar', 'baz': 'qux'}


def test_field_map_instantiation():
    fmap = FieldMap(mapping={'a': 'b'})
    assert fmap.mapping['a'] == 'b'


def test_custom_field_map():
    fmap = CustomFieldMap()
    assert fmap.mapping['foo'] == 'bar'
    assert fmap.mapping['baz'] == 'qux'
