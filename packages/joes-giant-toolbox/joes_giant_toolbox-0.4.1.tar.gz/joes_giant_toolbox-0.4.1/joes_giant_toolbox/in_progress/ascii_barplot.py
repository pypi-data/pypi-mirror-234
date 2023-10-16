def ascii_barplot(
    values_list,  # list of non-negative integers
    n_counts_per_symbol,  # each {n_counts_per_symbol} will print 1 symbol
    left_labels_list=None,  # labels to appear to left of bars
    right_labels_list=None,  # labels to appear
    symbol="|",  # symbol to use to build the bars
    baseline_value=0,  # value at which the bars start
) -> str:
    """
    a function which draws a barplot using only raw text symbols

    Parameters
    ----------
    values_list,  # list of non-negative integers

    n_counts_per_symbol,  # each {n_counts_per_symbol} will print 1 symbol

    left_labels_list=None,  # labels to appear to left of bars

    right_labels_list=None,  # labels to appear

    symbol="|",  # symbol to use to build the bars

    baseline_value=0,  # value at which the bars start

    Returns
    -------
    str
        The bar plot, exported as a multi-line string

    ## EXAMPLE USAGE ##
    import numpy as np
    from matplotlib import pyplot as plt
    random_nums = np.random.randint(10, 100, size = 10).tolist()
    print(
        ascii_barplot(
                values_list = random_nums
            ,   n_counts_per_symbol = 5
            ,   left_labels_list = [str(10**i) for i in range(len(random_nums))]
            ,   right_labels_list = [str(i) for i in random_nums]
            ,   symbol = "|"
            ,   baseline_value = 10
        )
    )
    """
    assert (
        sum([values_list[i] < baseline_value for i in range(len(values_list))]) == 0
    ), "no value can be less than the baseline value"
    symbol_vector = [
        int((i - baseline_value) // n_counts_per_symbol) * symbol for i in values_list
    ]
    if left_labels_list is None:
        left_labels_list = [""] * len(values_list)
    if right_labels_list is None:
        right_labels_list = [""] * len(values_list)

    left_label_width = max([len(i) for i in left_labels_list])
    barplot_string = ""
    for i in range(len(symbol_vector)):
        barplot_string += f"{left_labels_list[i].rjust(left_label_width)} {symbol_vector[i]} {right_labels_list[i]}\n"

    return barplot_string
