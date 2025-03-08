class Math:

    def addition(self, x, y):
        return x + y


    def subtraction(self, x, y):
        return x - y

    def multiplication(self, x, y):
        return x * y

    def division(self, x, y):
        try:
            num = x / y
            return num
        except ZeroDivisionError:
            return "На ноль делить нельзя"
        except Exception as e:
            return f"Ошибка при делении {e}"


math = Math()
print(math.division(10, 5))
print(math.division(10, 0))
print(math.addition(10, 11))
print(math.subtraction(10, 11))
print(math.multiplication(10, 11))
