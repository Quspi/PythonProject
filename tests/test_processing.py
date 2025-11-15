from src.processing import filter_by_state


# Тестирование функции filter_by_state
def test_filter_by_state_executed(sample_operations):
    result = filter_by_state(sample_operations)
    assert len(result) == 2
    assert all(item["state"] == "EXECUTED" for item in result)
    assert [item["id"] for item in result] == [41428829, 939719570]


def test_filter_by_state_canceled(sample_operations):
    result = filter_by_state(sample_operations, "CANCELED")
    assert len(result) == 2
    assert all(item["state"] == "CANCELED" for item in result)
    assert [item["id"] for item in result] == [594226727, 615064591]


def test_filter_by_state_pending(operations_additional_states):
    result = filter_by_state(operations_additional_states, "PENDING")
    assert len(result) == 1
    assert result[0]["state"] == "PENDING"
    assert result[0]["id"] == 2


def test_filter_by_state_empty_list(operations_empty_list):
    result = filter_by_state(operations_empty_list)
    assert result == []


def test_filter_by_state_missing_state_field(operations_empty_state):
    result = filter_by_state(operations_empty_state, "EXECUTED")
    assert len(result) == 1
    assert result[0]["id"] == 939719570


def test_filter_by_state_none_values(operations_none_values):
    result = filter_by_state(operations_none_values, "EXECUTED")
    assert len(result) == 1
    assert result[0]["id"] == 939719570

    result_canceled = filter_by_state(operations_none_values, "CANCELED")
    assert len(result_canceled) == 1
    assert result_canceled[0]["id"] == 594226727


def test_filter_by_state_nonexistent_state(sample_operations):
    result = filter_by_state(sample_operations, "NONEXISTENT")
    assert result == []


def test_filter_by_state_empty_string_state(sample_operations):
    result = filter_by_state(sample_operations, "")
    assert result == []
