## Imports
import random

from Animal import animal
from world.Water import water
from world.Food import food

class empty_space:
    type = "empty"
    finished = False

##########################
## Sim helper functions ##
##########################

def create_animals(number_of_animals, world_size):
    animals = []
    for i in range(number_of_animals):
        # Generate traits of animal
        endurance = random.randint(1, 10)
        strength = random.randint(1, 10)
        speed = random.randint(1, 10)
        reproductive_score = random.randint(1, 100)
        position = random.randint(1, world_size-1)

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
        amount = random.randint(1, 3)
        new_water = water(sickness_chance, amount)
        while True:
            location = random.randint(0, world_size-1)
            if world[location] is None:
                world[location] = new_water
                break
        amount_water_remaining -= 1

    while amount_food_remaining:
        nutrition = random.randint(1, 5)
        amount = random.randint(1, 3)
        sickness_chance = random.randint(1, 100)

        while True:
            location = random.randint(0, world_size-1)
            if world[location] is None:
                new_food = food(nutrition, amount, sickness_chance)
                world[location] = new_food
                break
        amount_food_remaining -= 1

    for n, space in enumerate(world):
        if space is None:
            world[n] = empty_space()

    return world

def create_food(world, food_missing):
    world_size = len(world)
    while food_missing:
        nutrition = random.randint(1, 5)
        amount = random.randint(1, 3)
        sickness_chance = random.randint(1, 100)

        new_food = food(nutrition, amount, sickness_chance)
        while True:
            location = random.randint(0, world_size-1)
            if world[location].type == "empty":
                world[location] = new_food
                break
        food_missing -= 1
    return world

def create_water(world, water_missing):
    world_size = len(world)
    while water_missing:
        sickness_chance = random.randint(1, 100)
        amount = random.randint(1, 3)
        new_water = water(sickness_chance, amount)
        while True:
            location = random.randint(0, world_size-1)
            # print (f"L: {location}")
            if world[location].type == "empty":
                world[location] = new_water
                break
        water_missing -= 1
    return world

## Sim object
class sim:
    def __init__(self):
        self.world_size = 100
        self.animals = create_animals(1, self.world_size) # List of animal objects
        self.world = create_world(self.world_size)
        self.food_missing = 0
        self.water_missing = 0

    ## Sim main loop function
    def run(self):
        cycles = 0
        animals_to_be_added = []
        while len(self.animals) > 0: # and cycles < 100
            print (f"Cycle: {cycles}")
            print (f"📘📘📘Population: {len(self.animals)}")
            #print ([animal.total_health for animal in self.animals])

            for animal_index, animal in enumerate(self.animals):
                animal.total_health = animal.hunger * 0.33 + animal.thirst * 0.33 + animal.fatigue * 0.33
                if animal.sickness:
                    animal.total_health -= 5
                if animal.total_health <= 0:
                    #print (f"Animal died, Hunger: {animal.hunger} Thirst: {animal.thirst} Fatigue: {animal.fatigue} number_reproduced: {animal.number_reproduced}")
                    self.animals.pop(animal_index)
                    continue

                reached_goal = animal.move(self.world)
                if reached_goal:
                    if animal.goal_type == "sleep":
                        animal.rest()
                    elif animal.goal_type == "food":
                        self.world = animal.eat(self.world)
                    elif animal.goal_type == "water":
                        self.world = animal.drink(self.world)
                        #print ("drink")

                    # Check for possible_mates
                    mates_nearby = [[mate, index] for index, mate in enumerate(self.animals) if abs(mate.position - mate.position) < 2]
                    possible_mates = [[mate, index] for mate, index in mates_nearby if mate.total_health + animal.reproductive_score > 150 and animal.total_health + mate.reproductive_score > 150]
                    if possible_mates:
                        nearest_mate = possible_mates.pop()
                        while possible_mates:
                            next_mate = possible_mates.pop()
                            if abs(animal.position - next_mate[0].position) < abs(animal.position - nearest_mate[0].position):
                                nearest_mate = next_mate

                        mate, mate_index = nearest_mate
                        new_animal = animal.reproduce(mate)

                        mate.fatigue -= 10
                        animal.fatigue -= 10
                        self.animals[mate_index] = mate
                        animals_to_be_added.append(new_animal)

                # Update list to reflect new animal state
                self.animals[animal_index] = animal


            # Update world to reflect resources that are gone
            for n, space in enumerate(self.world):
                if space.finished:
                    self.world[n] = empty_space()
                    if space.type == "food":
                        self.food_missing += 1
                    elif space.type == "water":
                        self.water_missing += 1

            if self.food_missing:
                self.world = create_food(self.world, self.food_missing)

            if self.water_missing:
                self.world = create_water(self.world, self.water_missing)

            self.food_missing, self.water_missing = 0, 0

            self.animals.extend(animals_to_be_added)
            animals_to_be_added = []
            cycles += 1


## Run the sim fucntion
if __name__ == '__main__':
    s = sim()
    s.run()
