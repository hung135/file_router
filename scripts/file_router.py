# https://www.python.org/dev/peps/pep-0008/#imports
import os
import yaml
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# import db
# from models import Session
from projectio import ProjectIO
################################################################################
# This can go in your actual scripts
################################################################################
# Do this whenever you need a connection to the DB. (typically once at the top of your script)
#sess = Session()

def yaml_reader():
   try:
      with open("file_router.yaml", "r") as f:
         return yaml.safe_load(f)
   except FileNotFoundError as e:
      print(e)


if __name__ == "__main__":
   config = yaml_reader()
   projects = []
   for project in config:
      proj = ProjectIO(project, **config[project])
      proj.outgoing.rename_options(proj.incoming.files)
      # If we wanted to do something with it later
      projects.append(proj)

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
