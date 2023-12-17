"""AoC 2023 Day 11"""
from re import finditer
from typing import TypeAlias

CoordinatePair: TypeAlias = tuple[int, int]


def get_distances(galaxies: list[CoordinatePair]) -> list[int]:
	"""Return a list of distances between all galary-pairs in galaxies list."""
	
	distances = []

	for i in range(len(galaxies)):
		for j in range(i + 1, len(galaxies)):
			distances.append(abs(galaxies[j][0] - galaxies[i][0]) +
			                 abs(galaxies[j][1] - galaxies[i][1]))

	return distances


def get_empty_cols_and_rows(lines: list[str]) -> tuple[list[int], list[int]]:
	"""Return a tuple (list of empty row nrw, list of empty col nrs)."""
	
	empty_rows = set()
	empty_cols = set(range(len(lines[0])))
	
	for line_nr, line in enumerate(lines):

		matches = finditer(r"#", line)

		empty_row = True
		for match in matches:
			empty_row = False
			empty_cols.discard(match.start())

		if empty_row:
			empty_rows.add(line_nr)
	
	return sorted(empty_rows), sorted(empty_cols)
	

def get_galaxies(lines: list[str],
                 empty_rows: list[int],
                 empty_cols: list[int], replace_by: int) \
	-> list[CoordinatePair]:
	"""Return a list of galaxy coordinate pairs adjusted for expansion. Each
	empty row and each empty col is replaced by replace_by rows and cols."""
	
	galaxies = []

	extra_rows = 0
	for row, line in enumerate(lines):

		if row in empty_rows:
			extra_rows += replace_by - 1

		matches = finditer(r"#", line)

		for match in matches:
			col = match.start()
			nr_empty_cols_before = len([c for c in empty_cols if c < col])
			extra_cols = nr_empty_cols_before * (replace_by - 1)
			
			galaxies.append((col + extra_cols, row + extra_rows))
	
	return galaxies


def solve() -> None:
	"""Solve the problems, print the solutions and - if solutions are already
	known - verify the solutions."""
	
	with open(f"Day11_input.txt") as input_file:
		lines = input_file.readlines()
	
	empty_rows, empty_cols = get_empty_cols_and_rows(lines)
		
	galaxies = get_galaxies(lines, empty_rows, empty_cols, 2)
	solution_1 = sum(get_distances(galaxies))

	galaxies = get_galaxies(lines, empty_rows, empty_cols, 1_000_000)
	solution_2 = sum(get_distances(galaxies))

	print(solution_1, solution_2)
	assert (solution_1, solution_2) == (9623138, 726820169514)


if __name__ == "__main__":
	solve()
