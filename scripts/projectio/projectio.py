import sys
from database.models import FileRouterHistory
from .incoming import Incoming
from .outgoing import Outgoing

class ProjectIO:
    def __init__(self, project, logger=None, **config):
        self.outgoing = Outgoing(project, logger, **config["outgoing"])
        self.incoming = Incoming(project, logger, **config["incoming"])
    
    def run_pipeline(self, session):
        if len(self.incoming.files) is 0:
            if self.incoming.logger is not None:
                self.incoming.logger.error(f"No files found For Project: {self.incoming.project}")
            #sys.exit(1)
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