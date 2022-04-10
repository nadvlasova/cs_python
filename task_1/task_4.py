"""
Задание 4.

Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

word1 = 'разработка'
word2 = 'администрирование'
word3 = 'protocol'
word4 = 'standard'

n = 0
all_word = (word1, word2, word3, word4)
for i in all_word:
    i_en = str.encode(i, encoding='utf-8')
    i_de = bytes.decode(i_en, encoding='utf-8')
    n += 1
    print(f'word{n} = {i_en}')
    print(f'word{n} = {i_de}')

# word1 = b'\xd1\x80\xd0\xb0\xd0\xb7\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xba\xd0\xb0'
# word1 = разработка
# word2 = b'\xd0\xb0\xd0\xb4\xd0\xbc\xd0\xb8\xd0\xbd\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb8\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5'
# word2 = администрирование
# word3 = b'protocol'
# word3 = protocol
# word4 = b'standard'
# word4 = standard

