"""AoC 2023 Day 2"""

from re import findall


def solve() -> None:
	"""Solve the problems, print the solutions and - if solutions are already
	known - verify the solutions."""
	
	max_allowed = {"red": 12, "green": 13, "blue": 14}
	colors = tuple(max_allowed.keys())
	solution_1 = 0
	solution_2 = 0
	
	with (open(f"Day02_input.txt") as input_file):
	
		for game_nr, line in enumerate(input_file, start=1):

			game_valid = True
			game_power = 1
			
			for color in colors:
				# noinspection RegExpAnonymousGroup
				max_found = max(map(int, findall(rf"(\d+) {color}", line)))
				game_valid = game_valid and max_found <= max_allowed[color]
				game_power *= max_found

			solution_1 += game_nr * game_valid
			solution_2 += game_power
			
	print(solution_1, solution_2)
	assert (solution_1, solution_2) == (1931, 83105)


if __name__ == "__main__":
	solve()
