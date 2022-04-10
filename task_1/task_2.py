"""
Задание 2.

Каждое из слов «class», «function», «method» записать в байтовом формате
без преобразования в последовательность кодов
не используя!!! методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.

Подсказки:
--- b'class' - используйте маркировку b''
--- используйте списки и циклы, не дублируйте функции
"""
word1 = b'class'
word2 = b"function"
word3 = b"method"

all_word = [word1, word2, word3]
for i in all_word:
    print(i)
    print(type(i))
    print(len(i))

# b'class'
# <class 'bytes'>
# 5
# b'function'
# <class 'bytes'>
# 8
# b'method'
# <class 'bytes'>
# 6