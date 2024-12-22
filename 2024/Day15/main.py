from dataclasses import dataclass
from enum import Enum
import os


@dataclass
class Position:
    row: int
    col: int

    def move(self, direction: "DirectionTuple") -> "Position":
        return Position(self.row + direction.value[0], self.col + direction.value[1])


class MapSymbols(Enum):
    robot = "@"
    box = "O"
    obsticle = "#"
    empty = "."
    boxopen = "["
    boxclose = "]"


class DirectionSymbol(Enum):
    up = "^"
    down = "v"
    left = "<"
    right = ">"


class DirectionTuple(Enum):
    up = (-1, 0)
    down = (1, 0)
    left = (0, -1)
    right = (0, 1)


@dataclass
class Direction:
    symbol: DirectionSymbol
    coordinates: DirectionTuple


class Robot:
    def __init__(self, starting_position: Position) -> None:
        self.position = starting_position

    def move(self, direction: Direction) -> None:
        self.position = self.position.move(direction.coordinates)


class DirectionList:
    def __init__(self, directions: str) -> None:
        self.directions: list[Direction] = []
        self.current_direction_index: int = 0
        for direction in directions:
            if direction == "^":
                self.directions.append(Direction(DirectionSymbol.up, DirectionTuple.up))
            elif direction == ">":
                self.directions.append(
                    Direction(DirectionSymbol.right, DirectionTuple.right)
                )
            elif direction == "v":
                self.directions.append(
                    Direction(DirectionSymbol.down, DirectionTuple.down)
                )
            elif direction == "<":
                self.directions.append(
                    Direction(DirectionSymbol.left, DirectionTuple.left)
                )

    def get_direction(self) -> Direction:
        direction = self.directions[self.current_direction_index]
        self.current_direction_index += 1
        return direction

    def get_prev_direction(self) -> Direction:
        if 0 <= self.current_direction_index <= len(self.directions):
            return self.directions[self.current_direction_index - 1]

        raise Exception(
            f"Current index is not a valid index: {self.current_direction_index}"
        )


class Map:
    def __init__(self, map_str: list[str]) -> None:
        self.map: list[list[MapSymbols]] = []
        for line in map_str:
            self.map.append([MapSymbols(symbol) for symbol in line])

        robot_row: int = -1
        robot_col: int = -1
        for r_index, r in enumerate(self.map):
            for c_index, c in enumerate(r):
                if c == MapSymbols.robot:
                    robot_col = c_index
                    robot_row = r_index
                    break
        if robot_col == -1 or robot_row == -1:
            raise Exception("Robot not found")

        self.robot = Robot(Position(robot_row, robot_col))

    def display(self) -> None:
        for row in self.map:
            print("".join([symbol.value for symbol in row]))

    def expand(self) -> None:
        new_map: list[list[MapSymbols]] = []
        for index, row in enumerate(self.map):
            new_map.append([])
            for col in row:
                if col == MapSymbols.obsticle:
                    new_map[index].append(MapSymbols.obsticle)
                    new_map[index].append(MapSymbols.obsticle)
                elif col == MapSymbols.empty:
                    new_map[index].append(MapSymbols.empty)
                    new_map[index].append(MapSymbols.empty)
                elif col == MapSymbols.robot:
                    new_map[index].append(MapSymbols.robot)
                    new_map[index].append(MapSymbols.empty)
                elif col == MapSymbols.box:
                    new_map[index].append(MapSymbols.boxopen)
                    new_map[index].append(MapSymbols.boxclose)

        self.map = new_map

    def get(self, position: Position) -> MapSymbols:
        return self.map[position.row][position.col]

    def set(self, position: Position, value: MapSymbols) -> None:
        self.map[position.row][position.col] = value

    def simulate_move(self, move: Direction) -> None:
        next_position: Position = self.robot.position.move(move.coordinates)
        next_tile: MapSymbols = self.get(next_position)

        def can_move_box() -> bool:
            box_to_look_at_pos: Position = next_position
            while True:
                if self.get(box_to_look_at_pos) == MapSymbols.box:
                    box_to_look_at_pos = box_to_look_at_pos.move(move.coordinates)
                elif self.get(box_to_look_at_pos) == MapSymbols.obsticle:
                    return False
                elif self.get(box_to_look_at_pos) == MapSymbols.empty:
                    return True

        def move_box() -> None:
            box_to_look_at_pos: Position = next_position
            while True:
                if self.get(box_to_look_at_pos) == MapSymbols.box:
                    box_to_look_at_pos = box_to_look_at_pos.move(move.coordinates)
                if self.get(box_to_look_at_pos) == MapSymbols.empty:
                    self.set(box_to_look_at_pos, MapSymbols.box)
                    return

        if next_tile == MapSymbols.obsticle:
            pass
        elif next_tile == MapSymbols.empty:
            self.set(self.robot.position, MapSymbols.empty)
            self.set(next_position, MapSymbols.robot)
            self.robot.move(move)
        elif next_tile == MapSymbols.box and can_move_box():
            move_box()
            self.set(self.robot.position, MapSymbols.empty)
            self.set(next_position, MapSymbols.robot)
            self.robot.move(move)

    def get_GPS_value(self) -> int:
        GPS_sum: int = 0
        for r_index, row in enumerate(self.map):
            for c_index, col in enumerate(row):
                if col == MapSymbols.box:
                    GPS_sum += 100 * r_index + c_index
        return GPS_sum


def read_file(file_name: str) -> list[str]:
    with open(file_name) as f:
        return f.readlines()


def get_direction_str_from_file(filename: str) -> str:
    lines: list[str] = read_file(filename)
    split_index: int = lines.index("\n")

    directions: str = ""
    for direction_line in lines[split_index + 1 :]:
        directions += direction_line.rstrip()

    return directions


def get_map_str_from_file(filename: str) -> list[str]:
    lines: list[str] = read_file(filename)
    split_index: int = lines.index("\n")

    map_str: list[str] = []
    for line in lines[:split_index]:
        map_str.append(line.rstrip())

    return map_str


def main() -> None:
    FILE_NAME = "input.txt"
    direction_str: str = get_direction_str_from_file(FILE_NAME)
    map_str: list[str] = get_map_str_from_file(FILE_NAME)

    map: Map = Map(map_str)
    # map.display()
    # input("Start")
    # os.system("clear")
    direction_list: DirectionList = DirectionList(direction_str)

    for direction in direction_list.directions:
        # print(direction.symbol.value)
        map.simulate_move(direction)
        # map.display()
        # input()
        # os.system("clear")

    GPS: int = map.get_GPS_value()

    print(GPS)


def main2() -> None:
    FILE_NAME = "test2.txt"
    direction_str: str = get_direction_str_from_file(FILE_NAME)
    map_str: list[str] = get_map_str_from_file(FILE_NAME)
    map: Map = Map(map_str)
    direction_list: DirectionList = DirectionList(direction_str)
    map.display()
    map.expand()
    map.display()


if __name__ == "__main__":
    main2()
