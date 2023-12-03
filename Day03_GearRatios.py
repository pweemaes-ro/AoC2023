"""AoC 2023 Day 2"""
from dataclasses import dataclass
from math import prod
from re import finditer
from typing import TypeAlias

tp_coordinate: TypeAlias = tuple[int, int]
tp_partnr: TypeAlias = int


@dataclass
class SymbolValue:
	"""A symbol consists of a string - like '*' - and a list of all connected
	part numbers."""

	symbol: str
	part_nrs: list[int]
	
	
@dataclass
class NumberKey:
	"""A number key holds the ranges for the rows and a cols that are relevant
	for checking for symbols."""
	
	row_range: range
	col_range: range
	
	def __hash__(self) -> int:
		"""Must provide hash func, since dict key must be hashable."""
		
		return hash((self.row_range, self.col_range))


numbers_dict: TypeAlias = dict[NumberKey, tp_partnr]
symbols_dict: TypeAlias = dict[tp_coordinate, SymbolValue]


def add_symbols(line: str, line_nr: int, symbols: symbols_dict) -> None:
	"""todo: add docstr"""

	matches = finditer(r"[^.0-9\n]", line)
	for match in matches:
		symbols[(line_nr, match.start())] = \
			SymbolValue(match.string[match.start():match.end()], [])


def add_numbers(line: str, line_nr: int, numbers: numbers_dict) -> None:
	"""todo: add docstr"""

	matches = finditer(r"[0-9]+", line)
	for match in matches:
		number_key = NumberKey(range(line_nr - 1, line_nr + 2),
		                       range(match.start() - 1, match.end() + 1))
		numbers[number_key] = int(match.string[match.start():match.end()])


def get_sum_of_connected_part_nrs(numbers: numbers_dict,
                                  symbols: symbols_dict) -> int:
	"""todo: add docstr, clean up"""

	parts_sum = 0

	for pos_info, value in numbers.items():

		is_part = False
		for row in pos_info.row_range:
			for col in pos_info.col_range:
				if symbol_value := symbols.get((row, col)):
					is_part = True
					if symbol_value.symbol == "*":
						symbol_value.part_nrs.append(value)
					break

			if is_part:
				parts_sum += value
				break
	
	return parts_sum


def solve() -> None:
	"""Solve the problems, print the solutions and - if solutions are already
	known - verify the solutions."""

	numbers: numbers_dict = dict()
	symbols: symbols_dict = dict()

	line_nr = 0
	with (open(f"Day03_input.txt") as input_file):
		while line := input_file.readline():
			add_symbols(line, line_nr, symbols)
			add_numbers(line, line_nr, numbers)
			line_nr += 1

	solution_1 = get_sum_of_connected_part_nrs(numbers, symbols)
	solution_2 = sum(prod(symbol.part_nrs)
	                 for symbol in symbols.values()
	                 if symbol.symbol == "*" and len(symbol.part_nrs) == 2)

	print(solution_1, solution_2)
	assert (solution_1, solution_2) == (527369, 73074886)


if __name__ == "__main__":
	solve()
