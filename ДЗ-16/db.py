import psycopg2


DB_CONFING = {
    "dbname": "warehouse",
    "user": "postgres",
    "password": "Totem151012",
    "host": "localhost",
    "port": "5432"
}

def connect_db():
    return psycopg2.connect(**DB_CONFING)


def init_db():
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS categories_goods(
        id SERIAL PRIMARY KEY,
        name VARCHAR(30)
        );
        """)


        cur.execute("""
        CREATE TABLE IF NOT EXISTS customers(
        id SERIAL PRIMARY KEY,
        name VARCHAR(30)
        );
        """)


        cur.execute("""
        CREATE TABLE IF NOT EXISTS suppliers(
        id SERIAL PRIMARY KEY,
        name VARCHAR(30)
        );
        """)


        cur.execute("""
        CREATE TABLE IF NOT EXISTS goods(
        id SERIAL PRIMARY KEY,
        name VARCHAR(30),
        quantity INT CHECK (quantity>=0),
        category_id INT REFERENCES categories_goods (id),
        full_cost DECIMAL(15, 2)
        );
        """)


        cur.execute("""
        CREATE TABLE IF NOT EXISTS orders_buy(
        id SERIAL PRIMARY KEY,
        goods_id INT REFERENCES goods(id),
        supplier_id INT REFERENCES suppliers(id),
        price DECIMAL(15, 2),
        quantity INT,
        date DATE
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS orders_sale(
        id SERIAL PRIMARY KEY,
        goods_id INT REFERENCES goods(id),
        customers_id INT REFERENCES customers(id),
        price DECIMAL(15, 2),
        quantity INT,
        date DATE
        );
        """)


        cur.execute("""
        CREATE TABLE IF NOT EXISTS bank_account(
        id SERIAL PRIMARY KEY,
        transaction_amount DECIMAL(15,2),
        description VARCHAR(500),
        transaction_date DATE
        );
        """)

    conn.close()



# ================================================================================================
# goods
def check_goods(goods):
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""SELECT id FROM goods where name = %s""", (goods,))
        product = cur.fetchall()
    conn.close()
    return product



def update_goods(quantity, full_cost, name):
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""
        UPDATE goods SET quantity = quantity + %s, full_cost = full_cost + %s WHERE name = %s""",
                    (quantity, full_cost, name))
    conn.close()



def insert_tn_buy_goods(tn_info):
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""
        INSERT INTO goods (name, quantity, category_id, full_cost) VALUES (%s, %s, %s, %s)
        """, tn_info)
    conn.close()



def update_tn_sale_goods(quantity, ids):
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""
        UPDATE goods SET full_cost = full_cost - ((full_cost/quantity) * %s), quantity = quantity - %s where id = %s 
        """, (quantity, quantity, ids))
    conn.close()



def get_goods():
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""
        select g.name as "Товар", g.quantity as "Количество", g.full_cost as "Общая стоимость", cg.name as "Категория" 
        from goods g left join categories_goods cg on g.category_id = cg.id
        """)
        goods = cur.fetchall()
    conn.close()
    return goods

def get_goods_by_categories():
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""
        select cg.name as "Категория", SUM(g.quantity) as "Количество", SUM(g.full_cost) as "Общая стоимость" 
        from goods g left join categories_goods cg on g.category_id = cg.id group by cg.name
        """)
        goods_categories = cur.fetchall()
    conn.close()
    return goods_categories



# ================================================================================================
# categories_goods
def get_categories():
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""SELECT * FROM categories_goods""")
        categories = cur.fetchall()
    conn.close()
    return categories



def check_categories(categories):
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""SELECT id FROM categories_goods where name=%s""", (categories,))
        categories = cur.fetchall()
    conn.close()
    return categories


def insert_categories(categories):
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""INSERT INTO categories_goods (name) VALUES (%s)""", (categories,))
    conn.close()




# ================================================================================================
# suppliers
def check_suppliers(supplier):
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""SELECT id FROM suppliers where name=%s""", (supplier,))
        suppliers = cur.fetchall()
    conn.close()
    return suppliers


def insert_suppliers(supplier):
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""INSERT INTO suppliers (name) VALUES (%s)""", (supplier,))
    conn.close()



# ================================================================================================
# customers
def check_customers(customer):
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""SELECT id FROM customers where name=%s""", (customer,))
        customers = cur.fetchall()
    conn.close()
    return customers


def insert_customer(customer):
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""INSERT INTO customers (name) VALUES (%s)""", (customer,))
    conn.close()


def get_customers():
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""SELECT * FROM customers""")
        customers = cur.fetchall()
    conn.close()
    return customers


# ================================================================================================
# orders_buy(
def insert_orders_buy(goods_id, supplier_id, price, quantity, date):
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""INSERT INTO orders_buy(goods_id, supplier_id, price, quantity, date) VALUES (%s, %s, %s, %s, %s)""",
                    (goods_id, supplier_id, price, quantity, date))
    conn.close()


def get_orders_buy(date_1, date_2):
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""select g.name as "Товар", o.price as "Цена партии", o.quantity as "Кол-во в партии", o."date" as "Дата ТН", s.name as "Поставщик"
        FROM orders_buy o join goods g on o.goods_id = g.id join suppliers s on o.supplier_id = s.id
        WHERE o.\"date\" BETWEEN %s and %s""", (date_1, date_2))
        orders_buy = cur.fetchall()
    conn.close()
    return orders_buy


def get_orders_buy_suppliers(supplier):
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""select g.name as "Товар", o.price as "Цена партии", o.quantity as "Кол-во в партии", o."date" as "Дата ТН", s.name as "Поставщик"
        FROM orders_buy o join goods g on o.goods_id = g.id join suppliers s on o.supplier_id = s.id
        WHERE s.name ILIKE %s""", (f'%{supplier}%',))
        orders_buy = cur.fetchall()
    conn.close()
    return orders_buy



# ================================================================================================
# orders_sale
def insert_orders_sale(goods_id, customers_id, price, quantity, date):
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""INSERT INTO orders_sale(goods_id, customers_id, price, quantity, date) VALUES (%s, %s, %s, %s, %s)""",
                    (goods_id, customers_id, price, quantity, date))
    conn.close()


def get_orders_sale(date1, date2):
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""select g.name, o.price, o.quantity, o.date, c.name 
        from orders_sale o 
        LEFT JOIN customers c on o.customers_id = c.id 
        left join goods g on o.goods_id = g.id where o.date between %s and %s""", (date1, date2))
        orders_sale = cur.fetchall()
    conn.close()
    return orders_sale


def get_orders_sale_by_client(client):
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""select g.name, o.price, o.quantity, o.date, c.name 
        from orders_sale o 
        LEFT JOIN customers c on o.customers_id = c.id 
        left join goods g on o.goods_id = g.id where c.name ILIKE %s""", (f'%{client}%',))
        orders_sale = cur.fetchall()
    conn.close()
    return orders_sale






# ================================================================================================
# bank_acc
def insert_transaction_bank_acc(transaction_amount, description, transaction_date):
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""INSERT INTO bank_account(transaction_amount, description, transaction_date) 
        VALUES (%s, %s, %s)""",
                    (transaction_amount, description, transaction_date))
    conn.close()



def get_balance():
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""SELECT SUM(transaction_amount) FROM bank_account""")
        balance = cur.fetchall()
    conn.close()
    return balance


def get_transaction(date_1, date_2):
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""SELECT transaction_amount, description, transaction_date FROM bank_account 
        WHERE transaction_date BETWEEN %s and %s""",
                    (date_1, date_2))
        transaction = cur.fetchall()
    conn.close()
    return transaction
