class Car:

    state = 0
    def __init__(self, color, type_a, year):
        self.__color = color
        self.__type_a = type_a
        self.__year = year


    def start(self):
        self.state = 1
        print("Автомобиль заведен")


    def stop(self):
        self.state = 0
        print("Автомобиль заглушен")


    def set_color(self, color):
        self.__color = color

    def set_type(self, type_a):
        self.__type_a = type_a


    def set_year(self, year):
        self.__year = year


    def car_state(self):
        if self.state == 0:
            print("Состояние: заглушен")
        else:
            print("Состояние: заведен")

    def car_info(self):
        print(f'Color: {self.__color}, type: {self.__type_a}, year: {self.__year}')

lada = Car("Белый", "Легковое авто", "2023")
mercedes_sprinter = Car("Черный", "Коммерческое авто", "2024")
tesla = Car("Зеленый", "Электрический", "2025")

tesla.color = "Черный"
tesla.car_info()
tesla.start()
tesla.car_state()
tesla.stop()
tesla.car_state()
tesla.set_color("Черный")
tesla.set_type("Летающий авто")
tesla.set_year("2125")
tesla.car_info()
