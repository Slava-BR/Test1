import csv
import os
import re
from typing import Union, NoReturn

# Название файла с приветствием.
WELCOME = 'welcome_en'
# Директория в которой распологается программа
WORK_DIR = os.getcwd()
# Длина названия столбца
LEN_COLUMN = 20
# Разделитель строк, используется при печати
DELIMITER_LINE = ('+' + '-'.center(LEN_COLUMN, '-')) * 6 + '+'
# Кол-во записей отображаемых при печати
RECORDS_ON_PAGE = 5
PAGE_INDENTATION = 50


class PhoneBook:
    # Кол-во записей отображаемых при печати, меняется во время работы программы(Для страниц где меньше записей).
    records_on_page = RECORDS_ON_PAGE
    # текущая страница
    current_page = 0
    mode = ''
    count_page = 0
    count_records = 0
    # прочитанные записи, все функцию будут сохранять данные сюда
    records = []
    index_records = []

    def __init__(self, path_to_file: str, file_name: str, delimiter: str = ','):
        """
        :param path_to_file: Путь к файлу.
        :param file_name: Название файла.
        :param delimiter: Разделитель.
        """
        # Команды доступные при mode = '' и функции, которые отвечают за их обработку
        self.global_command = {'add': self.add,
                               'start-view': self.start_view,
                               'update': self.update,
                               'find': self.find_records,
                               }
        # Команды доступные при mode = 'view' и функции, которые отвечают за их обработку
        self.view_command = {'>>': self.next,
                             '<<': self.prev,
                             'go': self.go,
                             'find': self.find_records,
                             'stop-view': self.stop_view, }
        # Команды доступные при mode = 'update' и функции, которые отвечают за их обработку
        self.update_command = {'find': self.find_records,
                               'update': self.update,
                               'stop-update': self.stop_update}
        # сопоставляем mode и списко команды, которые будут доступны
        self.mode_command = {'': self.global_command,
                             'view': self.view_command,
                             'update': self.update_command}
        self.path_to_file = path_to_file
        self.file_name = file_name
        self.delimiter = delimiter
        # функции которые отвечают за проверку корректности определенного поля
        self.column_name = {'last_name': self.word_is_valid,
                            'first_name': self.word_is_valid,
                            'patronymic': self.word_is_valid,
                            'organization_name': self.word_is_valid,
                            'work_phone': self.phone_is_valid,
                            'personal_phone': self.phone_is_valid}

    # ------------------------- #
    # FUNCTION TO PRESENT DATA  #
    # ------------------------- #
    def start_view(self) -> Union[bool, str]:
        """
        Считывает данные из файл. Определяет кол-во записей и страниц. Меняет режим на view.
        Если инструкции выполняются без ошибок возвращает False. Иначе строку с ошибкой.
        """
        try:
            with open(os.path.join(self.path_to_file, self.file_name), 'r') as file:
                self.records = list(csv.reader(file, delimiter=self.delimiter))
                # записываем параметры
                self.count_records = len(self.records)
                self.count_page = -1 * len(self.records) // RECORDS_ON_PAGE * -1

                if self.count_records < self.records_on_page:
                    self.records_on_page = self.count_records + 1
                self.mode = 'view'
                return False
        except Exception:
            return "something went wrong"

    def next(self) -> Union[bool, str]:
        """
        Меняет текущий номер страницы на следующий, если это возможно.
        Если инструкции выполняются без ошибок возвращает False. Иначе строку с ошибкой.
        """
        if not self.count_page:
            return "invalid action"
        if self.current_page < self.count_page:
            self.current_page += 1
            if self.current_page == self.count_page:
                self.records_on_page = self.count_records % self.records_on_page
            return False
        else:
            return "invalid action"

    def prev(self) -> Union[bool, str]:
        """
        Меняет текущий номер страницы на предыдущий, если это возможно.
        Если инструкции выполняются без ошибок возвращает False. Иначе строку с ошибкой.
        """
        if not self.count_page:
            return "invalid action"
        if self.current_page == self.count_page:
            self.records_on_page = RECORDS_ON_PAGE
        if self.current_page > 1:
            self.current_page -= 1
            return False
        else:
            return "invalid action"

    def go(self, **kwargs) -> Union[bool, str]:
        """
        Меняет текущий номер страницы на номер переданный в kwargs[page], если это возможно.
        Если инструкции выполняются без ошибок возвращает False. Иначе строку с ошибкой.
        """
        if not self.count_page:
            return "invalid action"
        if 0 <= int(kwargs['page']) - 1 <= self.count_page:
            self.current_page = int(kwargs['page']) - 1
            return False
        else:
            return "uncorrected page"

    def stop_view(self) -> bool:
        """обнуляем mode и закрываем файл"""
        self.mode = ''
        self.records = []

        self.current_page = 0
        return False

    # ---------------- #
    # FUNCTION TO ADD  #
    # ---------------- #
    @staticmethod
    def word_is_valid(word: str) -> bool:
        pattern = re.compile("^(?:[A-Z]{1}|[А-Я]{1})(?:[a-z]{1,19}|[а-я]{1,19})$")
        return True if pattern.match(word) else False

    @staticmethod
    def phone_is_valid(phone: str) -> bool:
        pattern = re.compile("^((\+7|7|8)+([0-9]){10})$")
        return True if pattern.match(phone) else False

    def data_is_correct(self, **kwargs) -> Union[bool, str]:
        """
        Проверяет все ли ключи переданы и корректные ли они.
        Если инструкции выполняются без ошибок возвращает False. Иначе строку с ошибкой.
        """
        # Все ключи переданы?
        if len(kwargs) != len(self.column_name):
            return f"uncorrected number of parameters"

        # проверяем корректность переданных значений
        for name, func in self.column_name.items():
            try:
                if func(kwargs[name]):
                    continue
                else:
                    return f"uncorrected parameter {name}"
            except KeyError:
                return f"uncorrected key {name}"
        return False

    def add(self, **kwargs) -> Union[bool, str]:
        """
        Добавляет запись в файл. Если инструкции выполняются без ошибок возвращает False. Иначе строку с ошибкой.
        """
        if a := self.data_is_correct(**kwargs):
            return a
        # записываем
        try:
            file = open(os.path.join(self.path_to_file, self.file_name), 'a', encoding='utf-8')
            writer = csv.DictWriter(
                file, fieldnames=self.column_name.keys(), delimiter=self.delimiter, lineterminator='\n')
            writer.writerow(kwargs)
            file.close()
            return False
        except Exception:
            return "something went wrong"

    # ------------------- #
    # FUNCTION TO UPDATE  #
    # ------------------- #
    def update(self, **kwargs) -> Union[bool, str]:
        """
        Меняте запись на запись, которая находится функцией find и изменяется.
        Если инструкции выполняются без ошибок возвращает False. Иначе строку с ошибкой.
        """
        if not self.records:
            self.mode = 'update'
            return False
        if a := self.data_is_correct(**kwargs):
            return a

        # нашли ли запись, которую надо изменить
        if len(self.records) == 1:
            temp = {}
            # Изменяем значения записи на значения переданные клиентом.
            for key in self.column_name.keys():
                temp[key] = kwargs[key]

            file = open(os.path.join(self.path_to_file, self.file_name), 'r')
            temp_records = list(csv.DictReader(file, delimiter=self.delimiter))
            file.close()

            temp_records[self.index_records[0]] = temp

            file = open(os.path.join(self.path_to_file, self.file_name), 'w')
            csv.DictWriter(file, fieldnames=self.column_name.keys(), delimiter=self.delimiter,
                           lineterminator='\n').writerows(temp_records)
            file.close()
            self.mode = ''
        else:
            return f'there should be one record, {len(self.records)} records are put on'
        return False

    def stop_update(self) -> bool:
        """Функция для выхода из режима update. Обнуляет нужные переменные"""
        self.mode = ''
        self.records = []
        self.index_records = []
        return False

    def find_records(self, **kwargs) -> Union[bool, str]:
        """
        Находит записи по переданным клиентом ключам.
        Если инструкции выполняются без ошибок возвращает False. Иначе строку с ошибкой.
        """
        self.current_page = 0
        self.records = []

        file = open(os.path.join(self.path_to_file, self.file_name), 'r')
        reader = csv.DictReader(file)
        # все значения ключей совпали - запись подходит
        flag = True

        for index, row in enumerate(reader):
            for key, value in kwargs.items():
                try:
                    if row[key] == value:
                        continue
                    else:
                        flag = False
                        break
                except KeyError:
                    return f"uncorrected parameter {key}"
            if flag:
                self.records.append(row.values())
                self.index_records.append(index)
            flag = True

        self.count_page = -1 * len(self.records) // RECORDS_ON_PAGE * -1
        file.close()
        return False

    # ----------------------- #
    # FUNCTION TO PRINT DATA  #
    # ----------------------- #
    def print_records_page(self) -> NoReturn:
        print(DELIMITER_LINE)
        print(self.records_to_str(self.current_page * RECORDS_ON_PAGE,
                                  self.current_page * RECORDS_ON_PAGE + self.records_on_page))
        print(DELIMITER_LINE)
        self.print_page()

    def print_page(self) -> NoReturn:
        string = ""

        if self.count_page <= 4:
            for i in range(1, self.count_page + 1):
                string += f'{i} ' if i != (self.current_page + 1) else f'[{self.current_page + 1}] '
            return print(string.rjust(PAGE_INDENTATION))
        else:
            for i in range(1, self.count_page + 1):
                if self.current_page == i or i == self.current_page + 2:
                    string += f'{i} '
                elif self.current_page + 1 == i:
                    string += f'[{i}] '
                elif i == 1:
                    string += '1 '
                elif i == self.count_page or i == self.count_page + 1:
                    string += f'{i} '
                else:
                    string += f'.'

            return print(string.rjust(PAGE_INDENTATION))

    # ----------------------------- #
    # function for formatting data  #
    # ----------------------------- #
    @staticmethod
    def record_to_str(record: list) -> str:
        """Формируем строку вывода записи"""
        return f"|{'|'.join(record)}|"

    def records_to_str(self, start: int, end: int) -> str:
        """Формируем строку вывода записей"""
        return ('\n' + DELIMITER_LINE + '\n').join(
            [self.record_to_str([i.center(LEN_COLUMN) for i in record]) for record in self.records[start:end]])

    @staticmethod
    def list_to_dict(lst: list) -> Union[dict, str]:
        """
        Конвертирует строку с ключами, переданную клиентом, в словарь.
        Если инструкции выполняются без ошибок возвращает False. Иначе строку с ошибкой.
        """
        key_dict = {}
        try:
            for i in lst:
                key, value = i.split('=')
                key_dict[key] = value
            return key_dict
        except Exception:
            return "something went wrong"

    def listen(self):
        """Основная функция. Считывает команды пользователя, и вызывает нужные функции обработки."""
        current_command = input('pb: ')

        while current_command != 'exit()':
            current_command = current_command.split(' ')

            try:
                # определяем какая функция обрабатывает текущую команду и её аргументы
                func = self.mode_command[self.mode][current_command[0]]
                kwargs = self.list_to_dict(current_command[1:])
                # возникла ли ошибка?
                if isinstance(kwargs, str):
                    print(kwargs)
                    current_command = input(f'pb {self.mode}: ')
                    continue
                # вызваем нужную функцию
                result = func(**kwargs)
                # функция может вернуть ошибку, если это строка, то печатаем.
                if result:
                    print(result)
                    current_command = input(f'pb {self.mode}: ')
                    continue
            except KeyError:
                print('available commands')
                current_command = input(f'pb {self.mode}: ')
                continue

            # выводим записи
            if self.records:
                self.print_records_page()

            # только вошил в update
            if self.mode == 'update' and not self.records:
                print(
                    "use the 'find' command to find the desired entry. Then repeat the update command with the parameters you want to change")
            # обнуляем записи, после режимов
            if self.mode == '':
                self.records = []
                self.index_records = []
            current_command = input(f'pb {self.mode}: ')


