import regex, locale
from html5lib.filters import base


PUNCT_REGEX = regex.compile(r"(\w)\s*([;:!\?%])\s*")
LAQUO_REGEX = regex.compile(r"«(\s)")
RAQUO_REGEX = regex.compile(r"(\s)»")
NOSPACEBEFORE_REGEX = regex.compile(r" ([\)\]\},])")
NOSPACEAFTER_REGEX = regex.compile(r"([\(\[\{]) ")
SPACEBEFORE_REGEX = regex.compile(r"(\w)([\(\[\{])", regex.UNICODE)
SPACEAFTER_REGEX = regex.compile(r"([\)\]\}:,])(\w)", regex.UNICODE)
DASHES_REGEX = regex.compile(r"([[:alpha:]])([–—])([[:alpha:]])", regex.UNICODE)
DASHES_THIN_REGEX = regex.compile(
    r"({})([–—])({})".format("\u202F", "\u202F"), regex.UNICODE
)


def fix_nospaces(text):
    """
    Removes spaces after:   [  (  {
    Removes spaces before:  ]  )  }  ,
    """
    text = NOSPACEBEFORE_REGEX.sub(r"\1", text)
    text = NOSPACEAFTER_REGEX.sub(r"\1", text)
    return text


def fix_punctuation(text):
    """
    Puts thin space before:   ;  :  !
    Replaces: [SPACE]?  by  [THINSP]?
    """
    text = PUNCT_REGEX.sub(r"\1\u202F\2 ", text)
    return text


def fix_quotes(text):
    """
    Replaces space with a thin space before/after French quotation mark.
    """
    text = LAQUO_REGEX.sub(r"«{}".format("\u202F"), text)
    text = RAQUO_REGEX.sub(r"{}»".format("\u202F"), text)
    return text


def fix_http(text):
    """
    Remove spaces around ":" in "http://"
    """
    return text.replace(r"http{}: //".format("\u202F"), "http://")


def fix_dashes(text):
    """
    Thin spaces around &ndash; and &mdash;
    """
    text = DASHES_REGEX.sub(r"\1{}\2{}\3".format("\u2009", "\u2009"), text)
    text = DASHES_THIN_REGEX.sub(
        r"{}\2{}".format("\u2009", "\u2009"), text
    )  # replaces non-breakable thin space by breakable thin spaces
    return text


def fix_thinspaces(text):
    """
    Replaces thin spaces with non-breakable thin spaces
    """
    return text.replace("\u2009", "\u202F")


class Filter(base.Filter):
    """
    >>> import html5lib
    >>> from html5lib.filters import sanitizer
    >>>
    >>> string = "Oui! Non  ? Regardez:  un chien  ;un chat. 55 % 45%"
    >>> dom = html5lib.parse(string, treebuilder="dom")
    >>> walker = html5lib.getTreeWalker("dom")
    >>>
    >>> stream = walker(dom)
    >>> stream = Filter(stream)
    >>>
    >>> s = html5lib.serializer.HTMLSerializer()
    >>> output = s.serialize(stream)
    >>>
    >>> print(repr(s.render(stream)))
    'Oui\u202f! Non\u202f? Regardez\u202f: un chien\u202f; un chat. 55\u202f% 45\u202f% '
    """

    def __iter__(self):
        for token in base.Filter.__iter__(self):
            type = token["type"]

            if type == "Characters":
                token["data"] = fix_punctuation(token["data"])
                token["data"] = fix_quotes(token["data"])
                token["data"] = fix_nospaces(token["data"])
                token["data"] = fix_thinspaces(token["data"])
                token["data"] = fix_http(token["data"])
                token["data"] = fix_dashes(token["data"])

            yield token


if __name__ == "__main__":
    import doctest

    doctest.testmod()
