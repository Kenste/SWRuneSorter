from typing import Callable

from src.runescorer.rune import Rune


def AND(*conditions: Callable[[Rune], bool]) -> Callable[[Rune], bool]:
    return lambda rune: all(condition(rune) for condition in conditions)

def OR(*conditions: Callable[[Rune], bool]):
    return lambda rune: any(condition(rune) for condition in conditions)

def NOT(condition: Callable[[Rune], bool]):
    return lambda rune: not condition(rune)

def AtLeast(n: int, *conditions: Callable[[Rune], bool]) -> Callable[[Rune], bool]:
    def check(rune):
        count = 0
        for condition in conditions:
            count += condition(rune)
            if count >= n:
                return True  # Short-circuit when enough conditions are met
        return False  # Not enough conditions met
    return check