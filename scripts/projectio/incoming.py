import sys
import os
import glob

from database.models import FileRouterHistory, ErrorLog, Session
from utils.customexceptions import ExitProjectException

class Incoming:
    file_pattern = []
    path = None
    def __init__(self, project, logger=None, **config):
        self.__dict__.update(config)
        self.path = os.path.abspath(self.path)
        self.project = project
        self.logger = logger
        self.files = self._walk_files()
        
        self.mappings = []

    def _walk_files(self):
        session=Session()
        try:
            paths = glob.glob(self.path + "/**/*", recursive=True)
            if hasattr(self, "file_pattern"):
                paths_based_on_file_pattern = []
                for t in self.file_pattern:
                    paths_based_on_file_pattern.extend(glob.glob(self.path + "/**/" + t, recursive=True))
                not_using = list(set(paths) - set(paths_based_on_file_pattern))
                if self.logger is not None:

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
            if self.logger is not None:
                self.logger.error("Something went wrong when walking the directory \n {0}".format(e))
            raise ExitProjectException("Something went wrong when walking the directory")

    def save_all(self, session):
        try:
            for f in self.files:
                new_record = FileRouterHistory(project_name=self.project, incoming_path=f)
                session.add(new_record)
                session.commit()
        except Exception as e:
            if self.logger is not None:
                self.logger.error("Seomthing went wrong for the intial save to the DB \n {0}".format(e))
            sys.exit(1)