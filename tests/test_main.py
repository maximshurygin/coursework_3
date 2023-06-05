import pytest
from main import (
    filter_executed_operations,
    sort_operations_by_date,
    mask_card_number,
    mask_account_number,
)


@pytest.fixture
def sample_data():
    return [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589"
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {
                "amount": "8221.37",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560"
        },
        {
            "id": 608117766,
            "state": "CANCELED",
            "date": "2018-10-08T09:05:05.282282",
            "operationAmount": {
                "amount": "77302.31",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на счет",
            "from": "Visa Gold 6527183396477720",
            "to": "Счет 38573816654581789611"
        }
    ]


def test_filter_executed_operations(sample_data):
    executed_operations = filter_executed_operations(sample_data)

    # Проверяем, что остались только операции с состоянием "EXECUTED"
    assert len(executed_operations) == 2
    assert all(operation["state"] == "EXECUTED" for operation in executed_operations)


def test_sort_operations_by_date(sample_data):
    sorted_operations = sort_operations_by_date(sample_data)

    # Проверяем, что операции отсортированы в правильном порядке
    assert len(sorted_operations) == 3
    assert sorted_operations[0]['date'][:10] == "2019-08-26"
    assert sorted_operations[1]['date'][:10] == "2019-07-03"
    assert sorted_operations[2]['date'][:10] == "2018-10-08"


def test_mask_card_number():
    card_number = "1596837868705199"
    card_number_2 = "7158300734726758"
    masked_card_number = mask_card_number(card_number)
    masked_card_number_2 = mask_card_number(card_number_2)

    # Проверяем, что номер карты маскируется правильно
    assert masked_card_number == "1596 83** **** 5199"
    assert masked_card_number_2 == "7158 30** **** 6758"


def test_mask_account_number():
    account_number = "64686473678894779589"
    account_number_2 = '35383033474447895560'
    masked_account_number = mask_account_number(account_number)
    masked_account_number_2 = mask_account_number(account_number_2)

    # Проверяем, что номер счета маскируется правильно
    assert masked_account_number == "**9589"
    assert masked_account_number_2 == "**5560"
