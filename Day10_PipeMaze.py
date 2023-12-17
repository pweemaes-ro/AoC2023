"""AoC 2023 Day 10"""
from __future__ import annotations

from enum import IntEnum, StrEnum, auto
from math import ceil
from typing import Any, Callable, cast, TypeAlias

# todo: Put as much as possible in a dataclass enum...


class Pipe(StrEnum):
	"""All pipe chars. DO NOT USE string literals, use Pipe enum!"""
	
	UL_CORNER = "F"
	UR_CORNER = "7"
	LL_CORNER = "L"
	LR_CORNER = "J"
	VERTICAL = "|"
	HORIZONTAL = "-"


class PrintablePipe(StrEnum):
	"""All PREFERED pipe chars. DO NOT USE string literals, use Pipe enum!"""

	UL_CORNER = "┌"
	UR_CORNER = "┐"
	LL_CORNER = "└"
	LR_CORNER = "┘"
	VERTICAL = "│"
	HORIZONTAL = "─"


transform_table = dict(zip(Pipe, PrintablePipe))

Direction: TypeAlias = tuple[int, int]
Directions: TypeAlias = tuple[Direction, ...]
NoDirections = ((0, 0), (0, 0))

symbol_to_directions: dict[str, Directions] = \
	{Pipe.VERTICAL: ((0, -1), (0, 1)),
	 Pipe.HORIZONTAL: ((-1, 0), (1, 0)),
	 Pipe.LL_CORNER: ((1, 0), (0, -1)),
	 Pipe.LR_CORNER: ((-1, 0), (0, -1)),
	 Pipe.UR_CORNER: ((-1, 0), (0, 1)),
	 Pipe.UL_CORNER: ((1, 0), (0, 1))}

# directions_to_symbol: dict[tuple[Direction, ...], str] = \
# 	{v: k for (k, v) in symbol_to_directions.items()} \
# 	| {(v[1], v[0]): k for (k, v) in symbol_to_directions.items()}


class LazyDirections:
	"""todo: add docstring."""
	
	def __init__(self, function: Callable[[Tile], Directions]) -> None:
		self.function = function
		self.name = function.__name__
		
	def __set_name__(self, owner: Any, name: str) -> None:
		self.name = name
	
	def __get__(self, obj: Any, parent_type: Any) -> Directions:
		obj.__dict__[self.name] = self.function(obj)
		return cast(Directions, obj.__dict__[self.name])


class Status(IntEnum):
	"""Status for a Tile."""
	
	UNKNOWN = auto()
	INSIDE = auto()
	PIPE = auto()


class Tile:
	"""The Matrix holds a list of 'lines' (lists) of Tile objects. Status is
	set to PIPE in Matrix.get_steps_to_farthest() if Tile is part of the
	closed circuit, and to OUTSIDE in Matrix.get_enclosed_tiles() if Tile is
	NOT a PIPE and NOT enclosed."""
	
	def __init__(self, symbol: str):
		self.symbol = symbol
		self.status = Status.UNKNOWN

	# NOTE: since we're only interested in directions of entries that are part
	# of the closed circuit, we do not initialize them immediately, but only
	# when really needed ('lazy' property), and then it's value is set once and
	# only once!
	@LazyDirections
	def directions(self) -> Directions:
		"""Return the directions for the symbol."""
	
		return symbol_to_directions.get(self.symbol, NoDirections)

	def get_exit_direction(self, incoming_direction: Direction) -> Direction:
		"""Given incoming connection from the incoming_direction, return the out
		direction."""
		
		other_out = (-incoming_direction[0], -incoming_direction[1])
		return self.directions[other_out == self.directions[0]]
	
	
