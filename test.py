import unittest

from navigation_system.randomiser import Randomiser
from navigation_system.robot import Robot, RobotIllegalDirection
from navigation_system.navigator import NavigationIllegalCoordinates, NavigationIllegalDirection, Navigator, Data


class RandomiserTest(unittest.TestCase):

    def test_constants(self):
        for c in ('MIN_X', 'MIN_Y', 'MAX_Y', 'MIN_ITER', 'MAX_ITER'):
            attr = getattr(Randomiser, c)
            self.assertIsInstance(attr, int)

    def test_random_position(self):
        position = Randomiser.get_random_position()
        x, y = position
        self.assertIsInstance(position, tuple)
        self.assertIsInstance(x, int)
        self.assertIsInstance(y, int)
        self.assertTrue((x > Randomiser.MIN_X) and (x < Randomiser.MAX_X))
        self.assertTrue((y > Randomiser.MIN_Y) and (y < Randomiser.MAX_Y))

    def test_random(self):
        route = Randomiser.get_random_route(0)
        self.assertTrue(len(route) > 0)

        route = Randomiser.get_random_route(2)
        self.assertEqual(len(route), 2)


class RobotTest(unittest.TestCase):

    def setUp(self):
        self.robot = Robot(log=False)
        self.target = (33, 33)

    def _robot_reset(self):
        self.robot.teleport((0, 0))
        self.robot.turn_to("north")

    def test_default_state(self):
        self.assertEqual(self.robot.coordinates, (0, 0))
        self.assertEqual(self.robot.name, "Jeday")
        self.assertEqual(self.robot.direction, "north")

    def test_illegal_values(self):
        def _spawn_bad_cords():
            return Robot(-1, -1)

        def _spawn_bad_direction():
            return Robot(direction="down")

        def _bad_turn():
            robot = Robot()
            robot.turn("top")

        self.assertRaises(RobotIllegalDirection, _bad_turn)

        self.assertRaises(NavigationIllegalCoordinates, _spawn_bad_cords)
        self.assertRaises(NavigationIllegalDirection, _spawn_bad_direction)

    def test_introduce(self):
        robot = Robot(99, 99, "south", "Anonymous")
        self.assertEqual(
            robot.introduce,
            'Hi! I am Anonymous, facing south at (99, 99)'
        )

    def test_movement_teleport(self):
        self.robot.teleport(self.target)
        self.assertEqual(self.robot.coordinates, self.target)
        self.assertEqual(self.robot.movements_count, 1)
        self.robot.clear_story()
        self.assertEqual(self.robot.movements_count, 0)

    def test_movement_turns(self):
        self.robot.turn_to("north")
        self.assertEqual(self.robot.direction, "north")

        self.robot.turn("left")
        self.assertEqual(self.robot.direction, "west")
        self.robot.turn("left")
        self.assertEqual(self.robot.direction, "south")
        self.robot.turn("left")
        self.assertEqual(self.robot.direction, "east")
        self.robot.turn("right")
        self.assertEqual(self.robot.direction, "south")

    def test_movement_move(self):
        self.robot.move(self.target[1])
        self.robot.turn("right")
        self.robot.move(self.target[0])
        self.assertEqual(self.robot.coordinates, self.target)

    def test_auto_movements(self):
        self.robot.clear_story()
        self.robot.go_to(self.target)
        # why 5 ?
        # ['go to (33, 33)', 'turn to east', 'go distance 33 to (33, 0)', 'turn to north', 'go distance 33 to (33, 33)']
        self.assertEqual(self.robot.movements_count, 5)


class NavigatorTest(unittest.TestCase):

    def setUp(self):
        raw_route = Randomiser.get_random_route(2)
        route = [Data.parse_raw(raw) for raw in raw_route]
        self.navigator = Navigator(route, log=False)

    def test_spawn_robot(self):
        self.assertIsNone(self.navigator.robot)
        self.navigator.spawn_robot()
        self.assertIsInstance(self.navigator.robot, Robot)

    def test_navigation(self):
        self.navigator.spawn_robot()
        self.navigator.start_navigation()
        self.assertEqual(self.navigator.robot.movements_count, 2)


if __name__ == '__main__':
    unittest.main()
