import os
import yaml
import argparse
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# import db
# from models import Session
from projectio import ProjectIO
from models import FileRouterHistory, Session
################################################################################
# This can go in your actual scripts
################################################################################
# Do this whenever you need a connection to the DB. (typically once at the top of your script)
sess = Session()

def yaml_reader(yaml_path=None):
   file_path=yaml_path or "file_router.yaml"
   try:
      with open(file_path, "r") as f:
         return yaml.safe_load(f)
   except FileNotFoundError as e:
      print(e)


def parse_cli():
   parser = argparse.ArgumentParser(description='Process a yaml file')
   parser.add_argument("--yaml", help="Location of the yaml file")
   parser.add_argument("--skeleton", help="Generates a skeleton.yaml file to the directory specified")
   args = parser.parse_args()
   return args 

def create_skeleton(path):
   example = {
      "project_name1": {
         "incoming": {
            "path": "<string>",
            "file_pathern": ["glob style of target file; i.e.: *.zip", "file_pathern_2"]
         }, 
         "outgoing": {
            "path": "<string>",
            "rename_options": ["rename_option1", "rename_option2"],
            "file_path_extract": "(\\d\\d\\d\\d)"
         }
      },
      "project_name2": {
         "incoming": {
            "path": "<string>",
            "file_pathern": ["glob style of target file; i.e.: *.zip", "file_pathern_2"]
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
      proj = ProjectIO(project, **config[project])
      proj.run_pipeline(sess)
      # proj.incoming.save_all(sess)
      # proj.incoming.files, proj.incoming.mappings = proj.outgoing.rename(proj.incoming.files)
      # proj.outgoing.file_history(proj.incoming, sess)
      # proj.outgoing.move_files(proj.incoming.files)
      projects.append(proj)

 
if __name__ == "__main__":
   args = parse_cli()
   if args.skeleton:
      create_skeleton(args.skeleton)
   runner(args)

# # Querying
# for rec in sess.query(PathConfig):
#    print(rec)

# # Adding
# new_rec = PathConfig(name="Bob", age=21)
# sess.add(new_rec)
# sess.commit()

# # Updating from object
# for rec in sess.query(Person).filter(Person.name == "John"):
#    rec.age = 40
#    sess.add(rec)
#    sess.commit()

# # Update query
# update_query = Person.__table__.update().where(Person.name == "John").values(age=40)
# sess.execute(update_query)
