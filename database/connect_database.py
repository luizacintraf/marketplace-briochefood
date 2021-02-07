# -*- coding: utf-8 -*-

#import libraries
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.models import *

#create engine
engine = create_engine('sqlite:///briochefood.db', echo=False)

#create session
Session = sessionmaker(bind=engine)

session = Session()