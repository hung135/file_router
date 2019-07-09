import os
import sqlalchemy
from sqlalchemy import Column, Integer, MetaData, Table

def get_engine(env=None, echo=False):
    if env is None:
        env = os.environ
    database = "postgresql+psycopg2://{user}:{password}@{database}:{port}".format(
        user=env["PGUSER"],
        password=env["PGPASSWORD"],
        database=env["PGHOST"],
        port=env["PGPORT"],
    )
    connect_args={'sslmode':env.get("PGSSLMODE",None)}
    return sqlalchemy.create_engine(database, connect_args=connect_args, echo=echo)

def get_metadata(engine=None, **kwargs):
    """get MetaData object. Any extra args are passed right to the MetaData constructor
    For instance, if you want to use a particular schema, use get_metadata(schema='myschema')"""
    if engine is None:
        engine = get_engine()
    meta = MetaData(bind=engine, **kwargs)
    return meta

def load_table(name, meta, id_col=None):
    """autoload a table/view.
    If it is a view, sqlalchemy does not know which column to use as the ID field,
    so you need to pass it in as id_col, which can either be a string or a Column"""
    if id_col is not None and isinstance(id_col, str):
        id_col = Column(id_col, Integer, primary_key=True)
        table = Table(name, meta, id_col, autoload=True)
    else:
        table = Table(name, meta, autoload=True)
    return table

class Base(object):
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
