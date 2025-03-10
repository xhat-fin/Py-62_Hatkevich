#1.
# Класс «Товар» содержит следующие закрытые поля:
#● название товара
#● название магазина, в котором подаётся товар
#● стоимость товара в рублях

#Класс «Склад» содержит закрытый массив товаров.
#Обеспечить следующие возможности:
#● вывод информации о товаре со склада по индексу
#● вывод информации о товаре со склада по имени товара
#● сортировка товаров по названию, по магазину и по цене
#● перегруженная операция сложения товаров по цене


class Product:
    def __init__(self, name_product, shop, price):
        self.__name_product = name_product
        self.__shop = shop
        self.__price = price


    def info(self):
        return {"name_product": self.__name_product, "shop": self.__shop, "price": self.__price}



class Warehaus:
    def __init__(self, *args):
        self.product_list = []
        for prod in args:
            self.product_list.append(prod.info())


    def get_info_index(self, index):
        product_i = self.product_list[index]
        return f'Product: {product_i.get('name_product')}, Shop: {product_i.get('shop')}, Price: {product_i.get('price')}'


    def get_info_name(self, name_product):
        for i in self.product_list:
            if i.get('name_product').lower().strip() == name_product.lower().strip():
                return f'Product: {i.get('name_product')}, Shop: {i.get('shop')}, Price: {i.get('price')}'


    def sort_by_shop(self):
        def get_shop(prod):
            return prod['shop']
        self.product_list.sort(key=get_shop)

    def sort_by_name(self):
        def get_name(name_prod):
            return name_prod['name_product']
        self.product_list.sort(key=get_name)


    def sort_by_price(self):
        def get_price(price_prod):
            return price_prod['price']
        self.product_list.sort(key=get_price)


    def __add__(self, other):
        full_price = 0
        for prod in self.product_list:
            full_price += prod.get('price')
        for prod in other.product_list:
            full_price += prod.get('price')
        return full_price


prod1 = Product("Orange", "A", 100)
prod2 = Product("Computer", "B", 1000)

wh = Warehaus(prod1, prod2)
wh1 = Warehaus(prod1, prod2)

print(wh + wh1)

wh.sort_by_price()

print(wh.get_info_index(0))
print(wh.get_info_name('CoMpUter'))