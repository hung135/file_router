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
    
    def run_pipeline(self):
        # run incoming first
        self.incoming
        # run outcoming next
        self._executor(self.outcoming)

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
        reg = self.file_path_extract if hasattr(self, "file_path_extract") else None
        options = FileHistory()
        for i,f in enumerate(files):
            fn = os.path.basename(f)
            md5, size, date, extract = FileHistory.file_information(f,reg)
            # save into db

    def move_files(self, files):
        if hasattr(self, "path"):
            [shutil.move(f, self.path) for f in files]

class Incoming:
    def __init__(self, project, **config):
        self.__dict__.update(config)
        self.project = project
        self.files = self._walk_files()

    def _walk_files(self):
        if hasattr(self, "file_pathern"):
            return glob.glob(self.path + "/**/" + self.file_pathern, recursive=True)
        else:
            return glob.glob(self.path+ "/**/", recursive=True)

    def save_all(self, session):
        for f in self.files:
            #  project_name = Column(String(32))
            # incoming_path = Column(Text)
            # outgoing_path = Column(Text,unique=True)
            # file_date = Column(TIMESTAMP)
            # file_md5 = Column(String(32))
            # file_size = Column(Integer)
            # file_path_extract = Column(String(32))
            new_record = FileRouterHistory(
                project_name = self.project,
                incoming_path = f,
                outgoing_path = f + "unique",
                file_date = datetime.timestamp(datetime.now()),
                file_md5 = "",
                file_size = 0,
                file_path_extract = ""
            )
            new_record = FileRouterHistory(incoming_path=f)
            session.add(new_record)
            session.commit()
