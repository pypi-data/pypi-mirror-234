from datetime import datetime
from dateutil import parser
import re


def is_uuid4(string):
    return bool(re.match(r'[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}', string))


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parser.parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def is_valid_date(date_str):
    """
    It verifies if the date is in the following format: 'DD-MM-YYYY' or 'MM-YYYY' or 'YYYY'.
    :param date_str:
    :return:
    """
    try:
        # Attempt to parse date using the different formats
        datetime.strptime(date_str, '%d-%m-%Y')
        return True
    except ValueError:
        pass

    try:
        datetime.strptime(date_str, '%m-%Y')
        return True
    except ValueError:
        pass

    try:
        datetime.strptime(date_str, '%Y')
        return True
    except ValueError:
        pass

    # None of the formats matched
    return False
