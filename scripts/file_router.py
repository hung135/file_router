import sys
import os
import yaml
import argparse
import logging
import datetime
from datetime import date, timedelta
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from projectio.projectio import ProjectIO
from database.models import FileRouterHistory, Session
from utils.utils import traverse_replace_yaml_tree, recurse_replace_yaml
from utils.logger import Logger

# Do this whenever you need a connection to the DB. (typically once at the top of your script)
sess = Session()
now = datetime.datetime.now()

runtime_dict = {"today": now.strftime("%Y-%m-%d") ,
   "yesterday": (date.today() - timedelta(days=1)).strftime("%Y-%m-%d"),
   "thisyear": now.strftime("%Y"),
   "thismonth": now.strftime("%Y-%m")
}

def yaml_reader(yaml_path=None):
   file_path = yaml_path or f"{os.path.dirname(__file__)}/file_router.yaml"
   try:
      with open(file_path, "r") as f:
         return yaml.safe_load(f)
   except FileNotFoundError as e:
      print(e)

def parse_cli():
   parser = argparse.ArgumentParser(description='Process a yaml file')
   parser.add_argument("-y","-yaml","--yaml", help="Location of the yaml file")
   parser.add_argument("-s", "-skeleton", "--skeleton", help="Generates a skeleton.yaml file to the directory specified")
   parser.add_argument("-v", "-verbose", help="Enable verbose mode", action="store_true")
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
   sys.exit(0)
 
def runner(args):
   config = yaml_reader(args.yaml)
   config = traverse_replace_yaml_tree(config)
   config = recurse_replace_yaml(config,runtime_dict)
   
   projects = []
   for project in config:
      try:
         logger = Logger(project, sess, config[project]["logging"], args.v)
      except KeyError:
         logger = Logger(project, sess, None, args.v)
      proj = ProjectIO(project, logger.logger, **config[project])
      proj.run_pipeline(sess)
      projects.append(proj)

 
if __name__ == "__main__":
   args = parse_cli()
   if args.skeleton:
      create_skeleton(args.skeleton)
   runner(args)