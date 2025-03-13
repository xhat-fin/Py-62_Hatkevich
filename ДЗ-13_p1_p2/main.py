"""
Реализовать программу для вывода
последовательности чисел Фибоначчи до определённого
числа в последовательности. Номер числа, до которого нужно
выводить, задаётся пользователем с клавиатуры. Для
реализации последовательности использовать генераторную
функцию
"""


def f(n):
    a, b = 0, 1
    for i in range(n):
        yield a
        a, b = b, a + b


g = f(int(input("Введите позицию числа Фибоначчи: ")))
print(f"Итерируем {g}, {type(g)}")
for i in g:
    print(i)



"""
Реализовать программу для бесконечной циклической
последовательности чисел (например, 1-2-3-1-2-3-1-2...).
Последовательность реализовать с помощью генераторной
функции, количество чисел для вывода задаётся
пользователем с клавиатуры.
"""

def generator(n):
    a = 1
    while a <= n:
        print(f'Последовательность {a}')
        a += 1
        for i in [1, 2, 3]:
            yield i


gen = generator(3)
for i in gen:
    print(i)