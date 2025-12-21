import json
from unittest.mock import patch

from src.utils import load_transactions


@patch("os.path.exists")
@patch("builtins.open")
@patch("json.load")
def test_load_transactions(mock_json_load, mock_open, mock_exists):
    mock_exists.return_value = True
    mock_json_load.return_value = [{"operation": 1}, {"operation": 2}, {"operation": 3}]

    result = load_transactions("test.json")

    assert result == [{"operation": 1}, {"operation": 2}, {"operation": 3}]
    mock_open.assert_called_once_with("test.json", "r", encoding="UTF-8")
    mock_json_load.assert_called_once()
    mock_exists.assert_called_once_with("test.json")


@patch("os.path.exists")
def test_load_transactions_not_exist_file(mock_exists):
    mock_exists.return_value = False

    result = load_transactions("test.json")

    assert result == []
    mock_exists.assert_called_once_with("test.json")


@patch("os.path.exists")
@patch("builtins.open")
@patch("json.load")
def test_load_transactions_invalid_json(mock_json_load, mock_open, mock_exists):
    mock_exists.return_value = True
    mock_json_load.side_effect = json.JSONDecodeError("Invalid JSON", "test data", 5)

    result = load_transactions("test.json")

    assert result == []
    mock_open.assert_called_once_with("test.json", "r", encoding="UTF-8")


@patch("os.path.exists")
@patch("builtins.open")
@patch("json.load")
def test_load_transactions_json_not_list(mock_json_load, mock_open, mock_exists):
    mock_exists.return_value = True
    mock_json_load.return_value = {"operation": 1}

    result = load_transactions("test.json")

    assert result == []
    mock_open.assert_called_once_with("test.json", "r", encoding="UTF-8")


@patch("os.path.exists")
@patch("builtins.open")
@patch("json.load")
def test_load_transactions_empty_list(mock_json_load, mock_open, mock_exists):
    mock_exists.return_value = True
    mock_json_load.return_value = []

    result = load_transactions("test.json")

    assert result == []
    mock_open.assert_called_once_with("test.json", "r", encoding="UTF-8")
