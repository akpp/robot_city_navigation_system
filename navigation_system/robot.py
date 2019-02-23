from .navigator import Navigator


class Robot:
    """Class Robot"""

    DIRECTIONS = ('left', 'right')

    def __init__(self, x: int=0, y: int=0, direction="north", name="Jeday", log=True):
        # store current position in the City
        self.coordinates = (x, y)
        self.direction = direction
        self.name = name
        self._log = log

        # store session movements
        self._movements = []

        Navigator.validate_coordinates(self.coordinates, critical=True)
        Navigator.validate_direction(self.direction, critical=True)

    def __str__(self):
        return self.introduce

    @property
    def introduce(self):
        """Hello World"""
        return f'Hi! I am {self.name}, facing {self.direction} at {self.coordinates}'

    @property
    def movements_count(self):
        return len(self._movements)

    def _save(self, movement):
        """Save movement and print if log is True"""
        self._movements.append(movement)
        if self._log:
            print(movement)

    def clear_story(self):
        """Clear session story movements"""
        self._movements = []

    def turn_to(self, direction):
        """
        Make turn to the direction
        :param direction:
        :return:
        """
        if Navigator.validate_direction(direction, critical=True) and \
           self.direction != direction:
            self.direction = direction
            self._save(f'turn to {direction}')

    def turn(self, direction):
        if Robot.validate_direction(direction, critical=True):
            if direction == 'right':
                if self.direction == 'north':
                    self.direction = 'east'
                elif self.direction == 'east':
                    self.direction = 'south'
                elif self.direction == 'south':
                    self.direction = 'west'
                elif self.direction == 'west':
                    self.direction = 'north'
            elif direction == 'left':
                if self.direction == 'north':
                    self.direction = 'west'
                elif self.direction == 'east':
                    self.direction = 'north'
                elif self.direction == 'south':
                    self.direction = 'east'
                elif self.direction == 'west':
                    self.direction = 'south'

            self._save(f'turn {direction}, facing {self.direction}')

    def move(self, distance: int):
        """
        Move toward the current direction,
        or if blocks is negative move back
        :param distance:
        :return:
        """
        if distance != 0:
            x, y = self.coordinates
            if self.direction == "north":
                y += distance
            elif self.direction == "south":
                y -= distance
            elif self.direction == "east":
                x += distance
            elif self.direction == "west":
                x -= distance

            if Navigator.validate_coordinates((x, y)):
                self.coordinates = (x, y)
                self._save(f'go distance {distance} to {self.coordinates}')
            else:
                print(f'WARNING! I can not go there {(x, y)}, there is nothing!')

    def teleport(self, coords):
        """
        Teleport a robot to the coordinates
        :param coords:
        :return:
        """
        if Navigator.validate_coordinates(coords, critical=True):
            self.coordinates = coords
            self._save(f'teleport to {coords}')

    def go_to(self, coords):
        """
        Make movements to the coordinates and change directions if necessary
        :param coords:
        :return:
        """
        if Navigator.validate_coordinates(coords, critical=True) and self.coordinates != coords:
            self._save(f'go to {coords}')

            x, y = coords
            current_x, current_y = self.coordinates

            # auto movements
            # here supposed to be tests with landmarks
            if x > current_x:
                self.turn_to("east")
                self.move(x - current_x)
            elif x < current_x:
                self.turn_to("west")
                self.move(current_x - x)
            if y > current_y:
                self.turn_to("north")
                self.move(y - current_y)
            elif y < current_y:
                self.turn_to("south")
                self.move(current_y - y)

    @staticmethod
    def validate_direction(direction, critical=False):
        """
        Validate direction
        could raise error on invalid coordinates if critical is True
        :param direction:
        :param critical:
        :return: True/False
        """
        if direction not in Robot.DIRECTIONS:
            if critical:
                raise RobotIllegalDirection(f'Illegal Direction: {direction}')
            return False
        return True


#
# Exceptions
#
class RobotIllegalDirection(Exception):
    pass
