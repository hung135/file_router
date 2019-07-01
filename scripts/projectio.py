import shutil
import glob
from logic.rename_options import RenameOptions

class ProjectIO:
    def __init__(self, project, **config):
        self.outgoing = Outgoing(**config["outgoing"])
        self.incoming = Incoming(**config["incoming"])

class Outgoing:
    def __init__(self, **config):
        self.__dict__.update(config)
    
    def rename_options(self, files):
        if hasattr(self, "rename_options"):
            options = RenameOptions()
            for option in self.rename_options:
                if hasattr(options, option):
                    for f in files:
                        f = getattr(options, option)(f)
                        shutil.copy(f, )

    def move_files(self, files):
        if hasattr(self, "path"):
            [shutil.move(f, self.path) for f in files]

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
