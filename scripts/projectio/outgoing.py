import sys
import os 
import shutil
import glob
import re
import requests
from logic.rename_options import RenameOptions
from logic.file_path_extract import FileHistory
from database.models import FileRouterHistory
from utils.customexceptions import ExitProjectException, InvalidAPIVersion
from utils.utils import call_api

class Outgoing:
    #making this visible to linter
    path = None
    rename_options = []
    file_path_extract = None
    def __init__(self, project, logger=None, **config):
        self.__dict__.update(config)
        self.project = project
        self.path = os.path.abspath(self.path)
        self.logger = logger

    def rename(self, files):
        files_mapping = {}
        if "rename_options" in self.logic:
            options = RenameOptions()
            for option in self.logic["rename_options"]:
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
        reg = self.logic["file_path_extract"] if "file_path_extract" in self.logic else None
        options = FileHistory()
        for key in incoming.mappings:
            files = (key, incoming.mappings[key])
            fn = os.path.basename(files[0])
            md5, size, date, extract = FileHistory.file_information(self.logger, files[1],reg)
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
                self.logger.error("Record {0} can not be saved, with error: {1}".format(fn, e))
                sys.exit(1)
    
    def call_api(self):
        try:
            if hasattr(self, "api"):
                call_api(self.api["uri"], self.api["pipeline"])
                if response.status_code != requests.codes.ok:
                    self.logger.error("Launch project \"%s\" to api: \"%s\" wasn't succesful" % (self.project, self.api))
        except KeyError as e:
            self.logger.error("Missing api creds for project \"%s\" and api \"%s\"" % (self.project, self.api))
        except requests.exceptions.MissingSchema as e:
            self.logger.error("Invalid api url \"%s\" %s" % (self.api, e))
        except InvalidAPIVersion as e:
            self.logger.error(e)
        except Exception as e:
            self.logger.error("Invalid api call: \n %s" % (e))

    def move_files(self, files):
        if hasattr(self, "path"):
            for f in files:
                try:
                    if not os.path.isdir(self.path):
                        os.makedirs( self.path)
                    shutil.move(f,  self.path)
                except shutil.Error:
                    self.logger.error("%s can not me moved" %(os.path.basename(f)))
                    raise ExitProjectException("Files can not be moved")