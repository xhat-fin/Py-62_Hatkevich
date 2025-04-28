import db


def sep_string(text):
    print()
    print('=' * 100)
    print(text)
    print('=' * 100, '\n')


def menu():
    print("-"*100)
    print("0 - Выйти из приложения")
    print("1 - Заполнить товарную накладную на реализацию товара")
    print("2 - Заполнить товарную накладную на покупку товара")
    print("3 - Отчет о движении денежных средств")
    print("4 - Отчет о движении товара")
    print("5 - Остатки товара на складе")
    print("6 - Поиск")
    print("-"*100)



def try_append(list_, type_p, descr):
    try:
        list_.append(type_p(input(descr).strip()))
    except ValueError:
        print("Введите корректное значение!")
        try_append(list_, type_p, descr)



db.init_db()


while True:
    menu()
    p_menu = input("Выберите пункт меню: ").strip()


    # =================================================================================
    # выход из меню
    if p_menu == "0":
        # 0 - Выйти из приложения
        print("-" * 100)
        break

    # =================================================================================
    # Реализация товаров
    elif p_menu == "1":
        tn_info = list()
        tn_info.append(input("Введите название реализуемого товара: ").lower().strip())
        goods_id = db.check_goods(tn_info[0])

        if not goods_id:
            sep_string('Нет такого товара для реализации!')
            continue

        if db.get_customers():
            print("-"*100)
            print("Существующие клиенты")
            for i in db.get_customers():
                print(f'ID: {i.id} - Name: {i.name}')
            print("-" * 100)

        tn_info.append(input("Введите покупателя: ").lower().strip())
        customer = db.check_customers(tn_info[-1])

        if not customer:
            db.insert_customer(tn_info[-1])
            customer = db.check_customers(tn_info[-1])



        try_append(tn_info, int, "Введите количество реализуемого товара: ")

        try_append(tn_info, float, "Введите сумму реализуемого товара: ")

        tn_info.append(input("Введите дату товарной накладной (формат: YYYY-MM-DD): "))

        # добавляем данные в бд
        try:
            db.update_tn_sale_goods(tn_info[2], goods_id[0])
        except Exception as e:
            print()
            print('='*100)
            print(f"Произошла ошибка {e}. Проверьте наличие необходимого количества товара")
            print('='*100)
            continue
        db.insert_orders_sale(goods_id[0], customer[0], tn_info[2], tn_info[3], tn_info[4])

        db.insert_transaction_bank_acc(tn_info[3], f'Реализация товара {tn_info[0]}, покупателю {tn_info[1]} на сумму {tn_info[3]}',
                                       tn_info[4])
        sep_string("База данных обновлена!")

    # =================================================================================
    # покупка товара у поставщика
    elif p_menu == "2":
        tn_info = list()
        tn_info.append(input("Введите название товара: ").lower().strip())

        # если такой товар уже есть, то редактируется стоимость и количество, если нет - добавляется
        goods_id = db.check_goods(tn_info[0])
        if goods_id:
            # tn_info.append(int(input("Введите количество товара: ")))
            # tn_info.append(float(input("Введите стоимость товара: ")))

            try_append(tn_info, int, "Введите количество товара: ")
            try_append(tn_info, float, "Введите стоимость товара: ")

        else:
            # tn_info.append(int(input("Введите количество товара: ")))
            try_append(tn_info, int, "Введите количество товара: ")


            categories = db.get_categories()
            if categories:
                print("-"*46)
                print("Существующие категории")
                for i in categories:
                    print(f'ID: {i.id} - Name: {i.name}')
                print("-"*46)

            name_categories = input("Введите название категории товара: ").lower().strip()

            if db.check_categories(name_categories):
                tn_info.append(db.check_categories(name_categories)[0])
            else:
                db.insert_categories(name_categories)
                tn_info.append(db.check_categories(name_categories)[0])

            # tn_info.append(float(input("Введите стоимость товара: ")))
            try_append(tn_info, float, "Введите стоимость товара: ")


        tn_info.append(input("Введите поставщика: ").lower().strip())
        suppliers_id = db.check_suppliers(tn_info[-1])
        if suppliers_id:
            pass
        else:
            db.insert_suppliers(tn_info[-1])

        tn_info.append(input("Введите дату товарной накладной (формат: YYYY-MM-DD): "))


        # добавляем информацию в базу данных:
        if len(tn_info) == 5:
            db.update_goods(tn_info[1], tn_info[2], tn_info[0])

            goods_id = db.check_goods(tn_info[0])
            suppliers_id = db.check_suppliers(tn_info[-2])
            db.insert_orders_buy(goods_id[0][0], suppliers_id[0][0], tn_info[2], tn_info[1], tn_info[-1])
            db.insert_transaction_bank_acc(-tn_info[2], f"Закупка {tn_info[0]} у {tn_info[-2]} в количестве {tn_info[1]}", tn_info[-1])
        else:
            db.insert_tn_buy_goods(tuple(tn_info[:4]))

            goods_id = db.check_goods(tn_info[0])
            suppliers_id = db.check_suppliers(tn_info[-2])
            db.insert_orders_buy(goods_id[0], suppliers_id[0], tn_info[3], tn_info[1], tn_info[-1])
            db.insert_transaction_bank_acc(-tn_info[3], f"Закупка {tn_info[0]} у {tn_info[-2]} в количестве {tn_info[1]}", tn_info[-1])


        sep_string("База данных обновлена!")


    # =================================================================================
    # 3 - Отчет о движении денежных средств

    elif p_menu == "3":
        print("Необходимый формат дат -> YYYY-MM-DD <-")
        date = [input("Введите дату начала транзакций: "), input("Введите дату окончания транзакций: ")]
        print()
        print('='*100)

        for i in db.get_transaction(*date):
            print(f'Сумма: {i[0]}, Назначение платежа: {i[1]}, Дата: {i[2]}')
        print(f'Текущий баланс: {db.get_balance()[0]}')

        while True:
            print('='*100, '\n'*2)

            print("1 - Назад")
            print("2 - Выгрузить текущий отчет в файл txt")

            cmd = input("Выберите пункт меню: ").strip()
            print('\n')
            if cmd == "1":
                print("-" * 100)
                break
            elif cmd == "2":
                with open('transaction.txt', "w") as file_tr:
                    for i in db.get_transaction(*date):
                        file_tr.write(f'Сумма: {i[0]}, Назначение платежа: {i[1]}, Дата: {i[2]}\n')
                    file_tr.write(f'Текущий баланс: {db.get_balance()[0]}')

                sep_string("Отчет выгружен в файл transaction.txt")
                break
            else:
                print("Выберите пункт из меню")


    # =================================================================================
    # 4 - Отчет о движении товара
    elif p_menu == "4":
        while True:
            print()
            print("0 - Выйти в основное меню")
            print("1 - Отчет о закупке товаров")
            print("2 - Отчет о реализации товаров", '\n')

            try:
                cmd = input("Выберите пункт меню: ").strip()
            except ValueError:
                print('Выберете пункт из меню')
                continue

            if cmd == "0":
                print('-' * 100)
                break

            elif cmd == "1":
                print("Необходимый формат дат -> YYYY-MM-DD <-")
                date = [input("Введите дату начала транзакций: "), input("Введите дату окончания транзакций: ")]

                print()
                print('=' * 100)

                for e, i in enumerate(db.get_orders_buy(*date), start = 1):
                    print(f'№ - {e} -- Товар: {i[0]}, Цена партии: {i[1]}, Количество товара в партии: {i[2]}, Дата: {i[3]}, Поставщик: {i[4]}')
                while True:
                    print('=' * 100, '\n')

                    print("1 - Назад")
                    print("2 - Выгрузить текущий отчет в файл txt")

                    s_cmd = input("Выберите пункт меню: ").strip()

                    if s_cmd == "1":
                        print("-" * 100)
                        break
                    elif s_cmd == "2":
                        with open('orders_buy.txt', "w") as file_tr:
                            for e, i in enumerate(db.get_orders_buy(*date), start = 1):
                                file_tr.write(f'№ - {e} -- Товар: {i[0]}, Цена партии: {i[1]}, Количество товара в партии: {i[2]}, Дата: {i[3]}, Поставщик: {i[4]}\n')


                        sep_string("Отчет выгружен в файл orders_buy.txt")
                        break
                    else:
                        print("Выберите пункт из меню")

            elif cmd == "2":
                # 2 - Отчет о реализации товаров
                print("Необходимый формат дат -> YYYY-MM-DD <-")
                date = [input("Введите дату начала транзакций: "), input("Введите дату окончания транзакций: ")]

                print()
                print('=' * 100)

                for e, i in enumerate(db.get_orders_sale(*date), start = 1):
                    print(f'№ - {e} -- Товар: {i[0]}, Цена партии: {i[2]}, Количество товара в партии: {i[1]}, Дата: {i[3]}, Клиент: {i[4]}')
                while True:
                    print('=' * 100, '\n')

                    print("1 - Назад")
                    print("2 - Выгрузить текущий отчет в файл txt")

                    s_cmd = input("Выберите пункт меню: ").strip()

                    if s_cmd == "1":
                        print("-" * 100)
                        break
                    elif s_cmd == "2":
                        with open('orders_sale.txt', "w") as file_tr:
                            for e, i in enumerate(db.get_orders_sale(*date), start = 1):
                                file_tr.write(f'№ - {e} -- Товар: {i[0]}, Цена партии: {i[2]}, Количество товара в партии: {i[1]}, Дата: {i[3]}, Клиент: {i[4]}\n')


                        sep_string("Отчет выгружен в файл orders_sale.txt")
                        break
                    else:
                        print("Выберите пункт из меню")
            else:
                print("Выберите пункт из меню")

    # =================================================================================
    # 5 - Остатки товара на складе
    elif p_menu == "5":
        while True:
            print()
            print("Тип отчета", '\n')
            print("0 - Выйти в основное меню")
            print("1 - Отчет по каждому товару")
            print("2 - Отчет по категориям товара")

            s_cmd = input("Выберите пункт меню: ").strip()

            if s_cmd == "0":
                print("-" * 100)
                break
            elif s_cmd == "1":
                # отчет по товарам
                print()
                print("=" * 100)
                for e, i in enumerate(db.get_goods(), start=1):
                    print(f'№ - {e} -- Товар: {i[0]}, Количество: {i[1]}, Закупочная стоимость: {i[2]}, Категория: {i[3]}')

                while True:
                    print("=" * 100, '\n')

                    print("1 - Назад")
                    print("2 - Выгрузить текущий отчет в файл txt")

                    s_cmd = input("Выберите пункт меню: ")

                    if s_cmd == "1":
                        print("-" * 100)
                        break
                    elif s_cmd == "2":
                        with open('goods_status.txt', "w") as file_tr:
                            for e, i in enumerate(db.get_goods(), start=1):
                                file_tr.write(
                                    f'№ - {e} -- Товар: {i[0]}, Количество: {i[1]}, Закупочная стоимость: {i[2]}, Категория: {i[3]}\n')
                        sep_string("Отчет выгружен в файл goods_status.txt")
                        break
                    else:
                        print("Выберите пункт из меню")

            elif s_cmd == "2":
                # отчет по категориям товаров
                print()
                print("=" * 100)
                for e, i in enumerate(db.get_goods_by_categories(), start=1):
                    print(f'№ - {e} -- Категория: {i[0]}, Количество: {i[1]}, Закупочная стоимость: {i[2]}')

                while True:
                    print("=" * 100, '\n')

                    print("1 - Назад")
                    print("2 - Выгрузить текущий отчет в файл txt")

                    s_cmd = input("Выберите пункт меню: ").strip()

                    if s_cmd == "1":
                        print("-" * 100)
                        break
                    elif s_cmd == "2":
                        with open('goods_by_categories.txt', "w") as file_tr:
                            for e, i in enumerate(db.get_goods(), start=1):
                                file_tr.write(
                                    f'№ - {e} -- Категория: {i[0]}, Количество: {i[1]}, Закупочная стоимость: {i[2]}\n')
                        sep_string("Отчет выгружен в файл goods_by_categories.txt")
                        break
                    else:
                        print("Выберите пункт из меню")
            else:
                print("Выберите пункт из меню")

    # =================================================================================
    # 6 - Поиск
    elif p_menu == "6":
        # 6 - Поиск
        while True:
            print("-" * 100)
            print("0 - Выйти в основное меню")
            print("1 - Реализация товара по клиенту")
            print("2 - Закупка товара по поставщику")
            print("-" * 100, '\n')
            s_cmd = input("Выберите пункт меню: ").strip()

            if s_cmd == "0":
                break
            elif s_cmd == "1":
                client = input("Введите название\часть названия клиента: ").strip()
                print()
                print('=' * 100)
                for i in db.get_orders_sale_by_client(client):
                    print(f'Товар: {i[0]}, Цена: {i[2]}, Количество: {i[1]}, Дата: {i[3]}, Клиент: {i[4]}')
                print('=' * 100, '\n')

                print("0 - Выйти в основное меню")
                print("1 - Сформировать еще раз")
                print("2 - Выгрузить в файл")
                s_cmd = input("Выбери пункт меню: ").strip()
                if s_cmd == "0":
                    break
                elif s_cmd == "1":
                    continue
                elif s_cmd == "2":
                    with open(f'orders_sale_{client}.txt', "w") as file_tr:
                        for e, i in enumerate(db.get_orders_sale_by_client(client), start=1):
                            file_tr.write(f'Товар: {i[0]}, Цена: {i[2]}, Количество: {i[1]}, Дата: {i[3]}, Клиент: {i[4]}\n')
                    sep_string(f"Отчет выгружен в файл orders_sale_{client}.txt")
                    break
                else:
                    print("Выберите пункт из меню")



            elif s_cmd == "2":
                suppliers = input("Введите название\часть названия клиента: ").strip()
                print()
                print('=' * 100)
                for i in db.get_orders_buy_suppliers(suppliers):
                    print(f'Товар: {i[0]}, Цена: {i[1]}, Количество: {i[2]}, Дата: {i[3]}, Поставщик: {i[4]}')
                print('=' * 100, '\n')

                print("0 - Выйти в основное меню")
                print("1 - Сформировать еще раз")
                print("2 - Выгрузить в файл")
                s_cmd = input("Выбери пункт меню: ").strip()
                if s_cmd == "0":
                    break
                elif s_cmd == "1":
                    continue
                elif s_cmd == "2":
                    with open(f'orders_buy_{suppliers}.txt', "w") as file_tr:
                        for e, i in enumerate(db.get_orders_buy_suppliers(suppliers), start=1):
                            file_tr.write(f'Товар: {i[0]}, Цена: {i[1]}, Количество: {i[2]}, Дата: {i[3]}, Поставщик: {i[4]}\n')
                    sep_string(f"Отчет выгружен в файл orders_buy_{suppliers}.txt")
                    break
                else:
                    print("Выберите пункт из меню")

            else:
                print("Выберите пункт из меню")

    else:
        print("Выберите пункт из меню")
