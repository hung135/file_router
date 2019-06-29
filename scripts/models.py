import db
from sqlalchemy import Column, Integer, Text, TIMESTAMP
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

################################################################################
# Do this once at the top of the file (or better yet in a models.py so multiple scripts can use it)
################################################################################
engine = db.get_engine()
meta = db.get_metadata(engine, schema="test")
Session = sessionmaker(bind=engine)

# Defining new tables in the DB
DecBase = declarative_base(bind=engine, metadata=meta)
# class PathConfig(DecBase, db.Base):
#     __tablename__= "path_config"
#     id = Column(Integer, primary_key=True)
#     project_name = Column(Text)
#     inbound_directory = Column(Text)
#     out_directory = Column(Text)
class FileRouterHistory(DecBase, db.Base):
    __tablename__= "file_router_history"
    id = Column(Integer, primary_key=True)
    project_name = Column(Text)
    age = Column(Integer)
DecBase.metadata.create_all(engine) #Creates the tables in the DB if they don't exist


################################################################################
# Load the tables you want to work with
################################################################################

# Autoloading tables that are already defined in the DB
class FileRouter(db.Base):
   pass
mytable = db.load_table("test1", meta, id_col="tbl_id")
mapper(FileRouter, mytable)

# Print MyTable attributes
mytable_attributes = [attr for attr in dir(FileRouter) if not attr.startswith('__')]
print('FileRouter def:{}'.format(mytable_attributes))
