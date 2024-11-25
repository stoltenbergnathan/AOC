from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class MapElements(Enum):
    start = "S"
    unvisited = "."
    rock = "#"


@dataclass
class MapCord:
    row: int
    column: int

    def __hash__(self) -> int:
        return hash((self.row, self.column))


memoized_tiles: dict[Tuple[MapCord, int], set[MapCord]] = {}


class Map:
    garden_map: list[str] = []

    @classmethod
    def initialize(cls, file_name: str) -> None:
        with open(file_name) as f:
            cls.garden_map = [line.strip() for line in f.readlines()]

    @classmethod
    def get_starting_cords(cls) -> MapCord:
        for index, row in enumerate(cls.garden_map):
            if MapElements.start.value not in row:
                continue
            return MapCord(index, row.find(MapElements.start.value))
        raise Exception("Starting Point not found.")

    @classmethod
    def get_value_at_cords(cls, cords: MapCord) -> MapElements | None:
        if cords.column < 0 or cords.row < 0:
            return None
        try:
            return MapElements(cls.garden_map[cords.row][cords.column])
        except Exception:
            return None


def get_valid_options(current_pos: MapCord) -> list[MapCord]:
    ahead_and_behind: list[int] = [-1, 1]
    valid_options: list[MapCord] = []

    for move in ahead_and_behind:
        new_cords = MapCord(current_pos.row, current_pos.column + move)
        new_pos: MapElements | None = Map.get_value_at_cords(new_cords)
        if new_pos is not None and new_pos != MapElements.rock:
            valid_options.append(new_cords)

        new_cords = MapCord(current_pos.row + move, current_pos.column)
        new_pos: MapElements | None = Map.get_value_at_cords(new_cords)
        if new_pos is not None and new_pos != MapElements.rock:
            valid_options.append(new_cords)

    return valid_options


def trace_steps(cords: MapCord, steps_left: int) -> set[MapCord]:
    if steps_left == 0:
        if Map.get_value_at_cords(cords) == MapElements.rock:
            return set()
        else:
            return {cords}

    if (cords, steps_left) in memoized_tiles:
        return memoized_tiles[(cords, steps_left)]

    possible_moves: list[MapCord] = get_valid_options(cords)
    plots_visited: set[MapCord] = set()
    for move in possible_moves:
        plots_visited.update(trace_steps(move, steps_left - 1))
    memoized_tiles[(cords, steps_left)] = plots_visited
    return plots_visited


if __name__ == "__main__":
    Map.initialize("input.txt")
    STEPS: int = 64
    total_plots: set[MapCord] = trace_steps(Map.get_starting_cords(), STEPS)
    print(len(total_plots))
