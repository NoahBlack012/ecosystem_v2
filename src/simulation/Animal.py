## Imports
import random

## Helper functions

## Animal Class
class animal:
    """docstring for animal."""

    def __init__(self, endurance, strength, speed, reproductive_score, position):
        """
        -------Characteristics-------
        Endurance: Fatigue gained per space moved (1 -> 10)
        Strength: Value that determines which animal wins in fight and how much damage each sustain (Higher value wins) (1 -> 10)
        Speed: Spaces that an animal can move per turn (1 -> 10)
        Reproductive_score: Value that determines an animals attractiveness to a potential mate (1 -> 100)
        Position: Postion in world (0 -> n, n is size of world)
        Gender: M/F
        """
        self.endurance = endurance
        self.strength = strength
        self.speed = speed
        self.reproductive_score = reproductive_score
        self.position = position
        if random.randint(1, 2) % 2 == 0:
            self.gender = "m"
        else:
            self.gender = "f"
        """
        -------Health Values-------
        Fatigue: How tired the animal is (0 -> 100), Closer to 0 - more tired
        Hunger: How hungry the animal is (0 -> 100), Closer to 0 - more hungry
        Thirst: How thirsty the animal is (0 -> 100), Closer to 0 - more thirsty
        Total Health: Health points - Health of the animal, (0 - 100), 0 - Dead, 100 - Perfectly healthy
        Max Total Health: Highest possible total health value
        Age: Age of animal, animal weakens with age - Endurance, strength, ect. reduce with age
        Sickness: If the animal has a sickness (Reduces max total_health)
        """
        self.fatigue = 100
        self.hunger = 100
        self.thirst = 100
        self.total_health = 100
        self.max_total_health = 100
        self.age = 0
        self.sickness = False

        """
        -------Behavioural Values-------
        Fight or Flight index: Willingness to fight another animal over resources (0 - 1), 0 - Run every time, 1 - Fight every time
        Consumption Type index: Preference to eating other animals or plants on the ground (0 - 1), 0 - Only eat plants, 1 - Only eat animals
        """
        self.f_or_f = 0.5
        self.consumption_type = 0.5

        """
        -------Current activities values-------
        Goal position: Position of space animal is moving towards
        Goal type: Goal animal is trying to accomplish (eat, drink, reproduce, sleep)
        Priority: Priority queue for what animal must do (Eat, drink, reproduce)
        Moves: Sequence of moves to reach goal (Enqueue at front, dequeue at back)
        """
        self.goal_position = None
        self.goal_type = None
        self.priority = []
        self.moves = []
        self.number_reproduced = 0

    def reproduce(self, mate):
        if self.gender == "f":
            new_position = self.position
        else:
            new_position = mate.position

        def create_attribute(a, b):
            if a < b:
                return random.randint(a, b)
            else:
                return random.randint(b, a)

        # Create animal attributes
        endurance = create_attribute(self.endurance, mate.endurance)
        strength = create_attribute(self.strength, mate.strength)
        speed = create_attribute(self.speed, mate.speed)
        reproductive_score = create_attribute(self.reproductive_score, mate.reproductive_score)
        position = new_position

        # Create animal object
        new_animal = animal(endurance, strength, speed, reproductive_score, position)
        self.number_reproduced += 1

        return new_animal

    def eat(self, world):
        if world[self.position].type == "food":
            if world[self.position].finished:
                # If food is finished, exit
                return world
            food = world[self.position]
            sickness = food.eat()
            self.hunger += food.nutrition
            if self.hunger > 100:
                self.hunger = 100
            if not self.sickness:
                self.sickness = sickness

            world[self.position] = food

        # Return new world state
        return world

    def drink(self, world):
        if world[self.position].type == "water":
            if world[self.position].finished:
                # If water is finished, exit
                return world
            water = world[self.position]
            sickness = water.drink()
            if not self.sickness:
                self.sickness = sickness

            world[self.position] = water

        # Return new world state
        return world

    def rest(self):
        self.fatigue += 20
        self.sickness = False

    def move(self, world):
        if not self.goal_position or not self.goal_type:
            self.get_move_sequence(world)
        goal = world[self.goal_position]
        if goal.type != self.goal_type:
            self.get_move_sequence(world)

        moves_remaining = self.speed
        if self.sickness:
            self.hunger -= 5
            self.thirst -= 5
            self.fatigue -= 5

        while moves_remaining > 0:
            if not self.moves:
                if world[self.position].type == self.goal_type:
                    return True
            move = self.moves.pop()
            self.position += move
            self.hunger -= 5 #Replace with animal-specific value
            self.thirst -= 5 #Replace with animal-specific value
            self.fatigue -= self.endurance

            moves_remaining -= 1
        if world[self.position].type == self.goal_type:
            return True
        return False


    def get_priority(self):
        number_options = {"food": self.hunger, "water": self.thirst, "sleep": self.fatigue}
        number_options = {key : value for key, value in sorted(number_options.items())}
        # Sort number options highest to lowest (Lowest priority -> highest priority)
        number_options_remaining = [i for i in number_options]

        priority = number_options_remaining
        # while len(priority) < 4:
        #     if ([i for i in number_options_remaining if number_options[i] < 85] and "reproduce" not in priority) or not number_options_remaining:
        #         # If remaining scores are high enough, reproduction can be a higher priority
        #         priority.append("reproduce")
        #     else:
        #         ## Get next item from number options and add to priority
        #         next_priority = number_options_remaining.pop()
        #         priority.append(next_priority)

        self.priority = priority

    def get_nearest_item_distance(self, world, type):
        distance = 0
        world_size = len(world)
        while self.position - distance >= 0 or self.position + distance < world_size:
            if self.position + distance < world_size:
                if world[self.position + distance].type == type:
                    return distance
            if self.position - distance > 0:
                if world[self.position - distance].type == type:
                    return -distance
            distance += 1
        return None

    def get_move_sequence(self, world):
        #Set sequence of moves to reach goal
        self.get_priority()
        # Get distance to item
        distance = None
        while distance is None:
            # Set goal type to highest priority item
            self.goal_type = self.priority.pop(0)
            if self.goal_type == "sleep":
                self.moves = [0, ]
                return # Set move sequence to not moving, exit function

            distance = self.get_nearest_item_distance(world, self.goal_type)

        self.goal_position = self.position + distance
        # Moves is an array of -1 or 1 of legnth distance
        if distance > 0:
            self.moves = [1, ] * distance
        else:
            self.moves = [-1, ] * (distance - (distance*2)) # Distance made positive


## Testing
if __name__ == '__main__':
    pass
