import sys
sys.path.append("..scripts")

import unittest
import os
from config_parent import Config
from file_router import yaml_reader
from projectio import ProjectIO
from lorem.text import TextLorem
import shutil   
import py_dbutils.rdbms.postgres as dbconn 
import random

__author__ = "Hung Nguyen"
__copyright__ = "Hung Nguyen"
__license__ = "mit"

FILE_TYPES = ['zip','txt','csv','db','xls']
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
    def test_01_clean_dirs(self): #using environment variables
        yaml_config= yaml_reader('/workspace/scripts/file_router.yaml')
        for project in yaml_config:
            incoming_path=yaml_config[project]['incoming']['path']
            outgoing_path=yaml_config[project]['outgoing']['path']
            shutil.rmtree(incoming_path)
            shutil.rmtree(outgoing_path)
    def test_02_make_dirs(self): #using environment variables
        yaml_config= yaml_reader('/workspace/scripts/file_router.yaml')
        for project in yaml_config:
             
            incoming=yaml_config[project]['incoming']
            outgoing=yaml_config[project]['outgoing']
            pio=ProjectIO(project=project,incoming=incoming,outgoing=outgoing)
            os.makedirs(os.path.abspath(pio.incoming.path),exist_ok=True)
            os.makedirs(os.path.abspath(pio.outgoing.path),exist_ok=True) 
            #print(yaml_reader('/workspace/scripts/file_router.yaml'))
            lorem = TextLorem(wsep='-', srange=(2,3) )
            for i in range(10):
                
                file_name=lorem.sentence()+random.choice(FILE_TYPES)
                with open(os.path.join(pio.incoming.path,file_name),'a') as f:
                    f.write(lorem.paragraph())
    def test_03_move_files(self):
        self.pio=[]
        yaml_config= yaml_reader('/workspace/scripts/file_router.yaml')
        for project in yaml_config:
            incoming=yaml_config[project]['incoming']
            outgoing=yaml_config[project]['outgoing']
            outgoing_path=yaml_config[project]['outgoing']['path']
            pio=ProjectIO(project=project,incoming=incoming,outgoing=outgoing)
            pio.outgoing.move_files(pio.incoming.files)
            self.pio.append(pio) #saving this so we can test base on values that current exists in this object
            for file in pio.incoming.files:
                new_path=os.path.join(outgoing_path,os.path.basename(file))
                
                print("Checking file in Out folder: ",new_path)
                self.assertTrue(os.path.isfile(new_path))
                    
    def test_04_query_db(self):
        db=dbconn.DB()
        #query the db for each file in the outgoing directory to make sure it was logged
        # for pio in self.pio:
 
        #     for file in pio.incoming.files:
        #         print("Checking file in DB: ",file)
        #         file_exists_in_db=0
        #         file_exists_in_db,_=db.query(f'select 1 from test.table where file_name="{new_path}"')
        #         self.assertTrue(int(file_exists_in_db),1)
if __name__ == '__main__':
    unittest.main()