import db
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

################################################################################
# Do this once at the top of the file (or better yet in a models.py so multiple scripts can use it)
################################################################################
engine = db.get_engine()
meta = db.get_metadata(engine, schema="myschema")
Session = sessionmaker(bind=engine)

# Autoloading tables that are already defined in the DB
class MyTable(db.Base):
   pass
mytable = db.load_table("mytable", meta, id_col="id")
mapper(MyTable, mytable)

# Print MyTable attributes
mytable_attributes = [attr for attr in dir(MyTable) if not attr.startswith('__')]
print('MyTable def:{}'.format(mytable_attributes))

# Defining new tables in the DB
DecBase = declarative_base(bind=engine, metadata=meta)
class Person(DecBase, db.Base):
    __tablename__= "people"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    age = Column(Integer)
DecBase.metadata.create_all(engine) #Creates the tables in the DB if they don't exist

################################################################################
# This can go in your actual scripts
################################################################################
# Do this whenever you need a connection to the DB. (typically once at the top of your script)
sess = Session()

# Querying
for rec in sess.query(Person).filter(Person.name == "John"):
   print(rec)

# Adding
new_rec = Person(name="Bob", age=21)
sess.add(new_rec)
sess.commit()

# Updating from object
for rec in sess.query(Person).filter(Person.name == "John"):
   rec.age = 40
   sess.add(rec)
   sess.commit()

# Update query
update_query = Person.__table__.update().where(Person.name == "John").values(age=40)
sess.execute(update_query)
