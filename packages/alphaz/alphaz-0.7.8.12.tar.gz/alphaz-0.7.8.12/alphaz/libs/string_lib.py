import re, string, chardet, unicodedata, encodings, warnings

import hashlib


def is_number(txt: str) -> bool:
    """
    Check if a string is a number.

    Args:
        txt: The string to check.

    Returns:
        True if the string is a number, False otherwise.
    """
    try:
        a = float(txt)
        return True
    except ValueError:
        return False


def is_upper(word: str) -> bool:
    """
    Check if a string is all uppercase.

    Args:
        word: The string to check.

    Returns:
        True if the string is all uppercase, False otherwise.
    """
    return all(c in string.ascii_uppercase for c in word)


def sort_words(words_dict: dict) -> dict:
    """
    Sort a dictionary of words by their count in descending order.

    Args:
        words_dict: A dictionary of words and their count.

    Returns:
        A sorted dictionary of words and their count in descending order.
    """
    return {
        x[0]: x[1]
        for x in sorted(words_dict.items(), key=lambda item: item[1], reverse=True)
    }


def is_carac(test: str) -> bool:
    """
    Check if a string contains special characters.

    Args:
        test: The string to check.

    Returns:
        True if the string contains special characters, False otherwise.
    """
    return re.search(r"[@_!#$%^&*()<>?/\|}{~:]", test) is not None


def get_words(txt: str) -> list[str]:
    """
    Extract words from text and filter out noise.

    The function removes parentheses and their contents, and then filters out words that contain specific characters
    or are on a list of common but meaningless words.

    Args:
        txt: A string representing the text to extract words from.

    Returns:
        A list of strings representing the words extracted from the text.
    """
    # Remove parentheses and their contents
    txt = re.sub(r"\([^()]*\)", "", txt)

    # Split text into words
    words = txt.split()

    # Filter out noise
    noise = ["+", "-", "'", ",", ";", "<", ">", "·", "[", "est", "le", "des", "les"]
    words_out = []
    for x in words:
        x = x.lower()
        if any(c in x for c in noise):
            continue
        if "." in x and not is_number(x):
            continue
        if len(x) <= 2 or is_number(x):
            continue
        words_out.append(x)
    return words_out


"""
def universal_decode(txt, encodings_methods=[], blacklist=[]):
    encodings_methods.extend(list(set(encodings.aliases.aliases.values())))

    result = txt
    for encoding_method in encodings_methods:
        if encoding_method not in blacklist:
            try:
                result = txt.decode(encoding_method)
                return result
            except:
                pass
    return result


def universal_decodes(txt, encodings_methods=[], blacklist=[]):
    encodings_methods.extend(list(set(encodings.aliases.aliases.values())))

    results = {}
    for encoding_method in encodings_methods:
        if encoding_method not in blacklist:
            try:
                results[encoding_method] = txt.decode(encoding_method)
            except:
                pass
    return results
"""


def universal_decode(txt: bytes) -> tuple[str, str]:
    """
    Decode bytes using the detected encoding.

    This function attempts to decode the given bytes using the detected encoding,
    which is determined using the `detect` method from the `chardet` library.

    Args:
        txt: The bytes to decode.

    Returns:
        A tuple containing the decoded text and the detected encoding.
    """
    result = txt
    encoding = chardet.detect(txt)["encoding"]
    try:
        result = txt.decode(encoding)
    except:
        pass
    return result, encoding


def universal_decodes(txts: list[bytes]) -> dict[str, str]:
    """
    Decode a list of bytes using the detected encoding for each.

    This function attempts to decode each of the given bytes using the detected encoding,
    which is determined using the `detect` method from the `chardet` library.

    Args:
        txts: A list of bytes to decode.

    Returns:
        A dictionary containing the detected encoding and the corresponding decoded text for each byte.
    """
    results = {}
    for txt in txts:
        encoding = chardet.detect(txt)["encoding"]
        try:
            results[encoding] = txt.decode(encoding)
        except:
            pass
    return results


def python_case(txt: str) -> str:
    """
    Convert a string to snake case.

    This function converts a string to snake case by replacing spaces with underscores
    and removing all non-alphanumeric characters except for periods and underscores.

    Args:
        txt: The string to convert.

    Returns:
        The string in snake case.
    """
    txt = txt.replace(" ", "_")
    txt = re.sub("[^a-zA-Z0-9_ \n\.]", "", txt)
    return txt.lower()


def pascal_case(txt: str) -> str:
    """
    Convert a string to PascalCase format.

    Args:
        txt: The string to convert.

    Returns:
        A string in PascalCase format.
    """
    if not isinstance(txt, str):
        raise TypeError("The input argument must be a string.")

    return re.sub(r"(^|_)([a-z])", lambda m: m.group(2).upper(), txt)


