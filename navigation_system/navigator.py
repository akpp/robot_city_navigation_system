import json
import os
import uuid


class Navigator:
    """Class Navigator"""

    DIRECTIONS = ['north', 'east', 'south', 'west']

    def __init__(self, route: list, robot=None, log=True):
        self.route = route
        self.robot = robot

        self._log = log

    def spawn_robot(self):
        """Create robot"""
        # to avoid import conflicts
        from .robot import Robot

        self.robot = Robot(log=self._log)

    def start_navigation(self):
        """
        Start navigate the Robot through the route
        """
        for instr in self.route:
            if instr["status"] == "done":
                if instr["action"] == "teleport":
                    self.robot.teleport((instr["x"], instr["y"]))
                elif instr["action"] == "turn":
                    self.robot.turn(instr["context"])
                elif instr["action"] == "move":
                    self.robot.move(instr["context"])
                elif instr["action"] == "move_with_turn":
                    self.robot.turn_to(instr["context"])
                    self.robot.move(instr["x"])

        if self._log:
            print(f'end ({self.robot.movements_count} executed instructions in total).\n')
            print(self.robot.introduce)

    @staticmethod
    def validate_coordinates(coords, critical=False):
        """
        Validate coordinates
        could raise error on invalid coordinates if critical is True
        :param coords:
        :param critical:
        :return: True/False
        """
        for p in coords:
            if not (isinstance(p, int) and p >= 0):
                if critical:
                    raise NavigationIllegalCoordinates(f'Invalid Coordinates: {coords}')
                return False
        return True

    @staticmethod
    def validate_direction(direction, critical=False):
        """
        Validate direction
        could raise error on invalid coordinates if critical is True
        :param direction:
        :param critical:
        :return: True/False
        """
        if direction not in Navigator.DIRECTIONS:
            if critical:
                raise NavigationIllegalDirection(f'Unknown Direction: {direction}')
            return False
        return True


class Data:
    """Class Data Navigator"""

    @staticmethod
    def save_route(route, destination):
        file_name = Data.generate_file_name()
        path = os.path.join(destination, file_name)
        with open(path, "w") as f:
            json.dump(route, f)

        print(f'Route saved as {file_name}\n')

    @staticmethod
    def generate_file_name():
        return f'{uuid.uuid4().hex}.json'

    @staticmethod
    def get_saved_route(path):
        with open(path, 'r') as f:
            route = json.load(f)
        return route

    @staticmethod
    def parse_raw(raw):
        step = {
            "raw_data": raw,
            "status": "in_progress",
            "action": None,
            "context": None,
            "x": None,
            "y": None,
        }

        # try get start coordinates
        if raw.startswith("start at", 0, 8):
            try:
                # terrible, but fastest decision to do
                x, y = raw.split("(")[1].split(")")[0].split(",")
                x, y = int(x), int(y)

                step.update(Data.get_instruction("teleport", "coords", x, y))
            except (ValueError, IndexError, TypeError):
                step["status"] = "error"

        # parse "go ..."
        elif raw.startswith("go ", 0, 4):
            raw = raw.split(" ")

            # go to direction
            if raw[1] in Navigator.DIRECTIONS:
                try:
                    direction, distance = raw[1], int(raw[2])
                    step.update(Data.get_instruction("move_with_turn", direction, distance))
                except (ValueError, IndexError, TypeError):
                    step["status"] = "error"
            else:
                try:
                    distance = int(raw[1])
                    step.update(Data.get_instruction("move", distance))
                except IndexError:
                    step["status"] = "error"
                except ValueError:
                    step["status"] = "unknown"

        # parse "turn ..."
        elif raw.startswith("turn ", 0, 6):
            raw = raw.split(" ")
            try:
                direction = raw[-1]
            except IndexError:
                direction = None
            if len(raw) == 2 and direction:
                step.update(Data.get_instruction("turn", direction))
            else:
                step["status"] = "error"

        # unknown instruction
        else:
            step["status"] = "unknown"

        return step

    @staticmethod
    def get_instruction(action, context=None, x=None, y=None, status="done"):
        return {
            "action": action,
            "context": context,
            "x": x,
            "y": y,
            "status": status,
        }


#
# Exceptions
#
class NavigationIllegalDirection(Exception):
    pass


class NavigationIllegalCoordinates(Exception):
    pass
