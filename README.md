Для хранения записок был выбран текстовый файл формата CSV, так как данные имеют табличный формат.

Все взаимодействия с файлом происходят через класс PhoneBook.
После того как пользователь ввел путь к файлу и название файла, инициализируем класс и запускаем метод listen.
Метод listen считывает команды пользователя, разделяет их и сопоставляет каждой команде свою функцию-обработчик.
Все функции-обработчики возвращают либо строку с ошибкой, либо False.
Если вернулось False и ошибок нет, проверяем, есть ли считанные из файла записи, и выводим их.
Если вернулась строка, то выводим ошибку.