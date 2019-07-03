import os 
import shutil
import glob
import re
from datetime import datetime
from logic.rename_options import RenameOptions
from logic.file_history import FileHistory
from models import FileRouterHistory

class ProjectIO:
    def __init__(self, project, **config):
        self.outgoing = Outgoing(project, **config["outgoing"])
        self.incoming = Incoming(project, **config["incoming"])
    
    def run_pipeline(self, session):
        # run incoming steps
        self.incoming.save_all(session)
        self.incoming.files, self.incoming.mappings = self.outgoing.rename(self.incoming.files)
        # run outgoing steps
        self.outgoing.file_history(self.incoming, session)
        self.outgoing.move_files(self.incoming.files)
    
    def _executor(self, _obj):
        # idea here: https://stackoverflow.com/questions/37075680/run-all-functions-in-class
        methods = [method for method in dir(_obj) if callable(getattr(_obj, method)) if not method.startswith("_")]
        for method in methods:
            getattr(_obj, method)(self.incoming.files)

class Outgoing:
    def __init__(self, project, **config):
        self.__dict__.update(config)
        self.project = project

    def rename(self, files):
        files_mapping = {}
        if hasattr(self, "rename_options"):
            options = RenameOptions()
            for option in self.rename_options:
                if hasattr(options, option):
                    for i,f in enumerate(files):
                        new = getattr(options, option)(f)
                        files_mapping[f] = new
                        os.rename(f, new)
                        files[i] = new
        return (files, files_mapping)

    def file_history(self, incoming, session):
        reg = self.file_path_extract if hasattr(self, "file_path_extract") else None
        options = FileHistory()
        for key in incoming.mappings:
            files = (key, incoming.mappings[key])
            fn = os.path.basename(files[1])
            md5, size, date, extract = FileHistory.file_information(files[1],reg)
            if all(val is not None for val in [md5, size, date]):
                for record in session.query(FileRouterHistory).filter(FileRouterHistory.project_name == self.project).filter(FileRouterHistory.incoming_path == files[0]):
                    record.outgoing_path = files[1]
                    record.file_date = date
                    record.file_md5 = md5
                    record.file_size = size
                    record.file_path_extract = extract
                    session.add(record)
                session.commit()
    def move_files(self, files):
        if hasattr(self, "path"):
            [shutil.move(f, self.path) for f in files]

class Incoming:
    def __init__(self, project, **config):
        self.__dict__.update(config)
        self.project = project
        self.files = self._walk_files()
        self.mappings = []

    def _walk_files(self):
        if hasattr(self, "file_pathern"):
            return glob.glob(self.path + "/**/" + self.file_pathern, recursive=True)
        else:
            return glob.glob(self.path+ "/**/", recursive=True)

    def save_all(self, session):
        for f in self.files:
            new_record = FileRouterHistory(project_name=self.project, incoming_path=f)
            session.add(new_record)
            session.commit()
