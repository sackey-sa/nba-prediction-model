""" This file creates the tables we defined in models """
from database import engine
from models import Base

Base.metadata.create_all(engine)
print("Tables created.")