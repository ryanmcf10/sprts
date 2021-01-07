from math import floor


def string_height_to_inches(string_height):
    """
    Given a string height like '6-10' (6 feet, 10 inches), convert it to an integer representing the height in inches
    :param string_height:
    :return:
    """
    feet, inches = string_height.split("-")

    height = 12 * int(feet) + int(inches)

    return height


def inches_to_string_height(inches):
    """
    Given a height in inches, format it as a string like '6-10' (6 feet, 10 inches)
    :param inches:
    :return:
    """
    string_feet = floor(inches / 12)
    string_inches = inches % 12

    return f"{string_feet}-{string_inches}"
