"""Provide utility functions for dealing with lists."""


def add_and_return_unique(*lists) -> list:
    """Add lists together and return a list of unique elements
    :param lists: lists to add together
    """
    unique_elements = set()
    for lst in lists:
        unique_elements.update(lst)
    return list(unique_elements)
