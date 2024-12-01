FILE_NAME: str = 'input.txt'


def get_future_value_from_history(history: list[int]) -> int:
  if history.count(0) == len(history):
    return history[-1]
  
  refined_list: list[int] = []
  for index in range(0, len(history) - 1):
    refined_list.append(history[index + 1] - history[index])
  return get_future_value_from_history(refined_list) + history[-1]

def get_previous_value_from_history(history: list[int]) -> int:
  if history.count(0) == len(history):
    return history[0]
  
  refined_list: list[int] = []
  for index in range(0, len(history) - 1):
    refined_list.append(history[index + 1] - history[index])
  return history[0] - get_previous_value_from_history(refined_list)

with open(FILE_NAME) as fs:
  lines: list[str] = fs.readlines()

histories: list[int] = []
for line in lines:
  num_list: list[int] = [int(num) for num in line.strip().split()]

  histories.append(get_previous_value_from_history(num_list))

print(sum(histories))