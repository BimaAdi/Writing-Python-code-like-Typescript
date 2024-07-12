def add(x, y):
    """Add two integer

    Parameter:\n
    x -- int\n
    y -- int\n

    Return: int
    >>> add(1, 2) # <-- I change it here
    3
    """
    return x + y


if __name__ == "__main__":
    import doctest

    doctest.testmod()
