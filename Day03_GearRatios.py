"""AoC 2023 Day 3"""
from dataclasses import dataclass
from math import prod
from re import finditer
from typing import TypeAlias

Coordinate: TypeAlias = tuple[int, int]


@dataclass
class NumberInfo:
	"""A number has a value and a flag indicating (after processing) if it is a
	part nr."""
	
	value: int
	is_part: bool


@dataclass
class SymbolInfo:
	"""A symbol consists of a string - like '*' - and a list of all connected
	part numbers, used to determine if it is a gear nr."""

	symbol: str
	part_nrs: list[int]
	
	
@dataclass
class RowColRanges:
	"""This is used as key in the numbers table. The row_range and col_range
	are (ordered and consequtive) row nrs and col nrs that must be checked to
	determine if a number is a part nr."""
	
	row_range: tuple[int, ...]
	col_range: tuple[int, ...]
	
	def __hash__(self) -> int:
		"""Must provide hash func, since dict key must be hashable."""
		
		return hash((self.row_range, self.col_range))


NumbersDict: TypeAlias = dict[RowColRanges, NumberInfo]
SymbolsDict: TypeAlias = dict[Coordinate, SymbolInfo]


def add_symbols(line: str, line_nr: int, symbols: SymbolsDict) -> None:
	"""Add an entry to the symbols table for all nrs on line. Each entry has a
	coordinate as its key. The value is a SymbolInfo consisting of a single
	char (the symbol) and an empty list (to store adjacent nrs, if any, during
	processing)."""

	matches = finditer(r"[^.0-9\n]", line)
	for match in matches:
		coordinate = line_nr, match.start()
		symbol = match.string[match.start():match.end()]
		symbols[coordinate] = SymbolInfo(symbol, [])


def add_numbers(line: str, line_nr: int, numbers: NumbersDict) -> None:
	"""Add an entry to the numbers table for all nrs on line. Each entry has a
	RowColRanges as key, consisting of a tuple with all (ordered) row nrs and a
	tuple with all (ordered) column nrs that must be verified for symbols when
	deciding if the number is a part number. The value is a NumberInfo object
	storing the value and a flag for storing whether it's a part number."""

	matches = finditer(r"[0-9]+", line)
	for match in matches:
		
		rows_range = line_nr - 1, line_nr, line_nr + 1
		cols_range = tuple(range(match.start() - 1, match.end() + 1))
		number_key = RowColRanges(rows_range, cols_range)
		number_value = int(match.string[match.start():match.end()], False)
		
		numbers[number_key] = NumberInfo(number_value, is_part=False)


def process_tables(numbers: NumbersDict, symbols: SymbolsDict) -> None:
	"""Process all data in numbers and symbols:
	1. mark numbers as part nr if they have an adjacent symbol
	2. add number to symbol's adjacent numbers if symbol = '*' (all symbol's
	   with exactly two adjacent numbers are gears)."""

	for number_key, number_info in numbers.items():

		for row in number_key.row_range:
			for col in number_key.col_range:
				if symbol_info := symbols.get((row, col)):
					numbers[number_key].is_part = True
					if symbol_info.symbol == "*":
						symbol_info.part_nrs.append(number_info.value)


def solve() -> None:
	"""Solve the problems, print the solutions and - if solutions are already
	known - verify the solutions."""

	numbers: NumbersDict = dict()
	symbols: SymbolsDict = dict()

	with (open(f"Day03_input.txt") as input_file):

		for line_nr, line in enumerate(input_file):
			add_symbols(line, line_nr, symbols)
			add_numbers(line, line_nr, numbers)
	
	process_tables(numbers, symbols)
	
	solution_1 = sum(number_info.value
	                 for number_info in numbers.values()
	                 if number_info.is_part)
	solution_2 = sum(prod(symbol_info.part_nrs)
	                 for symbol_info in symbols.values()
	                 if symbol_info.symbol == "*"
	                 and len(symbol_info.part_nrs) == 2)

	print(solution_1, solution_2)
	assert (solution_1, solution_2) == (527369, 73074886)


if __name__ == "__main__":
	solve()
