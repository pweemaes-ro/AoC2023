"""AoC 2023 day 1."""
from string import digits

day_nr = 1

# lookup table for digits as text, with corresponding values.
text_to_int = {"one": 1,
               "two": 2,
               "three": 3,
               "four": 4,
               "five": 5,
               "six": 6,
               "seven": 7,
               "eight": 8,
               "nine": 9}


def get_digits(line: str, reverse: bool = False) -> tuple[int, int]:
	"""Return tuple of two integers:
	- first integer is the value of the first (or last) digit in line
	- second integer is the value of the first (or last) digit or digit as
	  string (whichever was found first).
	If reverse == False, the values are the first found, elke the values are
	the last found. Raises ValueError if no digits found in line."""
	
	if reverse:
		indices = range(len(line) - 1, -1, -1)
	else:
		indices = range(len(line))

	first_digit: int | None = None
	first_any: int | None = None
	
	for index in indices:
		if first_digit is None and line[index] in digits:
			first_digit = int(line[index])
			first_any = first_any or first_digit
			return first_digit, first_any

		if first_any is None:
			for length in (3, 4, 5):
				if first_any := text_to_int.get(line[index:index + length]):
					break
	
	raise ValueError(f"No digits found in line '{line}'")


def get_line_values(line: str) -> tuple[int, int]:
	"""Return calibration values for the line. The first value only considers
	digits, the second also considers digits as text."""
	
	first_digit, first_any = get_digits(line)
	last_digit, last_any = get_digits(line, reverse=True)
	
	return 10 * first_digit + last_digit, 10 * first_any + last_any


def solve() -> None:
	"""Solve the problems, print the solutions and - if solutions are already
	known - verify the solutions."""
	
	solution_1 = 0
	solution_2 = 0

	with (open(f"Day{day_nr}_input.txt") as input_file):
		
		for line in input_file.readlines():
			part_1_value, part_2_value = get_line_values(line)
			solution_1 += part_1_value
			solution_2 += part_2_value
			
	print(solution_1, solution_2)
	assert (solution_1, solution_2) == (53921, 54676)   # verify


if __name__ == "__main__":
	solve()