def is_base_dir(path: str):
    """Проверяем ввел ли пользователь путь к файлу, если нет то ищем в рабочей директории"""
    if path:
        return path
    return WORK_DIR


def main():
    """Получаем файл от пользователя, запускаем listen"""
    path_to_file = is_base_dir(input("enter the path to the file if is current directory press enter: "))
    while True:
        try:
            file_dir = os.listdir(path_to_file)
        except Exception:
            print("uncorrected path")
            path_to_file = is_base_dir(input("Enter the path to the file: "))
            continue
        file_name = input("enter the name file: ")
        if file_name not in file_dir:
            print('File not found')
            path_to_file = is_base_dir(input("Enter the path to the file: "))
            file_name = input("enter the name file: ")
        else:
            break

    with open(os.path.join(WORK_DIR, WELCOME), 'r') as welcome:
        print(welcome.read())
    pb = PhoneBook(path_to_file=path_to_file, file_name=file_name)
    pb.listen()


if __name__ == '__main__':
    main()



# def filling():
#     first_name = [
#         'Аарон',
#         'Аббас',
#         'Абд аль-Узза',
#         'Абдуллах',
#         'Абид',
#         'Аботур',
#         'Аввакум',
#         'Август',
#         'Авдей',
#         'Авель',
#         'Авигдор',
#         'Авксентий',
#         'Авл',
#         'Авнер']
#
#     last_name = [
#         'Смирнов',
#         'Иванов',
#         'Кузнецов',
#         'Соколов',
#         'Попов',
#         'Лебедев',
#         'Козлов',
#         'Новиков',
#         'Морозов',
#         'Петров',
#         'Волков',
#         'Соловьёв',
#         'Васильев',
#         'Зайцев', ]
#
#     patronymic = ['Абакумович',
#                   'Абрамович',
#                   'Абросимович',
#                   'Аввакумович',
#                   'Августович',
#                   'Авдеевич',
#                   'Авдиевич',
#                   'Авенирович',
#                   'Авериевич',
#                   'Аверкиевич',
#                   'Аверьянович',
#                   'Авксентиевич',
#                   'Аврамович',
#                   'Агапович',
#                   ]
#
#     phone = ['89105418949']
#
#     pb = PhoneBook(WORK_DIR, 'pb.csv')
#     for i in range(len(first_name)):
#         parameters = {'last_name': last_name[i],
#                      'first_name': first_name[i],
#                      'patronymic': patronymic[i],
#                      'organization_name': "Tr",
#                      'work_phone': phone[0],
#                      'personal_phone': phone[0]}
#         pb.add(**parameters)
#
# filling()