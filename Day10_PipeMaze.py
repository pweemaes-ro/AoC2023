"""AoC 2023 Day 10"""
from enum import IntEnum, StrEnum, auto
from math import ceil
from typing import TypeAlias


class Pipe(StrEnum):
	"""All pipe chars. DO NOT USE string literals, use Pipe enum!"""
	
	UL_CORNER = "F"
	UR_CORNER = "7"
	LL_CORNER = "L"
	LR_CORNER = "J"
	VERTICAL = "|"
	HORIZONTAL = "-"


Direction: TypeAlias = tuple[int, int]
Directions: TypeAlias = tuple[Direction, Direction]

pipe_to_directions: dict[str, Directions] = \
	{Pipe.VERTICAL: ((0, -1), (0, 1)),
	 Pipe.HORIZONTAL: ((-1, 0), (1, 0)),
	 Pipe.LL_CORNER: ((1, 0), (0, -1)),
	 Pipe.LR_CORNER: ((-1, 0), (0, -1)),
	 Pipe.UR_CORNER: ((-1, 0), (0, 1)),
	 Pipe.UL_CORNER: ((1, 0), (0, 1))}


class TileStatus(IntEnum):
	"""TileStatus for a Tile."""
	
	INSIDE = auto()
	PIPE = auto()


class Tile:
	"""The Matrix holds a list of 'lines' (lists) of Tile objects. Status is
	set to PIPE in Matrix.get_steps_to_farthest() if Tile is part of the
	closed circuit."""
	
	def __init__(self, symbol: str):
		self.symbol = symbol
		self.status: TileStatus | None = None
		self._directions: Directions | None = None

	@property
	def directions(self) -> Directions:
		"""This is calculated only once, when requested, and never changes.
		Assumes tile has a pipe symbol!"""
		
		if not self._directions:
			self._directions = pipe_to_directions[self.symbol]
		return self._directions
	
	@directions.setter
	def directions(self, directions: Directions) -> None:
		self._directions = directions
	
	def get_exit_direction(self, incoming_direction: Direction) -> Direction:
		"""Given a connection coming in from incoming direction, return the
		direction of the tile's exit. Example: Suppose tile has connections in
		the directions left and up. If a connection comes in with direction
		down, it is connecting to the tile's up connection. The exit direction
		is then the tile's other direction: left."""
		
		other_out = (-incoming_direction[0], -incoming_direction[1])
		return self.directions[other_out == self.directions[0]]
	
	
