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
        Age: Age of animal, animal weakens with age - Endurance, strength, ect. reduce with age
        """
        self.fatigue = 100
        self.hunger = 100
        self.total_health = 100
        self.age = 0

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
        """
        self.goal_position = None
        self.goal_type = None
        #self.priority =

    def reproduce(self, mate):
        pass

    def eat(self, food):
        pass

    def drink(self, water):
        pass

    def rest(self):
        pass

    def move(self, goal):
        pass

    def get_priority(self):
        pass

    def get_move_sequence(self):
        #Set sequence of moves to reach event
        pass

## Testing
if __name__ == '__main__':
    pass
