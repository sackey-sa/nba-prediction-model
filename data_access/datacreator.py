""" This file creates the tables we defined in models """
from data_access.database import engine
from data_access.models import Base


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
print("Tables created.")
