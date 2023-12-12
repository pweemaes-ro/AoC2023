"""AoC 2023 Day 8"""
from collections import deque
from math import lcm
from re import findall
from typing import TypeAlias, TextIO, Literal

NodesTable: TypeAlias = dict[str, tuple[str, str]]


def nr_steps(start_key: str,
             nodes_table: NodesTable,
             rl_deque: deque[Literal[0, 1]],
             stop_key: str | None = None) -> int:
	"""Return nr of steps required to go from start key to stop key, or - if
	stop key is None - the length of one cycle from start key to start key."""
	
	steps = 0
	key = start_key

	while True:
		steps += 1
		rl_deque.append(index := rl_deque.popleft())
		key = nodes_table[key][index]
		if key == stop_key or (key == start_key and not steps % len(rl_deque)):
			break
	
	return steps


# def nr_steps_old(start_key: str,
#                  stop_condition: Callable[[str], bool],
#                  nodes_table: NodesTable,
#                  rl_deque: deque[Literal[0, 1]]) -> int:
# 	"""Return nr of steps required to get from start_key to a key that
# 	satisfies the stop condition."""
#
# 	# IMPORTANT NOTE: Since none of the part 2 stop-keys have a left or right
# 	# child equal to the start key, it seems a lucky coincident that the
# 	# solution for part 2 was right. In fact we should be looking for TWO times
# 	# the same stop-key to determine the nr of steps in a cycle...
#
# 	key = start_key
#
# 	while not stop_condition(key):
# 		rl_deque.append(index := rl_deque.popleft())
# 		key = nodes_table[key][index]
#
# 	# The following conditions are met:
# 	# - the nr of steps from start key to stop key (the first key satisfying
# 	#   the stop condition) is equal to the nr of steps from the first stop
# 	#   key's occurance to the next occurance of the same stop key, AND
# 	# - this nr of steps is an EXACT multiple of the nr or left/right
# 	#   instructions.
# 	# Therefore the nr of steps from start key to stop key (as could be counted
# 	# in the first loop) IS the nr of steps in one period for the given
# 	# stop-key. Then the LCM of the nr of steps for each of the six different
# 	# keys starting with an 'A' is the solution to part 2.
# 	#
# 	# Had the condition not been met, the algorithm would have been a bit more
# 	# complicated and time-consuming...
# 	# In fact we could have ignored the given start keys and use each of the
# 	# six keys ending with 'Z' as stop_key, skipping the first loop, and only
# 	# execute the second loop. SEE NEW VERSION of nr_steps function above!
#
# 	steps = 1
# 	stop_key = key
# 	while True:
# 		rl_deque.append(index := rl_deque.popleft())
# 		key = nodes_table[key][index]
# 		if key == stop_key and steps % len(rl_deque) == 0:
# 			# notice that when steps % len(rl_deque) == 0 also the next child
# 			# (left or right) will be the same as at start of loop, so we don't
# 			# have to check this.
# 			break
# 		else:
# 			steps += 1
#
# 	return steps


def process_node_lines(input_file: TextIO) -> tuple[list[str], NodesTable]:
	"""Process all node lines in input_file. Each line has format
	"KEY = (LEFT, RIGHT)". Return tuple containing
	- a (unordered) list of all KEY's found that end with an 'A',
	- a NodesTable object with key=KEY and value=(LEFT, RIGHT)."""

	nodes_table: NodesTable = dict()
	z_keys: list[str] = []
	
	while node_line := input_file.readline():
		key, left, right = findall(r"[a-zA-Z]{3}", node_line)
		nodes_table[key] = (left, right)
		
		if key[-1] == 'Z':
			z_keys.append(key)

	return z_keys, nodes_table


def solve() -> None:
	"""Solve the problems, print the solutions and - if solutions are already
	known - verify the solutions."""
	
	with (open(f"Day08_input.txt") as input_file):
		# noinspection PyTypeChecker
		right_left_idxs: list[Literal[0, 1]] = \
			[1 if c == 'R' else 0 for c in input_file.readline()[:-1]]
		input_file.readline()   # skip empty line
		
		z_keys, key_nodes = process_node_lines(input_file)
	
	rl_deque = deque(right_left_idxs)
	solution_1 = nr_steps("AAA", key_nodes, rl_deque, "ZZZ")
	
	# Re-initializing the rl_deque before starting part 2 is not strictly
	# required, since the nr of steps in part 1 is (by lucky concidence) an
	# exact multiple of the (constant) nr of items in the rl_deque! We do the
	# re-init here only for the sake of completeness...
	rl_deque = deque(right_left_idxs)
	# It is NOT necessary to re-init rl_deque between different keys in part 2,
	# since the nr of steps for each key is guaranteed (by nr_steps) to be an
	# EXACT multiple of the (constant) nr of items in the rl_deque.
	factors = list(nr_steps(key, key_nodes, rl_deque) for key in z_keys)
	solution_2 = lcm(*factors)
	
	print(solution_1, solution_2)
	assert (solution_1, solution_2) == (16343, 15299095336639)


if __name__ == "__main__":
	solve()
