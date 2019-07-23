import sys
import os
from database.models import FileRouterHistory
from utils.customexceptions import ExitProjectException
from .incoming import Incoming
from .outgoing import Outgoing

class ProjectIO:
    """
    Wrapper and executer for both the Outgoing and Incoming classes

    Attributes
    ----------
    outgoing: Outgoing
        projectio.outgoing
    incoming: incoming
        projectio.incoming
    dry: bool
        Dry run
    project: str
        Project name
    """
    def __init__(self, project, logger, dry=False, **config):
        self.outgoing = Outgoing(project, logger, dry, **config["outgoing"])
        self.incoming = Incoming(project, logger, dry, **config["incoming"])
        self.dry = dry
        self.project = project

    def dry_statistics(self, api=None):
        """
        Prints basic information about the execution without actually calling anyhting

        Parameters
        ----------
        api: bool
            Determines if an API would be called
        """
        print("\n-----DRY RUN MODE ENABLED------\nFile Transformations:")
        [print("\t%s --> %s" % (x,os.path.join(self.outgoing.path, os.path.basename(y))))
            for x, y in zip(self.incoming.mappings, self.incoming.files)]
        if api:
            print("API Call: \n\turi: %s \n\tpipeline: %s" % (api["uri"], api["pipeline"]))

    def run_pipeline(self, session):
        """
        Executes the pipeline using the incoming/outgoing objects in this order:
            1. Intial save of all files
            2. Rename files
            3. Generate a file history and save that information to the DB
            4. Move the files
            5. Call API

        Paremeters
        ----------
        session: sqlalchemy.orm.sessionmaker
            Session of the current DB connection
        """
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
                call = self.outgoing.call_api()

                if self.dry:
                    self.dry_statistics(call)
            return None
        except ExitProjectException as e:
            return e.message

    def _executor(self, _obj):
        """
        TODO: Reflectively call all funcitons
        """
        # idea here: https://stackoverflow.com/questions/37075680/run-all-functions-in-class
        methods = [method for method in dir(_obj) if callable(getattr(_obj, method)) if not method.startswith("_")]
        for method in methods:
            getattr(_obj, method)(self.incoming.files)