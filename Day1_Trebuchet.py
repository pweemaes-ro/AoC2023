"""AoC 2023 day 1."""
from string import digits

day_nr = 1


def get_digit(line: str, reverse: bool = False) -> int:
	"""Return the integer value of the first (if reverse == False) or last (if
	reverse == True) digit in line. Raises error if no digit found."""
	
	if reverse:
		indices = range(len(line) - 1, -1, -1)
	else:
		indices = range(len(line))

	for index in indices:
		if line[index] in digits:
			return int(line[index])

	raise ValueError(f"No digits found in line '{line}'")


def get_line_value(line: str) -> int:
	"""Return calibration value for the line."""
	
	return 10 * get_digit(line) + get_digit(line, reverse=True)


def solve() -> None:
	"""Solve the problem, print the solution and - if solution is already
	known - verify the solution."""
	
	with (open(f"Day{day_nr}_input.txt") as input_file):
		total = sum(get_line_value(line) for line in input_file.readlines())
	
	print(total)
	assert total == 53921   # verify

if __name__ == "__main__":
	solve()
