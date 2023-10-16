import re
from html5lib.filters import base


CHARS = {
    "SP": " ",
    "NBSP": "\u00A0",
    "ENSP": "\u2000",
    "EMSP": "\u2001",
    "THINSP": "\u2009",
    "NBTHINSP": "\u202F",
    "LAQUO": "\u00AB",
    "RAQUO": "\u00BB",
    "APOS": "\u0027",
    "RSQUO": "\u2019",
}


RE_APOSTROPHE_MATCH = re.compile(r"{APOS}\s*".format(**CHARS))
RE_APOSTROPHE_SUB = r"{RSQUO}".format(**CHARS)

RE_LBRAKET_MATCH = re.compile(r"([\(\[])\s*".format(**CHARS))
RE_LBRAKET_SUB = r"\1".format(**CHARS)

RE_RBRAKET_MATCH = re.compile(r"\s*([\)\]])".format(**CHARS))
RE_RBRAKET_SUB = r"\1".format(**CHARS)

RE_COMMA_OR_PERIOD_MATCH = re.compile(r"\s*([.,])".format(**CHARS))
RE_COMMA_OR_PERIOD_SUB = r"\1".format(**CHARS)

RE_COLUMN_MATCH = re.compile(r"\s*(http|https|ftp)?:".format(**CHARS))


def fix_columns(match):
    if match.group(1):
        return match.group()
    else:
        return r"{NBSP}:".format(**CHARS)


RE_PUNCT_MATCH = re.compile(r"\s*([;!\?%])".format(**CHARS))
RE_PUNCT_SUB = r"{NBTHINSP}\1".format(**CHARS)

RE_LAQUO_MATCH = re.compile(r"{LAQUO}\s*".format(**CHARS))
RE_LAQUO_SUB = r"{LAQUO}{NBTHINSP}".format(**CHARS)

RE_RAQUO_MATCH = re.compile(r"\s*{RAQUO}".format(**CHARS))
RE_RAQUO_SUB = r"{NBTHINSP}{RAQUO}".format(**CHARS)


class Filter(base.Filter):
    """
    >>> import html5lib
    >>> from html5lib.filters import sanitizer
    >>>
    >>> string = "Oui! Non  ? Regardez: un http://chien  ; un chat. 55 % 45%. Nom d'un petit bonhomme"
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
    'Oui\u202f! Non\u202f? Regardez\xa0: un http://chien\u202f; un chat. 55\u202f% 45\u202f%. Nom d\u2019un petit bonhomme'
    """

    def __iter__(self):
        for token in base.Filter.__iter__(self):
            type = token["type"]

            if type == "Characters":
                text = token["data"]

                text = RE_COLUMN_MATCH.sub(fix_columns, text)
                text = RE_COMMA_OR_PERIOD_MATCH.sub(RE_COMMA_OR_PERIOD_SUB, text)
                text = RE_PUNCT_MATCH.sub(RE_PUNCT_SUB, text)
                text = RE_LAQUO_MATCH.sub(RE_LAQUO_SUB, text)
                text = RE_RAQUO_MATCH.sub(RE_RAQUO_SUB, text)
                text = RE_LBRAKET_MATCH.sub(RE_LBRAKET_SUB, text)
                text = RE_RBRAKET_MATCH.sub(RE_RBRAKET_SUB, text)
                text = RE_APOSTROPHE_MATCH.sub(RE_APOSTROPHE_SUB, text)

                token["data"] = text

            yield token


if __name__ == "__main__":
    import doctest

    doctest.testmod()
