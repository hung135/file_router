import db
from sqlalchemy import Column, Integer, Text, TIMESTAMP, String, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

################################################################################
# Do this once at the top of the file (or better yet in a models.py so multiple scripts can use it)
################################################################################
engine = db.get_engine()
meta = db.get_metadata(engine, schema="file_router")
meta_logging = db.get_metadata(engine, schema="logging")
Session = sessionmaker(bind=engine)
 
# Defining new tables in the DB
DecBase = declarative_base(bind=engine, metadata=meta)
DecBase_logging = declarative_base(bind=engine, metadata=meta_logging)
# class PathConfig(DecBase, db.Base):
#     __tablename__= "path_config"
#     id = Column(Integer, primary_key=True)
#     project_name = Column(Text)
#     inbound_directory = Column(Text)
#     out_directory = Column(Text)
class FileRouterHistory(DecBase, db.Base):
    __tablename__= "file_router_history"
    id = Column(Integer, primary_key=True)
    project_name = Column(String(32))
    incoming_path = Column(Text)
    outgoing_path = Column(Text)
    file_date = Column(String(32))
    file_md5 = Column(String(32))
    file_size = Column(Integer)
    file_path_extract = Column(String(32))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
# DecBase.metadata.create_all(engine) #Creates the tables in the DB if they don't exist
class ErrorLog(DecBase_logging,db.Base):
    __tablename__= "errorlog"
    error_log_id =Column(Integer, primary_key=True)
    program_unit =Column(String(128)) 
    error_code =Column(String(5))  
    error_timestamp  =Column(DateTime, default=datetime.datetime.utcnow)
    user_name =Column(String(32))  
    sql_statement =Column(String(2000)) 

################################################################################
# Load the tables you want to work with
################################################################################

# # Autoloading tables that are already defined in the DB
# class FileRouter(db.Base):
#    pass
# mytable = db.load_table("test1", meta, id_col="tbl_id")
# mapper(FileRouter, mytable)

# # Print MyTable attributes
# mytable_attributes = [attr for attr in dir(FileRouter) if not attr.startswith('__')]
# print('FileRouter def:{}'.format(mytable_attributes))
