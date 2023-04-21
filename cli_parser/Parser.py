class Parser:
    @staticmethod
    def index(array: list, key: str):
        for index, item in enumerate(array):
            if item == key:
                return index

        return -1

    def parse(self, argv: list) -> dict:
        argv = argv[1:]

        parsed = dict()

        parsed['help'] = False

        if len(argv) == 1:
            if argv[0] == '-h' or argv[0] == '--help':
                parsed['help'] = True
                parsed['help_text'] = \
                    '-u <url> - url профиля пользователя (обязательный параметр)\n' \
                    '-c <значение> - количество выведенных записей. По-умолчанию выводит всех людей. ' \
                    '(Необязательный параметр)\n'

                return parsed

            raise ValueError('Неправильный набор параметров. Вызовите утилиту с флагом -h или --help')

        if '-u' not in argv:
            raise ValueError('Вы не ввели url адрес профиля пользователя')

        url_index = self.index(argv, '-u')

        if (url_index == len(argv) - 1) or (argv[url_index + 1] is None):
            raise ValueError('Вы не ввели значение для url')

        parsed['url'] = argv[url_index + 1]

        is_count = False

        if '-c' in argv:
            is_count = True

            count_index = self.index(argv, '-c')

            if (count_index == len(argv) - 1) or (argv[count_index + 1] is None):
                raise ValueError('Вы не ввели значение для количество выводимых записей в подборке')

            parsed['count'] = int(argv[count_index + 1])

        if (is_count and len(argv) != 4) or ((not is_count) and len(argv) != 2):
            raise ValueError('Вы ввели не корректное количество параметров')

        return parsed
