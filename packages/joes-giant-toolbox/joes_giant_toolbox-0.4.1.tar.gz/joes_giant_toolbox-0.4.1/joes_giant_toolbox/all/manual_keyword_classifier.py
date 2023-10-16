import collections

manual_rule = collections.namedtuple("manual_rule", ["", ""])


class ManualKeywordClassifier:
    """A simple multi-label classifier model based on user-defined keyword rules

    Example Usage
    -------------
    >>> keyword_model = ManualKeywordClassifier()
    >>> keyword_model.add_rule()
    """

    def __init__():
        self.manual_rules = []
