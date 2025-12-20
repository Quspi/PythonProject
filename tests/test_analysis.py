import pytest
from src.analysis import get_category_counts, filter_by_description


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

