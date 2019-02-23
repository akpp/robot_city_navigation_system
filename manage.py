import argparse
import glob
import os

from navigation_system import VERSION, Data, Navigator, Randomiser


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')


def run_navigator(route):
    """Common function to create and run Robot"""
    navigator = Navigator(route)
    # create a new robot
    navigator.spawn_robot()
    # say hello
    print(navigator.robot.introduce)
    # navigate the robot through the route
    navigator.start_navigation()


def proceed(args):
    # create a new route
    if args.file:
        print(f'Create new route from file "{args.file}", and move a Robot:\n')

        route = []
        with open(args.file, 'r') as f:
            for raw in f:
                # lower case, and escape empty
                raw = raw.strip().lower()
                if raw:
                    route.append(Data.parse_raw(raw))

        # save the route
        Data.save_route(route, DATA_DIR)

        run_navigator(route)

    # show the list of available routes
    elif args.list:
        print("Available routes:\n\nN | Name")

        files = sorted(glob.glob(DATA_DIR + '/*.json'))
        for n, f in enumerate(files, 1):
            name = f.split('/')[-1]
            print(f'{n} : {name}')
        if not files:
            print("No available routes")

    # try to move robot within that route
    elif args.route is not None:
        print("Open the route, and move a Robot:\n")
        path = os.path.join(DATA_DIR, args.route)
        route = Data.get_saved_route(path)

        run_navigator(route)

    # create a random route, optionally save it
    elif args.random is not None:
        print("Build a random route, and move a Robot:\n")
        raw_route = Randomiser.get_random_route(abs(args.random))
        route = [Data.parse_raw(raw) for raw in raw_route]

        # save the generated route
        if args.save:
            Data.save_route(route, DATA_DIR)

        run_navigator(route)

    # there is no arguments
    else:
        print("Try with --help")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A Robot City Navigator System. "
        "For more information, see README file.",
        epilog="Have a nice day!")

    parser.add_argument(
        "-v", "--version", action="version", version=f'Robot City Navigator System {VERSION}',
        help="show navigation system version")
    parser.add_argument(
        "-l", "--list", action="store_true", help="Show a list of exist routes")
    parser.add_argument(
        "-r", "--random", type=int, help="Move a robot by a random route, provide N (0 - random from 2 to 500)")
    parser.add_argument(
        "-s", "--save", action="store_true", help="Move a robot by a random route and save the route")
    parser.add_argument(
        "-f", "--file", type=str, help="Add new route from file")
    parser.add_argument(
        "--route", type=str, help="Move a robot by a valid route NAME (look up by list)")

    arguments = parser.parse_args()
    proceed(arguments)
