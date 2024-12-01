digit_mapping = {
  0: 'zero',
  1: 'one',
  2: 'two',
  3: 'three',
  4: 'four',
  5: 'five',
  6: 'six',
  7: 'seven',
  8: 'eight',
  9: 'nine'
}

def get_calibration_values(file_name: str) -> list[str]:
  lines = []
  with open(file_name) as fs:
    lines = fs.readlines()
  return lines

def get_first_number(value: str) -> str:
  positions = []
  # Get the earliest positions of each letter number 
  for (_, v) in digit_mapping.items():
    try:
      positions.append(value.index(v))
    except:
      positions.append(9999999999)
  
  # Get the earliest postions of each digit
  number_index = -1
  for (index, letter) in enumerate(value):
    if letter.isdigit():
      number_index = index
      break
  
  # Compare
  if number_index != -1:
    return_index = number_index
    return_value = value[return_index]
  else:
    return_index = 999999
    return_value = 999999
  for (ind, pos) in enumerate(positions):
    if pos < return_index:
      return_index = pos
      return_value = ind

  return return_value


def get_last_number(value: str) -> str:
  positions = []
  # Get the latest positions of each letter number 
  for (_, v) in digit_mapping.items():
    tv = value.rfind(v)
    if tv != -1:
      positions.append(value.rfind(v))
    else:
      positions.append(0)
  
  # Get the latest postions of each digit
  number_index = 0
  for (index, letter) in enumerate(value):
    if letter.isdigit():
      number_index = index

  return_index = number_index
  return_value = value[number_index]
  for (ind, pos) in enumerate(positions):
    if pos > return_index:
      return_index = pos
      return_value = ind

  return return_value

def decode_calibration_value(value: str) -> int:
  first = get_first_number(value)
  last = get_last_number(value)
  value = f"{first}{last}"
  return int(value)

def main():
  values = get_calibration_values("input.txt")
  decoded_values = []
  for value in values:
    decoded_values.append(decode_calibration_value(value))
  print("Sum of values is ", str(sum(decoded_values)))

def test():
  print(decode_calibration_value('67mcmfive1sixonefive\n'))

if __name__ == "__main__":
  main()
