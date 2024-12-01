from part1 import (
  Game,
  get_games
)

def main() -> None:
  game_list = get_games("input.txt")
  games = []
  for game in game_list:
    game = Game(game)
    games.append(game.max_blue * game.max_green * game.max_red)
  
  print(sum(games))

if __name__ == "__main__":
  main()
