from math import floor


def read_lines(filename: str) -> list[str]:
    with open(filename) as f:
        return f.readlines()


def get_starting_numbers(filename: str) -> list[int]:
    lines = read_lines(filename)
    return [int(line) for line in lines]


def mix(num1: int, num2: int) -> int:
    return num1 ^ num2


def prune(num: int) -> int:
    return num % 16777216


def step1(num: int) -> int:
    temp = num * 64
    temp = mix(num, temp)
    temp = prune(temp)
    return temp


def step2(num: int) -> int:
    temp = num / 32
    temp = floor(temp)
    temp = mix(num, temp)
    temp = prune(temp)
    return temp


def step3(num: int) -> int:
    temp = num * 2048
    temp = mix(num, temp)
    temp = prune(temp)
    return temp


def evolve(num: int) -> int:
    temp = step1(num)
    temp = step2(temp)
    temp = step3(temp)
    return temp


def get_secret_number(num: int, iterations: int) -> int:
    for _ in range(iterations):
        num = evolve(num)
    return num


def main() -> None:
    FILE = "input.txt"
    starting_nums = get_starting_numbers(FILE)

    iterations = 2000
    final_nums: list[int] = []
    for num in starting_nums:
        secret = get_secret_number(num, iterations)
        final_nums.append(secret)
    print(sum(final_nums))


def watch_evolve(num: int) -> None:
    print(num)
    while True:
        input()
        num = evolve(num)
        print(num)


if __name__ == "__main__":
    main()
