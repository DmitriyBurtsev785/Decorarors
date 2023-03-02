import os
from datetime import datetime

# Задание 1 (декоратор, который записывает в файл)

def logger(old_function):
    def new_function(*args, **kwargs):
        current_time = datetime.now().strftime('дата %d-%m-%Y время %H:%M:%S')
        name_func = old_function.__name__
        results = old_function(*args, **kwargs)
        with open('main.log', 'a', encoding='utf-8') as file:
            file.write(f'Время вызова функции - {current_time}, '
                       f'имя функции - {name_func}, '
                       f'аргументы функции - {args, kwargs}, '
                       f'значение функции - {results}')
        return results
    return new_function

# Задание 2 (Путь к файлу передаётся в аргументах декоратора)

def logger_func(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            current_time = datetime.now().strftime('дата %d-%m-%Y время %H:%M:%S')
            name_func = old_function.__name__
            results = old_function(*args, **kwargs)
            with open(path, 'a', encoding='utf-8') as file:
                file.write(f'Дата и время вызова функции - {current_time}, '
                           f'Имя функции - {name_func}, '
                           f'Аргументы функции - {args, kwargs}, '
                           f'Возвращаемое значение функции - {results}')

            return results
        return new_function
    return __logger



def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()


# Задание 3 (Применил написанный логгер к приложению из прошлого ДЗ)

class FlatIterator:
    @logger
    def __init__(self, current_list):
        self.current_list = current_list # складываем сюда список
        self.cursor = -1 # определяем переменную для прохода по основному списку
        self.list_len = len(self.current_list) # кол-во проходов по основному циклу

    @logger
    def __iter__(self):
        self.cursor += 1 # начинаем итерацию, увеличиваем переменную для обхода основного списка на 1
        self.nested_cursor = 0 # создаём переменную для обхода внутреннего списка
        return self # возвращаем ссылку на объект класса

    @logger
    def __next__(self):
        if self.nested_cursor == len(self.current_list[self.cursor]): # если вложенный список дошёл до конца,
          iter(self) #  то, вызываем метод iter(), переходим к следующему вложенному списку
        if self.cursor == self.list_len: # если основной список дошёл до конца,
          raise StopIteration # останавливаем наш итератор
        self.nested_cursor += 1 # о мере итерации увеличиваем на 1 переменную для подсчёта кол-ва итераций по внутренним спискам
        return self.current_list[self.cursor][self.nested_cursor - 1] # возвращаем текущий элемент списка


def test_1():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


if __name__ == '__main__':
    test_1()

list_of_lists = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

flat_list = [item for item in FlatIterator(list_of_lists)]
print(flat_list)