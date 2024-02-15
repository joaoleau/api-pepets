import collections


def cleaned_data(value):

    if not isinstance(value, str):
        return value
    if isinstance(value, collections.OrderedDict):
        return value

    value = value.strip()
    value = " ".join(value.split())
    value = value.capitalize()
    return value
