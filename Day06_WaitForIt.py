"""AoC 2023 Day 5"""
from math import ceil, sqrt, floor, prod
from re import findall


def get_range(time_and_distance: tuple[int, int]) -> tuple[int, int]:
	"""Solve -x^2 - time * x > distance. Return the smallest and larges integer
	values for x satisfying this equation."""

	time, distance = time_and_distance

	# We calculate the roots of -x^2 - time * x - distance = 0.
	discriminant = (time * time) - (distance << 2)

	assert discriminant > 0

	square_root_of_discriminant = sqrt(discriminant)
	#  The one where we take the negative square root is always the largest of
	#  the two roots.
	roots = [(-time + square_root_of_discriminant) / -2,
	         (-time - square_root_of_discriminant) / -2]
	
	# integer roots should be adjusted to satisfy inequality!
	if int(roots[0]) == roots[0]:
		assert int(roots[1]) == roots[1]
		return int(roots[0]) + 1, int(roots[1]) - 1
	
	# we need integers, so for non-integer roots take ceil of smallest root and
	# floor of largest root.
	return ceil(min(roots)), floor(max(roots))


def solve() -> None:
	"""Solve the problems, print the solutions and - if solutions are already
	known - verify the solutions."""
	
	with (open(f"Day06_input.txt") as input_file):
		times = [*map(int, findall(r"[0-9]+", input_file.readline()))]
		distances = [*map(int, findall(r"[0-9]+", input_file.readline()))]
		solution_1 = prod(last - first + 1
		                  for (first, last) in
		                  map(get_range, zip(times, distances)))
	solution_2 = 0
	
	print(solution_1, solution_2)
	assert (solution_1, solution_2) == (131376, 0)


if __name__ == "__main__":
	solve()
