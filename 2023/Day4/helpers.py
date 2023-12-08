from dataclasses import dataclass


def get_file_input(file_name: str) -> list[str]:
  with open(file_name) as fs:
    return fs.readlines()

@dataclass
class CardInfo:
  card_number: int
  winning_numbers: list[str]
  current_numbers: list[str]

def parse_card_info(card_data: str) -> CardInfo:
  NUM_OF_WINNING_NUMBERS: int = 10
  NUM_OF_CURRENT_NUMBERS: int = 25

  # Prep the original str
  card_data = card_data.replace('\n', '')

  game_data_split: list[str] = card_data.split(':')

  # Get card number
  card_number = int(game_data_split[0].split()[-1])

  numbers = game_data_split[1].split('|')

  # Grab number lists
  winning_numbers = numbers[0].split()
  if len(winning_numbers) != NUM_OF_WINNING_NUMBERS:
    raise Exception(f"Expected {NUM_OF_WINNING_NUMBERS} winning numbers, but instead got {len(winning_numbers)}. Here is line info: {card_data}")
  
  current_numbers = numbers[1].split()
  if len(current_numbers) != NUM_OF_CURRENT_NUMBERS:
    raise Exception(f"Expected {NUM_OF_CURRENT_NUMBERS} winning numbers, but instead got {len(current_numbers)}. Here is line info: {card_data}")

  return CardInfo(card_number, winning_numbers, current_numbers)


def get_points(card: CardInfo) -> int:
  first_match: bool = True
  points: int = 0

  for num in card.winning_numbers:
    if num in card.current_numbers:
      if first_match:
        points += 1
        first_match = False
      else:
        points *= 2
  
  return points

def get_matches(card: CardInfo) -> int:
  matches: int = 0

  for num in card.winning_numbers:
    if num in card.current_numbers:
      matches += 1
  
  return matches

def generate_original_stack(cards_data: list[str]) -> dict[int, list[CardInfo]]:
  og_stack: dict[int, list[CardInfo]] = {}
  for card_data in cards_data:
    card: CardInfo = parse_card_info(card_data)
    og_stack[card.card_number] = [card]
  return og_stack
