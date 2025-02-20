from typing import Callable

from runescorer.rune import Rune


def AND(*conditions: Callable[[Rune], bool]) -> Callable[[Rune], bool]:
    return lambda rune: all(condition(rune) for condition in conditions)

def OR(*conditions: Callable[[Rune], bool]):
    return lambda rune: any(condition(rune) for condition in conditions)

def NOT(condition: Callable[[Rune], bool]):
    return lambda rune: not condition(rune)