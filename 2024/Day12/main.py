from dataclasses import dataclass


@dataclass
class Position:
    row: int
    col: int

    def __hash__(self) -> int:
        return hash((self.row, self.col))


@dataclass
class Edge:
    plot1: Position
    plot2: Position

    def __hash__(self) -> int:
        return hash((self.plot1, self.plot2))


@dataclass
class Side:
    edges: list[Edge]


@dataclass
class Plot:
    name: str
    area: int
    perimeter: int
    sides: int
    positions: set[Position]

    def draw(self):
        min_row = min(p.row for p in self.positions)
        max_row = max(p.row for p in self.positions)
        min_col = min(p.col for p in self.positions)
        max_col = max(p.col for p in self.positions)
        for row in range(min_row - 1, max_row + 2):
            for col in range(min_col - 1, max_col + 2):
                print(
                    self.name if Position(row, col) in self.positions else ".",
                    end="",
                )
            print()

    def calculate_perimeter(self):
        for position in self.positions:
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for d in directions:
                next_position = Position(position.row + d[0], position.col + d[1])
                if next_position not in self.positions:
                    self.perimeter += 1

    def calculate_sides(self):
        def get_all_edges() -> list[Edge]:
            edges: list[Edge] = []
            for position in self.positions:
                directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                for d in directions:
                    next_position = Position(position.row + d[0], position.col + d[1])
                    if next_position not in self.positions:
                        edges.append(Edge(position, next_position))
            return edges

        def are_adjacent(edge1: Edge, edge2: Edge) -> bool:
            # Horizontal
            if (
                edge1.plot1.row == edge2.plot1.row
                and abs(edge1.plot1.col - edge2.plot1.col) == 1
            ) and (
                edge2.plot2.row == edge1.plot2.row
                and abs(edge2.plot2.col - edge1.plot2.col) == 1
            ):
                return True

            # Vertical
            if (
                edge1.plot1.col == edge2.plot1.col
                and abs(edge1.plot1.row - edge2.plot1.row) == 1
            ) and (
                edge2.plot2.col == edge1.plot2.col
                and abs(edge2.plot2.row - edge1.plot2.row) == 1
            ):
                return True

            return False

        def combine_sides(sides: list[Side]) -> list[Side]:
            combined: list[Side] = []
            visited: set[int] = set()

            for i, side in enumerate(sides):
                if i in visited:
                    continue

                new_side_edges = set(side.edges)

                for j, other_side in enumerate(sides):
                    if i == j or j in visited:
                        continue

                    if any(
                        are_adjacent(edge1, edge2)
                        for edge1 in new_side_edges
                        for edge2 in other_side.edges
                    ):
                        new_side_edges.update(other_side.edges)
                        visited.add(j)

                visited.add(i)
                combined.append(Side(list(new_side_edges)))

            return combined

        def get_sides(edges: list[Edge]) -> list[Side]:
            sides: list[Side] = [Side([edge]) for edge in edges]
            while True:
                combined = combine_sides(sides)
                if len(combined) == len(sides):
                    break
                sides = combined

            return sides

        edges = get_all_edges()
        self.sides = len(get_sides(edges))

    def calculate_area(self):
        self.area = len(self.positions)


class Map:
    def __init__(self, map: list[list[str]]):
        self.map = map

    def get(self, position: Position):
        return self.map[position.row][position.col]

    def is_in_map(self, position: Position):
        return 0 <= position.row < len(self.map) and 0 <= position.col < len(
            self.map[0]
        )


def read_file(file_name: str) -> list[list[str]]:
    with open(file_name) as f:
        return [list(s.rstrip()) for s in f.readlines()]


def get_plots(map: Map, visited: set[Position] = set()) -> list[Plot]:
    plots: list[Plot] = []
    for row_index, row in enumerate(map.map):
        for col_index, col in enumerate(row):
            if Position(row_index, col_index) not in visited:
                plots.append(
                    Plot(
                        name=col,
                        area=0,
                        perimeter=0,
                        sides=0,
                        positions=flood_fill(
                            map, Position(row_index, col_index), visited, col
                        ),
                    )
                )
    return plots


def flood_fill(
    map: Map, position: Position, visited: set[Position], value: str
) -> set[Position]:
    if map.get(position) != value:
        return set()

    visited.add(position)

    positions: set[Position] = set([position])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for direction in directions:
        next_position = Position(
            position.row + direction[0], position.col + direction[1]
        )
        if map.is_in_map(next_position) and next_position not in visited:
            positions.update(flood_fill(map, next_position, visited, value))

    return positions


def main() -> None:
    map = Map(read_file("input.txt"))
    plots: list[Plot] = get_plots(map)
    PART2: bool = True

    prices: list[int] = []
    for plot in plots:
        plot.calculate_area()
        plot.calculate_perimeter()
        plot.calculate_sides()
        price: int
        if PART2:
            price = plot.area * plot.sides
        else:
            price = plot.area * plot.perimeter
        prices.append(price)
        print(
            "Plot name {}, area {}, perimeter {}, sides {}, price {}".format(
                plot.name, plot.area, plot.perimeter, plot.sides, price
            )
        )
        plot.draw()

    print(sum(prices))


if __name__ == "__main__":
    main()
