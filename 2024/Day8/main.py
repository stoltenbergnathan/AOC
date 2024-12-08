from dataclasses import dataclass
from itertools import combinations


PART_2: bool = True


@dataclass
class Position:
    row: int
    col: int

    def __hash__(self) -> int:
        return hash((self.row, self.col))


class AntennaMap:
    def __init__(self, map: list[list[str]]) -> None:
        self.map = map
        self.rows = len(map)
        self.cols = len(map[0])
        self.antennas: dict[str, list[Position]] = {}
        self.__get_antennas()

    def __get_antennas(self) -> None:
        for row_index, row in enumerate(self.map):
            for col_index, col in enumerate(row):
                if col != ".":
                    if col in self.antennas:
                        self.antennas[col].append(Position(row_index, col_index))
                    else:
                        self.antennas[col] = [Position(row_index, col_index)]

    def get(self, position: Position) -> str:
        return self.map[position.row][position.col]

    def display(self) -> None:
        for row in self.map:
            print("".join(row))

    def is_in_map(self, position: Position) -> bool:
        return 0 <= position.row < self.rows and 0 <= position.col < self.cols

    def get_antinodes(self) -> list[Position]:
        antinodes: list[Position] = []

        for frequency in self.antennas:
            antennas = self.antennas[frequency]

            antenna_combinations: list[tuple[Position, Position]] = list(
                combinations(antennas, 2)
            )

            for combo in antenna_combinations:
                if PART_2:
                    antinodes.extend(self.calculate_antinodes_pt2(combo))
                else:
                    antinodes.extend(self.calculate_antinodes(combo))

        return antinodes

    def calculate_antinodes(
        self, antenna_pair: tuple[Position, Position]
    ) -> list[Position]:
        antinodes: list[Position] = []

        row_diff: int = antenna_pair[0].row - antenna_pair[1].row
        col_diff: int = antenna_pair[0].col - antenna_pair[1].col

        if row_diff == 0 or col_diff == 0:
            raise Exception("Antennas are in the same row or column")

        first_antinode: Position = Position(
            antenna_pair[0].row + row_diff, antenna_pair[0].col + col_diff
        )
        second_antinode: Position = Position(
            antenna_pair[1].row + (row_diff * -1),
            antenna_pair[1].col + (col_diff * -1),
        )

        if self.is_in_map(first_antinode):
            antinodes.append(first_antinode)

        if self.is_in_map(second_antinode):
            antinodes.append(second_antinode)

        return antinodes

    def calculate_antinodes_pt2(
        self, antenna_pair: tuple[Position, Position]
    ) -> list[Position]:
        antinodes: list[Position] = []

        antinodes.append(antenna_pair[0])
        antinodes.append(antenna_pair[1])

        row_diff: int = antenna_pair[0].row - antenna_pair[1].row
        col_diff: int = antenna_pair[0].col - antenna_pair[1].col

        if row_diff == 0 or col_diff == 0:
            raise Exception("Antennas are in the same row or column")

        counter: int = 1
        while True:

            possible_antinode: Position = Position(
                antenna_pair[0].row + (row_diff * counter),
                antenna_pair[0].col + (col_diff * counter),
            )

            if self.is_in_map(possible_antinode):
                antinodes.append(possible_antinode)
            else:
                break

            counter += 1

        counter: int = 1
        while True:

            possible_antinode: Position = Position(
                antenna_pair[1].row + (row_diff * counter * -1),
                antenna_pair[1].col + (col_diff * counter * -1),
            )

            if self.is_in_map(possible_antinode):
                antinodes.append(possible_antinode)
            else:
                break

            counter += 1

        return antinodes


def read_input() -> list[list[str]]:
    with open("input.txt") as f:
        return [list(s.rstrip()) for s in f.readlines()]


def main() -> None:
    map: AntennaMap = AntennaMap(read_input())
    antinodes: list[Position] = map.get_antinodes()

    print(len(set(antinodes)))

    for antinode in antinodes:
        if map.get(antinode) == ".":
            map.map[antinode.row][antinode.col] = "#"

    map.display()


if __name__ == "__main__":
    main()
