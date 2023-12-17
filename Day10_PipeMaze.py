"""AoC 2023 Day 10"""
from __future__ import annotations

from enum import Enum, IntEnum, StrEnum, auto
from math import ceil
from typing import Any, Callable, cast, TypeAlias

# todo: Put as much as possible in a dataclass enum...


class _Pipe(StrEnum):
	"""All pipe chars. DO NOT USE string literals, use Pipe enum!"""
	
	UPPER_LEFT_CORNER = "F"
	UPPER_RIGHT_CORNER = "7"
	LOWER_LEFT_CORNER = "L"
	LOWER_RIGHT_CORNER = "J"
	VERTICAL = "|"
	HORIZONTAL = "-"


class Pipe(StrEnum):
	"""All PREFERED pipe chars. DO NOT USE string literals, use Pipe enum!"""
	
	UPPER_LEFT_CORNER = "┌"
	UPPER_RIGHT_CORNER = "┐"
	LOWER_LEFT_CORNER = "└"
	LOWER_RIGHT_CORNER = "┘"
	VERTICAL = "│"
	HORIZONTAL = "─"


transform_table = \
	{k.value: v.value for k, v in zip(_Pipe, Pipe)} | {".": ".", "S": "S"}

connected_below_symbols = (Pipe.VERTICAL,
                           Pipe.UPPER_LEFT_CORNER,
                           Pipe.UPPER_RIGHT_CORNER)

connected_above_symbols = (Pipe.VERTICAL,
                           Pipe.LOWER_LEFT_CORNER,
                           Pipe.LOWER_RIGHT_CORNER)

connected__left_symbols = (Pipe.HORIZONTAL,
                           Pipe.UPPER_RIGHT_CORNER,
                           Pipe.LOWER_RIGHT_CORNER)

connected_right_symbols = (Pipe.HORIZONTAL,
                           Pipe.UPPER_LEFT_CORNER,
                           Pipe.LOWER_LEFT_CORNER)


class Direction(Enum):
	"""Each direction has as value a tuple (delta_x, delta_y), the change in
	coordinates to move to the neighbor in that direction."""
	
	UP = (0, -1)
	RIGHT = (1, 0)
	DOWN = (0, 1)
	LEFT = (-1, 0)
	NO_DIRECTION = (0, 0)


direction_opposite: dict[Direction, Direction] = \
	{Direction.UP: Direction.DOWN,
	 Direction.DOWN: Direction.UP,
     Direction.LEFT: Direction.RIGHT,
     Direction.RIGHT: Direction.LEFT,
     Direction.NO_DIRECTION: Direction.NO_DIRECTION}

NoDirections = (Direction.NO_DIRECTION, Direction.NO_DIRECTION)

Directions: TypeAlias = tuple[Direction, ...]

symbol_to_directions: dict[str, Directions] = \
	{"│": (Direction.UP, Direction.DOWN),
    "─": (Direction.LEFT, Direction.RIGHT),
    "└": (Direction.RIGHT, Direction.UP),
    "┘": (Direction.LEFT, Direction.UP),
    "┐": (Direction.LEFT, Direction.DOWN),
    "┌": (Direction.RIGHT, Direction.DOWN)}

directions_to_symbol: dict[tuple[Direction, ...], str] = \
	{v: k for (k, v) in symbol_to_directions.items()} \
	| {(v[1], v[0]): k for (k, v) in symbol_to_directions.items()}


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
		
		other_out = direction_opposite[incoming_direction]
		return self.directions[other_out == self.directions[0]]
	
	
class Matrix(list[list[Tile]]):
	"""todo: add docstring."""
	
	def __init__(self, symbol_lines: list[str]) -> None:
		
		super().__init__()
		self.s_x: int = -1
		self.s_y: int = -1
		for symbol_line in symbol_lines:
			self.__add_line(symbol_line)
		self.__set_start_directions()
		self.nr_pipes = 0
		self.nr_outside = 0
		self.nr_inside = 0
		
	def __add_line(self, line: str) -> None:
		"""Add line to the matrix (also check for and set for start
		location)."""
		
		self.append([Tile(transform_table[c]) for c in line[:-1]])

		if self.s_x == self.s_y == -1 and (x := line.find("S")) >= 0:
			self.s_x = x
			self.s_y = len(self) - 1
			self[self.s_y][self.s_x].status = Status.PIPE
			
	def __set_start_directions(self) -> None:
		"""Set the directions of the Tile at the location of "S"."""

		s_directions = []

		x = self.s_x

		y = self.s_y - 1
		if self[y][x].symbol in connected_below_symbols:
			s_directions.append(Direction.UP)
		
		y = self.s_y + 1
		if self[y][x].symbol in connected_above_symbols:
			s_directions.append(Direction.DOWN)
		
		y = self.s_y
		if len(s_directions) < 2:
			x = self.s_x + 1
			if self[y][x].symbol in connected__left_symbols:
				s_directions.append(Direction.RIGHT)
		
		if len(s_directions) < 2:
			x = self.s_x - 1
			if self[y][x].symbol in connected_right_symbols:
				s_directions.append(Direction.LEFT)
		
		self[self.s_y][self.s_x].directions = tuple(s_directions)
		self[self.s_y][self.s_x].symbol = \
			directions_to_symbol[self[self.s_y][self.s_x].directions]
	
	def _print_circuit(self, start_line: int = 0, stop_line: int = -1) -> None:

		if stop_line == -1:
			stop_line = len(self)

		for y, line in enumerate(self[start_line: stop_line]):
			for x, me in enumerate(line):
				if me.status == Status.INSIDE:
					print("1", end='')
				elif me.status == Status.PIPE:
					print(me.symbol, end='')
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
			x += exit_direction.value[0]
			y += exit_direction.value[1]
			
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
					case Pipe.UPPER_LEFT_CORNER | Pipe.UPPER_RIGHT_CORNER:
						below = not below
					case Pipe.LOWER_LEFT_CORNER | Pipe.LOWER_RIGHT_CORNER:
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
