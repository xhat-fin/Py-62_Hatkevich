"""
2. ПчёлоСлон
Экземпляр класса инициализируется двумя целыми числами,
первое относится к пчеле, второе – к слону. Класс реализует
следующие методы:
● fly() – возвращает True, если часть пчелы не меньше части
слона, иначе – False
● trumpet() – если часть слона не меньше части пчелы,
возвращает строку “tu-tu-doo-doo”, иначе – “wzzzz”
● eat(meal, value) – может принимать в meal только ”nectar”
или “grass”. Если съедает нектар, то value вычитается из
части слона, пчеле добавляется. Иначе – наоборот. Не
может увеличиваться больше 100 и уменьшаться меньше 0.
"""

class ElBee:
    def __init__(self, elephant, bee):
        self.el = elephant
        self.bee = bee

    def fly(self):
        if self.bee >= self.el:
            return True
        return False


    def trumpet(self):
        if self.el >= self.bee:
            return 'tu-tu-doo-doo'
        return 'wzzzz'


    def eat(self, meal, value):
        if meal.lower().strip() in ['grass', 'nectar']:
            if meal == 'grass' and (self.el + value) <= 100 and (self.bee - value) > 0:
                self.el += value
                self.bee -= value
            elif meal == 'nectar' and (self.bee + value) <= 100 and (self.el - value) > 0:
                self.bee += value
                self.el -= value
            else:
                return print('некорректные значения')
        else:
            return print("send grass or nectar")



elbee = ElBee(50, 50)


print(elbee.fly())
print(elbee.trumpet())

print(elbee.el)
print(elbee.bee)

elbee.eat('nectar', 20)
print(elbee.fly())
print(elbee.trumpet())

print(elbee.el)
print(elbee.bee)

elbee.eat('grass', 50)
print(elbee.fly())
print(elbee.trumpet())

print(elbee.el)
print(elbee.bee)

elbee.eat('grass', 50)