def camel_case(txt: str) -> str:
    """
    Convert a string to camelCase format.

    Args:
        txt: The string to convert.

    Returns:
        A string in camelCase format.
    """
    if not isinstance(txt, str):
        raise TypeError("The input argument must be a string.")

    parts = txt.split("_")
    return parts[0] + "".join(x.title() for x in parts[1:])


def levenshtein(mot1: str, mot2: str) -> int:
    """
    Compute the Levenshtein distance between two strings.

    The Levenshtein distance is the minimum number of single-character edits (insertions, deletions or substitutions)
    required to change one string into the other.

    Args:
        mot1: The first string.
        mot2: The second string.

    Returns:
        The Levenshtein distance between the two strings.
    """
    if not isinstance(mot1, str) or not isinstance(mot2, str):
        raise TypeError("The input arguments must be strings.")

    m, n = len(mot1), len(mot2)
    d = [[0] * (n + 1) for i in range(m + 1)]

    for i in range(1, m + 1):
        d[i][0] = i
    for j in range(1, n + 1):
        d[0][j] = j

    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if mot1[i - 1] == mot2[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min(d[i - 1][j], d[i][j - 1], d[i - 1][j - 1]) + 1

    return d[m][n]


def found_best_match(
    word: str, words: list[str], threshold: float = None
) -> tuple[str, float]:
    """
    Find the word in a list of words that has the best match with a given word.

    The match is calculated as the ratio between the number of letters that match and the difference in length between
    the two words. The resulting match values are compared and the word with the highest match value is returned.

    Args:
        word: The word to compare.
        words: The list of words to search for the best match.
        threshold: The minimum match value required for a match to be considered valid. If no match meets this threshold,
            None is returned.

    Returns:
        A tuple containing the best matching word and its match value.

    """
    if len(words) == 0:
        return None, 0.0
    match_values = [
        (word in w) / abs(len(word) - len(w) if len(word) != len(w) else 0.5)
        for w in words
    ]
    max_value = max(match_values)
    if threshold is not None and max_value < threshold:
        return None, max_value
    return words[match_values.index(max_value)], max_value


def to_list(o: str) -> list[str]:  # TODO delete ?
    """
    Convert a string representation of a list to a list of strings.

    The input string should be a comma-separated list of values, optionally enclosed in square brackets. String values
    may be enclosed in either single or double quotes.

    Args:
        o: The string to convert to a list.

    Returns:
        A list of string values.

    """
    if o is None:
        return []
    if isinstance(o, list):
        return o
    if len(o) == 0:
        return []
    if len(o) < 2:
        return [o]
    if o[0] == "[" and o[-1] == "]":
        o = o[1:-1]
    output = []
    for el in o.split(","):
        el = el.strip()
        if el.startswith(("'", '"')):
            el = el[1:]
        if el.endswith(("'", '"')):
            el = el[:-1]
        output.append(el)
    return output


def str_to_str_list(input_str: str, separators: list[str] | None = None) -> list[str]:
    if separators is None:
        separators = [",", ";"]
    # Check if the input string is "[]"
    if input_str == "[]":
        return []

    # Remove outer brackets if present
    input_str = re.sub(r"^\[(.+)\]$", r"\1", input_str)

    # Split on "," or ";" if present, otherwise return the original string
    if "," in input_str or ";" in input_str:
        return re.split("|".join(separators), input_str)
    elif input_str == "":
        return []
    else:
        return [input_str]


def escape_ansi(line: str) -> str:
    """
    Remove ANSI escape codes from a string.

    Args:
        line: A string that may contain ANSI escape codes.

    Returns:
        A string with the ANSI escape codes removed.
    """
    ansi_escape = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]")
    return ansi_escape.sub("", str(line))

    # def remove_accents(old):
    """
    Removes common accent characters, lower form.
    Uses: regex.
    """
    """new = old.lower()
    new = re.sub(r"[àáâãäå]", "a", new)
    new = re.sub(r"[èéêë]", "e", new)
    new = re.sub(r"[ìíîï]", "i", new)
    new = re.sub(r"[òóôõö]", "o", new)
    new = re.sub(r"[ùúûü]", "u", new)
    return new"""


def remove_accents(old: str) -> str:
    """
    Remove accent characters from a string and convert to lowercase.

    Args:
        old: A string that may contain accent characters.

    Returns:
        A string with accent characters removed and converted to lowercase.
    """
    new = unicodedata.normalize("NFKD", old).encode("ascii", "ignore").decode("utf-8")
    new = new.lower()
    return new


def create_hash(*args):
    hash_obj = hashlib.sha256()
    for arg in args:
        hash_obj.update(str(arg).encode("utf-8"))
    return hash_obj.hexdigest()
