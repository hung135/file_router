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
    """
    Set by the 'outgoing' section in the YAML file

    Attributes
    ----------
    project: str
        Project name
    logger: logging.logger
    dry: bool
        Dry Run
    config: **kwarg, dict
    """

    path = None
    rename_options = []
    file_path_extract = None
    def __init__(self, project, logger=None, dry=False, **config):
        self.__dict__.update(config)
        self.project = project
        self.path = os.path.abspath(self.path)
        self.logger = logger
        self.dry = dry

    def rename(self, files):
        """
        Renames the files based on the given logic

        Parameters
        ----------
        files: list
            List of file paths

        Returns
        -------
        tuple
            (Files found, Equivalent files found but with logic ran over them)
        """
        files_mapping = {}
        if "rename_options" in self.logic:
            options = RenameOptions()
            for option in self.logic["rename_options"]:
                if hasattr(options, option):
                    self.logger.warning("Running rename_option: %s " % option)
                    for i,f in enumerate(files):
                        new = getattr(options, option)(f)
                        files_mapping[f] = new
                        if not self.dry:
                            os.rename(f, new)
                        files[i] = new
                else:
                    self.logger.warning("The rename_options function %s does not exists" % (option))
        return (files, files_mapping)

    def file_history(self, incoming, session):
        """
        Gathers the file information (md5, size, creation date) and saves it to the Database

        Parameters
        ----------
        incoming: projectio.Incoming
            Incoming object of the current project
        session: sqlalchemy.orm.sessionmaker
            Session of the current DB connection
        """
        reg = self.logic["file_path_extract"] if "file_path_extract" in self.logic else None
        self.logger.warning("Found regex for file_path_extract %s, now saving file history to db" % reg)
        options = FileHistory()
        for key in incoming.mappings:
            files = (key, incoming.mappings[key])
            fn = os.path.basename(files[0])
            md5, size, date, extract = FileHistory.file_information(self.logger, files[1], reg)
            try:
                if all(val is not None for val in [md5, size, date]) and not self.dry:
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
        """
        Calls the API

        Returns
        -------
        dict:
            API object for printing/loggin
        """
        try:
            if hasattr(self, "api"):
                if not self.dry:
                    response = call_api(self.api["uri"], self.api["pipeline"])
                    if response.status_code != requests.codes.ok:
                        self.logger.error("Launch project \"%s\" to api: \"%s\" wasn't succesful" % (self.project, self.api))
                    else:
                        self.logger.warning("Project %s to api's pipeline: %s has launched" % (self.project, self.api["pipeline"]))
                return self.api
        except KeyError as e:
            self.logger.error("Missing api creds for project \"%s\" and api \"%s\"" % (self.project, self.api))
        except requests.exceptions.MissingSchema as e:
            self.logger.error("Invalid api url \"%s\" %s" % (self.api, e))
        except InvalidAPIVersion as e:
            self.logger.error(e)
        except Exception as e:
            self.logger.error("Invalid api call: \n %s" % (e))

    def move_files(self, files):
        """
        Moves the files from the incoming directory to the outgoing directory

        Parameters
        ----------
        files: list
            List of file paths
        """
        if hasattr(self, "path"):
            self.logger.warning("Moving files to outgoing directory: %s" % self.path)
            for f in files:
                self.logger.warning("File %s" % f)
                try:
                    if not self.dry:
                        if not os.path.isdir(self.path):
                            os.makedirs( self.path)
                        shutil.move(f,  self.path)
                except shutil.Error:
                    self.logger.error("%s can not me moved" %(os.path.basename(f)))
                    raise ExitProjectException("Files can not be moved")