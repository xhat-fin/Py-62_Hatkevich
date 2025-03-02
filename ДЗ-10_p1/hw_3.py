# Напишите программу, которая считывает текст из
# файла (в файле может быть больше одной строки) и выводит
# в новый файл самое часто встречаемое слово в каждой
# строке и число – счётчик количества повторений этого слова
# в строке.
import string
from collections import Counter

with open('file.txt') as f:
    text = f.readlines()

text_list = []
for t in text:
    t = t.replace('\n', '')
    text_list.append(t.lower())

for e, str_line in enumerate(text_list, start=1):
    for p in string.punctuation:
        str_line = str_line.replace(p, '')
    str_line = str_line.split(' ')
    count_word = Counter(str_line).most_common(1)
    print(f'Часто повторяемое слово в строке {e} - "{count_word[0][0]}" с повторением {count_word[0][1]} раз/а')
