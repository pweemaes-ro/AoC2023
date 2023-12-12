"""AoC 2023 Day 9"""
from collections import deque
from itertools import pairwise
from re import findall


def find_extrapolations(numbers: deque[int]) -> tuple[int, int]:
	"""Return the extrapolations before and after numbers"""
	
	difference_lines: list[deque[int]] = [numbers]
	current_line = numbers

	while True:
		next_line = deque(b - a for (a, b) in pairwise(current_line))
		difference_lines.append(next_line)
		if all(number == 0 for number in current_line):
			break
		current_line = next_line
	
	difference_lines[-1].append(0)
	# start with current line the last line and move backward through all
	# lines until the current line is the second line (and previous the first).
	for index in range(len(difference_lines) - 1, 0, -1):
		current_line = difference_lines[index]
		previous_line = difference_lines[index - 1]
		# add extrapolation to front of previous line
		previous_line.appendleft(previous_line[0] - current_line[0])
		# add extrapolation to beack of previous line
		previous_line.append(previous_line[-1] + current_line[-1])
	
	return difference_lines[0][0], difference_lines[0][-1]


def solve() -> None:
	"""Solve the problems, print the solutions and - if solutions are already
	known - verify the solutions."""
	
	solution_1 = solution_2 = 0

	with open(f"Day09_input.txt") as input_file:
		while line := input_file.readline():
			numbers = deque(map(int, findall(r"-?[0-9]+", line)))
			before, after = find_extrapolations(numbers)
			solution_1 += after
			solution_2 += before
			
	print(solution_1, solution_2)
	assert (solution_1, solution_2) == (1868368343, 1022)


if __name__ == "__main__":
	solve()
