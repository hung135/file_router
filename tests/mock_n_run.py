import sys
  
import os
 
from file_router import yaml_reader
from projectio.projectio import ProjectIO
from lorem.text import TextLorem
import shutil   
import py_dbutils.rdbms.postgres as dbconn 
import random
from models import FileRouterHistory, Session,DecBase,engine
from file_router import parse_cli,runner
 

FILE_TYPES = ['zip','txt','csv','db','xls']
SESS = Session()
DecBase.metadata.create_all(engine)
yaml_config= yaml_reader('/workspace/scripts/file_router.yaml')
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
 
def step1_clean_dirs(): #using environment variables
        
    for project in yaml_config:
        incoming_path=yaml_config[project]['incoming']['path']
        outgoing_path=yaml_config[project]['outgoing']['path']
        if os.path.exists(incoming_path):
            shutil.rmtree(incoming_path)
        if os.path.exists(outgoing_path):
            shutil.rmtree(outgoing_path)
def step2_mokc_data(): #using environment variables
    
    for project in yaml_config:
            
        incoming=yaml_config[project]['incoming']
        outgoing=yaml_config[project]['outgoing']
        pio=ProjectIO(project=project,incoming=incoming,outgoing=outgoing)
        
        os.makedirs(os.path.abspath(pio.incoming.path),exist_ok=True)
        os.makedirs(os.path.abspath(pio.outgoing.path),exist_ok=True) 
        #print(yaml_reader('/workspace/scripts/file_router.yaml'))
        lorem = TextLorem(wsep='_', srange=(2,3) )
        for i in range(10):
            
            file_name=lorem.sentence()+random.choice(FILE_TYPES)
            with open(os.path.join(pio.incoming.path,file_name),'a') as f:
                f.write(lorem.paragraph())
            os.chmod(os.path.join(pio.incoming.path,file_name), 0o777)
    
if __name__ == '__main__':
    step1_clean_dirs()
    step2_mokc_data()
    import file_router
    args = parse_cli()
    runner(args)