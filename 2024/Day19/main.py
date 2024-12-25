def get_available_towels(lines: list[str]) -> list[str]:
    towels: str = lines[0]
    return [towel.rstrip().lstrip() for towel in towels.split(",")]


def get_wanted_designs(lines: list[str]) -> list[str]:
    return [line.rstrip() for line in lines[2:]]


def read_file(filename: str) -> list[str]:
    with open(filename) as f:
        return f.readlines()


def add_towel(current_design: str, towel: str) -> str:
    return f"{current_design}{towel}"


def main() -> None:
    FILE = "input.txt"
    lines = read_file(FILE)
    available_towels: list[str] = get_available_towels(lines)
    wanted_designs: list[str] = get_wanted_designs(lines)
    valid_designs: list[str] = []

    for design in wanted_designs:
        current_matches: list[str] = available_towels.copy()
        while current_matches:
            current_towel: str = max(current_matches, key=len)
            current_matches.remove(current_towel)

            for towel in available_towels:
                new_design: str = add_towel(current_towel, towel)

                if new_design == design[: len(new_design)]:
                    if len(new_design) == len(design):
                        valid_designs.append(new_design)
                        current_matches.clear()
                        print(new_design)
                        break
                    current_matches.append(new_design)

    print(len(valid_designs))


if __name__ == "__main__":
    main()
