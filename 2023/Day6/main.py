with open('input.txt') as fs:
  lines: list[str] = fs.readlines()

race_times: list[int] = [int(time) for time in lines[0][5:].split()]
race_distances: list[int] = [int(distance) for distance in lines[1][9:].split()]

records: int = 1
for index in range(0, len(race_times)):
  time_held: int = 0
  record_beaters: int = 0
  for t in range(0, race_times[index] + 1):
    time_left: int = race_times[index] - time_held
    if time_left * time_held > race_distances[index]:
      record_beaters += 1
    time_held += 1
  records *= record_beaters
print(records)