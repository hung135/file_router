import sys
from database.models import FileRouterHistory
from utils.customexceptions import ExitProjectException
from .incoming import Incoming
from .outgoing import Outgoing

class ProjectIO:
    def __init__(self, project, logger=None, **config):
        self.outgoing = Outgoing(project, logger, **config["outgoing"])
        self.incoming = Incoming(project, logger, **config["incoming"])
    
    def run_pipeline(self, session):
        try:
            if len(self.incoming.files) is 0:
                self.incoming.logger.error(f"No files found For Project: {self.incoming.project}")
                return "Files not found"
            else:
                # run incoming steps
                self.incoming.save_all(session)
                self.incoming.files, self.incoming.mappings = self.outgoing.rename(self.incoming.files)
                # run outgoing steps
                self.outgoing.file_history(self.incoming, session)
                self.outgoing.move_files(self.incoming.files)
                self.outgoing.call_api()
            return None
        except ExitProjectException as e:
            return e.message

    
    def _executor(self, _obj):
        # idea here: https://stackoverflow.com/questions/37075680/run-all-functions-in-class
        methods = [method for method in dir(_obj) if callable(getattr(_obj, method)) if not method.startswith("_")]
        for method in methods:
            getattr(_obj, method)(self.incoming.files)