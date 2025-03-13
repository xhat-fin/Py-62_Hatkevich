"""
3. Класс «Автобус». Класс содержит свойства:
● скорость
● максимальное количество посадочных мест
● максимальная скорость
● список фамилий пассажиров
● флаг наличия свободных мест
● словарь мест в автобусе
Методы:
● посадка и высадка одного или нескольких пассажиров
● увеличение и уменьшение скорости на заданное значение
● операции in, += и -= (посадка и высадка пассажира по
фамилии)
"""

class Autobus:
    def __init__(self, max_speed, max_seat):
        self.speed = 0
        self.max_seat = max_seat
        self.max_speed = max_speed
        self.free_seat = max_seat > 0
        self.dict_seat = {i: "Свободное место" for i in range(1, self.max_seat + 1)}
        self.fio_passenger = []


    def board(self, *passengers):
        for e, passenger in enumerate(passengers):
            if "Свободное место" not in self.dict_seat.values():
                print(f"Нет свободных мест для {[passenger for passenger in passengers][e:]}")
                self.free_seat = False
                break
            for key_seat in self.dict_seat:
                if self.dict_seat[key_seat] == "Свободное место":
                    self.dict_seat[key_seat] = passenger
                    self.fio_passenger.append(passenger)
                    break


    def exit(self, *passengers):
        for passenger in passengers:
            if passenger in self.fio_passenger:
                self.fio_passenger.remove(passenger)
                for key in self.dict_seat:
                    if self.dict_seat[key] == passenger:
                        self.dict_seat[key] = "Свободное место"
                        self.free_seat = True


    def change_speed(self, value, increase:bool):
        if increase == True:
            if (self.speed + value) > self.max_speed:
                self.speed = self.max_speed
            else:
                self.speed += value
        else:
            if (self.speed - value) < 0:
                self.speed = 0
            else:
                self.speed -= value


    def __iadd__(self, passenger):
        self.board(passenger)
        return self


    def __isub__(self, passenger):
        self.exit(passenger)
        return self


    def __contains__(self, passenger):
        return passenger in self.fio_passenger

bus = Autobus(120, 5)

bus += 'Nikita'

print('Nikita' in bus)
print('NIKITA' in bus)

bus += 'Dima'
bus += 'Ignat'
bus.board('Atrem', 'John', 'Andre', 'Petya')

bus -= 'Atrem'
bus -= 'John'

print('Флаг свободного места: ', bus.free_seat)

bus.board('Andre', 'Petya', 'Atrem', 'John')

print('Флаг свободного места: ', bus.free_seat)
