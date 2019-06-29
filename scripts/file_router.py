import db
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import models
from models import   Session
import yaml
from utils import getListOfFiles
import os
################################################################################
# This can go in your actual scripts
################################################################################
# Do this whenever you need a connection to the DB. (typically once at the top of your script)
sess = Session()
yaml_config=None


with open('file_router.yaml','r') as f:
   yaml_config=yaml.safe_load(f)


for i in yaml_config:
   print(i,"----------------------")
   incoming=i['incoming']
   path=os.path.abspath(incoming['path'])
   list_of_files=getListOfFiles(path)
   outgoing=i['outgoing']
   #walk_dir(incoming)
   #move_dir(outgoing)

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
