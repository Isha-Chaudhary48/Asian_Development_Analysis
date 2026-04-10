import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv('DB_URL'))
def get_engine():
    return engine

def upload_data():
    df = pd.read_csv('Data/world_bank_cleaned.csv')
    df.to_sql('World_Bank',engine,if_exists = 'replace',index = False)
    print(f"Uploaded {df.shape[0]} rows,{df.shape[1]}columns")

if __name__ == '__main__':
    upload_data()
    
    