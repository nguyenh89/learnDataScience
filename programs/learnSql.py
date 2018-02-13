# this program reads a csv file to an sql database
from time import time
from sqlalchemy import Column, Integer, Float, Date, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, inspect, MetaData, Table
from sqlalchemy.orm import sessionmaker
import pymysql
import csv
import pandas as pd

#access database and display the tables in the database
engine = create_engine('mysql+pymysql://hangnguyen:hangtest@localhost/study')

inspector=inspect(engine)
engine.table_names()
print(inspector.get_table_names())
print(inspector.get_columns('example'))

metadata=MetaData()
grade=Table('grade', metadata,autoload=True, autoload_with=engine)
print(repr(grade))

# create new base class

Base = declarative_base()
class politician(Base):
    #Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
    __tablename__ = 'politicians'
    __table_args__ = {'sqlite_autoincrement': True}
    #tell SQLAlchemy the name of column and its attributes:
    birth_date = Column(String(60))
    id = Column(String(250), primary_key=True, nullable=False)
    name = Column(String(250))
    fromfile=Column(String(250))


#check that table is created
politician.__table__

# create new table in database and check table names
Base.metadata.create_all(engine)
engine.table_names()

# start a new session

session = sessionmaker()
session.configure(bind=engine)
s = session()

# read csv file and insert into sql database

file_name = "/Users/daithang1111/Documents/datasets/everypolitician.csv" 

everypolitician = pd.read_csv(file_name, encoding='latin1')  

everypolitician1= everypolitician[['birth_date','id','name','fromfile']]

everypolitician1.to_sql('politicians', engine, index=False,if_exists='replace')

# connect to engine and run some sql queries

# get records with Null birth_date
connection=engine.connect()
stmt='select name, fromfile from politicians \
      where birth_date is null'
result = connection.execute(stmt).fetchall()
print (result[0:10])
# create new column and update that column
connection.execute('alter table politicians\
        add column country varchar(250);')

connection.execute('update politicians\
                    set country=Substring_index(fromfile,"-",1);')

#get a list of distinct countries
result= connection.execute('select distinct country from politicians').fetchall()
result



