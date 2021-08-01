import random

class water:
    """docstring for water."""

    def __init__(self, sickness_chance, amount):
        self.type = "water"
        self.sickness_chance = sickness_chance # 1 -> 100. percentage
        self.amount = amount # 1 -> 10
        self.finished = False

    def drink(self):
        self.amount -= 1
        if self.amount < 1:
            self.finished = True

        sickness_value = random.randint(1, 100)
        sickness = False
        if sickness_value < self.sickness_chance:
            sickness = True

        return sickness
