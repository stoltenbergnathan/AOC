from dataclasses import dataclass


@dataclass
class Stone:
    value: int

    def blink(self) -> list["Stone"]:
        if self.value == 0:
            return [Stone(1)]
        elif len(str(self.value)) % 2 == 0:
            str_values: list[str] = [
                str(self.value)[: len(str(self.value)) // 2],
                str(self.value)[len(str(self.value)) // 2 :],
            ]
            return [Stone(int(x)) for x in str_values]

        else:
            return [Stone(self.value * 2024)]

    def __hash__(self) -> int:
        return hash(self.value)


def read_file(file_name: str) -> str:
    with open(file_name) as f:
        return f.read()


learned_arrangements: dict[tuple[Stone, int], int] = {}


def arrange_stones(stones: list[Stone], blinks: int) -> int:
    if blinks == 0:
        return len(stones)

    new_stone_count: int = 0
    for stone in stones:
        if (stone, blinks) in learned_arrangements:
            new_stone_count += learned_arrangements[(stone, blinks)]
        else:
            stone_count: int = arrange_stones(stone.blink(), blinks - 1)
            learned_arrangements[(stone, blinks)] = stone_count
            new_stone_count += stone_count

    return new_stone_count


def main() -> None:
    line: str = read_file("input.txt")
    line = line.strip()
    stones: list[Stone] = [Stone(int(x)) for x in line.split(" ")]

    final_stones: int = arrange_stones(stones, 75)

    print(final_stones)


if __name__ == "__main__":
    main()
