from dataclasses import dataclass
from enum import Enum


@dataclass
class Position:
    row: int
    col: int

    def __hash__(self) -> int:
        return hash((self.row, self.col))

    def move(self, direction: str) -> "Position":
        if direction == "right":
            return Position(self.row, self.col + 1)
        elif direction == "left":
            return Position(self.row, self.col - 1)
        elif direction == "up":
            return Position(self.row - 1, self.col)
        elif direction == "down":
            return Position(self.row + 1, self.col)
        else:
            raise Exception("Invalid direction")


class MapSymbol(Enum):
    free = "."
    corrupted = "#"
    taken = "O"


@dataclass
class PositionNode:
    position: Position
    parent: "PositionNode | None"
    f: int
    g: int
    h: int

    def __hash__(self) -> int:
        return hash((self.position, self.parent, self.f, self.g, self.h))


class Map:
    def __init__(
        self, bytes: list[str], max_row: int, max_col: int, bytes_to_read: int
    ) -> None:
        self.map: list[list[MapSymbol]] = [
            [MapSymbol.free for _ in range(max_col + 1)] for _ in range(max_row + 1)
        ]

        self.bytes = bytes
        for byte_index in range(bytes_to_read):
            byte_col, byte_row = bytes[byte_index].split(",")
            byte_pos: Position = Position(int(byte_row), int(byte_col))

            self.map[byte_pos.row][byte_pos.col] = MapSymbol.corrupted

        self.byte_index = bytes_to_read

        self.start: Position = Position(0, 0)
        self.end: Position = Position(max_row, max_col)

        self.path: PositionNode | None = None

    def read_next_byte(self) -> Position:
        byte_col, byte_row = self.bytes[self.byte_index].split(",")
        byte_pos: Position = Position(int(byte_row), int(byte_col))
        self.set(byte_pos, MapSymbol.corrupted)

        self.byte_index += 1

        return byte_pos

    def show_path(self) -> None:
        if self.path is None:
            return
        current_node: PositionNode | None = self.path
        while current_node is not None:
            self.set(current_node.position, MapSymbol.taken)
            current_node = current_node.parent

    def clear_path(self) -> None:
        if self.path is None:
            return
        current_node: PositionNode | None = self.path
        while current_node is not None:
            if self.get(current_node.position) == MapSymbol.taken:
                self.set(current_node.position, MapSymbol.free)
            current_node = current_node.parent

        self.path = None

    def display(self) -> None:
        for row in self.map:
            for col in row:
                print(col.value, end="")
            print()

    def get(self, position: Position) -> MapSymbol:
        return self.map[position.row][position.col]

    def set(self, position: Position, value: MapSymbol) -> None:
        self.map[position.row][position.col] = value

    def is_in_map(self, position: Position) -> bool:
        return 0 <= position.row < len(self.map) and 0 <= position.col < len(
            self.map[0]
        )

    def solve(self) -> int:
        open_set: set[PositionNode] = set([PositionNode(self.start, None, 0, 0, 0)])
        closed_set: set[PositionNode] = set()

        while open_set:
            q: PositionNode = min(open_set, key=lambda node: node.f)
            open_set.remove(q)

            for successor_pos in [
                q.position.move("up"),
                q.position.move("down"),
                q.position.move("left"),
                q.position.move("right"),
            ]:
                if successor_pos == self.end:
                    self.path = q
                    return q.g + 1

                if not self.is_in_map(successor_pos):
                    continue

                if self.get(successor_pos) == MapSymbol.corrupted:
                    continue

                successor_g = q.g + 1
                successor_h = abs(successor_pos.row - self.end.row) + abs(
                    successor_pos.col - self.end.col
                )
                successor_f = successor_g + successor_h

                matching_node_open: list[PositionNode] = [
                    node for node in open_set if node.position == successor_pos
                ]

                matching_node_closed: list[PositionNode] = [
                    node for node in closed_set if node.position == successor_pos
                ]

                if matching_node_open:
                    matching_node = matching_node_open[0]
                    if matching_node.f < successor_f:
                        continue

                elif matching_node_closed:
                    matching_node = matching_node_closed[0]
                    if matching_node.f < successor_f:
                        continue

                else:
                    matching_node = PositionNode(
                        successor_pos, q, successor_f, successor_g, successor_h
                    )
                    open_set.add(matching_node)

            closed_set.add(q)

        return -1


def read_lines(filename: str) -> list[str]:
    with open(filename) as f:
        return f.readlines()


def main() -> None:
    FILE = "input.txt"
    ROWS = 70
    COLS = 70
    BYTES_TO_READ = 2898

    bytes: list[str] = read_lines(FILE)
    map: Map = Map(bytes, ROWS, COLS, BYTES_TO_READ)

    while map.solve() != -1:
        p = map.read_next_byte()
        map.clear_path()

    map.show_path()
    map.display()

    print(p.col, p.row)


if __name__ == "__main__":
    main()
