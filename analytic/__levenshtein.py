from Levenshtein import *


def percentage(str1, str2):
    """Calculates the percentage similarity between two strings using Levenshtein distance."""
    # Calculate Levenshtein distance
    lev_distance = distance(str1, str2)

    # Normalize distance to get a percentage value
    if not len(str1) or not len(str2):
        return 0
    else:
        return (1 - lev_distance / max(len(str1), len(str2))) * 100
