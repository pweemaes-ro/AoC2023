"""AoC 2023 Day 6"""
from math import ceil, sqrt, floor, prod
from re import findall
from typing import TypeAlias

Interval: TypeAlias = tuple[int, int]


def get_interval_size(time_and_distance: tuple[int, int]) -> int:
	"""Return size of interval [r, s] with r the smallest x and s the largest x
	satisfying equation -x^2 - time * x > distance."""

	time, distance = time_and_distance

	# We calculate the roots of -x^2 - time * x = distance.
	# abc formula: a = -1, b = -time, c = -distance, so
	# 1. a < 0 => parabola has maximum
	# 2. discriminant = -time * -time - -4 * -1 * distance
	#                 = time * time - (distance << 2)
	discriminant = time * time - (distance << 2)

	assert discriminant > 0

	square_root_of_discriminant = sqrt(discriminant)
	# 1. roots = (-b pm square_root_of_discriminant) / 2a
	#          = (time pm square_root_of_discriminant) / -2
	# 2. Since denominator < 0 and roots are always positive, numerator < 0, so
	#    (time + square_root_of_discriminant) / -2 is smallest of the two roots.
	roots = [(time + square_root_of_discriminant) / -2,
	         (time - square_root_of_discriminant) / -2]
	
	# If integer roots, then smaller must be incremented, larger decremented to
	# satisfy inequality! Then:
	# -  interval size = int((root[1] - 1) - (root[0] + 1) + 1)
	#                  = int(root[1] - root[0] - 1)
	if int(roots[0]) == roots[0]:
		return int(roots[1] - roots[0] - 1)
	
	# float roots, smaller root should be rounded up, larger rounded down.
	return floor(max(roots)) - ceil(min(roots)) + 1


def solve() -> None:
	"""Solve the problems, print the solutions and - if solutions are already
	known - verify the solutions."""
	
	with (open(f"Day06_input.txt") as input_file):
		times = findall(r"[0-9]+", input_file.readline())
		distances = findall(r"[0-9]+", input_file.readline())

	solution_1 = prod(map(get_interval_size,
	                      zip([*map(int, times)], [*map(int, distances)])))
	
	solution_2 = get_interval_size((int(''.join(times)),
	                                int(''.join(distances))))
	
	print(solution_1, solution_2)
	assert (solution_1, solution_2) == (131376, 34123437)


if __name__ == "__main__":
	solve()
