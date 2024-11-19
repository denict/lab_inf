def parse_key_value(line):
    """Парсинг разных типов данных для строк yaml 'ключ-значение'"""
    try:
        line_split = line.split(": ", 1)
        key, value = line_split

        # проверка ключа
        if ":" in key:  # если в ключе встречается ":"
            key = key[:-1]

        if key[0] in ("'", '"') and key[0] == key[-1]:  # обрезаем кавычки у ключа
            key = key[1:-1]


        # проверка значения на тип str
        if value[0] in ("'", '"') and value[0] == value[-1]:
            value = value[1:-1]  # убираем кавычки для значений для конвертирования из yaml в dict
        elif all(i.isdigit() for i in value):  # если все символы в value являются цифрами, то value - число
            value = int(value)
        # проверка значения на разные типы данных
        # проверка value на булевый тип данных
        if value == "true":
            value = 'True'
        elif value == "false":
            value = "False"
        elif value == "null":
            value = "None"

        return key, value
    except:
        return None, None


def count_space(line: str):
    count = 0
    while line[count] == " ":
        count += 1
    return count


def parse_object(lines: list, current_indent: int, current_position: int = 0):  # current_i - текущая позиция, current_indent - текущее кол-во отступов
    """Рекурсивная функция для парсинга объектов ключ-значение"""

    obj_data = dict() # словарь объектов
    position = 0

    while position < len(lines):  # перебираем строки
        if position + current_position in parsed_lines:  # если уже была запарсена, то мы её повторно не учитываем
            position += 1
            continue

        line = lines[position].rstrip()  # пробелы справа убраны
        line_lstrip = line.lstrip()  # убираем отступы в начале строки
        current_indent = count_space(line)

        if line_lstrip.startswith("-"):
            # # если строка начинается с "-", то это начало массива, поэтому отступ увеличивается на 2
            current_indent += 2


        # рассматриваемые случаи перевода строк типа данных YAML языка на тип данных словаря (ключ-значение) формального языка Python
        # 1-ый случай
        # кончается на ":" - открывание словаря с элементами типа "ключ-значение"
        if line_lstrip.endswith(":"):
            key = line_lstrip[:-1]  # ключ - вся строка, не включая ":"
            indent_data = parse_object(lines[position + 1:], current_indent + 2, position + current_position + 1)  # вызов рекурсии, начиная от следующей строки до конца
            if line_lstrip.startswith("-"):  # флажок на то, что у нас начинается список элементов
                if isinstance(obj_data, dict):
                    obj_data = []  # создаём массив для добавления в него элементов типа "ключ-значение"
                obj_data.append({key[2:]: indent_data})  # добавляем в массив "-" + " " + key - ключ, indent_data - значение obj_data для следующей позиции
            else:
                obj_data[key] = indent_data  # ключ-значение: ключ - строка, значение - кол-во отступов

            parsed_lines.add(current_position + position)  # добавление запарсенной строки


        # случай №2
        # начало списка элементов
        elif line_lstrip.startswith("-"):
            if isinstance(obj_data, dict):  # проверка на словарь
                obj_data = []  # создаём массив
            key, value = parse_key_value(line_lstrip[2:])  # парсит словарь и возвращает кортеж ключ-значение в качестве строк
            if key is not None or value is not None:  # если это ключ значение
                changed_lines = lines.copy()
                changed_lines[position] = " " * current_indent + line_lstrip[2:]
                obj_data.append(parse_object(changed_lines[position:], current_indent, position + current_position))
            else:  # если это не ключ-значение
                value = line_lstrip[2:]  # значение - строка
                obj_data.append(value)

            parsed_lines.add(current_position + position)  # добавление запарсенной строки

        # случай 3
        # если это не начало перечисления элементов словаря и не список элементов
        # просто пара "ключ-значение"
        else:
            key, value = parse_key_value(line_lstrip)

            if isinstance(obj_data, dict):
                obj_data[key] = value
            else:
                obj_data.append({key: value})

            # if isinstance(value, str):
            #     if value == "[" + value[1:-1] + "]":
            #         value = value[1:-1].split(", ")

            parsed_lines.add(current_position + position)

        # нужно рано или поздно выйти из рекурсии...
        if position + 1 < len(lines):
            # next_line = lines[position + 1]
            # next_indent = count_space(next_line)

            if max(parsed_lines) <= current_position + position:
                next_line = lines[position + 1]
            else:
                if max(parsed_lines) - current_position + 1 < len(lines):
                    next_line = lines[max(parsed_lines) - current_position + 1]
                else:
                    return obj_data
            next_indent = count_space(next_line)
            if next_line[next_indent] == "-":
                next_indent += 2
            if isinstance(obj_data, list):
                if next_indent < current_indent:
                    return obj_data
            else:
                if next_indent < current_indent or next_line.lstrip().startswith("-") and next_indent == current_indent:
                    return obj_data

        position += 1  # смотрим на следующую строку

    return obj_data



