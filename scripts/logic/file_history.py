import os
import re
import hashlib
from datetime import datetime

class FileHistory():
    @classmethod
    def file_information(self, f, reg=None):
        try:
            _extract = None
            _md5 = hashlib.md5(open(f, "rb").read()).hexdigest()
            _size = os.path.getsize(f)
            _date = datetime.fromtimestamp(os.stat(f).st_mtime)

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
            #found = re.findall(reg, f)
            found=re.search(reg,f) or ''
            if found:
                #todo
                #currently searches from left to right and finds the first...
                #we want the last item that matches regex
                extracted_data=found.group()
                return extracted_data
            return None  
        except re.errors:
            print("invalid regex, skipping")
            return None