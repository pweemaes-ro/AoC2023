"""AoC 2023 Day 7"""
import collections
from dataclasses import dataclass

frequencies_to_score: dict[tuple[int, ...], int] = {(5,): 7,
                                                    (4, 1): 6,
                                                    (3, 2): 5,
                                                    (3, 1, 1): 4,
                                                    (2, 2, 1): 3,
                                                    (2, 1, 1, 1): 2,
                                                    (1, 1, 1, 1, 1): 1}


@dataclass(order=True)
class PokerHand:
	"""Order of fields is relevant! Sorting will use tuple of fields in order
	they appear in the class! Sorting will therefor be on score first, and if
	equal, on hand (which is a converted string, see transform function!) hands
	are sorted correctly."""
	
	score: int      # 1 is lowest (high card), 6 is highest (5 of a kind).
	hand: str       # converted so it can be used for sorting
	bid: int        # as read from file


orders = ("23456789TJQKA", "J23456789TQKA")
sortables = tuple({letter: chr(ord('A') + index)
                   for (index, letter) in enumerate(order)}
                  for order in orders)


def get_transforms(hand: str) -> tuple[str, ...]:
	"""Return transformed hand, which has a natural ordering, since any card
	symbol in '23456789TJQKA' is replaced by the letter from 'ABCDEFGHIJKLM' at
	the same index ('2' -> 'A', '3' -> 'B', ..., 'K' -> 'L', 'A' -> 'M')."""
	
	return tuple((''.join(sortable[c] for c in hand)
	              for sortable in sortables))


def get_scores(hand: str) -> tuple[int, int]:
	"""Return score for the hand"""

	counter = collections.Counter(hand)
	hand_frequencies = sorted(counter.values(), reverse=True)

	hand_score_1 = frequencies_to_score[tuple(hand_frequencies)]

	hand_score_2 = hand_score_1
	if nr_jokers := counter.get('J', 0):
		if nr_jokers == 5:
			hand_score_2 = 7
		else:
			hand_frequencies.remove(nr_jokers)
			hand_frequencies[0] += nr_jokers
			hand_score_2 = frequencies_to_score[tuple(hand_frequencies)]

	return hand_score_1, hand_score_2


def solve() -> None:
	"""Solve the problems, print the solutions and - if solutions are already
	known - verify the solutions."""
	
	_hands: tuple[list[PokerHand], list[PokerHand]] = ([], [])
	solutions = [0, 0]

	with (open(f"Day07_input.txt") as input_file):
		for line in input_file.readlines():
			hand, bid = line[:-1].split(" ")
			scores = get_scores(hand)
			_transforms = get_transforms(hand)
			for (score, transform, hands) in zip(scores, _transforms, _hands):
				hands.append(PokerHand(score, transform, int(bid)))

	for index, hands in enumerate(_hands):
		hands.sort()
		solutions[index] = \
			sum(rank * hand.bid
			    for (rank, hand) in enumerate(hands, start=1))

	print(solutions[0], solutions[1])
	assert (solutions[0], solutions[1]) == (253313241, 253362743)


if __name__ == "__main__":
	solve()
