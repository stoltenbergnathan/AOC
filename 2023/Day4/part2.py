from helpers import (
  get_file_input,
  get_matches,
  generate_original_stack,
  CardInfo
)

def main() -> None:
  file_input: list[str] = get_file_input("input.txt")
  stack: dict[int, list[CardInfo]] = generate_original_stack(file_input)
  processed: int = 0

  for card_ids in stack.keys():
    for card in stack[card_ids]:
      processed += 1
      matches: int = get_matches(card)
      for offset in range(1, matches + 1):
        stack[card.card_number + offset].append(stack[card.card_number + offset][0])
  print(processed)

if __name__ == "__main__":
  main()