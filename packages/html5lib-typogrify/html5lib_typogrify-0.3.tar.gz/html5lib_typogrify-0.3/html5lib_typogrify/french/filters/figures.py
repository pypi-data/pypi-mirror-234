import re
from html5lib.filters import base


CHARS = {
    "NBTHINSP": "\u202F",
}


FIGURE_REGEX = re.compile(r"\d{1,3}(.\d{3})+(,\d+)?")


def fix_figure(match):
    return match.group().replace(u".", CHARS["NBTHINSP"])


class Filter(base.Filter):
    """
    >>> import html5lib
    >>> from html5lib.filters import sanitizer
    >>>
    >>> string = "By January 1, 2008, the total population of Charleroi was 201.593."
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
    'By January 1, 2008, the total population of Charleroi was 201\u202f593.'
    """

    def __iter__(self):
        for token in base.Filter.__iter__(self):
            type = token["type"]

            if type == "Characters":
                text = token["data"]
                text = FIGURE_REGEX.sub(fix_figure, text)
                token["data"] = text

            yield token


if __name__ == "__main__":
    import doctest

    doctest.testmod()
