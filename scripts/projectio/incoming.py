import sys
import os
import glob

from database.models import FileRouterHistory, ErrorLog, Session
from utils.customexceptions import ExitProjectException

class Incoming:
    """
    Set by the 'incoming' section in the YAML file

    Attributes
    ----------
    project: str
        Name of project
    logger: logging.logger
    dry: bool
        Dry run
    config: **kwarg, dict
    """

    # linter
    file_pattern = []
    path = None
    def __init__(self, project, logger, dry=False,  **config):
        self.__dict__.update(config)
        self.path = os.path.abspath(self.path)
        self.project = project
        self.logger = logger
        self.dry = dry
        self.files = self._walk_files()
        self.mappings = []

    def _walk_files(self):
        """
        Gather all the files (path+name) recursively based on a given path 

        Returns
        -------
        list
            Path+file_names found
        """
        session=Session()
        try:
            paths = glob.glob(self.path + "/**/*", recursive=True)
            self.logger.warning("Walking incoming path: %s" % self.path)
            if hasattr(self, "file_pattern"):
                paths_based_on_file_pattern = []
                for t in self.file_pattern:
                    self.logger.warning("Walking above path with file_pattern: %s" % t)
                    paths_based_on_file_pattern.extend(glob.glob(self.path + "/**/" + t, recursive=True))
                not_using = list(set(paths) - set(paths_based_on_file_pattern))
                if  not self.dry:
                    # program_unit =Column(String(128)) 
                    # error_code =Column(String(5))  
                    # error_timestamp  =Column(DateTime, default=datetime.datetime.utcnow)
                    # user_name =Column(String(32))  
                    # sql_statement =Column(String(2000)) 
                    for fn in not_using:
                        new_record = ErrorLog(program_unit=f'switchboard: {self.project}',error_code='?????',user_name='GOCD',
                        error_message=f'{os.path.basename(fn)}: No matching REGEX in yaml')
                        session.add(new_record)
                    
                        self.logger.warning("Will not process this file %s" % (os.path.basename(fn)))
                    session.commit()
                paths = paths_based_on_file_pattern
            paths = [p for p in paths if os.path.basename(p) != "."]
            return paths
        except Exception as e:
            self.logger.error("Something went wrong when walking the directory \n {0}".format(e))
            raise ExitProjectException("Something went wrong when walking the directory")

    def save_all(self, session):
        """
        Renames the files based on the given logic

        Parameters
        ----------
        files: list
            List of file paths
        """
        try:
            self.logger.warning("Saving intial incoming records to database")
            for f in self.files:
                self.logger.warning("Saving %s" % f)
                if not self.dry:
                    new_record = FileRouterHistory(project_name=self.project, incoming_path=f)
                    session.add(new_record)
                    session.commit()
        except Exception as e:
            self.logger.error("Seomthing went wrong for the intial save to the DB \n {0}".format(e))
            sys.exit(1)