"""AoC 2023 Day 8"""
from collections import deque
from collections.abc import Callable
from math import lcm
from re import findall
from typing import TypeAlias, TextIO, Literal

NodesTable: TypeAlias = dict[str, tuple[str, str]]


def nr_steps(start_key: str,
             stop_condition: Callable[[str], bool],
             nodes_table: NodesTable, rl_deque: deque[Literal[0, 1]]) -> int:
	"""Return nr of steps required to get from start_key to a key that
	satisfies the stop condition."""
	
	steps = 0
	key = start_key
	while not stop_condition(key):
		steps += 1
		rl_deque.append(index := rl_deque.popleft())
		key = nodes_table[key][index]
	return steps


def process_node_lines(input_file: TextIO) -> tuple[list[str], NodesTable]:
	"""Process all node lines in input_file. Each line has format
	 "KEY = (LEFT, RIGHT)". Return tuple containing
	- a (unordered) list of all KEY's found that end with an 'A',
	- a NodesTable object with key=KEY and value=(LEFT, RIGHT)."""

	nodes_table: NodesTable = dict()
	a_keys: list[str] = []
	
	while node_line := input_file.readline():
		key, left, right = findall(r"[a-zA-Z]{3}", node_line)
		nodes_table[key] = (left, right)
		
		if key[-1] == 'A':
			a_keys.append(key)

	return a_keys, nodes_table


def solve() -> None:
	"""Solve the problems, print the solutions and - if solutions are already
	known - verify the solutions."""
	
	with (open(f"Day08_input.txt") as input_file):
		# noinspection PyTypeChecker
		right_left_idxs: list[Literal[0, 1]] = \
			[1 if c == 'R' else 0 for c in input_file.readline()[:-1]]
		input_file.readline()   # skip empty line
		
		a_keys, key_nodes = process_node_lines(input_file)

	rl_deque = deque(right_left_idxs)
	# Re-initializing the rl_deque before each call to steps_for_key is not
	# strictly required, since the nr of steps for each key processed is an
	# exact multiple of the (constant) nr of items in the rl_deque!

	solution_1 = nr_steps("AAA", lambda key: key == "ZZZ", key_nodes, rl_deque)
	factors = (nr_steps(key, lambda key: key[-1] == 'Z', key_nodes, rl_deque)
	           for key in a_keys)
	solution_2 = lcm(*factors)
	
	print(solution_1, solution_2)
	assert (solution_1, solution_2) == (16343, 15299095336639)


if __name__ == "__main__":
	solve()
