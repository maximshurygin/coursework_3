import json


def load_json_file(json_file):
    """
    Загружает данные из JSON-файла и возвращает их в виде словаря.
    """
    with open(json_file) as file:
        data = json.load(file)
    return data


def filter_executed_operations(data):
    """
    Фильтрует операции с состоянием "EXECUTED" из данных.
    Возвращает список отфильтрованных операций.
    """
    executed_operations = [operation for operation in data if 'state' in operation and operation['state'] == 'EXECUTED']
    return executed_operations


def sort_operations_by_date(operations):
    """
    Сортирует операции по дате в убывающем порядке.
    Возвращает отсортированный список операций.
    """
    sorted_operations = sorted(operations, key=lambda x: x['date'], reverse=True)
    return sorted_operations


def mask_card_number(card_number):
    """
    Маскирует номер карты, оставляя видимыми только первые 6 и последние 4 цифры.
    Возвращает маскированный номер карты.
    """
    masked_card_number = card_number[:4] + ' ' + card_number[4:6] + '*' * 2 + ' ' + '*' * 4 + ' ' + card_number[-4:]
    return masked_card_number


def mask_account_number(account_number):
    """
    Маскирует номер счета, оставляя видимыми только последние 4 цифры.
    Возвращает маскированный номер счета.
    """
    masked_account_number = '**' + account_number[-4:]
    return masked_account_number


def print_recent_executed_operations(json_file):
    """
    Выводит список последних 5 операций.
    """
    data = load_json_file(json_file)
    executed_operations = filter_executed_operations(data)
    sorted_operations = sort_operations_by_date(executed_operations)

    for operation in sorted_operations[:5]:
        operation_date = operation['date'][:10]
        formatted_date = operation_date[8:] + '.' + operation_date[5:7] + '.' + operation_date[:4]
        operation_description = operation['description']
        operation_from = operation.get('from')
        operation_to = operation['to']
        operation_amount = operation['operationAmount']['amount']
        operation_currency = operation['operationAmount']['currency']['name']

        masked_card_number = None
        if operation_from:
            card_number = operation_from.split(' ')[-1]
            masked_card_number = mask_card_number(card_number)

        masked_account_number = mask_account_number(operation_to)

        print(formatted_date, operation_description)
        if masked_card_number:
            print(masked_card_number, '-> Счет', masked_account_number)
        else:
            print('Unknown -> Счет', masked_account_number)
        print(operation_amount, operation_currency)
        print()


json_file = 'operations.json'
print_recent_executed_operations(json_file)