class Matrix(list[list[Tile]]):
	"""A Matrix holds a collection of lines of tiles. It also has functions to
	solve the problem."""

	line_symbols: dict[str, str] = dict()
	directions_to_symbol: dict[tuple[Direction, Direction], str] = \
		{v: k for (k, v) in pipe_to_directions.items()} \
		| {(v[1], v[0]): k for (k, v) in pipe_to_directions.items()}
	
	def __init__(self, symbol_lines: list[str], printable: bool = False) \
		-> None:
		
		super().__init__()
		self.s_x: int = -1
		self.s_y: int = -1
		for symbol_line in symbol_lines:
			self.__add_line(symbol_line)
		self.__update_start_tile()
		if printable:
			class PrintablePipe(StrEnum):
				"""Use these chars to make a nice print of the loop."""
				
				UL_CORNER = "┌"
				UR_CORNER = "┐"
				LL_CORNER = "└"
				LR_CORNER = "┘"
				VERTICAL = "│"
				HORIZONTAL = "─"
			
			self.line_symbols = dict(zip(Pipe, PrintablePipe))
			
	def __add_line(self, line: str) -> None:
		"""Add line to the matrix (also check for and set for start
		location)."""
		
		self.append([Tile(c) for c in line])

		if self.s_x == self.s_y == -1 and (x := line.find("S")) >= 0:
			self.s_x = x
			self.s_y = len(self) - 1
			
	def __get_s_directions(self) -> Directions:
		"""Return directions of 'S'-tile, given pipes of its neighores."""
		
		directions = []

		for connected_symbols, delta_x, delta_y in (
			((Pipe.HORIZONTAL, Pipe.UL_CORNER, Pipe.LL_CORNER), -1, 0),
			((Pipe.HORIZONTAL, Pipe.UR_CORNER, Pipe.LR_CORNER), 1, 0),
			((Pipe.VERTICAL, Pipe.UL_CORNER, Pipe.UR_CORNER), 0, -1),
			((Pipe.VERTICAL, Pipe.LL_CORNER, Pipe.LR_CORNER), 0, 1)):
			neighbor_tile = self[self.s_y + delta_y][self.s_x + delta_x]
			neighbor_symbol = neighbor_tile.symbol
			if neighbor_symbol in connected_symbols:
				directions.append((delta_x, delta_y))
	
		return directions[0], directions[1]
	
	def __get_s_pipe(self) -> str:
		"""Return the pipe for the start location, given its directions."""
		
		tile = self[self.s_y][self.s_x]
		return self.directions_to_symbol[tile.directions]
	
	def __update_start_tile(self) -> None:
		"""Set the status, directions and symbol of the 'S'-tile."""

		s_tile = self[self.s_y][self.s_x]

		s_tile.status = TileStatus.PIPE
		s_tile.directions = self.__get_s_directions()
		s_tile.symbol = self.__get_s_pipe()
	
	def print_circuit(self, start_line: int = 0, stop_line: int = -1) -> None:
		"""Prints the circuit. Inner tiles will only be distinguishable if
		printable=True when creating the matrix."""
		
		if stop_line == -1:
			stop_line = len(self)

		for y, line in enumerate(self[start_line: stop_line]):
			for x, me in enumerate(line):
				if me.status == TileStatus.INSIDE:
					print("█", end='')  # █ = alt-219
				elif me.status == TileStatus.PIPE:
					if self.line_symbols:
						pipe = self.line_symbols.get(me.symbol, me.symbol)
					else:
						pipe = me.symbol
					print(pipe, end='')
				else:
					print(' ', end='')
			print()

	def count_steps_to_farthest(self) -> int:
		"""Return the nr of steps to get to the farthest tile in the closed
		loop starting at the tile marked with 'S'."""
		
		x, y = self.s_x, self.s_y
		direction = self[y][x].directions[1]  # directions[0] should also work!
		nr_pipes = 1    # 'S' is a pipe!
		
		while True:
			x, y = x + direction[0], y + direction[1]
			
			if (x, y) == (self.s_x, self.s_y):
				return ceil(nr_pipes / 2)

			nr_pipes += 1
			tile = self[y][x]
			tile.status = TileStatus.PIPE
			direction = tile.get_exit_direction(direction)

	@staticmethod
	def process_line(line: list[Tile], printable: bool = False) -> int:
		"""Set status for tiles on line that are inside the closed loop to
		TileStatus.INSIDE. Return number of tiles that was set."""
		
		inside_above = inside_below = False
		nr_inside = 0
		
		for tile in line:
			if tile.status == TileStatus.PIPE:
				match tile.symbol:
					case Pipe.VERTICAL:
						inside_above = inside_below = not inside_below
					case Pipe.UL_CORNER | Pipe.UR_CORNER:
						inside_below = not inside_below
					case Pipe.LL_CORNER | Pipe.LR_CORNER:
						inside_above = not inside_above

			elif inside_above:
				# assert inside_below == inside_above
				if printable:
					tile.status = TileStatus.INSIDE   # required for printing...
				nr_inside += 1
			
		return nr_inside
	
	def count_inside_tiles(self) -> int:
		"""Return total nr of INSIDE tiles."""
		
		return sum(self.process_line(line, bool(self.line_symbols))
		           for line in self)
	

def solve() -> None:
	"""Solve the problems, print the solutions and - if solutions are already
	known - verify the solutions."""
	
	with open(f"Day10_input.txt") as input_file:
		matrix = Matrix(input_file.readlines(), printable=True)
	
	solution_1 = matrix.count_steps_to_farthest()
	solution_2 = matrix.count_inside_tiles()

	print(solution_1, solution_2)
	assert (solution_1, solution_2) == (6757, 523)
	matrix.print_circuit()


if __name__ == "__main__":
	solve()
