# Напишите программу, которая получает на вход строку
# с названием текстового файла и выводит на экран
# содержимое этого файла, заменяя все запрещённые слова
# звездочками. Запрещённые слова, разделённые символом
# пробела, должны храниться в файле stop_words.txt.

# Программа должна находить
# запрещённые слова в любом месте файла, даже в середине
# другого слова. Замена независима от регистра: если в списке
# запрещённых есть слово exam, то замениться должны exam,
# eXam, EXAm и другие вариации.
# Пример: в stop_words.txt записаны слова: hello email
# python the exam wor is
# Текст файла для цензуры выглядит так: Hello, World! Python
# IS the programming language of thE future. My EMAIL is...
# PYTHON as AwESOME!
# Тогда итоговый текст: *****, ***ld! ****** ** *** programming
# language of *** future. My ***** **... ****** ** awesome!!!!


with open('stop_list.txt', 'r') as f:
    stop_words = f.read()
stop_words = stop_words.split(' ')

print(stop_words)

with open(input("Send path file: "), 'r') as f:
    text = f.read()

text = text.split(' ')

for stop in stop_words:
    for t in text:
        if stop.lower() in t.lower():
            text[text.index(t)] = t.lower().replace(stop.lower(), len(stop) * '*')

print(' '.join(text))