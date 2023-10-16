import sklearn.feature_extraction.text


class RapidBagOfWordsClassifier:
    """TODO

    Example Usage
    -------------
    >>> import sklearn.datasets
    >>> X, y = sklearn.datasets.fetch_20newsgroups(
        subset="test",
        shuffle=True,
        random_state=69,
        remove=("headers", "footers", "quotes"),
        return_X_y=True,
    )
    >>> bow_classifier = RapidBagOfWordsClassifier(x=X, y=y, verbose=True, eval_code=True)
    >>> bow_classifier.tokenize_x()
    """

    def __init__(self, x, y, verbose, eval_code):
        self.global_params = {
            "verbose": verbose,
            "eval_code": eval_code,
        }
        self.data = {
            "x": x,
            "y": y,
        }
        self.sklearn_components = {
            "tokenizer": None,
            "models": {},
        }
        self.full_model_script = """
# import packages #
from sklearn.feature_extraction.text import CountVectorizer        
        """

    def tokenize_x(self, **kwargs):
        """documentation TODO"""
        self.sklearn_components[
            "tokenizer"
        ] = sklearn.feature_extraction.text.CountVectorizer(**kwargs)
