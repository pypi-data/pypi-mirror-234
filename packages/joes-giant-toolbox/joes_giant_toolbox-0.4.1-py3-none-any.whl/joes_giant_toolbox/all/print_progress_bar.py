import sys
import math


class print_progress_bar:
    """Prints a progress bar (to standard out) while code is running

    Notes
    -----
    Other printing to the standard out will interfere with the progress bar printing

    Attributes
    ----------
    base_message: str
        This text is printed to the left of the progress bar
    bar_length: int, optional (default: 50)
        The total length (number of characters) of the completed progress bar
    progress_char: str, optional (default: ".")
        The character to print within the progress bar

    Example Usage
    -------------
    >>> import time
    >>> progress_printer = print_progress_bar(base_message="running model")
    >>> for i in [x/1_000 for x in range(0,1_001)]:
    ...     progress_printer.print_progress(percent_complete=i)
    ...     time.sleep(0.05)
    running model |..................................................| 100.00%
    """

    def __init__(
        self, base_message: str, bar_length: int = 50, progress_char: str = "."
    ):
        assert len(progress_char) == 1, "len(progress_char) must equal 1"
        self.base_message = base_message
        self.bar_length = bar_length
        self.progress_char = progress_char

    def print_progress(self, percent_complete: float) -> None:
        if percent_complete >= 1.0:
            print(f"{self.base_message} |{self.progress_char*self.bar_length}| 100.00%")
        else:
            n_completed_symbols = math.floor(self.bar_length * percent_complete)
            n_incomplete_symbols = self.bar_length - n_completed_symbols
            print(
                f"{self.base_message} |{self.progress_char*n_completed_symbols}{' '*n_incomplete_symbols}| {100*percent_complete:.2f}%",
                flush=True,
                file=sys.stdout,
                end="\r",
            )
