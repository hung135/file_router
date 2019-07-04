import os 
import shutil
import glob
import re

from logic.rename_options import RenameOptions
from logic.file_history import FileHistory
from models import FileRouterHistory

class Outgoing:
    #making this visible to linter
    path = None
    rename_options = []
    file_path_extract = None
    def __init__(self, project, logger=None, **config):
        self.__dict__.update(config)
        self.project = project
        self.logger = logger

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
                    else:
                        if self.logger is not None: 
                            self.logger.warning("The rename_options function %s does not exists" % (option))
        return (files, files_mapping)

    def file_history(self, incoming, session):
        reg = self.file_path_extract if hasattr(self, "file_path_extract") else None
        options = FileHistory()
        for key in incoming.mappings:
            files = (key, incoming.mappings[key])
            fn = os.path.basename(files[0])
            md5, size, date, extract = FileHistory.file_information(files[1],reg)
            try:
                if all(val is not None for val in [md5, size, date]):
                    for record in session.query(FileRouterHistory).filter(FileRouterHistory.project_name == self.project).filter(FileRouterHistory.incoming_path == files[0]):
                        record.outgoing_path = os.path.join(self.path,os.path.basename(files[1]))
                        record.file_date = date
                        record.file_md5 = md5
                        record.file_size = size
                        record.file_path_extract = extract
                        session.add(record)
                    session.commit()
            except Exception as e:
                if self.logger is not None:
                    self.logger.error("Record %s can not be saved" % (fn))

    def move_files(self, files):
        if hasattr(self, "path"):
            for f in files:
                try:
                    
                    if  os.path.isdir(self.path) == False:
                         
                        os.makedirs(os.path.abspath(self.path)  )
                        
                    
                    shutil.move(f, os.path.abspath(self.path))
                except shutil.Error:
                    if self.logger is not None:
                        self.logger.error("%s can not me moved" %(os.path.basename(f)))