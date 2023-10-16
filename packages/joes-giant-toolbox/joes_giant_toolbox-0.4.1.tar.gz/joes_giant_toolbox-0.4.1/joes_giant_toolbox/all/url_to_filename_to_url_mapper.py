class url_to_filename_to_url_mapper:
    """Converts a webpage URL into a useable filename, where the URL can be recovered from the filename

    Example Usage
    -------------
    >>> mapper_obj = url_to_filename_to_url_mapper()
    >>> url = "https://www.linkedin.com/search/results/people/?currentCompany=%5B%227936%22%5D&origin=COMPANY_PAGE_CANNED_SEARCH&sid=OQs"
    >>> filename = mapper_obj.to_filename(url)
    >>> print(filename)
    https__colon____forwardSlash____forwardSlash__www__dot__linkedin__dot__com__forwardSlash__search__forwardSlash__results__forwardSlash__people__forwardSlash____questionMark__currentCompany__equalSign____percentSign__5B__percentSign__227936__percentSign__22__percentSign__5D__ampersand__origin__equalSign__COMPANY_PAGE_CANNED_SEARCH__ampersand__sid__equalSign__OQs
    >>> recover_url = mapper_obj.to_url(filename)
    >>> (recover_url == url)
    True
    """

    def __init__(self):
        self.url_to_filename_convert_char_ref = {
            ":": "__colon__",
            "&": "__ampersand__",
            "?": "__questionMark__",
            "-": "__dash__",
            ".": "__dot__",
            "~": "__tilde__",
            "/": "__forwardSlash__",
            "#": "__hash__",
            "[": "__openSquareBracket__",
            "]": "__closeSquareBracket__",
            "@": "__atSign__",
            "!": "__exclamationMark__",
            "$": "__dollarSign__",
            "'": "__apostrophe__",
            "(": "__openBracket__",
            ")": "__closeBracket__",
            "*": "__asterisk__",
            "+": "__plusSign__",
            ",": "__comma__",
            ";": "__semiColon__",
            "%": "__percentSign__",
            "=": "__equalSign__",
        }

        self.filename_to_url_convert_char_ref = {
            self.url_to_filename_convert_char_ref[k]: k
            for k in self.url_to_filename_convert_char_ref
        }

    def to_filename(self, url_str):
        for k in self.url_to_filename_convert_char_ref:
            url_str = url_str.replace(k, self.url_to_filename_convert_char_ref[k])
        return url_str

    def to_url(self, filename_str):
        for k in self.filename_to_url_convert_char_ref:
            filename_str = filename_str.replace(
                k, self.filename_to_url_convert_char_ref[k]
            )
        return filename_str
