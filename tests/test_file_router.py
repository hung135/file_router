import sys
sys.path.append("..scripts")

import unittest
import os
from config_parent import Config
from file_router import *


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
    def test_01(self): #using environment variables
        os.makedirs(os.path.abspath(self.dirs['working_dir']),exist_ok=True)
          
        print(fr.yaml_config)
        
if __name__ == '__main__':
    unittest.main()