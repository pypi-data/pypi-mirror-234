"""Units tests related to function joes_giant_toolbox.text.longest_common_substring"""

import random
import string
import joes_giant_toolbox.text


# pylint: disable=line-too-long
def generate_random_rubbish(n_chars: int) -> str:
    """Generates random characters of specified length"""
    if n_chars > len(string.printable):
        raise ValueError("n_chars cannot exceed 100")
    return "".join(random.sample(string.printable, k=n_chars))


def test_longest_common_substring():
    """check that true pattern is found"""
    str1 = f"{generate_random_rubbish(random.randint(0, 10))}aCtUaL-pAtTeRn{generate_random_rubbish(random.randint(0, 10))}"
    str2 = f"{generate_random_rubbish(random.randint(0, 10))}aCtUaL-pAtTeRn{generate_random_rubbish(random.randint(0, 10))}"
    func_output = joes_giant_toolbox.text.longest_common_substring(str1, str2)
    assert (
        func_output in str1 and func_output in str2 and "aCtUaL-pAtTeRn" in func_output
    ), "Did not find expected longest substring 'aCtUaL-pAtTeRn'"
