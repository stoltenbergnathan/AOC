from dataclasses import dataclass


@dataclass
class Update:
    page_numbers: list[int]


@dataclass
class OrderRule:
    x: int
    y: int


def read_file(file_name: str) -> list[str]:
    with open(file_name) as f:
        return f.readlines()


def get_updates(lines: list[str]) -> list[Update]:
    updates: list[Update] = []

    divider: int = lines.index("\n")
    second_half: list[str] = lines[divider + 1 :]
    for update in second_half:
        page_numbers: list[int] = []
        split: list[str] = update.split(",")
        for number in split:
            page_numbers.append(int(number))
        updates.append(Update(page_numbers))

    return updates


def get_order_rules(lines: list[str]) -> list[OrderRule]:
    rules: list[OrderRule] = []

    divider: int = lines.index("\n")
    first_half: list[str] = lines[:divider]
    for rule in first_half:
        split: list[str] = rule.split("|")
        x: int = int(split[0])
        y: int = int(split[1])
        rules.append(OrderRule(x, y))

    return rules


def is_rule_broken(rule: OrderRule, current: int, rest: list[int]) -> bool:
    if rule.x in rest:
        return True
    else:
        return False


def is_valid_update(update: Update, order_rules: list[OrderRule]) -> bool:
    for index, page in enumerate(update.page_numbers):
        rest_of_page: list[int] = update.page_numbers[index + 1 :]
        filterd_rules: list[OrderRule] = []
        for rule in order_rules:
            if rule.y == page:
                filterd_rules.append(rule)

        for rule in filterd_rules:
            if is_rule_broken(rule, page, rest_of_page):
                return False

    return True


def get_relevant_rules(pages: list[int], rules: list[OrderRule]) -> list[OrderRule]:
    filterd_rules: list[OrderRule] = []
    for rule in rules:
        if rule.x in pages and rule.y in pages:
            filterd_rules.append(rule)

    return filterd_rules


def rule_broken(compared_num: int, rules: list[OrderRule]) -> bool:
    for rule in rules:
        if rule.x == compared_num:
            return True
    return False


def order_invalid_update(update: Update, order_rules: list[OrderRule]) -> Update:
    page_numbers: list[int] = update.page_numbers.copy()
    filtered_rules: list[OrderRule] = get_relevant_rules(
        update.page_numbers, order_rules
    )

    index: int = 0
    while index < len(page_numbers) - 1:
        relevant_rules: list[OrderRule] = [
            rule for rule in filtered_rules if rule.y == page_numbers[index]
        ]
        temp_index: int = index + 1
        is_rule_broken: bool = False
        while temp_index < len(page_numbers) and len(relevant_rules) != 0:
            if rule_broken(page_numbers[temp_index], relevant_rules):
                is_rule_broken = True
                temp: int = page_numbers[index]
                page_numbers[index] = page_numbers[temp_index]
                page_numbers[temp_index] = temp
                break
            else:
                temp_index += 1

        if not is_rule_broken:
            index += 1

    return Update(page_numbers)


def get_middle(update: Update) -> int:
    return update.page_numbers[int(len(update.page_numbers) / 2)]


def main() -> None:
    lines: list[str] = read_file("input.txt")
    updates: list[Update] = get_updates(lines)
    order_rules: list[OrderRule] = get_order_rules(lines)
    valid_updates: list[Update] = []

    for update in updates:
        if is_valid_update(update, order_rules):
            valid_updates.append(update)

    middle_sum: int = 0
    for update in valid_updates:
        middle_sum += get_middle(update)

    print(middle_sum)


def part2() -> None:
    lines: list[str] = read_file("input.txt")
    updates: list[Update] = get_updates(lines)
    order_rules: list[OrderRule] = get_order_rules(lines)
    invalid_updates: list[Update] = []

    for update in updates:
        if not is_valid_update(update, order_rules):
            invalid_updates.append(update)

    new_updates: list[Update] = []
    for update in invalid_updates:
        new_updates.append(order_invalid_update(update, order_rules))

    middle_sum: int = 0
    for update in new_updates:
        middle_sum += get_middle(update)

    print(middle_sum)


if __name__ == "__main__":
    part2()
