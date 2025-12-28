import pandas as pd
import sqlite3
import os

DB_NAME = "patient_data.db"
DATASOURCE_DIR = "Datasource"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    
    # List of files to import
    files = [
        "patients.csv",
        "clinicaldiagnosis.csv",
        "examinations.csv",
        "familyhistory.csv",
        "followup.csv",
        "investigations.csv",
        "pasthistory.csv",
        "surgery.csv"
    ]
    
    for file_name in files:
        file_path = os.path.join(DATASOURCE_DIR, file_name)
        if os.path.exists(file_path):
            print(f"Importing {file_name}...")
            # Using low_memory=False to handle mixed types
            df = pd.read_csv(file_path, low_memory=False)
            table_name = file_name.split('.')[0]
            df.to_sql(table_name, conn, if_exists='replace', index=False)
        else:
            print(f"Warning: {file_path} not found.")
            
    conn.close()
    print("Database initialization complete.")

if __name__ == "__main__":
    init_db()
