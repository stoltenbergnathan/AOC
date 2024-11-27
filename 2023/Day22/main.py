from dataclasses import dataclass
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random


@dataclass
class BrickCord:
    x: int
    y: int
    z: int


@dataclass
class Brick:
    name: str
    cord1: BrickCord
    cord2: BrickCord
    supporting: list[str]
    supported_by: list[str]


def brick_sort(brick: Brick) -> int:
    return min(brick.cord1.z, brick.cord2.z)


def intersection(list1: list[int], list2: list[int]) -> bool:
    intersect_list = list(set(list1) & set(list2))
    if len(intersect_list) == 0:
        return False
    return True


def how_many_spaces_to_fall(brick: Brick, bricks_below: list[Brick]) -> int:
    current_brick_x: list[int] = list(range(brick.cord1.x, brick.cord2.x + 1))
    current_brick_y: list[int] = list(range(brick.cord1.y, brick.cord2.y + 1))

    for below_brick in reversed(bricks_below):
        below_brick_x: list[int] = list(
            range(below_brick.cord1.x, below_brick.cord2.x + 1)
        )
        below_brick_y: list[int] = list(
            range(below_brick.cord1.y, below_brick.cord2.y + 1)
        )
        if not intersection(current_brick_x, below_brick_x) or not intersection(
            current_brick_y, below_brick_y
        ):
            pass
        else:
            return (brick.cord1.z - below_brick.cord1.z) - 1

    return brick.cord1.z - 1


def get_supporting(brick: Brick, layer_above: list[Brick]) -> list[str]:
    supporting: list[str] = []
    current_brick_x: list[int] = list(range(brick.cord1.x, brick.cord2.x + 1))
    current_brick_y: list[int] = list(range(brick.cord1.y, brick.cord2.y + 1))

    for brick_above in layer_above:
        brick_above_x: list[int] = list(
            range(brick_above.cord1.x, brick_above.cord2.x + 1)
        )
        brick_above_y: list[int] = list(
            range(brick_above.cord1.y, brick_above.cord2.y + 1)
        )
        if intersection(current_brick_x, brick_above_x) or intersection(
            current_brick_y, brick_above_y
        ):
            supporting.append(brick_above.name)

    return supporting


class World:
    def __init__(self, bricks: list[Brick]) -> None:
        self.bricks = bricks
        self.bricks.sort(key=brick_sort)

    def fall(self) -> None:
        for index, brick in enumerate(self.bricks):
            fall_distance: int = how_many_spaces_to_fall(brick, self.bricks[:index])

            brick.cord1.z -= fall_distance
            brick.cord2.z -= fall_distance

    def attach_deps(self) -> None:
        for brick in self.bricks:
            supporting = get_supporting(
                brick, [b for b in self.bricks if b.cord1.z - 1 == brick.cord2.z]
            )
            brick.supporting = supporting
            for s_brick_name in supporting:
                s_brick: Brick = [b for b in self.bricks if b.name == s_brick_name][0]
                s_brick.supported_by.append(brick.name)

    def disintegrate(self) -> list[Brick]:
        disintegrated_bricks: list[Brick] = []
        self.attach_deps()
        for brick in self.bricks:
            # If you're not supporting anything you can be destroyed
            if len(brick.supporting) == 0:
                disintegrated_bricks.append(brick)
                continue

            # If all bricks you're supporting can be supported by another brick
            # you can be destroyed
            all_supported: bool = all(
                len(
                    [b for b in self.bricks if b.name == supported_brick][
                        0
                    ].supported_by
                )
                > 1
                for supported_brick in brick.supporting
            )

            if all_supported:
                disintegrated_bricks.append(brick)

        return disintegrated_bricks


def get_cords(str_cords: str) -> BrickCord:
    cords: list[str] = str_cords.split(",")
    return BrickCord(int(cords[0]), int(cords[1]), int(cords[2]))


def get_bricks_from_input() -> list[Brick]:
    FILE_NAME: str = "input.txt"
    lines: list[str] = []
    with open(FILE_NAME) as f:
        lines = f.readlines()

    bricks: list[Brick] = []
    brick_num: int = 1
    for line in lines:
        brick_cords: list[str] = line.split("~")
        cord1: BrickCord = get_cords(brick_cords[0])
        cord2: BrickCord = get_cords(brick_cords[1])

        brick: Brick
        if cord1.z <= cord2.z:
            brick = Brick(str(brick_num), cord1, cord2, [], [])
        else:
            brick = Brick(str(brick_num), cord2, cord1, [], [])
        bricks.append(brick)
        brick_num += 1

    return bricks


def visualize_layer(bricks: list[Brick]) -> None:
    _, ax = plt.subplots()  # type: ignore
    for brick in bricks:
        color = f"#{random.randint(0, 0xFFFFFF):06x}"
        x_min = min(brick.cord1.x, brick.cord2.x)
        x_max = max(brick.cord1.x, brick.cord2.x)
        y_min = min(brick.cord1.y, brick.cord2.y)
        y_max = max(brick.cord1.y, brick.cord2.y)

        min_thickness = 0.2
        if x_min == x_max:  # Constant x
            x_min -= min_thickness / 2
            x_max += min_thickness / 2
        if y_min == y_max:  # Constant y
            y_min -= min_thickness / 2
            y_max += min_thickness / 2

        rect = patches.Rectangle(
            (x_min, y_min), x_max - x_min, y_max - y_min, color=color, alpha=0.7
        )
        ax.add_patch(rect)

    ax.set_xlim(-1, 3)
    ax.set_ylim(-1, 3)
    ax.set_aspect("equal")
    plt.show()  # type: ignore


def test_fall() -> None:
    bricks = get_bricks_from_input()
    brick_map = World(bricks)
    for index, brick in reversed(list(enumerate(brick_map.bricks))):
        fall = how_many_spaces_to_fall(brick, brick_map.bricks[:index])
        print(fall)


def main() -> None:
    bricks = get_bricks_from_input()
    brick_map = World(bricks)
    brick_map.fall()
    bye_bricks = brick_map.disintegrate()
    print(len(bye_bricks))


if __name__ == "__main__":
    main()
