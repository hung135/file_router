import re

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')

class RenameOptions:
    # Stolen from:
    # https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    def snakecase(path):
        # process path
        s1 = first_cap_re.sub(r'\1_\2', filename)
        return all_cap_re.sub(r'\1_\2', s1).lower()

    def lowercase(path):
        # process path
        return filename.lower()