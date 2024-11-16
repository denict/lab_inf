# Декодирование кода Хэмминга (7, 4)
def haming_encoding(bits):
    # Подсчёт синдромов, битов чётности
    s1 = bits[0] ^ bits[2] ^ bits[4] ^ bits[6]
    s2 = bits[1] ^ bits[2] ^ bits[5] ^ bits[6]
    s3 = bits[3] ^ bits[4] ^ bits[5] ^ bits[6]
    # Вычисление позиции ошибочного символа
    err_pos = s1 + s2 * 2 + s3 * 4
    # инвертирование ошибочного символа (при наличии)
    if err_pos != 0:
        err_pos = err_pos - 1  # err_pos - 1, потому что индексы массива начинаются с 0
        bits[err_pos] = (bits[err_pos] + 1) % 2
    return [bits[2], bits[4], bits[5], bits[6]], err_pos


d = {0: "r1", 1: "r2", 2: "i1", 3: "r3", 4: "i2", 5: "i3", 6: "i4"}
bits = list(map(int, list(input("Введите сообщение из 7 символов\n"))))
info_bits, err_pos = haming_encoding(bits)

if err_pos == 0:
    print("Изначальное сообщение не содержит ошибок\n Сообщение информационных битов:", *bits)
else:
    print("Верное сообщение информационных битов:", *bits)
    print("Ошибочный бит", d[err_pos])

