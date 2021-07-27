import random

class food:
    def __init__(self, position, nutrition, amount, sickness_chance):
        """
        Nutrition: Hunger value lost from food
        Amount: Number of servings avalible
        Sickness chance: % Chance of getting sickness - Sickness reduces health
        """
        self.type = "food"
        self.position = position
        self.nutrition = nutrition
        self.amount = amount
        self.sickness_chance = sickness_chance
        self.finished = False

    def eat(self):
        self.amount -= 1
        if self.amount < 1:
            self.finished = True

        sickness_value = random.randint(1, 100)
        sickness = False
        if sickness_value < self.sickness_chance:
            sickness = True

        return self.nutrition, sickness
