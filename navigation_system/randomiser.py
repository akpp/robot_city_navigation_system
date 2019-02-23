import random


class Randomiser:

    MIN_X = 0
    MAX_X = 10000
    MIN_Y = 0
    MAX_Y = 10000

    MIN_ITER = 2
    MAX_ITER = 500

    INSTRUCTIONS = {
        'turn': lambda: random.choice(('turn left', 'turn right')),
        'go': lambda: f'go {Randomiser.get_random_distance()} blocks',
    }

    @staticmethod
    def get_random_position():
        return random.randint(Randomiser.MIN_X, Randomiser.MAX_X), \
               random.randint(Randomiser.MIN_Y, Randomiser.MAX_Y)

    @staticmethod
    def get_random_distance():
        return random.randint(1, 500)

    @staticmethod
    def get_random_instruction():
        choice = random.choice(list(Randomiser.INSTRUCTIONS.keys()))
        return Randomiser.INSTRUCTIONS[choice]()

    @staticmethod
    def get_random_route(iterations: int=2):
        """Provide a random route"""
        if abs(iterations) < 2:
            iterations = random.randint(Randomiser.MIN_ITER, Randomiser.MAX_ITER)

        start_position = Randomiser.get_random_position()
        route = [f'start at {start_position}']
        for _ in range(iterations - 1):
            route.append(Randomiser.get_random_instruction())
        return route