parsed_lines = set()  # строки, над которыми уже производился парсинг
def yaml_to_dict(yaml):
    """перевод из YAML языка в словарь языка Python"""
    while "\n\n" in yaml:
        yaml = yaml.replace("\n\n", "\n")
    lines = yaml.split("\n")
    # убираем пустые строки и комментарии
    lines = [st for st in lines if st.replace(" ", "") != "" and st.replace(" ", "")[0] != "#"]
    dict_py = parse_object(lines, 0)

    return dict_py  # возвращает словарь


# with open('C://Users/denict/PycharmProjects/LabsAndEdu/Labs_inf/lab_inf_4/data/input.yml', 'r',encoding='utf-8') as file_yaml:
#     yaml_string = file_yaml.read()
#     dict_py = yaml_to_dict(yaml_string)
#     print(dict_py)

def escaping_special_characters(string):
    """экранирование служебных символов: одинарные и двойные кавычки, символ перевода строк и символ табуляции"""
    string = string.replace("\'", "\\'").replace('\"', '\\"')
    string = string.replace("\n", "\\n").replace("\t", "\\t")
    return string



def from_list_py_to_json(list_py, current_indent: int = 1):
    """Преобразование списка языка Python в строку формата JSON"""

    items = []  # сохраняем запарсенные значения
    for json_value in list_py:

        # преобразуем значения
        if isinstance(json_value, str):
            json_value = escaping_special_characters(json_value) # # экранирование специальных символов в ключе, если ключ содержит их
            json_value = f'"{json_value}"'
        elif isinstance(json_value, (int, float)):
            json_value = str(json_value)
        elif isinstance(json_value, bool):
            json_value = 'true' if json_value else 'false'
        elif json_value is None:
            json_value = 'null'
        elif isinstance(json_value, list):
            json_value = from_list_py_to_json(json_value, current_indent + 1)
        elif isinstance(json_value, dict):
            json_value = from_dict_py_to_json(json_value, current_indent + 1)
        else:
            raise TypeError(f"Неизвестный тип данных")

        items.append("\t" * current_indent + json_value)
    return "[\n" + ",\n".join(items) + "\n" + "\t" * (current_indent - 1) + "]"


def from_dict_py_to_json(dict_py, current_indent: int = 1):
    """Преобразование словаря языка Python в строку формата JSON"""

    if isinstance(dict_py, dict):
        items = []
        for json_key, json_value in dict_py.items():  # достаём ключи-значения из словаря
            json_key = escaping_special_characters(json_key)  # экранирование специальных символов в ключе, если ключ содержит их
            json_key = f'"{json_key}"'  # все ключи в JSONе хранятся в двойных кавычках
            if isinstance(json_value, str):
                if json_value[0] in ("'", '"') and json_value[0] == json_value[-1]:
                    json_value = json_value[1:-1]
                json_value = escaping_special_characters(json_value)
                json_value = f'"{json_value}"'
            elif isinstance(json_value, (int, float)):
                json_value = str(json_value)
            elif isinstance(json_value, bool):
                json_value = ("false", "true")[json_value]
            elif json_value is None:
                json_value = "null"
            elif isinstance(json_value, list):
                json_value = from_list_py_to_json(json_value, current_indent + 1)
            elif isinstance(json_value, dict):
                json_value = from_dict_py_to_json(json_value, current_indent + 1)
            else:
                raise TypeError(f"Неизвестный тип: {type(json_value)}")

            items.append("\t" * current_indent + f"{json_key}: {json_value}")

        return "{\n" + ",\n".join(items) + "\n" + "\t" * (current_indent - 1) + "}"

    elif isinstance(dict_py, list):  # если dict_py оказался list_py
        return from_list_py_to_json(dict_py)

    else:
        raise TypeError (f" Неизвестный тип данных")


# if __name__ == "__main__":
#     with open('C://Users/denict/PycharmProjects/LabsAndEdu/Labs_inf/lab4_inf/src/input.yml', 'r', encoding='utf-8') as file_yaml:
#         yaml_string = file_yaml.read()
#
#         dict_py = yaml_to_dict(yaml_string)
#     with open('/LabsAndEdu/Labs_inf/lab_inf_4/data/out1_dop.json', 'w', encoding="utf-8") as file_json:
#         file_json.write(from_dict_py_to_json(dict_py))