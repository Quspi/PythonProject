import pytest

from src.analysis import filter_by_description, get_category_counts


@pytest.mark.parametrize(
    "operations, categories, expected",
    [
        ([{"description": "A"}], ["A"], {"A": 1}),
        ([], ["A"], {}),
        ([{"description": "A"}], [], {}),
        ([{"description": "A"}], ["B"], {}),
        ([{"description": "A"}, {"description": "A"}], ["A"], {"A": 2}),
        ([{"description": "A"}, {"description": "B"}], ["A", "B"], {"A": 1, "B": 1}),
        ([{"amount": 100}], ["A"], {}),
        ([{"description": None}], ["A"], {}),
        ([{"description": 123}], ["123"], {}),
    ],
)
def test_get_category_counts(operations, categories, expected):
    assert get_category_counts(operations, categories) == expected


@pytest.mark.parametrize(
    "operations, search_string, expected",
    [
        ([{"description": "Перевод организации"}], "Перевод", [{"description": "Перевод организации"}]),
        (
            [{"description": "Перевод организации"}, {"description": "Покупка товаров"}],
            "Перевод",
            [{"description": "Перевод организации"}],
        ),
        (
            [{"description": "Перевод организации"}, {"description": "Перевод физ лицу"}],
            "Перевод",
            [{"description": "Перевод организации"}, {"description": "Перевод физ лицу"}],
        ),
        ([{"description": "Покупка товаров"}], "Перевод", []),
        ([], "Перевод", []),
        ([{"amount": 100}], "Перевод", []),
        ([{"description": None}], "Перевод", []),
        ([{"description": "перевод организации"}], "Перевод", [{"description": "перевод организации"}]),
        ([{"description": "Оплата картой *1234"}], "*1234", [{"description": "Оплата картой *1234"}]),
    ],
)
def test_filter_by_description(operations, search_string, expected):
    result = filter_by_description(operations, search_string)
    assert result == expected
