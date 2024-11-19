def count_space(string: str):  # функция, которая подсчитывает количество пробелов в начале строки до первого не пробельного символа или индекс первого непробельного символа
    count = 0
    while string[count] == " ":
        count += 1
    return count


def yaml_to_json(input_string: str):
    """конвертирование из YAML в JSON"""
    data = [string + "\n" for string in input_string.split("\n") if
            string.replace(" ", "") != "" and string.replace(" ", "") != "#"]
    # небольшая работа с отступами
    for i in range(len(data)):
        stri = data[i]
        # Добавление кавычки перед именем поля
        if not "- " in stri:
            # Преобразование строчки, если с неё начинается список
            stri = " " * count_space(stri) + "\"" + stri[count_space(stri):]
        # добавление запятой после значения
        if not (stri.endswith(":\n") or stri.endswith(": \n")):  # строка не оканчивается на ":" и в следующей строке нет "- "
            stri = stri.rstrip() + "\",\n"  # добавляем кавычку справа для значений
            stri = stri.replace(": ", ": \"") # добавление кавычки слева для значений
        data[i] = stri  # меняем значение
    closed_rect_cntr = 0  # кол-во закрытий прямоугольных скобок
    i = 0
    while i < len(data):
        stri = data[i]
        # если начинается массив
        if stri.lstrip().startswith("- "):
            lenspacesi = count_space(stri)  # количество отступов в начале строки
            stri = stri.replace("- ", "{\n" + (" " * (lenspacesi + 2)) + "\"")  # замена
            data[i] = stri
            # вложенный цикл для того, чтобы узнать окончание массива
            for j in range(i + 1, len(data)):
                strj = data[j]
                lenspacesj = count_space(strj)
                if lenspacesj < lenspacesi:
                    data.insert(j, (" " * lenspacesi) + "}\n")  # добавляем на j-ю позицию списка соответствующую строку закрывания списка "}"
                    break
                elif lenspacesj == lenspacesi:
                    data.insert(j, (" " * lenspacesj) + "},\n")  # то же самое, на j-ю позицию списка добавляем строку закрывания списка "}"
                    break
        #
        if ":\n" in stri or ": \n" in stri:
            stri = stri.replace(":\n", ": [\n")
            stri = stri.replace(": \n", ": [\n")
            data[i] = stri
            lenspacesi = count_space(stri)
            is_closed_added = False
            for j in range(i + 1, len(data)):  # вложенный цикл для нахождения закрытия
                strj = data[j]
                lenspacesj = count_space(strj)
                if lenspacesi == lenspacesj:  # нашли окончание
                    data.insert(j, (" " * (lenspacesi)) + "]\n")  # добавляем закрытие
                    is_closed_added = True
                    break
                if lenspacesi > lenspacesj:  # то же самое
                    data.insert(j, (" " * (lenspacesi)) + "]\n")  # добавляем закрытие
                    is_closed_added = True
                    break
            # после окончания двойного цикла
            if not is_closed_added:  # не нашли окончание, добавление в конец формата JSON закрывающие скобки
                data.insert(len(data) - closed_rect_cntr + 1, (" " * lenspacesi) + "]\n")  # добавляем в конец
                closed_rect_cntr += 1
        stri = stri.replace(": ", "\": ")  # добавляем для ключей двойную кавычку '"'
        data[i] = stri
        i += 1

    # результат
    res_str = "".join(data).split("\n")

    # Убираем лишние запятые у элементов перед },
    for i in range(1, len(res_str)):
        if "}" in res_str[i]:
            res_str[i - 1] = res_str[i - 1].replace("\",", "\"")
        res_str[i] += "\n"

    res_str[0] += "\n" # баг с первой строкой
    res_str.insert(0, "{\n")  # добавление первой открывающей скобки
    for i in range(1, len(res_str) - 1):  # кол-во отступов увеличиваем на 2
        res_str[i] = "  " + res_str[i]
        if "]" in res_str[i] and ("}" not in res_str[i] and "}" not in res_str[i + 1]) and i < len(res_str) - 2:
            res_str[i] = res_str[i][:res_str[i].index("]")] + "]," + res_str[i][res_str[i].index("]") + 1:]  # добавление запятой после ] в одном случае
        # if "]" not in res_str[i] and "[" not in res_str[i] and "{" not in res_str[i] and "}" not in res_str[i] and "'" not in res_str[i]: # добавление скобкам значение
        #     res_split = res_str[i].split(": ")
        #     if ",\n" in res_split[1]:
        #         res_split[1] = '"' + res_split[1][:res_split[1].index(",\n")] + '",\n'
        #     else:
        #         res_split[1] = '"' + res_split[1] + '"'
        #     res_str[i] = ": ".join(res_split)

    del res_str[len(res_str) - 1]
    res_str.append("}")
    res_str = "".join(res_str)
    return res_str


