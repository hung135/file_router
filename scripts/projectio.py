import os 
import shutil
import glob
import re
from logic.rename_options import RenameOptions
from logic.file_history import FileHistory

class ProjectIO:
    def __init__(self, project, **config):
        self.outgoing = Outgoing(**config["outgoing"])
        self.incoming = Incoming(**config["incoming"])
    
    def run_pipeline(self):
        # run incoming first
        self.incoming
        # run outcoming next
        self._executor(self.outcoming)

    def _executor(self, _obj):
        # idea here: https://stackoverflow.com/questions/37075680/run-all-functions-in-class
        methods = [method for method in dir(_obj) if callable(getattr(_obj, method) if not method.startswith("_"))]
        for method in methods:
            getattr(_obj, method)(self.incoming.files)

class Outgoing:
    def __init__(self, **config):
        self.__dict__.update(config)

    def rename(self, files):
        if hasattr(self, "rename_options"):
            options = RenameOptions()
            for option in self.rename_options:
                if hasattr(options, option):
                    for i,f in enumerate(files):
                        new = getattr(options, option)(f)
                        os.rename(f, new)
                        files[i] = new
        return files

    def file_history(self, files):
        responses = {}
        if hasattr(self, "file_history"):
            options = FileHistory()
            for option in self.file_history:
                if hasattr(options, option):
                    for i,f in enumerate(files):
                        responses[option] = getattr(options, option)(f)



    def move_files(self, files):
        if hasattr(self, "path"):
            [shutil.move(f, self.path) for f in files]

class Incoming:
    def __init__(self, **config):
        self.__dict__.update(config)
        self.files = self._walk_files()

    def _walk_files(self):
        if hasattr(self, "file_pathern"):
            return glob.glob(self.path + "/**/" + self.file_pathern, recursive=True)
        else:
            return glob.glob(self.path+ "/**/", recursive=True)

    def save_all(self, session):
        # record = DatabaseType(**kwargs)
        # session.add(record)
        # session.commit()
        return true
