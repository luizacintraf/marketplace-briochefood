# -*- coding: utf-8 -*-

#import libraries
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from database.models import Base

def create():
    """
    Cria os bancos de dados no modelo
    """
    engine = create_engine('sqlite:///briochefood.db', echo=True)
    Base.metadata.create_all(engine)