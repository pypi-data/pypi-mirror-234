from orup_errors import all_errors
from orup_errors.tests import args_test


def test_check_func(error_name: str, correct_args: dict, incorrect_args: dict, errors_dict=all_errors.orup_brutto_errors):
    """ Универсальная функция для тестирования check_func (функции проверки) с correct_args (на которые ожидается ответ
    False) и incorrect_args (на которые ожидается True)"""
    print('\nChecking %s' % error_name)
    check_func = get_check_func(error_name, errors_dict)
    print('\tTesting with correct args:')
    if not check_func(**correct_args):
        correct_result()
    print('\tTesting with incorrect args:')
    if check_func(**incorrect_args):
        correct_result()
    else:
        incorrect_result()

def get_check_func(error_name, errors_dict):
    """ Вернуть функцию проверку на ошибку по имени ошибки error_name """
    return errors_dict[error_name]['check_func']

def correct_result(*args, **kwargs):
    """ Совершается, если тест пройден успешно"""
    print("\t\tTest success")

def incorrect_result(*args, **kwargs):
    """ Совершается, если тест пройден успешно"""
    print("\t\tTest failed")

for error_name, error_info in all_errors.orup_brutto_errors.items():
    test_check_func(error_name, error_info['tests']['correct_values'], error_info['tests']['incorrect_values'])