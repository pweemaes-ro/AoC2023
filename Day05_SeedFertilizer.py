"""AoC 2023 Day 5"""
from __future__ import annotations

from dataclasses import dataclass
from re import findall
from typing import TextIO


# todo: This could be done slightly more efficient if you use a bisect (a list
#       that is automagically always sorted after an item is added or deleted.
#       Then you could iterate over de sorted intervals and the Map's MapLines
#       in one loop, moving forward by incrementing index of Map's Maplines.
#       You'd have to remove processed intervals from the bisect list and work
#       with the first item until the list is empty, since otherwise you'd get
#       in trouble iterating over a list that's modified inside the loop. Also
#       you'd have to put the resulting destination intervals in a bisect list.

@dataclass(order=True)
class Interval:
	"""An Interval is bounded by a first and last integer. These and all
	integers in between are in the interval."""

	first: int
	last: int


@dataclass(order=True)
class MapLine:
	"""A map line has an interval and an offset (by which to adjust all sources
	that fall within the interval)."""
	
	interval: Interval
	offset: int    # add this to each source in interval to get destination.


class Map:
	"""A map has a SORTED list of MapLine object, and functionality to perform
	the conversion of sources using the Mapline objects."""
	
	def __init__(self, map_lines: list[MapLine]):
		"""map lines MUST be sorted ascending!"""
		map_lines.sort()
		self.map_lines = map_lines
	
	@staticmethod
	def _get_before(interval: Interval, map_interval: Interval) \
		-> Interval | None:
		"""Return the part of interval that's before map_interval (or None)."""
		
		if interval.first < map_interval.first:
			return Interval(interval.first,
			                min(interval.last, map_interval.first - 1))
		return None
	
	@staticmethod
	def _get_in(interval: Interval, map_interval: Interval, offset: int) \
		-> Interval | None:
		"""Return the part of interval that's in map_interval (or None)."""

		candidate = Interval(max(interval.first, map_interval.first),
		                     min(interval.last, map_interval.last))
		if candidate.first > candidate.last:
			return None
		else:
			candidate.first += offset
			candidate.last += offset
			return candidate
		
	@staticmethod
	def _get_after(interval: Interval, map_interval: Interval) \
		-> Interval | None:
		"""Return the part of interval that's after map_interval (or None)."""

		if interval.last <= map_interval.last:
			return None
		else:
			return Interval(max(interval.first, map_interval.last + 1),
			                interval.last)
	
	def _get_interval_parts(self, interval: Interval, map_line: MapLine) \
		-> tuple[Interval | None, Interval | None, Interval | None]:
		"""Return the part before, the ADJUSTED part in and the part after
		map_line's interval. Missing parts are returned as None."""
		
		after = self._get_after(interval, map_line.interval)
		if after and after == interval:
			return None, None, after
		
		before = self._get_before(interval, map_line.interval)
		if before and before.last == interval.last:
			return before, None, after
		
		_in = self._get_in(interval, map_line.interval, map_line.offset)
		
		return before, _in, after

	def convert_intervals(self, source_intervals: list[Interval]) \
		-> list[Interval]:
		"""Return a list of destination intervals for source_intervals."""
		
		destination_intervals = []
		
		while source_intervals:

			interval = source_intervals.pop()

			for map_line in self.map_lines:
				
				before, _in, after = \
					self._get_interval_parts(interval, map_line)
				
				if interval == after:
					continue

				if before:
					destination_intervals.append(before)
				
				if _in:
					destination_intervals.append(_in)
				
				if after:
					source_intervals.append(after)

				break

			else:
				destination_intervals.append(interval)
		
		return destination_intervals
	
	def _get_destination(self, source: int) -> int:
		"""Return the destination of the source."""
		
		for map_line in self.map_lines:
			if source > map_line.interval.last:
				continue
			if map_line.interval.first <= source:
				# source <= map_line.interval.last implied from above
				return source + map_line.offset
			return source
		
		return source
	
	def convert_nrs(self, source_nrs: list[int]) -> list[int]:
		"""Return list of destinations for all source_nrs."""
		
		return [self._get_destination(source) for source in source_nrs]


def get_map_lines(input_file: TextIO) -> Map | None:
	"""Return a Map object loaded with map lines from input file."""
	
	if not input_file.readline():   # no xxx-to-yyy line anymore
		return None

	map_lines = []
	
	while len(line := input_file.readline()) > 1:
		destination, first, length = map(int, findall(r"[0-9]+", line))
		interval = Interval(first, first + length - 1)
		map_lines.append(MapLine(interval, destination - first))

	return Map(map_lines)


def get_seed_intervals(seed_nrs: list[int]) -> list[Interval]:
	"""Return list of intervals derived from a list of seed nrs."""

	seed_nrs_iterator = iter(seed_nrs)
	seeds_as_start_length = [*zip(seed_nrs_iterator, seed_nrs_iterator)]
	return [Interval(start, start + length - 1)
	                  for (start, length) in seeds_as_start_length]


def solve() -> None:
	"""Solve the problems, print the solutions and - if solutions are already
	known - verify the solutions."""
	
	with (open(f"Day05_input.txt") as input_file):

		source_nrs = [*map(int, findall(r"[0-9]+", input_file.readline()))]
		source_intervals = get_seed_intervals(source_nrs)

		input_file.readline()  # skip empty conversion_interval
		
		while map_lines := get_map_lines(input_file):
			source_nrs = map_lines.convert_nrs(source_nrs)
			source_intervals = map_lines.convert_intervals(source_intervals)
	
	solution_1 = min(source_nrs)
	solution_2 = min(interval.first for interval in source_intervals)
	
	print(solution_1, solution_2)
	assert (solution_1, solution_2) == (910845529, 77435348)
	

if __name__ == "__main__":
	solve()
