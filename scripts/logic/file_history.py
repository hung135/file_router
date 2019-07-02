import os
import re
import hashlib

class FileHistory():
    @classmethod
    def file_information(self, f, reg=None):
        try:
            _extract = None
            _md5 = hashlib.md5(open(f, "rb").read()).hexdigest()
            _size = os.path.getsize(f)
            _date = os.stat(f).st_mtime

            if reg is not None:
                _extract = self.file_path_extract(f, reg)

            return (_md5, _size, _date, _extract)
        except Exception as e:
            print("Something went wrong \n %s" % (e))
            return (None, None, None, None)

    @staticmethod
    def file_path_extract(f, reg):
        try:
            reg = re.compile(reg)
            found = re.findall(reg, f)
            return None if len(found) == 0 else found[-1]
        except re.errors:
            print("invalid regex, skipping")
            return None