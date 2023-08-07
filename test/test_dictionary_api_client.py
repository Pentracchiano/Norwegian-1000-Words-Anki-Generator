import pytest
from unittest.mock import Mock
from dictionary_api_client import DictionaryAPIClient


def test_find_ids_by_word():
    session_mock = Mock()
    session_mock.get.return_value.json.return_value = {"articles": {"bm": [1, 2, 3]}}
    client = DictionaryAPIClient(session_mock)

    ids = client.find_ids_by_word('hund')
    assert len(ids) > 0
    assert isinstance(ids[0], int)
    assert 2 in ids
