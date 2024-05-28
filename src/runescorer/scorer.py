from runescorer.rune import Rune
from runescorer.weight import WeightProfile

_profiles = []


def curr_score(rune: Rune) -> tuple[float, str]:
    """
    Calculates the current score of the given rune using each parsed profile.
    Returns the maximum score for the given rune as well as the name of the profile the rune scored highest with.
    :param rune: the rune to score
    :return: the max current score for the given rune as well as the name of the profile
    """
    scores = [(rune.normalized_score(profile), profile.name) for profile in _profiles]
    return max(scores, key=lambda x: x[0])


def max_score(rune: Rune) -> tuple[float, str]:
    """
    Calculates the maximum score of the given rune using each parsed profile.
    Returns the maximum score for the given rune as well as the name of the profile the rune scored highest with.
    :param rune: the rune to score
    :return: the max maximum score for the given rune as well as the name of the profile
    """
    scores = [(rune.max_normalized_score(profile), profile.name) for profile in _profiles]
    return max(scores, key=lambda x: x[0])


def min_score(rune: Rune) -> tuple[float, str]:
    """
    Calculates the minimum score of the given rune using each parsed profile.
    Returns the maximum score for the given rune as well as the name of the profile the rune scored highest with.
    The maximum score is used because it shows the "best" worst-case the rune can achieve.
    :param rune: the rune to score
    :return: the max minimum score for the given rune as well as the name of the profile
    """
    scores = [(rune.min_normalized_score(profile), profile.name) for profile in _profiles]
    return max(scores, key=lambda x: x[0])


def get_profiles() -> [WeightProfile]:
    """
    Returns all weights profiles used to evaluate runes.
    :return: all weights profiles used to evaluate runes
    """
    return _profiles


def add_profile(profile: WeightProfile) -> None:
    """
    Adds the given weight profile to the list of profiles used for rune evaluation.
    :param profile: the weight profile to add
    """
    _profiles.append(profile)
