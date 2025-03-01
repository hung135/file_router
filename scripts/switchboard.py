import sys
import os
import yaml
import argparse
import logging
import datetime
import re
import pprint
from datetime import date, timedelta
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from projectio.projectio import ProjectIO
from database.models import FileRouterHistory, Session
from utils.utils import traverse_replace_yaml_tree, recurse_replace_yaml, get_logic_function_names
from utils.logger import Logger
from version import version_dict

# Do this whenever you need a connection to the DB. (typically once at the top of your script)
sess = Session()
now = datetime.datetime.now()

runtime_dict = {"today": now.strftime("%Y-%m-%d") ,
   "yesterday": (date.today() - timedelta(days=1)).strftime("%Y-%m-%d"),
   "thisyear": now.strftime("%Y"),
   "thismonth": now.strftime("%Y-%m")
}

def yaml_reader(yaml_path=None):
   """
   Reads the yaml file from the path specified into the program.

   Parameters
   ----------
   yaml_path: str
      YAML path specified in the required arguments

   Returns
   -------
   dict
      Values of the yaml file
   """
   file_path = yaml_path or f"{os.path.dirname(__file__)}/switchboard.yaml"
   try:
      with open(file_path, "r") as f:
         return yaml.safe_load(f)
   except FileNotFoundError as e:
      print(e)

def parse_cli():
   """
   Parses the arguments passed into the program using argparse. 
   If the requried -y/-yaml/--yaml isn't found the program will cease execution.

   Returns
   -------
   dict
      Arguments found
   """
   parser = argparse.ArgumentParser(description='Process a yaml file')
   required_group = parser.add_argument_group("Required")
   required_group.add_argument("-y","-yaml","--yaml", help="Location of the yaml file")
   parser.add_argument("-s", "-skeleton", "--skeleton", help="Generates a skeleton.yaml file to the directory specified")
   parser.add_argument("-v", "-verbose", help="Enable verbose mode", action="store_true")
   parser.add_argument("-d", "--dry", 
      help="Enable dry mode which will run the entire yaml file with output only, nothing will be moved or saved", 
      action="store_true")
   parser.add_argument("--version", help="Version of executable", action="store_true")
   args = parser.parse_args()
   return args 

def create_skeleton(path):
   """
   Creates a skeleton yaml file as an example based on the path specified

   Parameters
   ----------
   path: str
      Path to dump the yaml file
   """
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
            "file_path_extract": "(\\d\\d\\d\\d)",
            "api": {
               "uri": "uri",
               "pipeline": "pipeline"
            }
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
            "file_path_extract": "(\\d\\d\\d\\d)",
            "api": {
               "uri": "uri",
               "pipeline": "pipeline"
            }
         }
      }
   }
   try:
      with open(path + "skeleton.yaml", "w") as f:
         yaml.dump(example, f, default_flow_style=False)
   except Exception as e:
      print(e)
   sys.exit(0)

def _print_msg(msg, val):
   """
   Wrapper that prints an error passed in, ends with an hard exit

   Parameters
   ----------
   msg: str
      Messsage to print out
   val: str
      Item to be formatted with
   """
   print(msg.format(val))
   sys.exit(1)

def print_version():
   """
   Prints version of the compiled switchboard executable
   """
   pprint.pprint(version_dict)
   sys.exit(0)

def validate_yaml(config):
   """
   Validates a given YAML files configuration to ensure it 

   Iterates through the given YAML file's configuration to ensure:
      1. Ensure a "path" variable is in both incoming and outgoing
      2. Validate their is a function for each defined "logic" in the YAML file
   If any of the these parameters are not met or missing the system will hard exit with a detailed 
   message describing the issue.

   Parameters
   ----------
   config: dict
      imported YAML file
   """
   funcs = get_logic_function_names()
   for project in config:
      message = "Path not found in incoming/outgoing for project: {0}"
      try:
         incoming = config[project]["incoming"]
         outgoing = config[project]["outgoing"]
         if "path" not in incoming.keys() or "path" not in outgoing.keys():
            _print_msg(message, project)
      except KeyError:
         _print_msg(message, project)
      try:
         message = "Invalid yaml option: {0}"
         for logic in config[project]["outgoing"]["logic"]:
            if logic in list(funcs.keys()):
               if type(config[project]["outgoing"]["logic"][logic]) is list:
                  for func in config[project]["outgoing"]["logic"][logic]:
                     if func not in funcs[logic]:
                        _print_msg(message, logic)
               else:
                  if logic not in funcs[logic]:
                     _print_msg(message, logic)
            else:
               _print_msg(message, logic)
      except KeyError:
         _print_msg(message, logic)

def runner(args):
   """
   Runner is the inital function that should be called to kick off all projects and launches them.

   Parameters
   ----------
   args: dict
      Arguments passed in at runtime
   """
   config = yaml_reader(args.yaml)
   config = traverse_replace_yaml_tree(config)
   config = recurse_replace_yaml(config,runtime_dict)
   validate_yaml(config)
   aborted_projects = {}
   for project in config:
      try:
         logger = Logger(project, sess, config[project]["logging"], args.v, args.dry)
      except KeyError:
         logger = Logger(project, sess, None, args.v, args.dry)
      proj = ProjectIO(project, logger.logger, args.dry, **config[project])
      errors = proj.run_pipeline(sess)
      if errors is not None:
         aborted_projects[project] = errors

   if len(aborted_projects) != 0:
      [print("Project: %s, reason: %s" % (key, val)) for key, val in aborted_projects.items()]
      
 
if __name__ == "__main__":
   """
   Intial entry to the program which gets the arguments and calls Runner
   """
   args = parse_cli()
   if args.skeleton:
      create_skeleton(args.skeleton)
   if args.version:
      print_version()
   runner(args)