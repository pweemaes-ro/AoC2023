"""AoC 2023 Day 7"""
import collections
from dataclasses import dataclass
from typing import Literal, TypeAlias

Score: TypeAlias = Literal[1, 2, 3, 4, 5, 6, 7]
frequencies_to_score: dict[tuple[int, ...], Score] = {(5,): 7,
                                                    (4, 1): 6,
                                                    (3, 2): 5,
                                                    (3, 1, 1): 4,
                                                    (2, 2, 1): 3,
                                                    (2, 1, 1, 1): 2,
                                                    (1, 1, 1, 1, 1): 1}


@dataclass(order=True)
class PokerHand:
	"""Order of fields is relevant! Default sorting will use a tuple of the
	fields in the order in which they appear in the class: (score, hand, bid)!
	('bid' will not be used, since all (score, hand) combinations are unique).
	"""
	
	score: Score    # 1 is lowest ('high card'), 7 is highest ('5 of a kind').
	hand: str       # converted so it can be used for sorting
	bid: int        # as read from file


Game: TypeAlias = list[PokerHand]
orders = ("23456789TJQKA", "J23456789TQKA")
sortables = tuple({letter: chr(ord('A') + index)
                   for (index, letter) in enumerate(order)}
                  for order in orders)


def get_transforms(hand: str) -> tuple[str, ...]:
	"""Return transformed hands for part 1 and part 2, where each card symbol
	in hand is replaced by a letter from "abcdefghijklm" according to
	its weight (which is different for each part of the problem), which allows
	for default sorting."""
	
	return tuple((''.join(sortable[c] for c in hand)
	              for sortable in sortables))


def get_scores(hand: str) -> tuple[Score, Score]:
	"""Return scores for part 1 and part 2."""

	counter = collections.Counter(hand)
	hand_frequencies = sorted(counter.values(), reverse=True)

	hand_score_1 = frequencies_to_score[tuple(hand_frequencies)]

	hand_score_2 = hand_score_1
	if (nr_jokers := counter.get('J', 0)) and nr_jokers != 5:
		# Remove the 'J' (joker) frequency and add its value to card with
		# highest frequency (this is always the first in the list). If there
		# are NO jokers ar ALL cards are jokers, hand_score is equal to
		# hand_score_1 (default value).
		hand_frequencies.remove(nr_jokers)
		hand_frequencies[0] += nr_jokers
		hand_score_2 = frequencies_to_score[tuple(hand_frequencies)]

	return hand_score_1, hand_score_2


def solve() -> None:
	"""Solve the problems, print the solutions and - if solutions are already
	known - verify the solutions."""

	games: tuple[Game, Game] = ([], [])
	solutions = [0, 0]

	with (open(f"Day07_input.txt") as input_file):
		for line in input_file.readlines():
			hand, bid = line[:-1].split(" ")
			scores = get_scores(hand)
			transforms = get_transforms(hand)
			for (score, transform, game) in zip(scores, transforms, games):
				game.append(PokerHand(score, transform, int(bid)))

	for index, game in enumerate(games):
		game.sort()
		solutions[index] = sum(rank * hand.bid
		                       for (rank, hand) in enumerate(game, start=1))

	print(solutions[0], solutions[1])
	assert (solutions[0], solutions[1]) == (253313241, 253362743)


if __name__ == "__main__":
	solve()
