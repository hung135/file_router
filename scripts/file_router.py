import os
import yaml
import argparse
import logging
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from projectio.projectio import ProjectIO
from models import FileRouterHistory, Session

# Do this whenever you need a connection to the DB. (typically once at the top of your script)
sess = Session()

def yaml_reader(yaml_path=None):
   #print("---------------------------",__file__,os.path.dirname(__file__))
   file_path = yaml_path or f"{os.path.dirname(__file__)}/file_router.yaml"
   try:
      with open(file_path, "r") as f:
         return yaml.safe_load(f)
   except FileNotFoundError as e:
      print(e)

def generate_logger(logging_path):
   logging.basicConfig(filename=logging_path, filemode="a", format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s,", datefmt="%H:%M:%S",level=logging.DEBUG)
   logger = logging.getLogger()
   return logger

def parse_cli():
   parser = argparse.ArgumentParser(description='Process a yaml file')
   parser.add_argument("--yaml", help="Location of the yaml file")
   parser.add_argument("--skeleton", help="Generates a skeleton.yaml file to the directory specified")
   args = parser.parse_args()
   return args 

def create_skeleton(path):
   example = {
      "project_name1": {
         "logging": "<path>",
         "incoming": {
            "path": "<string>",
            "file_pattern": ["glob style of target file; i.e.: *.zip", "file_pattern_2"]
         }, 
         "outgoing": {
            "path": "<string>",
            "rename_options": ["rename_option1", "rename_option2"],
            "file_path_extract": "(\\d\\d\\d\\d)"
         }
      },
      "project_name2": {
         "logging": "<path>",
         "incoming": {
            "path": "<string>",
            "file_pattern": ["glob style of target file; i.e.: *.zip", "file_pattern_2"]
         }, 
         "outgoing": {
            "path": "<string>",
            "rename_options": ["rename_option1", "rename_option2"],
            "file_path_extract": "(\\d\\d\\d\\d)"         
         }
      }
   }
   try:
      with open(path + "skeleton.yaml", "w") as f:
         yaml.dump(example, f, default_flow_style=False)
   except Exception as e:
      print(e)

def runner(args):
   config = yaml_reader(args.yaml)
   projects = []
   for project in config:
      logger = None
      try:
         logger = generate_logger(config[project]["logging"])
      except KeyError:
         continue
      proj = ProjectIO(project, logger, **config[project])
      proj.run_pipeline(sess)
      projects.append(proj)

 
if __name__ == "__main__":
   args = parse_cli()
   if args.skeleton:
      create_skeleton(args.skeleton)
   runner(args)