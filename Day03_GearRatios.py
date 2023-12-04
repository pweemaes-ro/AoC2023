"""AoC 2023 Day 3"""
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
	
	row_range: tuple[int, ...]
	col_range: tuple[int, ...]
	
	def __hash__(self) -> int:
		"""Must provide hash func, since dict key must be hashable."""
		
		return hash((self.row_range, self.col_range))


numbers_dict: TypeAlias = dict[NumberKey, tp_partnr]
symbols_dict: TypeAlias = dict[tp_coordinate, SymbolValue]


def add_symbols(line: str, line_nr: int, symbols: symbols_dict) -> None:
	"""todo: add docstr"""

	matches = finditer(r"[^.0-9\n]", line)
	for match in matches:
		coordinate = (line_nr, match.start())
		symbol = match.string[match.start():match.end()]
		symbols[coordinate] = SymbolValue(symbol, [])


def add_numbers(line: str, line_nr: int, numbers: numbers_dict) -> None:
	"""todo: add docstr"""

	matches = finditer(r"[0-9]+", line)
	for match in matches:
		
		rows_range = tuple(range(line_nr - 1, line_nr + 2))
		cols_range = tuple(range(match.start() - 1, match.end() + 1))
		number_key = NumberKey(rows_range, cols_range)
		number_value = int(match.string[match.start():match.end()])
		
		numbers[number_key] = number_value


def get_sum_of_part_nrs(numbers: numbers_dict,
                        symbols: symbols_dict) -> int:
	"""Return the sum of all part nrs. If (and only if) at the location of any
	of the s's there is a symbol, then the number is a part nr:
		sss ssss sssss
		s1s s12s s123s
		sss ssss sssss
	The symbol's connected values list is updated with the number if any of the
	s's is a '*'. (Any "*" that ends up with exactly 2 numbers in its connected
	values list is a gear.)"""
	
	parts_sum = 0

	for pos_info, value in numbers.items():

		is_part = False

		for row in pos_info.row_range:
			for col in pos_info.col_range:
				if symbol_value := symbols.get((row, col)):
					is_part = True
					if symbol_value.symbol == "*":
						symbol_value.part_nrs.append(value)

		parts_sum += value * is_part
	
	return parts_sum


def solve() -> None:
	"""Solve the problems, print the solutions and - if solutions are already
	known - verify the solutions."""

	numbers: numbers_dict = dict()
	symbols: symbols_dict = dict()

	with (open(f"Day03_input.txt") as input_file):

		for line_nr, line in enumerate(input_file):
			add_symbols(line, line_nr, symbols)
			add_numbers(line, line_nr, numbers)

	solution_1 = get_sum_of_part_nrs(numbers, symbols)
	solution_2 = sum(prod(symbol.part_nrs)
	                 for symbol in symbols.values()
	                 if symbol.symbol == "*" and len(symbol.part_nrs) == 2)

	print(solution_1, solution_2)
	assert (solution_1, solution_2) == (527369, 73074886)


if __name__ == "__main__":
	solve()
