import re
from textwrap import TextWrapper

BACKSLASH_SPACE = "__bs__"


def protect_backslash_space(text):
    return text.replace(r"\ ", BACKSLASH_SPACE)


def unprotect_backslash_space(text):
    return text.replace(BACKSLASH_SPACE, r"\ ")


wrapper = TextWrapper(break_long_words=False, width=87, break_on_hyphens=False)


def wrap(text):
    if not text:
        return text
    number_newlines_begin = 0
    while text and text[0] == "\n":
        text = text[1:]
        number_newlines_begin += 1

    number_newlines_end = 0
    while text and text[-1] == "\n":
        text = text[:-1]
        number_newlines_end += 1

    wrapped = wrapper.fill(text)

    return "\n" * number_newlines_begin + wrapped + "\n" * number_newlines_end


def remove_more_than_3_spaces(text):
    return re.sub(r"\s{3,}|\t+", "  ", text)


def remove_trailing_whitespaces(text):
    return "\n".join(line.rstrip() for line in text.split("\n"))
