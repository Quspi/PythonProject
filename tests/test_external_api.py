from unittest.mock import Mock, patch

import pytest
from requests.exceptions import RequestException

from src.external_api import convert_transaction_to_rub


def test_convert_rub_transaction(transaction_rub):
    result = convert_transaction_to_rub(transaction_rub)

    assert result == 31957.58


@patch("requests.get")
@patch("os.getenv")
def test_convert_usd_transaction_success(mock_getenv, mock_get, transaction_usd):
    mock_getenv.return_value = "test_api_key"

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 200.0}

    mock_get.return_value = mock_response

    result = convert_transaction_to_rub(transaction_usd)

    assert result == 200.0
    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert",
        headers={"apikey": "test_api_key"},
        params={"to": "RUB", "from": "USD", "amount": 2.5},
        timeout=15,
    )


@patch("requests.get")
@patch("os.getenv")
def test_convert_eur_transaction_success(mock_getenv, mock_get, transaction_eur):
    mock_getenv.return_value = "test_api_key"

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 86.5624}

    mock_get.return_value = mock_response

    result = convert_transaction_to_rub(transaction_eur)

    assert result == 86.56
    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert",
        headers={"apikey": "test_api_key"},
        params={"to": "RUB", "from": "EUR", "amount": 1.0},
        timeout=15,
    )


def test_invalid_transaction_format(transaction_invalid_transaction_format):
    with pytest.raises(KeyError, match="Некорректный формат данных"):
        convert_transaction_to_rub(transaction_invalid_transaction_format)


@patch("os.getenv")
def test_missing_api_key(mock_getenv, transaction_usd):
    mock_getenv.return_value = None

    with pytest.raises(ValueError, match="API_KEY не найден в переменных окружения"):
        convert_transaction_to_rub(transaction_usd)


@patch("requests.get")
@patch("os.getenv")
def test_test_api_4xx_error(mock_getenv, mock_get, transaction_eur):
    mock_getenv.return_value = "test_api_key"

    response_mock = Mock()
    response_mock.status_code = 400

    mock_get.return_value = response_mock

    with pytest.raises(ValueError, match=f"Код ошибки: {response_mock.status_code}"):
        convert_transaction_to_rub(transaction_eur)


@patch("requests.get")
@patch("os.getenv")
def test_test_api_5xx_error(mock_getenv, mock_get, transaction_eur):
    mock_getenv.return_value = "test_api_key"

    response_mock = Mock()
    response_mock.status_code = 500

    mock_get.return_value = response_mock

    with pytest.raises(ConnectionError, match=f"Код ошибки: {response_mock.status_code}"):
        convert_transaction_to_rub(transaction_eur)


@patch("requests.get")
@patch("os.getenv")
def test_api_unexpected_status(mock_getenv, mock_get, transaction_eur):
    mock_getenv.return_value = "test_api_key"

    response_mock = Mock()
    response_mock.status_code = 300

    mock_get.return_value = response_mock

    with pytest.raises(ConnectionError, match=f"Код ошибки: {response_mock.status_code}"):
        convert_transaction_to_rub(transaction_eur)


def test_unsupported_currency(transaction_gbp):
    with pytest.raises(ValueError, match="Неподдерживаемая валюта:"):
        convert_transaction_to_rub(transaction_gbp)


@patch("requests.get")
@patch("os.getenv")
def test_api_network_error(mock_getenv, mock_get, transaction_eur):
    mock_getenv.return_value = "test_api_key"

    mock_get.side_effect = RequestException

    with pytest.raises(ConnectionError, match="Ошибка сети:"):
        convert_transaction_to_rub(transaction_eur)
