def filter_by_state(items: list[dict], state: str = "EXECUTED") -> list[dict]:
    result = []
    for item in items:
        if item.get("state") == state:
            result.append(item)
    return result


# if __name__ == "__main__":
#     test_data = [
#         {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
#         {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
#         {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
#         {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
#     ]
#     new_state = "CANCELED"
#     print(filter_by_state(test_data, new_state))
