from sqlalchemy import create_engine, text
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))

def get_phone_by_model(model_name):
    query = text("""
    SELECT * FROM mobile_specs
    WHERE LOWER("Model") LIKE LOWER(:model_name)
    """)
    with engine.connect() as conn:
        return pd.read_sql(query, conn, params={"model_name": f"%{model_name}%"})

def get_all_phones():
    with engine.connect() as conn:
        return pd.read_sql(text('SELECT * FROM mobile_specs'), conn)
