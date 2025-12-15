from unittest.mock import patch

import pandas as pd
import pytest

from src.data_loader import read_csv_transactions, read_excel_transactions


@patch("pandas.read_csv")
def test_read_csv_transactions(read_csv_mock, sample_dataframe):
    read_csv_mock.return_value = sample_dataframe
    result = read_csv_transactions("data/test.csv", delimiter=";")
    expected_result = [{"amount": 100, "currency": "USD", "id": 1}, {"amount": 200, "currency": "EUR", "id": 2}]

    assert result == expected_result
    assert isinstance(result, list)
    assert isinstance(result[0], dict)
    assert result[0]["id"] == 1
    assert result[0]["amount"] == 100

    read_csv_mock.assert_called_once_with("data/test.csv", delimiter=";")


@patch("pandas.read_csv")
def test_invalid_path_read_csv_transactions(read_csv_mock):
    read_csv_mock.side_effect = FileNotFoundError

    with pytest.raises(ValueError, match="Файл не найден"):
        read_csv_transactions("invalid_path.csv")

    read_csv_mock.assert_called_once_with("invalid_path.csv", delimiter=",")


@patch("pandas.read_csv")
def test_empty_data_read_csv_transactions(read_csv_mock):
    read_csv_mock.return_value = pd.DataFrame()
    result = read_csv_transactions("empty_file.csv", delimiter=".")

    assert len(result) == 0
    assert isinstance(result, list)

    read_csv_mock.assert_called_once_with("empty_file.csv", delimiter=".")


@patch("pandas.read_excel")
def test_read_excel_transactions(read_excel_mock, sample_dataframe):
    read_excel_mock.return_value = sample_dataframe
    result = read_excel_transactions("data/test.xlsx", sheet_name="sheet1")
    expected_result = [{"amount": 100, "currency": "USD", "id": 1}, {"amount": 200, "currency": "EUR", "id": 2}]

    assert result == expected_result
    assert isinstance(result, list)
    assert isinstance(result[0], dict)
    assert result[0]["id"] == 1
    assert result[0]["amount"] == 100

    read_excel_mock.assert_called_once_with("data/test.xlsx", sheet_name="sheet1")


@patch("pandas.read_excel")
def test_invalid_path_read_excel_transactions(read_excel_mock):
    read_excel_mock.side_effect = FileNotFoundError

    with pytest.raises(ValueError, match="Файл не найден"):
        read_excel_transactions("invalid_path.xlsx")

    read_excel_mock.assert_called_once_with("invalid_path.xlsx", sheet_name=0)


@patch("pandas.read_excel")
def test_empty_data_read_excel_transactions(read_excel_mock):
    read_excel_mock.return_value = pd.DataFrame()
    result = read_excel_transactions("empty_file.xlsx", sheet_name=10)

    assert len(result) == 0
    assert isinstance(result, list)

    read_excel_mock.assert_called_once_with("empty_file.xlsx", sheet_name=10)
