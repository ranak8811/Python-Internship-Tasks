import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

database = os.getenv("DB_NAME")

def import_csv_to_db():
    try:
        engine = create_engine(os.getenv("DATABASE_URL"))
        
        csv_file = "samsung_specs.csv"
        print(f"Reading {csv_file}...")
        df = pd.read_csv(csv_file)
        
        table_name = "mobile_specs"
        print(f"Writing to table '{table_name}' in database '{database}'...")

        # adding mobile specs to postgres database
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        
        print("Data imported successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import_csv_to_db()