def main() -> None:
    list1: list[int] = []
    list2: list[int] = []

    lines: list[str] = []

    with open("input.txt") as f:
        lines = f.readlines()

    for line in lines:
        nums: list[str] = line.split("   ")
        num1: int = int(nums[0])
        num2: int = int(nums[1])
        list1.append(num1)
        list2.append(num2)

    list1.sort()
    list2.sort()

    diffs: list[int] = get_similarity_score(list1, list2)

    print(sum(diffs))


def return_differences(list1: list[int], list2: list[int]) -> list[int]:
    diffs: list[int] = []

    for index in range(0, len(list1)):
        diffs.append(abs(list1[index] - list2[index]))

    return diffs


def get_similarity_score(list1: list[int], list2: list[int]) -> list[int]:
    similarity_list: list[int] = []

    for num in list1:
        instances: int = 0
        for num2 in list2:
            if num2 == num:
                instances += 1
        similarity_list.append(instances * num)

    return similarity_list


main()
