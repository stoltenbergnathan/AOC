def get_calibration_values(file_name: str) -> list[str]:
  lines = []
  with open(file_name) as fs:
    lines = fs.readlines()
  return lines

def decode_calibration_value(value: str) -> int:
  decoded_value = ""
  last_digit = ""

  for letter in value:
    if letter.isdigit():
      if len(decoded_value) == 0:
        decoded_value += letter
      else:
        last_digit = letter
  if last_digit == "":
    decoded_value += decoded_value
  else:
    decoded_value += last_digit

  return int(decoded_value)

def main():
  values = get_calibration_values("input.txt")
  decoded_values = []
  for value in values:
    decoded_values.append(decode_calibration_value(value))
  print("Sum of values is ", str(sum(decoded_values)))

if __name__ == "__main__":
  main()
