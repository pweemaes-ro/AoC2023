"""AoC 2023 Day 4"""
from collections import defaultdict
from re import findall

nr_card_copies: dict[int, int] = defaultdict(lambda: 1)


def nr_of_winning_nrs(line: str) -> int:
	"""Return the number of winning numbers on the line."""
	
	winning_part, my_part = line.split(": ")[1].split(" | ")
	
	winning_nrs = set(map(int, findall(r"[0-9]+", winning_part)))
	my_nrs = set(map(int, findall(r"[0-9]+", my_part)))
	
	return len(winning_nrs.intersection(my_nrs))


def solve() -> None:
	"""Solve the problems, print the solutions and - if solutions are already
	known - verify the solutions."""

	solution_1 = 0
	
	with (open(f"Day04_input.txt") as input_file):
		
		for line_nr, line in enumerate(input_file, start=1):
			# make sure nr_card_copies[line_nr] is set to 1 of no value yet.
			nr_copies = nr_card_copies[line_nr]
			nr_wins = nr_of_winning_nrs(line)

			if nr_wins > 0:
				solution_1 += 1 << (nr_wins - 1)
				for i in range(1, nr_wins + 1):
					nr_card_copies[line_nr + i] += nr_copies

	solution_2 = sum(v for (k, v) in nr_card_copies.items() if k <= line_nr)
	
	print(solution_1, solution_2)
	assert (solution_1, solution_2) == (22674, 5747443)


if __name__ == "__main__":
	solve()
