import datetime
from sqlalchemy import Column, Integer, Text, TIMESTAMP, String, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .db import get_engine, get_metadata, Base

################################################################################
# Do this once at the top of the file (or better yet in a models.py so multiple scripts can use it)
################################################################################
engine = get_engine()
meta = get_metadata(engine, schema="switchboard")
meta_logging = get_metadata(engine, schema="logging")
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
class FileRouterHistory(DecBase, Base):
    __tablename__= "switchboard_history"
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
class ErrorLog(DecBase_logging, Base):
    __tablename__= "error_log"
    error_log_id =Column(Integer, primary_key=True)
    program_unit =Column(String(128)) 
    error_code =Column(String(5))  
    error_timestamp  =Column(DateTime, default=datetime.datetime.utcnow)
    user_name =Column(String(32))  
    error_message =Column(String(2000))  
    sql_statement =Column(String(2000)) 

class Logging(DecBase_logging, Base):
    __tablename__ = "load_status"
    load_status_id = Column(Integer, primary_key=True)
    program_unit = Column(String(128))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    program_unit_type_code = Column(String(25))
    file_path = Column(String(2000))
    created_by = Column(String(25)

    def __init__(self, project_name=None, level=None, msg=None):
        self.program_unit = project_name
        self.program_unit_type_code = level
        self.file_path = msg

#DecBase_logging.metadata.create_all(engine)
# load_status_id integer NOT NULL DEFAULT nextval('logging.load_status_id_seq'::regclass),
#     table_name character varying(64) COLLATE pg_catalog."default" NOT NULL,
#     program_unit character varying(128) COLLATE pg_catalog."default" NOT NULL,
#     program_unit_type_code character varying(10) COLLATE pg_catalog."default" NOT NULL,
#     file_path text COLLATE pg_catalog."default" NOT NULL,
#     success character(1) COLLATE pg_catalog."default" NOT NULL,
#     start_date timestamp without time zone NOT NULL,
#     end_date timestamp without time zone NOT NULL,
#     previous_record_count bigint NOT NULL,
#     current_record_count bigint NOT NULL,
#     records_inserted integer NOT NULL,
#     records_updated integer NOT NULL,
#     records_deleted integer NOT NULL,
#     created_by character varying(32) COLLATE pg_catalog."default" NOT NULL,
#     created_date timestamp without time zone NOT NULL,