from helpers import (
  get_file_input,
  parse_card_info,
  get_points,
  CardInfo
)

def main() -> None:
  file_input: list[str] = get_file_input("input.txt")
  scores: list[int] = []
  for line in file_input:
    card: CardInfo = parse_card_info(line)
    scores.append(get_points(card))
  print(sum(scores))

if __name__ == "__main__":
  main()