class Matrix(list[list[Tile]]):
	"""todo: add docstring."""
	
	def __init__(self, symbol_lines: list[str]) -> None:
		
		super().__init__()
		self.s_x: int = -1
		self.s_y: int = -1
		for symbol_line in symbol_lines:
			self.__add_line(symbol_line)
		self.__update_start_tile()
		self.nr_pipes = 0
		self.nr_outside = 0
		self.nr_inside = 0
		
	def __add_line(self, line: str) -> None:
		"""Add line to the matrix (also check for and set for start
		location)."""
		
		self.append([Tile(c) for c in line[:-1]])

		if self.s_x == self.s_y == -1 and (x := line.find("S")) >= 0:
			self.s_x = x
			self.s_y = len(self) - 1
			# self[self.s_y][self.s_x].status = Status.PIPE
			
	def __get_directions(self, x: int, y: int) -> tuple[Direction]:
		directions = []

		for connected_symbols, delta_x, delta_y in (
			((Pipe.HORIZONTAL, Pipe.UL_CORNER, Pipe.LL_CORNER), -1, 0),
			((Pipe.HORIZONTAL, Pipe.UR_CORNER, Pipe.LR_CORNER), 1, 0),
			((Pipe.VERTICAL, Pipe.UL_CORNER, Pipe.UR_CORNER), 0, -1),
			((Pipe.VERTICAL, Pipe.LL_CORNER, Pipe.LR_CORNER), 0, 1)):
			neighbor_tile = self[y + delta_y][x + delta_x]
			neighbor_symbol = neighbor_tile.symbol
			if neighbor_symbol in connected_symbols:
				directions.append((delta_x, delta_y))
	
		return tuple(directions)
	
	@staticmethod
	def __get_symbol_from_directions(tile: Tile) -> str:
		
		directions_to_symbol: dict[tuple[Direction, ...], str] = \
			{v: k for (k, v) in symbol_to_directions.items()} \
			| {(v[1], v[0]): k for (k, v) in symbol_to_directions.items()}
		
		return directions_to_symbol[tile.directions]
	
	def __update_start_tile(self) -> None:
		"""Set the directions of the Tile at the location of "S"."""

		s_tile = self[self.s_y][self.s_x]

		s_tile.status = Status.PIPE
		s_tile.directions = self.__get_directions(self.s_x, self.s_y)
		s_tile.symbol = self.__get_symbol_from_directions(s_tile)
		# directions_to_symbol: dict[tuple[Direction, ...], str] = \
		# 	{v: k for (k, v) in symbol_to_directions.items()} \
		# 	| {(v[1], v[0]): k for (k, v) in symbol_to_directions.items()}
		#
		# s_tile.symbol = directions_to_symbol[s_tile.directions]
	
	def _print_circuit(self, start_line: int = 0, stop_line: int = -1) -> None:

		if stop_line == -1:
			stop_line = len(self)

		for y, line in enumerate(self[start_line: stop_line]):
			for x, me in enumerate(line):
				if me.status == Status.INSIDE:
					print("1", end='')
				elif me.status == Status.PIPE:
					print(transform_table.get(me.symbol, me.symbol), end='')
				else:
					print(' ', end='')
			print()

	def count_steps_to_farthest(self) -> int:
		"""Return the nr of steps to get to the farthest tile in the closed
		loop starting at the tile marked with 'S'."""
		
		x, y = self.s_x, self.s_y
		tile = self[y][x]
		# Take any of the two directions out of s_coordinate...
		exit_direction = tile.directions[0]
		
		self.nr_pipes = 1
		
		while True:
			x += exit_direction[0]
			y += exit_direction[1]
			
			if (x, y) == (self.s_x, self.s_y):
				return ceil(self.nr_pipes / 2)

			self.nr_pipes += 1
			
			self[y][x].status = Status.PIPE
			exit_direction = self[y][x].get_exit_direction(exit_direction)
	
	@staticmethod
	def process_line(line: list[Tile]) -> int:
		"""Set tiles that are not pipe to inside or outside. Return number of
		tiles that was set to INSIDE."""
		
		above = below = False
		nr_inside = 0
		
		for tile in line:
			if tile.status == Status.PIPE:
				match tile.symbol:
					case Pipe.VERTICAL:
						above = below = not below
					case Pipe.UL_CORNER | Pipe.UR_CORNER:
						below = not below
					case Pipe.LL_CORNER | Pipe.LR_CORNER:
						above = not above

			elif above:
				tile.status = Status.INSIDE
				nr_inside += 1
			
		return nr_inside
	
	def count_inside_tiles(self) -> int:
		"""Return total nr of INSIDE tiles."""
		
		return sum(self.process_line(line) for line in self)
	

def solve() -> None:
	"""Solve the problems, print the solutions and - if solutions are already
	known - verify the solutions."""
	
	with open(f"Day10_input.txt") as input_file:
		matrix = Matrix(input_file.readlines())
	
	solution_1 = matrix.count_steps_to_farthest()
	solution_2 = matrix.count_inside_tiles()

	print(solution_1, solution_2)
	assert (solution_1, solution_2) == (6757, 523)
	matrix._print_circuit()
	

if __name__ == "__main__":
	solve()
