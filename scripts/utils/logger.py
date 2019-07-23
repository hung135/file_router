import datetime
import logging
from database.models import Logging

class Logger():
    """
    Attribtutes
    -----------
    logger: logging.logger
    """

    def __init__(self, project_name, session, logging_path=None, verbose=False, dry=False):
        self.logger = self._setuplogger(project_name, session, logging_path, verbose) if not dry else logging.getLogger()

    def _setuplogger(self, project_name, session, logging_path, verbose):
        """
        Setups up the a custom logger

        Will always setup a logger with both a StreamHandler and a LogDBHandler. If the logging_path
        isn't empty it will append a FileHandler. The Verbose is used to determine if we log only errors or 
        warnings and errors.

        Parameters
        ---------
        project_name: str
            Project Name
        session: sqlalchemy.orm.sessionmaker
            Database session
        loggin_path: str
            Output for logging
        verbose: bool
            Verbose for printing warnings and errors

        Returns
        -------
        logger
            Custom logger built
        """
        my_handlers = [logging.StreamHandler(), LogDBHandler(session, project_name)]
        if logging_path is not None:
            my_handlers.append(logging.FileHandler(filename=logging_path, mode="a"))
        logging.basicConfig(
            level=40 if not verbose else 30,
            format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s,",
            handlers=my_handlers
        )
        return logging.getLogger()

class LogDBHandler(logging.Handler):
    """
    Attributes
    ----------
    session: sqlalchemy.orm.sessionmaker
    project: str
        Project Name
    """
    def __init__(self, session, project_name):
        logging.Handler.__init__(self)
        self.session = session
        self.project = project_name
    
    def emit(self, record):
        """
        Persists message to database

        Parameters
        ----------
        record: obj
            Message that is being sent to the logger
        """
        log = Logging(
            project_name=self.project,
            level=record.__dict__['levelname'],
            msg=record.__dict__['msg'])
        self.session.add(log)
        self.session.commit()