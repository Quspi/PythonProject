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
