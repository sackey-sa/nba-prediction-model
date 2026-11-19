""" Database Connection SetUp File"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()
password = os.getenv("DB_PASSWORD")


engine = create_engine(f"mysql+pymysql://root:{password}@127.0.0.1:3306/nba_prediction_analysis",echo=True)

SESSION_LOCAL = sessionmaker(bind=engine)
