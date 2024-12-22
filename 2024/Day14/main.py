from dataclasses import dataclass
import os


@dataclass
class Position:
    row: int
    col: int

    def copy(self) -> "Position":
        return Position(self.row, self.col)


@dataclass
class Velocity:
    row_vel: int
    col_vel: int

    def copy(self) -> "Velocity":
        return Velocity(self.row_vel, self.col_vel)


@dataclass
class Robot:
    position: Position
    velocity: Velocity

    def copy(self) -> "Robot":
        return Robot(self.position.copy(), self.velocity.copy())

    def get_next_position(self, map_max_rows: int, map_max_cols: int) -> Position:
        next_row: int = self.position.row + self.velocity.row_vel
        next_col: int = self.position.col + self.velocity.col_vel

        if next_row >= map_max_rows:
            next_row -= map_max_rows
        elif next_row < 0:
            next_row += map_max_rows

        if next_col >= map_max_cols:
            next_col -= map_max_cols
        elif next_col < 0:
            next_col += map_max_cols

        return Position(next_row, next_col)


class Map:
    def __init__(self, num_row: int, num_col: int, robots: list[Robot]) -> None:
        self.max_row = num_row
        self.max_col = num_col
        self.robots = robots
        self.seconds = 0

    def simulate(self) -> None:
        self.seconds += 1
        for robot in self.robots:
            robot.position = robot.get_next_position(self.max_row, self.max_col)

    def display(self, with_quads: bool = False) -> None:
        map = [[0 for _ in range(self.max_col)] for _ in range(self.max_row)]

        for robot in self.robots:
            map[robot.position.row][robot.position.col] += 1

        for r_index, row in enumerate(map):
            for c_index, col in enumerate(row):
                if with_quads and (
                    c_index == (self.max_col - 1) / 2
                    or r_index == (self.max_row - 1) / 2
                ):
                    print(" ", end="")
                elif col == 0:
                    print(".", end="")
                else:
                    print(col, end="")
            print()

    def doubled(self) -> bool:
        map = [[0 for _ in range(self.max_col)] for _ in range(self.max_row)]

        for robot in self.robots:
            map[robot.position.row][robot.position.col] += 1

        for row in map:
            for col in row:
                if col >= 2:
                    return True

        return False

    def count_robots_in_quadrant(self, quad: int) -> int:
        @dataclass
        class Range:
            lower: int
            upper: int

        @dataclass
        class QuadRange:
            col_range: Range
            row_range: Range

        def get_quad_ranges() -> dict[int, QuadRange]:
            return {
                1: QuadRange(
                    Range(0, int((self.max_col - 1) / 2) - 1),
                    Range(0, int((self.max_row - 1) / 2) - 1),
                ),
                2: QuadRange(
                    Range(int((self.max_col - 1) / 2) + 1, self.max_col - 1),
                    Range(0, int((self.max_row - 1) / 2) - 1),
                ),
                3: QuadRange(
                    Range(0, int((self.max_col - 1) / 2) - 1),
                    Range(int((self.max_row - 1) / 2) + 1, self.max_row - 1),
                ),
                4: QuadRange(
                    Range(int((self.max_col - 1) / 2) + 1, self.max_col - 1),
                    Range(int((self.max_row - 1) / 2) + 1, self.max_row - 1),
                ),
            }

        quad_range = get_quad_ranges()

        map = [[0 for _ in range(self.max_col)] for _ in range(self.max_row)]

        for robot in self.robots:
            map[robot.position.row][robot.position.col] += 1

        robots_in_quad: int = 0

        for r_index, row in enumerate(map):
            for c_index, col in enumerate(row):
                if (
                    quad_range[quad].col_range.lower
                    <= c_index
                    <= quad_range[quad].col_range.upper
                    and quad_range[quad].row_range.lower
                    <= r_index
                    <= quad_range[quad].row_range.upper
                ):
                    robots_in_quad += col

        return robots_in_quad


def read_file(filename: str) -> list[str]:
    with open(filename) as f:
        return f.readlines()


def get_robots_from_file(filename: str) -> list[Robot]:
    lines = read_file(filename)

    robots: list[Robot] = []
    for line in lines:
        position_str, velocity_str = line.split(" ")

        col_pos, row_pos = position_str.split("=")[1].split(",")
        col_vel, row_vel = velocity_str.split("=")[1].split(",")

        position = Position(int(row_pos), int(col_pos))
        velocity = Velocity(int(row_vel), int(col_vel))
        robots.append(Robot(position, velocity))

    return robots


def main() -> None:
    MAX_ROWS: int = 103
    MAX_COLS: int = 101
    robots: list[Robot] = get_robots_from_file("input.txt")
    robot_map: Map = Map(MAX_ROWS, MAX_COLS, robots)

    for _ in range(100000000000000000000000000000000):
        robot_map.simulate()
        if not robot_map.doubled():
            robot_map.display()
            print(robot_map.seconds)
            input()
            os.system("clear")

    robots_in_quad: int = 1
    for quad in [1, 2, 3, 4]:
        robots_in_quad *= robot_map.count_robots_in_quadrant(quad)

    print(robots_in_quad)


if __name__ == "__main__":
    main()
