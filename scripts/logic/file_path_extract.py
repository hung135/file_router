import os
import re
import hashlib
from datetime import datetime

class FileHistory():
    @classmethod
    def file_information(self, logger, f, reg=None):
        try:
            _extract = None
            _md5 = hashlib.md5(open(f, "rb").read()).hexdigest()
            _size = os.path.getsize(f)
            _date = datetime.fromtimestamp(os.stat(f).st_mtime)

            if reg is not None:
                _extract = self.file_path_extract(f, reg, logger)

            return (_md5, _size, _date, _extract)
        except Exception as e:
            if logger is not None:
                logger.warning("Something went wrong trying to get file information for: {0}, e: {1}".format(f, e))
            return (None, None, None, None)

    @classmethod
    def file_path_extract(self, f, reg, logger):
        try:
            reg = re.compile(reg)
            found = re.findall(reg, f)
            return None if len(found) == 0 else found[-1]
        except re.error:
            if logger is not None:
                logger.warning("Invalid regex {0}, skipping".format(reg))
            return None