import os
import glob
from models import FileRouterHistory

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
        paths = glob.glob(self.path + "/**/*", recursive=True)
        if hasattr(self, "file_pattern"):
            paths_based_on_file_pattern = []
            for t in self.file_pattern:
                paths_based_on_file_pattern.extend(glob.glob(self.path + "/**/" + t, recursive=True))
            not_using = list(set(paths) - set(paths_based_on_file_pattern))
            if self.logger is not None:
                [self.logger.warning("Will not process this file %s" % (os.path.basename(fn))) for fn in not_using]
            paths = paths_based_on_file_pattern
        paths = [p for p in paths if os.path.basename(p) != "."]
        return paths

    def save_all(self, session):
        for f in self.files:
            new_record = FileRouterHistory(project_name=self.project, incoming_path=f)
            session.add(new_record)
            session.commit()