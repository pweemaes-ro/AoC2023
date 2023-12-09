"""AoC 2023 Day 5"""
from __future__ import annotations

from dataclasses import dataclass
from re import findall
from typing import TextIO


@dataclass(order=True)
class Interval:
	"""An Interval has a first and last int. These and all integers in between
	are in the interval."""
	
	first: int
	last: int
	

@dataclass(order=True)
class MapLine:
	"""A map line has an interval and an offset (by which to adjust all
	source_nrs that are in the interval)."""
	
	interval: Interval
	offset: int    # add this to each source in interval to get destination.


class ConversionMap:
	"""A conversion map has a SORTED list of MapLine objects that describe how
	to convert source_nrs that fall in a MapLine's interval."""
	
	def __init__(self, map_lines: list[MapLine]):
		self.map_lines = map_lines
		map_lines.sort()
	
	@staticmethod
	def get_before(interval: Interval, map_interval: Interval) \
		-> Interval | None:
		"""Return the part of interval that's before map_interval (or None)."""
		
		if interval.first < map_interval.first:
			return Interval(interval.first,
			                min(interval.last, map_interval.first - 1))
		return None
	
	@staticmethod
	def get_overlap(interval: Interval, map_interval: Interval, offset: int) \
		-> Interval:
		"""Return the part of interval that's in map_interval. Assumes there is
		an overlap between interval and map_interval!"""

		return Interval(
			max(map_interval.first, interval.first) + offset,
			min(map_interval.last, interval.last) + offset)
		
	@staticmethod
	def get_after(interval: Interval, map_interval: Interval) \
		-> Interval | None:
		"""Return the part of interval that's afte  map_interval (or None)."""

		if interval.last > map_interval.last:
			return Interval(map_interval.last + 1, interval.last)
		return None
	
	def get_interval_parts(self, interval: Interval, map_line: MapLine) \
		-> tuple[Interval | None, Interval | None, Interval | None]:
		"""Return the part before, the part (adjusted!) overlapping and the
		part after map_line's interval. Missing parts are returned as None."""
		
		map_interval = map_line.interval
		
		if interval.first > map_interval.last:
			return None, None, interval
		
		before = self.get_before(interval, map_interval)

		overlap = None
		if before is None or before != interval:
			overlap = self.get_overlap(interval, map_interval, map_line.offset)

		after = self.get_after(interval, map_interval)
		
		return before, overlap, after
	
	def _get_destination_intervals(self, interval: Interval) -> \
		tuple[list[Interval], Interval | None]:

		destinations = []
		for map_line in self.map_lines:
			
			before, _in, after = self.get_interval_parts(interval, map_line)

			if after == interval:
				continue
				
			if before:
				destinations.append(before)

			if _in:
				destinations.append(_in)

			return destinations, after
			
		return [interval], None

	def get_destination_intervals(self, source_intervals: list[Interval]) \
		-> list[Interval]:
		"""Return sorted list of destination intervals for source intervals."""
		
		all_destinations = []
		
		for interval in source_intervals:
			
			destinations, after = self._get_destination_intervals(interval)
			all_destinations.extend(destinations)
		
			while after:
				destinations, after = self._get_destination_intervals(after)
				all_destinations.extend(destinations)

		all_destinations.sort()
		return all_destinations
	
	def get_destination(self, source: int) -> int:
		"""Return the destination of the source."""
		
		for map_line in self.map_lines:
			if source > map_line.interval.last:
				continue
			if map_line.interval.first <= source <= map_line.interval.last:
				return source + map_line.offset
			return source
		
		return source
	
	def get_destinations(self, source_nrs: list[int]) -> list[int]:
		"""Return list of destinations for all source_nrs."""
		
		return [self.get_destination(source) for source in source_nrs]


def get_conversion_table(input_file: TextIO) -> ConversionMap:
	"""Return a ConversionMap object loaded with conversion map data from
	the input file."""
	
	map_lines = []
	while len(line := input_file.readline()) > 1:
		destination, _start, length = (map(int, findall(r"[0-9]+", line)))
		map_line = MapLine(Interval(_start, _start + length - 1),
		                   destination - _start)
		map_lines.append(map_line)
	
	return ConversionMap(map_lines)


def get_sorted_seed_intervals(seed_nrs: list[int]) -> list[Interval]:
	"""Return list of intervals derived from a list of seed nrs."""
	
	seed_nrs_iterator = iter(seed_nrs)
	seeds_as_tuples = [*zip(seed_nrs_iterator, seed_nrs_iterator)]
	seed_intervals = [Interval(start, start + length - 1)
	                  for (start, length) in seeds_as_tuples]
	seed_intervals.sort()
	return seed_intervals


def get_seed_nrs(line: str) -> list[int]:
	"""Return a list of seed nrs from the line."""
	
	return [*map(int, findall(r"[0-9]+", line))]


def solve() -> None:
	"""Solve the problems, print the solutions and - if solutions are already
	known - verify the solutions."""
	
	with (open(f"Day05_input.txt") as input_file):
		source_nrs = get_seed_nrs(input_file.readline())
		source_intervals = get_sorted_seed_intervals(source_nrs)
		
		input_file.readline()  # skip empty conversion_interval
		
		while input_file.readline():   # skip header line
			ct = get_conversion_table(input_file)
			source_nrs = ct.get_destinations(source_nrs)
			source_intervals = ct.get_destination_intervals(source_intervals)

	solution_1 = min(source_nrs)
	solution_2 = source_intervals[0].first
	
	print(solution_1, solution_2)
	assert (solution_1, solution_2) == (910845529, 77435348)
	

if __name__ == "__main__":
	solve()
