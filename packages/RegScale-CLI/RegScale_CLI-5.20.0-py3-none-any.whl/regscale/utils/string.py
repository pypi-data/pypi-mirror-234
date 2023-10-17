"""Define commonly used methods for strings."""
import re


ANSI_ESCAPE_REGEX = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def remove_ansi_escape_sequences(text: str) -> str:
    """Remove all ANSI escape sequences from a text
    :param str text: a string to remove ANSI escape sequences from
    :returns: a string with no ANSI escape sequences
    :rtype: str
    """
    return ANSI_ESCAPE_REGEX.sub("", text)


def replace_unknown_spaces_and_newlines(input_string: str) -> str:
    """Replace unknown spaces and newlines with a single space
    :param str input_string: a string to replace unknown spaces and newlines with a single space
    :returns: a string with unknown spaces and newlines replaced with a single space
    :rtype: str
    """
    return re.sub(r"\s+", " ", input_string)


def extract_double_curly_braces_contents(query_string: str) -> list[str]:
    """Extract the contents of double curly braces from a string
    :param str query_string: a string to extract the contents of double curly braces from
    :returns: a list of strings that were contained within double curly braces
    :rtype: list[str]
    """
    pattern = r"{{(.*?)}}"
    return re.findall(pattern, query_string)


def extract_dag_run_conf_key(query_string: str) -> str:
    """Extract the key from a dag_run.conf key-value pair
    :param str query_string: a string to extract the key from a dag_run.conf key-value pair
    :returns: the key from a dag_run.conf key-value pair
    :rtype: str
    """
    pattern = r"dag_run\.conf\[['\"]([^'\"]+)['\"]\]"
    match = re.search(pattern, query_string)
    return match[1] if match else None


def extract_param(query_string: str) -> list:
    """Extract the parameter from a params key-value pair
    :param str query_string: a string to extract the parameter from a params key-value pair
    :returns: the parameter from a params key-value pair
    :rtype: str
    """
    pattern = r"\bparams\.(\w+)\s.*"
    matches = re.findall(pattern, query_string)
    return matches[0] if matches else None
