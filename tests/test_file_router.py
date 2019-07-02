import sys
sys.path.append("..scripts")

import unittest
import os
from config_parent import Config
from file_router import yaml_reader
from projectio import ProjectIO
from lorem.text import TextLorem
import shutil.rmtree as rmtree


__author__ = "Hung Nguyen"
__copyright__ = "Hung Nguyen"
__license__ = "mit"

def clean_working_dir(folder: str):
    import os, shutil
     
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
class TestFileRouter(unittest.TestCase,Config):
    def test_make_dirs(self): #using environment variables
        os.makedirs(os.path.abspath(self.dirs['working_dir']),exist_ok=True)
        yaml_config= yaml_reader('/workspace/scripts/file_router.yaml')
        for project in yaml_config:
            print(yaml_config[project])
            incoming=yaml_config[project]['incoming']
            outgoing=yaml_config[project]['outgoing']
            pio=ProjectIO(project=project,incoming=incoming,outgoing=outgoing)
            os.makedirs(os.path.abspath(pio.incoming.path),exist_ok=True)
            os.makedirs(os.path.abspath(pio.outgoing.path),exist_ok=True) 
            #print(yaml_reader('/workspace/scripts/file_router.yaml'))
            lorem = TextLorem(wsep='-', srange=(2,3) )
            for i in range(10):
                print(lorem.sentence())
                file_name=lorem.sentence()+'.zip'
                with open(os.path.join(pio.incoming.path,file_name),'a') as f:
                    f.write(lorem.paragraph())
    def test_clean_dirs(self): #using environment variables
        yaml_config= yaml_reader('/workspace/scripts/file_router.yaml')
        for project in yaml_config:
            incoming_path=yaml_config[project]['incoming']['path']
            outgoing_path=yaml_config[project]['outgoing']['path']
            rmtree(incoming_path)
if __name__ == '__main__':
    unittest.main()