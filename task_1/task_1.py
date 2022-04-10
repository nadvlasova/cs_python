"""
Задание 1.

Каждое из слов «разработка», «сокет», «декоратор» представить
в буквенном формате и проверить тип и содержание соответствующих переменных.
Затем с помощью онлайн-конвертера преобразовать
в набор кодовых точек Unicode (НО НЕ В БАЙТЫ!!!)
и также проверить тип и содержимое переменных.

Подсказки:
--- 'разработка' - буквенный формат
--- '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430' - набор кодовых точек
--- используйте списки и циклы, не дублируйте функции
"""

word1 = "разработка"
word2 = "сокет"
word3 = "декоратор"
all_words = [word1, word2, word3]

# Uword1 = b'\xd1\x80\xd0\xb0\xd0\xb7\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xba\xd0\xb0'
# Uword2 = b'\xd1\x81\xd0\xbe\xd0\xba\xd0\xb5\xd1\x82'
# Uword3 = b'\xd0\xb4\xd0\xb5\xd0\xba\xd0\xbe\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80'
#
# all_Uwords = (Uword1, Uword2, Uword3)
# for word in all_Uwords:
#     print(word)
#     print(type(word))

# b'\xd1\x80\xd0\xb0\xd0\xb7\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xba\xd0\xb0'
# <class 'bytes'>
# b'\xd1\x81\xd0\xbe\xd0\xba\xd0\xb5\xd1\x82'
# <class 'bytes'>
# b'\xd0\xb4\xd0\xb5\xd0\xba\xd0\xbe\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80'
# <class 'bytes'>

for word in all_words:
    print(f"'{word}' - буквенный формат - {type(word)}")
    print(f"'{word.encode('unicode_escape').decode('utf-8')}' - набор кодовых точек - {type(word)}")

# 'разработка' - буквенный формат - <class 'str'>
# '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430' - набор кодовых точек - <class 'str'>
# 'сокет' - буквенный формат - <class 'str'>
# '\u0441\u043e\u043a\u0435\u0442' - набор кодовых точек - <class 'str'>
# 'декоратор' - буквенный формат - <class 'str'>
# '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440' - набор кодовых точек - <class 'str'>