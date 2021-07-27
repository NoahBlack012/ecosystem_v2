## Imports

## Helper functions

## Animal Class
class animal:
    """docstring for animal."""

    def __init__(self, endurance, strength, speed, reproductive_score, position):
        """
        -------Characteristics-------
        Endurance: Fatigue gained per space moved (1 -> 10)
        Strength: Value that determines which animal wins in fight and how much damage each sustain (Higher value wins)
        Speed: Spaces that an animal can move per turn (1 -> 10)
        Reproductive_score: Value that determines an animals attractiveness to a potential mate (1 -> 10)
        Position: Postion in world (0 -> n, n is size of world)
        """
        self.endurance = endurance
        self.strength = strength
        self.speed = speed
        self.reproductive_score = reproductive_score
        self.position = position

        """
        -------Health Values-------
        Fatigue: How tired the animal is (0 -> 100), Closer to 0 - more tired
        Hunger: How hungry the animal is (0 -> 100), Closer to 0 - more hungry
        Total Health: Health points - Health of the animal, (0 - 100), 0 - Dead, 100 - Perfectly healthy
        Max Total Health: Highest possible total health value
        Age: Age of animal, animal weakens with age - Endurance, strength, ect. reduce with age
        Sickness: If the animal has a sickness (Reduces max total_health)
        """
        self.fatigue = 100
        self.hunger = 100
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
        Goal type: Resource animal is moving towards
        Priority: Priority queue for what animal must do (Eat, drink, reproduce)
        Moves: Sequence of moves to reach goal (Enqueue at front, dequeue at back)
        """
        self.goal_position = None
        self.goal_type = None
        #self.priority =
        self.moves = []

    def reproduce(self, mate):
        pass

    def eat(self, world):
        if world[self.position].type == "food":
            food = world[self.position]
            nutrition, sickness = food.eat()
            self.hunger += nutrition
            if self.hunger > 100:
                self.hunger = 100
            if not self.sickness:
                self.sickness = sickness

        return food


    def drink(self, water):
        pass

    def rest(self):
        self.fatigue += 20
        self.sickness = False

    def move(self, world):
        goal = world[self.goal_position]
        if goal.type != self.goal_type:
            self.get_move_sequence()

        moves_remaining = self.speed
        while moves_remaining > 0:
            if not self.moves:
                self.eat(goal)
                break
            move = self.moves.pop()
            self.position += move
            self.fatigue -= self.endurance
            moves_remaining -= 1

        if moves_remaining > 0:
            self.get_move_sequence()
            self.move(world)

    def get_priority(self):
        pass

    def get_nearest_item_distance(self, world, type):
        distance = 0
        world_size = len(world)
        while self.position - distance >= 0 and self.position + distance < world_size:
            if world[self.position + distance].type == type:
                return distance
            if world[self.position - distance].type == type:
                return -distance
            distance += 1
        return 0

    def get_move_sequence(self, world):
        #Set sequence of moves to reach goal
        self.get_priority()

        # Get distance to item
        distance = 0
        while distance == 0:
            self.goal_type = self.priority.pop(0)
            if self.goal_type == "rest":
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
