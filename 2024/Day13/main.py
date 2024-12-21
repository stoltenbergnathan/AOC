from dataclasses import dataclass
from typing import Any
from sympy import Rational, Integer
from sympy.abc import a, b
from sympy.solvers import solve

PART2: bool = True


@dataclass
class Button:
    name: str
    x_change: int
    y_change: int

    def cost(self, presses: int) -> int:
        if self.name == "A":
            return 3 * presses
        else:
            return 1 * presses


@dataclass
class Prize:
    x: int
    y: int


class ClawMachine:
    def __init__(self, input_str: list[str]) -> None:
        buttona_str: str = input_str[0].split(": ")[1]
        buttonb_str: str = input_str[1].split(": ")[1]

        self.buttona: Button = Button(
            "A", int(buttona_str.split(",")[0][1:]), int(buttona_str.split(",")[1][3:])
        )
        self.buttonb: Button = Button(
            "B", int(buttonb_str.split(",")[0][1:]), int(buttonb_str.split(",")[1][3:])
        )

        prize_str: str = input_str[2].split(": ")[1]
        self.prize: Prize = Prize(
            int(prize_str.split(",")[0][2:]), int(prize_str.split(",")[1][3:])
        )

        if PART2:
            self.prize.x += 10000000000000
            self.prize.y += 10000000000000

    def tokens_to_solve(self) -> int:
        combonations: list[tuple[int, int]] = []
        for a in range(0, 101):
            for b in range(0, 101):
                if (
                    a * self.buttona.x_change + b * self.buttonb.x_change
                    == self.prize.x
                    and a * self.buttona.y_change + b * self.buttonb.y_change
                    == self.prize.y
                ):
                    combonations.append((a, b))

        if len(combonations) == 0:
            return -1

        return min(
            [
                self.buttona.cost(presses[0]) + self.buttonb.cost(presses[1])
                for presses in combonations
            ]
        )

    def tokens_to_solve2(self) -> int:
        answer: dict[Any, Any] = solve(
            [
                a * self.buttona.x_change + b * self.buttonb.x_change - self.prize.x,
                a * self.buttona.y_change + b * self.buttonb.y_change - self.prize.y,
            ],
            [a, b],
        )

        if type(answer[a]) is Rational or type(answer[b]) is Rational:
            return -1

        return self.buttona.cost(int(answer[a])) + self.buttonb.cost(int(answer[b]))


def read_file(file_name: str) -> list[str]:
    with open(file_name) as f:
        return f.readlines()


def main() -> None:
    file_lines: list[str] = read_file("input.txt")

    input_strs: list[list[str]] = [
        file_lines[i : i + 3] for i in range(0, len(file_lines), 4)
    ]

    claw_machines: list[ClawMachine] = [
        ClawMachine(input_str) for input_str in input_strs
    ]

    tokens_used: int = 0
    if not PART2:
        for claw_machine in claw_machines:
            cost = claw_machine.tokens_to_solve()
            if cost != -1:
                tokens_used += cost
    else:
        for claw_machine in claw_machines:
            cost = claw_machine.tokens_to_solve2()
            if cost != -1:
                tokens_used += cost

    print(tokens_used)


if __name__ == "__main__":
    main()
