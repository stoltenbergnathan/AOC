from dataclasses import dataclass


@dataclass
class Position:
    row: int
    col: int

    def copy(self) -> "Position":
        return Position(self.row, self.col)

    def __hash__(self) -> int:
        return hash((self.row, self.col))


class TMap:
    def __init__(self, map: list[list[str]]) -> None:
        self.map: list[list[str]] = map
        self.trailheads: list[Position] = self.find_trailheads()

    def get(self, position: Position) -> str:
        return self.map[position.row][position.col]

    def is_in_map(self, position: Position) -> bool:
        return 0 <= position.row < len(self.map) and 0 <= position.col < len(
            self.map[0]
        )

    def find_trailheads(self) -> list[Position]:
        trailheads: list[Position] = []

        for row_index, row in enumerate(self.map):
            for col_index, col in enumerate(row):
                if col == "0":
                    trailheads.append(Position(row_index, col_index))

        return trailheads

    def get_next_valid_positions(self, position: Position) -> list[Position]:
        next_positions: list[Position] = []

        direction = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for d in direction:
            next_position = Position(position.row + d[0], position.col + d[1])
            if not self.is_in_map(next_position):
                continue

            if int(self.get(position)) + 1 == int(self.get(next_position)):
                next_positions.append(next_position.copy())

        return next_positions

    def get_trail_head_score(self, position: Position) -> set[Position]:
        if self.get(position) == "9":
            return set([position])

        next_postions: list[Position] = self.get_next_valid_positions(position)

        positions: list[Position] = []
        for next_position in next_postions:
            positions.extend(self.get_trail_head_score(next_position))

        return set(positions)

    def get_trail_head_rating(self, position: Position) -> list[Position]:
        if self.get(position) == "9":
            return [position]

        next_postions: list[Position] = self.get_next_valid_positions(position)

        positions: list[Position] = []
        for next_position in next_postions:
            positions.extend(self.get_trail_head_rating(next_position))

        return positions


def read_file(filename: str) -> list[list[str]]:
    with open(filename) as fs:
        return [list(s.rstrip()) for s in fs.readlines()]


def main() -> None:
    trail_map: TMap = TMap(read_file("input.txt"))

    score: int = 0
    for position in trail_map.trailheads:
        score += len(trail_map.get_trail_head_score(position))
    print(score)

    rating: int = 0
    for position in trail_map.trailheads:
        rating += len(trail_map.get_trail_head_rating(position))
    print(rating)


if __name__ == "__main__":
    main()
