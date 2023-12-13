"""AoC 2023 Day 8"""
from collections import deque
from math import lcm
from re import findall
from typing import TypeAlias, TextIO, Literal

NodesTable: TypeAlias = dict[str, tuple[str, str]]


# This solution takes full advantage of the following discoveries (that can
# easily be veried programmatically):
# 1. The length n[i] of the path from A-node A[i] to nearest Z-node Z[j] is
#    equal to that of the Z[j]-cycle (path from Z[j] to Z[j]), and n[i] is a
#    multiple of the length of the left/right instructions cycle.
# 2. There are no other A-nodes in the path from A[i] to Z[j].
# 3. There are no other A-nodes or Z-nodes in the Z[j]-cycle.
# This means that all A[i] -> Z[j] -> Z[j] are disjunct. It also implies that
# there is no need for ever resetting the deque that cycles through the
# left/right instructions. Then the answer for part 2 is the LCM of all n[i]
# values.

def get_nr_steps(start_keys: tuple[str, ...],
                 stop_keys: tuple[str, ...],
                 nodes_table: NodesTable,
                 rl_deque: deque[Literal[0, 1]]) -> list[int]:
	"""Return a list of steps[i] required to go from start_key[i] to
	stop_keys[i] for all start keys in start_keys."""
	
	steps = 0
	keys = start_keys
	nr_keys = len(keys)
	retvals = [0] * nr_keys
	retvals_set = 0

	while True:
		steps += 1
		rl_deque.append(index := rl_deque.popleft())
		keys = tuple(nodes_table[key][index] for key in keys)
		
		for idx, (key, stop_key, retval) in \
			enumerate(zip(keys, stop_keys, retvals)):
			if not retval and key == stop_key:
				retvals[idx] = steps
				retvals_set += 1
				if retvals_set == nr_keys:
					return retvals


def process_node_lines(input_file: TextIO) -> (
	tuple)[tuple[str, ...], NodesTable]:
	"""Process all node lines in input_file. Each line has format
	"KEY = (LEFT, RIGHT)". Return tuple containing
	- a tuple of all KEY's found that end with an 'A',
	- a NodesTable object with key=KEY and value=(LEFT, RIGHT)."""

	nodes_table: NodesTable = dict()
	z_keys: set[str] = set()
	
	while node_line := input_file.readline():
		key, left, right = findall(r"[a-zA-Z]{3}", node_line)
		nodes_table[key] = (left, right)
		
		if key[-1] == 'Z':
			z_keys.add(key)

	return tuple(z_keys), nodes_table


def solve() -> None:
	"""Solve the problems, print the solutions and - if solutions are already
	known - verify the solutions."""
	
	with (open(f"Day08_input.txt") as input_file):
		# noinspection PyTypeChecker
		right_left_idxs: list[Literal[0, 1]] = \
			[1 if c == 'R' else 0 for c in input_file.readline()[:-1]]
		input_file.readline()  # skip empty line
		z_keys, key_nodes = process_node_lines(input_file)
	
	rl_deque = deque(right_left_idxs)

	solution_1 = get_nr_steps(("AAA",), ("ZZZ",), key_nodes, rl_deque)[0]

	factors = get_nr_steps(z_keys, z_keys, key_nodes, rl_deque)
	solution_2 = lcm(*factors)
	
	print(solution_1, solution_2)
	assert (solution_1, solution_2) == (16343, 15299095336639)


if __name__ == "__main__":
	solve()
