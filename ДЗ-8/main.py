# . Реализовать программу для подсчёта индекса массы
# тела человека. Пользователь вводит рост и вес с клавиатуры.
# На выходе – ИМТ и пояснение к нему в зависимости от
# попадания в тот или иной диапазон. Использовать обработку
# исключений.


# ИМТ = ВЕС / РОСТ * РОСТ

def response_imt(imtt):
    if imtt < 18.5:
        return "недостаточности"
    elif 18.5 <= imtt <= 24.9:
        return "нормы"
    elif 25.0 <= imtt <= 29.9:
        return "избыточности"
    elif 30.0 <= imtt <= 34.9:
        return "ожирения 1-й степени"
    elif 35.0 <= imtt <= 39.9:
        return "ожирения 2-й степени"
    elif imtt>= 40.0:
        return "ожирения 3-й степени"
    else:
        return None

def index_body():
    while True:
        print("\n--------\n")
        print("1 - узнать индекс массы тела", "2 - закрыть программу", sep= '\n')
        try:
            select = int(input("Пункт меню: "))
        except ValueError:
            print("Введите номер из меню")
            continue
        if select == 1:
            while True:
                try:
                    height = float(input("Введите свой рост в (сантиметры): "))
                    weight = float(input("Введите свой вес (кг): "))
                    imt = round(weight / ((height / 100) ** 2), 1)
                    response = response_imt(imt)
                    print(f'\nИндекс массы тела равен {imt} и находится в пределах {response}')
                except ValueError:
                    print("Необходим указать корректные значения")
                    continue
                except ZeroDivisionError:
                    print("Значения не могут быть равны нулю!")
                    continue
                except Exception as e:
                    print(f"Произошла ошибка {e}")
                    index_body()

                while True:
                    try:
                        select_two = int(input("\n0 - выход в главное меню / 1 - посчитать ИМТ еще раз: "))
                        if select_two in (0, 1):
                            break
                        else:
                            print("Введите пункт из меню")
                    except ValueError:
                        print("Введите пункт из меню")
                        continue
                if select_two == 0:
                    break
        elif select == 2:
            break
        else:
            print("Выберете пункт из меню!")

# вызов функции имт
index_body()


# -------------------------------


# Реализовать программу с функционалом калькулятора
# для операций над двумя числами. Числа и операция вводятся
# пользователем с клавиатуры. Использовать обработку
# исключений.


def calc():
    # список операций
    operation = ["1 - Сложение",
                 "2 - Разность",
                 "3 - Умножение",
                 "4 - Деление",
                 "5 - Целочисленное деление",
                 "6 - Остаток от деления"
                 ]

    # главное меню
    menu = ['1 - Калькулятор', '2 - Выйти из приложения']

    # функция для определения чисел
    def inp_num():
        try:
            num1 = float(input(f"({operation[select_operation - 1]}) Введите первое число: "))
            num2 = float(input(f"({operation[select_operation - 1]}) Введите второе число: "))
        except ValueError:
            print("Необходимо указать корректные значения!")
            inp_num()
        return num1, num2

    # функция для подсчета из списка
    def select_math_operation(key_num, num1, num2):
        math_operation = {1: f'{num1} + {num2} = {num1 + num2}',
                          2: f'{num1} - {num2} = {num1 - num2}',
                          3: f'{num1} * {num2} = {num1 * num2}',
                          4: f'{num1} / {num2} = {num1 / num2}',
                          5: f'{num1} // {num2} = {num1 // num2}',
                          6: f'{num1} % {num2} = {num1 % num2}',
                          }
        return math_operation[key_num]


    # Начало калькулятора
    while True:
        print("\nМеню:")
        for i in menu:
            print(i)

        try:
            select_menu = int(input("\nПункт меню: "))
            if select_menu not in [1, 2]:
                raise ValueError
        except ValueError:
            print("\nНеобходимо ввести цифру из меню!")
            continue
        except Exception as e:
            print(f'\n{e}  или что-то пошло не так, но попробуй еще раз :) ')
            continue

        if select_menu == 1:
            while True:
                print("\nДоступные операции:\n")

                for i in operation:
                    print(i)

                try:
                    select_operation = int(input("\nНомер операции: "))
                    if select_operation == 0:
                        break
                    elif select_operation not in [i for i in range(1, 7)]:
                        raise ValueError
                except ValueError:
                    print("\nНеобходимо ввести цифру операции!!")
                    continue
                except Exception as e:
                    print(f'\n{e}  или что-то пошло не так, но попробуй еще раз :) ')
                    continue


                try:
                    print(f'\n({operation[select_operation - 1]}) Ответ: {select_math_operation(select_operation, *inp_num())}\n')
                except ZeroDivisionError:
                    print("При делении и умножении число не может быть равным нулю")

                while True:
                    try:
                        task_continue = int(input("0 - Выйти в главное меню / 1 - Посчитать еще раз: "))
                        if task_continue not in [0, 1]:
                            raise ValueError
                    except ValueError:
                        print("Необходимо выбрать пункт из меню!")
                        continue
                    if task_continue in [0, 1]:
                        break
                if task_continue == 0:
                    break
                elif task_continue == 1:
                    continue


        elif select_menu == 2:
            break


# Запуск калькулятора
calc()
