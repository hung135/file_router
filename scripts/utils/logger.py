import datetime
import logging
from database.models import Logging

class Logger():
    def __init__(self, project_name, session, logging_path=None, verbose=False):
        self._setuplogger(project_name, session, logging_path, verbose)

    def _setuplogger(self, project_name, session, logging_path, verbose):
        my_handlers = [logging.StreamHandler(), LogDBHandler(session, project_name)]
        if logging_path is not None:
            my_handlers.append(logging.FileHandler(filename=logging_path, mode="a"))
        logging.basicConfig(
            level=40 if not verbose else 30,
            format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s,",
            handlers=my_handlers
        )
        self.logger = logging.getLogger()

class LogDBHandler(logging.Handler):
    def __init__(self, session, project_name):
        logging.Handler.__init__(self)
        self.session = session
        self.project = project_name
    
    def emit(self, record):
        log = Logging(
            project_name=self.project,
            level=record.__dict__['levelname'],
            msg=record.__dict__['msg'])
        self.session.add(log)
        self.session.commit()