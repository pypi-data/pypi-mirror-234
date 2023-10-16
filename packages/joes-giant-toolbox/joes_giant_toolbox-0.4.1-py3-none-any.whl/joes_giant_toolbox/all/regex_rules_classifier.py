"""Defines the class 'RegexRulesClassifier', which is a multi-class text classifier using manual
regex rules"""

import random
import re
from typing import List


class RegexRulesClassifier:
    """A multi-class text classifier model using manual regex rules

    For a particular example, points are awarded to class labels based on which regex rules
    match for that example, and the class label with the highest total points is then the model
    prediction for that example.

    Refer to "Example Usage" below.

    Notes
    -----
    Unlike other popular python model packages, this model generates predictions for one
    example at a time.
    Therefore, to predict for multiple examples, multiple calls must be made to .predict() function
    e.g.
    >>> predictions: list = [
    ...     my_model.predict(example_i)
    ...     for example_i in ("example 1 text", "example 2 text", "example 3 text")
    ... ]

    Attributes
    ----------
    verbose : bool
        Whether the model should print process information while it runs

    Methods
    -------
    define_rules()
        Passes all user-defined regex rules to the model
    predict(ties_handling="first")
        Generates a single predicted class label for a single input example
    predict_scores
        Returns the total scores for all of the class labels for a single input example
    predict_proba
        Returns the normalized scores for all of the class labels for a single input example

    Example Usage
    -------------
    >>> import joes_giant_toolbox.text
    >>> clothing_gender_classifier = joes_giant_toolbox.text.RegexRulesClassifier(verbose=True)
    >>> clothing_gender_classifier.define_rules(
    ...     {
    ...         r"\\bmen": {"mens": 10}, # e.g. will not match "women"
    ...         r"(\\bbikini\\b)|(\\bskirt)|(\\bdress)": {"ladies": 10}, # must match 1+ of these
    ...         r"(\\bchild)|(\\bkid)": {"childrens": 10}, # match "child","children","kid","kids"
    ...         r"\\bgirls?\\b": {"ladies": 5, "childrens": 5},
    ...         r"\\badult": {"ladies":5, "mens":5},
    ...         r"\\bhawaiian\\b.*\\bshirt\\b": {"mens":10}, # must "hawaiian" AND "shirt"
    ...     }
    ... )
    defined 6 rules
    >>> clothing_gender_classifier.predict("girls bikini top")
    rule match: '(\bbikini\b)|(\bskirt)|(\bdress)'
            "ladies" +10
    rule match: '\bgirls?\b'
            "ladies" +5
            "childrens" +5
    'ladies'
    >>> clothing_gender_classifier.predict_scores("girls bikini top")
    ...
    {'ladies': 15, 'childrens': 5, 'mens': 0}
    >>> clothing_gender_classifier.predict_proba("girls bikini top")
    ...
    {'ladies': 0.75, 'childrens': 0.25, 'mens': 0.0}
    >>> clothing_gender_classifier.predict_scores("adults denim")
    {'ladies': 5, 'mens': 5, 'childrens': 0}
    >>> clothing_gender_classifier.predict("adults denim", ties_handling="first")
    'ladies'
    >>> clothing_gender_classifier.predict("adults denim", ties_handling="all")
    ['ladies', 'mens']
    >>> clothing_gender_classifier.predict("adults denim", ties_handling="random")
    'mens'
    >>> clothing_gender_classifier.predict("shirt", ties_handling="all")
    ['ladies', 'mens', 'childrens']
    >>> clothing_gender_classifier.predict("hawaiian patterned shirt", ties_handling="all")
    ['mens']
    """

    def __init__(self, verbose: bool = True) -> None:
        self._rules_dict: dict = {}
        self._unique_labels: tuple = ()
        self.verbose: bool = verbose

    def define_rules(self, manual_rules_dict: dict) -> None:
        """Passes all user-defined regex rules to the model

        Parameters
        ----------
        manual_rules_dict : dict
            A dictionary containing all of the regex rules
            The format of the dictionary is:
                {
                    "regex1": {
                        "class_label1": <label1_points>,
                        "class_label2": <label2_points>,
                        ...},
                    "regex2": {
                        "class_label1": <label1_points>,
                        "class_label2": <label2_points>,
                        ...}
                    ...
                }
            Refer to the examples in help(RegexRulesClassifier)
        """
        all_labels: list = []
        for k in manual_rules_dict:
            all_labels += list(manual_rules_dict[k].keys())
        self._unique_labels: tuple = tuple(set(all_labels))
        self._rules_dict = manual_rules_dict
        if self.verbose:
            print(f"defined {len(self._rules_dict)} rules")

    def __tally_label_scores(self, text_str: str) -> dict:
        """A private function which counts up the scores for each class label

        Parameters
        ----------
        text_str : str
            A single input example (text)

        Returns
        -------
        dict
            A dictionary containing the score for each possible class label
            The format of the dictionary is:
                {"label1": <label1_points>, "label2": <label2_points>, ...}
        """
        scores_dict: dict = {k: 0 for k in self._unique_labels}
        for rule in self._rules_dict:
            if re.search(rule, text_str):
                if self.verbose:
                    print(f"rule match: '{rule}'")
                for label in self._rules_dict[rule]:
                    if self.verbose:
                        print(f'\t"{label}" +{self._rules_dict[rule][label]}')
                    scores_dict[label] += self._rules_dict[rule][label]

        return scores_dict

    def predict(
        self, text_str: str, ties_handling: str = "first"
    ) -> str | List[str] | None:
        """Generates a single predicted class label for a single input example

        Parameters
        ----------
        text_str : str
            A single input example (text)
        ties_handling : str
            Tells .predict() what to do when 2 or more labels have the same total score
            One of:
                "first":    return the first class label
                "all":      return all of the tied class labels in a list
                "random":   return a random class label amongst the tied labels

        Returns
        -------
        str | List[str] | None
            Returns one of:
                * A single predicted class label (if ties_handling in ["first","random"])
                * A list of predicted class labels (if ties_handling=="all")
                * None if no class label was awarded any points (i.e. no regex matches at all)
        """
        scores_dict: dict = self.__tally_label_scores(text_str)
        if max(scores_dict.values()) == 0:
            if ties_handling == "all":
                return []
            return None
        if ties_handling == "first":
            return max(scores_dict, key=scores_dict.get)
        if ties_handling == "all":
            return [
                k for k in scores_dict if scores_dict[k] == max(scores_dict.values())
            ]
        if ties_handling == "random":
            return random.choice(
                [k for k in scores_dict if scores_dict[k] == max(scores_dict.values())]
            )
        raise ValueError("argument 'tie_handling' must be one of ['first','all']")

    def predict_scores(self, text_str: str) -> dict:
        """Returns the total scores for all of the class labels for a single input example

        Parameters
        ----------
        text_str : str
            A single input example (text)

        Returns
        -------
        dict
            A dictionary containing the score for each possible class label
            The format of the dictionary is:
                {"label1": <label1_points>, "label2": <label2_points>, ...}
        """
        scores_dict: dict = self.__tally_label_scores(text_str)
        return scores_dict

    def predict_proba(self, text_str: str) -> dict:
        """Returns the normalized scores for all of the class labels for a single input example

        The normalized scores sum to 1.0 across all of the possible class labels

        Parameters
        ----------
        text_str : str
            A single input example (text)

        Returns
        -------
        dict
            A dictionary containing the normalized score for each possible class label
            (normalized scores sum to 1.0 across all of the possible class labels)
            The format of the dictionary is:
                {"label1": <label1_density>, "label2": <label2_density>, ...}
        """
        scores_dict: dict = self.__tally_label_scores(text_str)
        return {k: scores_dict[k] / sum(scores_dict.values()) for k in scores_dict}
