import re


def restore_shape(template: str, replacement: str):
    if re.fullmatch(template, replacement):
        return replacement

    if re.fullmatch(template, capitalized := replacement.capitalize()):
        return capitalized

    if re.fullmatch(template, upper := replacement.upper()):
        return upper

    return replacement
