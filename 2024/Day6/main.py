from enum import Enum
from dataclasses import dataclass


class Direction(Enum):
    up = "^"
    right = ">"
    left = "<"
    down = "v"

    def next(self) -> "Direction":
        order = [
            Direction.up,
            Direction.right,
            Direction.down,
            Direction.left,
        ]
        return order[(order.index(self) + 1) % len(order)]


@dataclass
class Position:
    col: int
    row: int

    def copy(self) -> "Position":
        return Position(self.col, self.row)

    def move(self, direction: Direction) -> "Position":
        col_row_changes: dict[Direction, tuple[int, int]] = {
            Direction.up: (0, -1),
            Direction.down: (0, 1),
            Direction.left: (-1, 0),
            Direction.right: (1, 0),
        }
        col_change, row_change = col_row_changes[direction]
        return Position(self.col + col_change, self.row + row_change)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Position):
            return False
        return self.row == other.row and self.col == other.col


@dataclass
class Guard:
    position: Position
    direction: Direction

    def copy(self) -> "Guard":
        return Guard(self.position.copy(), self.direction)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Guard):
            return False
        return self.position == other.position and self.direction == other.direction


def read_file(file_name: str) -> list[list[str]]:
    with open(file_name) as f:
        return [list(s.rstrip()) for s in f.readlines()]


def get_gaurd_pos(map: list[list[str]]) -> Position:
    for row_index, row_str in enumerate(map):
        for col_index, char in enumerate(row_str):
            if char == Direction.up.value:
                return Position(col_index, row_index)
    raise Exception("Guard not found")


def within_bounds(position: Position, map: list[list[str]]) -> bool:
    return 0 <= position.row < len(map) and 0 <= position.col < len(map[0])


def valid_position(position: Position, map: list[list[str]]) -> bool:
    return map[position.row][position.col] != "#"


def move_guard(guard: Guard, map: list[list[str]]) -> bool:
    next_possible_position: Position = guard.position.move(guard.direction)
    if not within_bounds(next_possible_position, map):
        return False

    if valid_position(next_possible_position, map):
        guard.position = next_possible_position
        return True

    guard.direction = guard.direction.next()
    return True


def main() -> None:
    map: list[list[str]] = read_file("test.txt")
    guard: Guard = Guard(get_gaurd_pos(map), Direction.up)
    positions_visisted: list[Position] = []

    while True:
        current_position: Position = guard.position.copy()
        if current_position not in positions_visisted:
            positions_visisted.append(current_position)
            map[current_position.row][current_position.col] = "X"

        if not move_guard(guard, map):
            next_position = guard.position.move(guard.direction)
            if not within_bounds(next_position, map):
                break

    print(len(positions_visisted))


def causes_loop(guard: Guard, map: list[list[str]]) -> bool:
    copy_guard: Guard = guard.copy()
    visited_states: set[tuple[int, int, Direction]] = set()

    while True:
        if not move_guard(copy_guard, map):
            return False
        state = (copy_guard.position.row, copy_guard.position.col, copy_guard.direction)
        if state in visited_states:
            return True
        visited_states.add(state)


def part2() -> None:
    map: list[list[str]] = read_file("input.txt")
    starting_pos: Position = get_gaurd_pos(map)
    guard: Guard = Guard(starting_pos, Direction.up)
    valid_obsticles: list[Position] = []

    while True:
        current_position: Position = guard.position.copy()
        next_position = guard.position.move(guard.direction)
        map[current_position.row][current_position.col] = "X"

        if within_bounds(next_position, map) and valid_position(next_position, map):
            holder: str = map[next_position.row][next_position.col]
            map[next_position.row][next_position.col] = "#"

            if causes_loop(guard, map) and next_position not in valid_obsticles:
                valid_obsticles.append(next_position)

            map[next_position.row][next_position.col] = holder

        if not move_guard(guard, map):
            break

    print(len(valid_obsticles))


if __name__ == "__main__":
    part2()
