from part import Part
from part_category import PartCategory
from rule import Rule
from system import System
from workflow import Workflow


FILE: str = "input.txt"


def main() -> None:
    with open(FILE) as fs:
        lines: list[str] = [line.strip() for line in fs.readlines()]

    system, parts = get_information_from_text(lines)

    part_sum: int = 0
    for part in parts:
        if system.part_passes(part):
            part_sum += part.x + part.m + part.a + part.s
    print(part_sum)


def get_information_from_text(lines: list[str]) -> tuple[System, list[Part]]:
    workflows: list[Workflow] = []
    parts: list[Part] = []

    on_parts: bool = False
    for line in lines:
        if line == "":
            on_parts = True
            continue

        if on_parts:
            values: list[str] = line.replace("{", "").replace("}", "").split(",")
            part: Part = Part(
                int(values[0][2:]),
                int(values[1][2:]),
                int(values[2][2:]),
                int(values[3][2:]),
            )
            parts.append(part)
        else:
            a: list[str] = line.replace("}", "").split("{")
            name: str = a[0]

            raw_rules: list[str] = a[1].split(",")
            last_rule: str = raw_rules[-1]

            raw_rules.pop()
            rules: list[Rule] = []
            for rule in raw_rules:
                part_cat: PartCategory = PartCategory(rule[0])
                condition: str = rule[1]
                value: int = int(rule[2 : rule.index(":")])
                next_step: str = rule[rule.index(":") + 1 :]
                rules.append(Rule(part_cat, condition, value, next_step))
            rules.append(Rule(None, None, None, last_rule))

            workflows.append(Workflow(name, rules))

    return (System(workflows), parts)


if __name__ == "__main__":
    main()
