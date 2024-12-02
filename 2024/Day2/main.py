def is_safe(levels: list[str]) -> bool:
    previous: int = -1
    direction: int = 0
    safe: bool = True
    for level in levels:
        if previous == -1:
            previous = int(level)
            continue

        gap = int(level) - previous

        if gap == 0:
            safe = False
            break

        if abs(gap) > 3:
            safe = False
            break

        previous = int(level)
        if direction == 0:
            if gap > 0:
                direction = 1
            else:
                direction = -1
        else:
            if direction == 1 and gap < 0:
                safe = False
                break
            elif direction == -1 and gap > 0:
                safe = False
                break
            else:
                pass
    return safe


def main2() -> None:
    lines: list[str] = []
    safe_reports: int = 0
    with open("input.txt") as f:
        lines = f.readlines()

    for line in lines:
        levels: list[str] = line.split(" ")
        if not is_safe(levels):
            for index in range(len(levels)):
                levels_c: list[str] = levels.copy()
                levels_c.pop(index)
                if is_safe(levels_c):
                    safe_reports += 1
                    break
        else:
            safe_reports += 1

    print(safe_reports)


def main() -> None:
    lines: list[str] = []
    safe_reports: int = 0
    with open("test.txt") as f:
        lines = f.readlines()

    for line in lines:
        levels: list[str] = line.split(" ")
        previous: int = -1
        direction: int = 0
        errored: bool = False
        safe: bool = True
        for index, level in enumerate(levels):
            if previous == -1:
                previous = int(level)
                continue

            gap = int(level) - previous

            if gap == 0:
                if errored:
                    safe = False
                    break
                else:
                    errored = True
                    previous = int(level)
                    continue

            if abs(gap) > 3:
                if errored:
                    safe = False
                    break
                else:
                    if index == 1:
                        next_num: int = int(levels[index + 1])
                        if abs(previous - next_num) <= 3:
                            pass
                        else:
                            previous = int(level)
                    errored = True
                    continue

            if direction == 0:
                if gap > 0:
                    direction = 1
                else:
                    direction = -1
                previous = int(level)
            else:
                if direction == 1 and gap < 0:
                    if errored:
                        safe = False
                        break
                    else:
                        errored = True
                elif direction == -1 and gap > 0:
                    if errored:
                        safe = False
                        break
                    else:
                        errored = True
                else:
                    previous = int(level)

        if safe:
            safe_reports += 1
        else:
            if is_safe(levels[1:]):
                safe_reports += 1
            else:
                print(levels)

    print(safe_reports)


if __name__ == "__main__":
    main2()
