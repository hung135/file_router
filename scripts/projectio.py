import shutil
import glob

class ProjectIO:
    def __init__(self, project, **config):
        self.outgoing = Outgoing(**config["outgoing"])
        self.incoming = Incoming(**config["incoming"])

class Outgoing:
    def __init__(self, **config):
        self.__dict__.update(config)
    
    def move_files(self, files):
        if hasattr(self, "path"):
            for f in glob(files):
                shutil.move(f, self.path)

class Incoming:
    def __init__(self, **config):
        self.__dict__.update(config)
        self.files = self._walk_files()

    def _walk_files(self):
        if hasattr(self, "file_pathern"):
            return glob.glob(self.path + "/**/" + self.file_pathern, recursive=True)
        else:
            return glob.glob(self.path+ "/**/", recursive=True)

    def save_all(self, session):
        # record = DatabaseType(**kwargs)
        # session.add(record)
        # session.commit()
        return true
