from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

PART2 = True

class HandType(Enum):
  FiveOfAKind = 0
  FourOfAKind = 1
  FullHouse = 2
  ThreeOfAKind = 3
  TwoPair = 4
  OnePair = 5
  HighCard = 6


@dataclass
class CamelHand:
  cards: str
  hand_type: HandType
  bet: int

  def compare(self, obj: CamelHand) -> int:
    card_order = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    if PART2:
      card_order = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
    if self.hand_type != obj.hand_type:
      return -1 if self.hand_type.value > obj.hand_type.value else 1
    
    for i in range(0, len(self.cards)):
      if self.cards[i] != obj.cards[i]:
        return 1 if card_order.index(self.cards[i]) < card_order.index(obj.cards[i]) else -1
    
    return 0

  def __lt__(self, obj: CamelHand): 
    return True if self.compare(obj) == -1 else False 

  def __gt__(self, obj: CamelHand): 
    return True if self.compare(obj) == 1 else False 

  def __eq__(self, obj: CamelHand): 
    return True if self.compare(obj) == 0 else False 


def determine_hand(cards: str) -> HandType:
  cards_dict = {"A": 0, "K": 0, "Q": 0, "J": 0, "T": 0, "9": 0, "8": 0, "7": 0, "6": 0, "5": 0, "4": 0, "3": 0, "2": 0}
  for card in cards_dict.keys():
    cards_dict[card] = cards.count(card)
    if PART2:
      cards_dict[card] += cards.count("J")
    
  if PART2:
    cards_dict["J"] = 0

  full_house_condition = 3 in cards_dict.values() and 2 in cards_dict.values()
  if PART2 and "J" in cards:
    full_house_condition = list(cards_dict.values()).count(3) == 2
  
  if "J" in cards:
    pass

  if 5 in cards_dict.values():
    return HandType.FiveOfAKind
  elif 4 in cards_dict.values(): 
    return HandType.FourOfAKind
  elif full_house_condition:
    return HandType.FullHouse
  elif 3 in cards_dict.values():
    return HandType.ThreeOfAKind
  elif list(cards_dict.values()).count(2) == 2:
    return HandType.TwoPair
  elif 2 in cards_dict.values():
    return HandType.OnePair
  else:
    if PART2:
      if cards.count("J") > 0:
        raise Exception("Found a J in part 2 and result was high card. Cards: ", cards)
    return HandType.HighCard

def hand_generator(lines: list[str]) -> CamelHand:
  for line in lines:
    data = line.split()
    yield CamelHand(
      data[0],
      determine_hand(data[0]),
      int(data[1])
    )

def main():
  file_name = 'input.txt'
  with open(file_name) as fs:
    lines = fs.readlines()

  processed_hands: list[CamelHand] = []
  for hand in hand_generator(lines):
    processed_hands.append(hand)
  
  processed_hands = sorted(processed_hands)

  total_winnings: int = 0
  for (index, hand) in enumerate(processed_hands):
    total_winnings += (index + 1) * hand.bet
  
  print(total_winnings)

if __name__ == "__main__":
  main()