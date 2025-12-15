import pandas as pd
import pytest


@pytest.fixture
def sample_operations():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def operations_empty_state():
    return [
        {"id": 1, "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 3, "date": "2018-09-12T21:27:25.241689"},
    ]


@pytest.fixture
def operations_empty_list():
    return []


@pytest.fixture
def operations_none_values():
    return [
        {"id": 1, "state": None, "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": None},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    ]


@pytest.fixture
def operations_additional_states():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "state": "PENDING", "date": "2019-06-30T02:08:58.425572"},
        {"id": 3, "state": "FAILED", "date": "2019-05-12T21:27:25.241689"},
        {"id": 4, "state": "PROCESSING", "date": "2019-04-14T08:21:33.419441"},
    ]


@pytest.fixture
def sample_transactions():
    return [
        {"id": 1, "operationAmount": {"amount": "100.0", "currency": {"code": "USD", "name": "US Dollar"}}},
        {"id": 2, "operationAmount": {"amount": "200.0", "currency": {"code": "EUR", "name": "Euro"}}},
        {"id": 3, "operationAmount": {"amount": "300.0", "currency": {"code": "USD", "name": "US Dollar"}}},
        {"id": 4, "operationAmount": {"amount": "400.0", "currency": {"code": "RUB", "name": "Russian Ruble"}}},
    ]


@pytest.fixture
def empty_transactions():
    return []


@pytest.fixture
def usd_only_transactions():
    return [
        {"id": 1, "operationAmount": {"amount": "100.0", "currency": {"code": "USD", "name": "US Dollar"}}},
        {"id": 2, "operationAmount": {"amount": "200.0", "currency": {"code": "USD", "name": "US Dollar"}}},
    ]


@pytest.fixture
def invalid_structure_transactions():
    return [
        {"id": 1},
        {"id": 2, "operationAmount": {"amount": "100"}},
        {"id": 3, "operationAmount": {"amount": "100", "currency": {}}},
    ]


@pytest.fixture
def transactions_with_descriptions():
    return [
        {"description": "Payment", "operationAmount": {"currency": {"code": "USD"}}},
        {"description": "Transfer", "operationAmount": {"currency": {"code": "EUR"}}},
        {"description": "Withdrawal", "operationAmount": {"currency": {"code": "USD"}}},
    ]


@pytest.fixture
def transactions_without_descriptions():
    return [
        {"operationAmount": {"currency": {"code": "USD"}}},
        {"operationAmount": {"currency": {"code": "EUR"}}},
        {"operationAmount": {"currency": {"code": "RUB"}}},
    ]


@pytest.fixture
def transactions_mixed_descriptions():
    return [
        {"description": "Payment", "operationAmount": {"currency": {"code": "USD"}}},
        {"operationAmount": {"currency": {"code": "EUR"}}},
        {"description": "", "operationAmount": {"currency": {"code": "GBP"}}},
        {"description": None, "operationAmount": {"currency": {"code": "JPY"}}},
    ]


@pytest.fixture
def transactions_long_description():
    return [
        {"description": "A" * 1000, "operationAmount": {"currency": {"code": "USD"}}},
    ]


@pytest.fixture
def transaction_rub():
    return {"operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}}}


@pytest.fixture
def transaction_usd():
    return {"operationAmount": {"amount": "2.5", "currency": {"code": "USD"}}}


@pytest.fixture
def transaction_eur():
    return {"operationAmount": {"amount": "1.0", "currency": {"code": "EUR"}}}


@pytest.fixture
def transaction_invalid_transaction_format():
    return {"Amount": {"amount": "1.0", "currency": {"code": "EUR"}}}


@pytest.fixture
def transaction_gbp():
    return {"operationAmount": {"amount": "1.0", "currency": {"code": "GBP"}}}


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({"id": [1, 2], "amount": [100, 200], "currency": ["USD", "EUR"]})
