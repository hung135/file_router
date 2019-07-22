import re
import os

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')

class RenameOptions:
    # Modified from from:
    # https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    def snakecase(self, given_path):
        """
        Snakecase of the basename of a given path

        Parameters
        ----------
        given_path: str

        Returns
        -------
        str
            New path
        """
        filename = os.path.basename(given_path)
        filename = first_cap_re.sub(r'\1_\2', filename)
        filename = all_cap_re.sub(r'\1_\2', filename).lower()
        return given_path.replace(os.path.basename(given_path), filename)

    def lowercase(self, given_path):
        """
        Lowercase version of the basename of a given path

        Parameters
        ----------
        given_path: str

        Returns
        -------
        str
            New path
        """
        filename = os.path.basename(given_path).lower()
        return given_path.replace(os.path.basename(given_path), filename)