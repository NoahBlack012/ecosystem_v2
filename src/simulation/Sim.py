## Imports
import random

from Animal import animal
from .world import water, food

class empty_space:
    type = "empty"

## Sim helper functions
def create_animals(number_of_animals, world_size):
    animals = []
    for i in range(number_of_animals):
        # Generate traits of animal
        endurance = random.randint(1, 10)
        strength = random.randint(1, 10)
        speed = random.randint(1, 10)
        reproductive_score = random.randint(1, 10)
        position = random.randint(1, world_size)

        # Create animal object and add to list of animals
        new_animal = animal(endurance, strength, speed, reproductive_score, position)
        animals.append(new_animal)

    return animals

def create_world(world_size):
    world = [None, ] * world_size
    amount_water_remaining = world_size // 10
    amount_food_remaining = world_size // 10

    while amount_water_remaining:
        sickness_chance = random.randint(1, 100)
        amount = random.randint(1, 10)
        new_water = water(sickness_chance, amount)
        while True:
            location = random.randint(0, world_size)
            if world[location] is not None:
                world[location] = new_water
                break
        amount_water_remaining -= 1

    while amount_food_remaining:
        nutrition = random.randint(1, 5)
        amount = random.randint(1, 10)
        sickness_chance = random.randint(1, 100)

        new_food = food(nutrition, amount, sickness_chance)
        while True:
            location = random.randint(0, world_size)
            if world[location] is not None:
                world[location] = new_food
                break
        amount_food_remaining -= 1

    for n, space in enumerate(world):
        if space is None:
            world[n] = empty_space()

    return world

## Sim object
class sim:
    def __init__(self):
        self.world_size = 100
        self.animals = create_animals(10, self.world_size) # List of animal objects
        self.world = create_world(self.world_size)

    ## Sim main loop function
    def run(self):
        while True:
            for animal in self.animals:
                reached_goal = animal.move()
                if reached_goal:
                    if animal.goal_type == "sleep":
                        animal.rest()
                    elif animal.goal_type == "eat":
                        self.world = animal.eat(self.world)
                    elif animal.goal_type == "drink":
                        self.world = animal.drink(self.world)
                    else:
                        pass
                        ## Reproduce




## Run the sim fucntion
if __name__ == '__main__':
    s = sim()
    s.run()
