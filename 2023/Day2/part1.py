RED_CUBES = 12
GREEN_CUBES = 13
BLUE_CUBES = 14


class Game:
  def __init__(self, game_input: str) -> None:
    self.game_input: str = game_input
    self.game_id: int = 0
    self.max_red: int = 0
    self.max_green: int = 0
    self.max_blue: int = 0
    self.get_max_possible()
  
  def get_max_possible(self) -> None:
    game_split = self.game_input.split(':')
    if len(game_split) > 2:
      raise Exception("Found more than two substrings for ", self.game_input) 
    
    # Get the game id (Game n)
    self.game_id = int(game_split[0].replace("Game ", ''))

    # Grab the max seen for red, green, blue
    revealed_split = game_split[1].split(';')
    for split in revealed_split:
      color_split = split.split(',')
      for c_split in color_split:
        c_split: str = c_split.replace(' ', '')
        die_grabbed = ''
        currnet_i = 0
        while c_split[currnet_i].isdigit():
          die_grabbed += c_split[currnet_i]
          currnet_i += 1
          
        die_grabbed = int(die_grabbed)
        if "red" in c_split:
          if die_grabbed > self.max_red:
            self.max_red = die_grabbed
        elif "green" in c_split:
          if die_grabbed > self.max_green:
            self.max_green = die_grabbed
        elif "blue" in c_split:
          if die_grabbed > self.max_blue:
            self.max_blue = die_grabbed
        else:
          raise Exception("How tf")
    
  def is_possible(self) -> bool:
    if self.max_red > RED_CUBES:
      return False
    elif self.max_green > GREEN_CUBES:
      return False
    elif self.max_blue > BLUE_CUBES:
      return False
    else:
      return True


def get_games(filename: str) -> list[str]:
  with open(filename) as fs:
    return fs.readlines()

def main() -> None:
  game_list = get_games("input.txt")
  games = []
  for game in game_list:
    game = Game(game)
    possible = game.is_possible()
    if possible:
      games.append(game.game_id)
  id_sum = sum(games)
  print(id_sum)

if __name__ == "__main__":
  main()
