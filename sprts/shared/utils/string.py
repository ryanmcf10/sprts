def xstr(value):
    """
    Format a string whose value is potentially None.

    :param value:
    :return: '' if value is None, else, value
    """
    return '' if value is None else value
