import os
import re
import hashlib

class FileHistory:
    def md5(self, f):
        return hashlib.md5(open(f, "rb")).read()).hexdigest()

    def file_size(self, f):
        return os.path.getsize(f)

    def file_date():
        return os.stat(f).st_mtime

    def file_path_extract(self, files):
        if hasattr(self, "date_extract"):
            try:
                # check if regex is valid
                reg = re.compile(self.date_extract)

            except re.errors:
                print("invalid regex, skipping")
            except Exception as e:
                print("Something went wrong \n %s" % (e))