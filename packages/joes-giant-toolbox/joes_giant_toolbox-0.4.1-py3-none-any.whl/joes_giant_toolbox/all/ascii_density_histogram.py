import math
from typing import List


def ascii_density_histogram(
    values_list: List[int | float],
    n_bins: int = 50,
    draw_character: str = "|",
    density_per_symbol: float = 0.005,
    label_round_n_places: int = 2,
) -> str:
    """
    Draws a histogram using raw text symbols

    [-5.2, -3.3) ||
    [-3.3, -1.4) ||||
    [-1.4, 0.5)  ||||||||
    [0.5, 2.4)   ||||||||||
    [2.4, 4.3)   ||||||||||||||||||
    [4.3, 6.2)   ||||||||||||||
    [6.2, 8.1)   ||||||||||||||||||||||||||||
    [8.1, 10.0)  ||||||||||||||||||||||||||||
    [10.0, 11.8) ||||||||||||||||||||||||||
    [11.8, 13.7) ||||||||||||||||||||||||
    [13.7, 15.6) ||||||||||||||||
    [15.6, 17.5) ||||||||||||
    [17.5, 19.4) ||||
    [19.4, 21.3) ||
    [21.3, 23.2] ||||

    Parameters
    ----------
    values_list: List[int | float]
        The vector of values whose distribution is to be represented by the histogram
    n_bins: int, optional (default: 50)
        The number of bins to use when building the histogram
    draw_character: str, optional (default: "|")
        The string character to use to draw the histogram bars
    density_per_symbol: float, optional (default: 0.005)
        The percentage of the total sample represented by each printed character in the histogram
        e.g. density_per_symbol=0.01 means that each drawn character represents 1% of the total data
    label_round_n_places: int, optional (default: 2)
        The number of places to round the printed axis bin labels to

    Returns
    -------
    str
        The histogram, returned as a multi-line string

    Example Usage
    -------------
    >>> import numpy as np
    >>> from matplotlib import pyplot as plt
    >>> sample_size=1_000_000
    >>> dbn_choices=np.random.choice(a=[1,2], size=sample_size, replace=True)
    >>> values=(
    ...     (dbn_choices==1) * np.random.normal(size=1_000_000, loc=0, scale=1).tolist() +
    ...     (dbn_choices==2) * np.random.normal(size=1_000_000, loc=10, scale=4).tolist()
    ... ).tolist()
    >>> print(
    ...     ascii_density_histogram(
    ...         values_list=values,
    ...         n_bins=25,
    ...         draw_character="|",
    ...         density_per_symbol=0.005,
    ...         label_round_n_places=1,
    ...     )
    ... )
    >>> # compare to matplotlib histogram #
    >>> plt.hist(values, bins=25)
    """
    if label_round_n_places < 0:
        raise ValueError("[label_round_n_places] must be non-negative")
    # sorted_value_list = value_list.copy()  # so as not to sort the global value_list
    # sorted_value_list.sort()
    n_samples_total: int = len(values_list)
    min_value: float | int = min(values_list)  # sorted_value_list[0]
    max_value: float | int = max(values_list)  # sorted_value_list[-1]
    bin_width: float = (max_value - min_value) / n_bins

    # calculate bin assignment for every value in values_list #
    assigned_bin_idx: list = [
        math.floor((x - min_value) / bin_width)
        if x < max_value
        else (n_bins - 1)  # put max_value into top bin
        for x in values_list
    ]

    # create a dictionary containing the bin definitions #
    bin_ref: dict = {}
    for i in range(n_bins):
        bin_ref[i] = {
            "BIN_MIN_INCL": min_value + i * bin_width,
            "BIN_MAX_EXCL": min_value + (i + 1) * bin_width,
            "n_samples_in_bin": 0,  # to be populated later
            "percent_of_total_sample": None,  # to be populated later
            "axis_label_str": None,  # to be populated later
            "drawn_bar_str": None,  # to be populated later
        }
    bin_ref[n_bins - 1]["NOTE"] = "this bin includes the maximum value in the sample"

    # populate the bins #
    for idx in assigned_bin_idx:
        bin_ref[idx]["n_samples_in_bin"] += 1

    # generate the string elements for each histogram bar #
    for bin_idx in bin_ref:
        bin_ref[bin_idx]["percent_of_total_sample"] = (
            bin_ref[bin_idx]["n_samples_in_bin"] / n_samples_total
        )
        bin_ref[bin_idx]["axis_label_str"] = (
            "["
            + f"{bin_ref[bin_idx]['BIN_MIN_INCL']:.{label_round_n_places}f}, "
            + f"{bin_ref[bin_idx]['BIN_MAX_EXCL']:.{label_round_n_places}f}"
            + ")"
        )
        bin_ref[bin_idx]["drawn_bar_str"] = draw_character * (
            math.floor(bin_ref[bin_idx]["percent_of_total_sample"] / density_per_symbol)
        )
    bin_ref[bin_idx]["axis_label_str"] = bin_ref[bin_idx]["axis_label_str"].replace(
        ")", "]"
    )  # top bin includes maximum value

    # build the histogram string #
    max_axis_label_nchars = max([len(bin_ref[k]["axis_label_str"]) for k in bin_ref])
    histogram_string = ""
    for bin_idx in bin_ref:
        histogram_string += (
            "\n"
            + f"{bin_ref[bin_idx]['axis_label_str']:<{max_axis_label_nchars+1}}"
            + bin_ref[bin_idx]["drawn_bar_str"]
        )

    return histogram_string
