from typing import List, Tuple
from dictionary import Dictionary
import re
import string

# 0 1 2 3 4 5 6 7 8 9

# a b c d e f g h i j k l m n o p q r s t u v w x y z
# a b c d 3 f g h i j k l m n 0 p q r 5 t u v w x y z
_COOLIFY_SUB = {
        'e' : '3',
        'o' : '0',
        's' : '5',
}

d = Dictionary()
short_to_long_form = d.TO_UNCOOL
long_to_short_form = d.TO_COOL

def split_text(text: str) -> List[str]:
    """Split the text string based on the specified delimiter and keeps the
    delimiter. It also ignores space(s) and empty string.

    params:
        text: Input string from user

    returns: List of string.
    """
    return list(filter(lambda s: s and not s.isspace(), re.split(r'([,\.\s+\?!])', text)))


def totuple(curr: Tuple[str], nextv: str) -> Tuple[str, bool]:
    """Create tuple from given tuple and a string. A boolean `True` is added
    at the end of the tuple to mark the continuation of the match.

    params:
        curr: Tuple of string and maybe at the end there's a bool
        nextv: String which will be added to the end of the tuple.

    returns: Tuple added `nextv` at the end
    """
    return (*curr[:-1], nextv, True)


def get_best_long_match(text: str, index: int) -> Tuple[bool, int, str]:
    if index >= len(text):
        raise IndexError('Out of Index')

    curr = ()
    candidates = []
    for i in range(index, len(text)):
        curr = totuple(curr, text[i].lower())

        if curr[:-1] in long_to_short_form:  # if current (not longer version) available add to a list
            candidates.append(curr[:-1])

        if not curr in long_to_short_form:
            break

    candidates.sort(key=len, reverse=True)

    if not candidates: # no candidates!
        return False, 0, None
    else:
        return True, len(candidates[0]), long_to_short_form[candidates[0]]


# FIXME: doesn't work if there's a fullstop after a word

def coolify(text: str) -> str:
    # TODO: make a generator version for this str.split() method
    text = split_text(text)
    out = []

    i = 0
    while i < len(text):
        got_match, length, value = get_best_long_match(text, i)

        if got_match:
            i += length
            out.append(value)
        else:
            out.append(text[i])  # we also need to coolify here
            i += 1

    PUNCT = set(string.punctuation)
    ret = ''.join(w if w in PUNCT else ' ' + w for w in out)
    return ret.strip()


if __name__ == '__main__':
    text = """
    I'm bored af. I can't say for sure.
    Before I started I knew nothing.
    As far as I know he won't do it.
    Be like him.
    See you tomorrow.
    are you okay?
    """
    print(split_text(text))
    print(coolify(text))
