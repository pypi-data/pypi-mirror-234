"""This script the function joes_giant_toolbox.text.longest_common_substring"""

from difflib import SequenceMatcher


def longest_common_substring(str1: str, str2: str) -> str:
    """Identifies the longest substring appearing in both strings

    Example Usage
    -------------
    >>> import joes_giant_toolbox.text
    >>> joes_giant_toolbox.text.longest_common_substring(
    ...     "xdsfjknfgiubdljsabnfdsjoeisthebestzdfkjbieuwflbd",
    ...     "xhjfdbfmnjoeisthebestsdjkfnhbpiuqygqvqwe",
    ... )
    'joeisthebest'
    """
    match = SequenceMatcher(None, str1, str2, autojunk=False).find_longest_match(
        0, len(str1), 0, len(str2)
    )
    return str1[match.a : match.a + match.size]
