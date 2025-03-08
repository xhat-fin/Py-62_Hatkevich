class Soda:
    def __init__(self, taste='обычная'):
        self.taste = taste

    def info(self):
        if self.taste == "обычная":
            print(f"У вас {self.taste} газировка")
        else:
            print(f'У вас {self.taste} газировка')

soda = Soda()
soda.info()

soda = Soda('клубничная')
soda.info()
