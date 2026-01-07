from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import pandas as pd
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import importlib_metadata
import importlib.metadata
importlib.metadata.packages_distributions = importlib_metadata.packages_distributions

import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS setup for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_NAME = "patient_data.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

class PatientSummary(BaseModel):
    BCNo: str
    PatientName: str
    Age: Optional[int]
    Gender: Optional[str]
    Stage: Optional[str]
    Diagnosis: Optional[str]

@app.get("/")
def read_root():
    return {"message": "BrCa AI Analysis API is running"}

@app.get("/patients", response_model=List[PatientSummary])
def get_patients(search: Optional[str] = None):
    conn = get_db_connection()
    if search:
        query = """
        SELECT p.BCNo, p.PatientName, p.Age, p.Gender, cd.Stage, cd.FinalClinicalDiagnosis as Diagnosis
        FROM patients p
        LEFT JOIN clinicaldiagnosis cd ON p.BCNo = cd.BCNo
        WHERE p.PatientName LIKE ? OR p.BCNo LIKE ?
        LIMIT 100
        """
        params = (f"%{search}%", f"%{search}%")
        df = pd.read_sql_query(query, conn, params=params)
    else:
        query = """
        SELECT p.BCNo, p.PatientName, p.Age, p.Gender, cd.Stage, cd.FinalClinicalDiagnosis as Diagnosis
        FROM patients p
        LEFT JOIN clinicaldiagnosis cd ON p.BCNo = cd.BCNo
        LIMIT 100
        """
        df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient="records")

@app.get("/patient/{bcno}")
def get_patient_details(bcno: str):
    conn = get_db_connection()
    tables = ["patients", "clinicaldiagnosis", "examinations", "familyhistory", "followup", "investigations", "pasthistory", "surgery"]
    details = {}
    for table in tables:
        query = f"SELECT * FROM {table} WHERE BCNo = ?"
        df = pd.read_sql_query(query, conn, params=(bcno,))
        details[table] = df.to_dict(orient="records")
    conn.close()
    return details

from nlp_service import NLPService

nlp = NLPService()

class QuestionRequest(BaseModel):
    bcno: str
    question: str

@app.get("/summary/{bcno}")
def get_summary(bcno: str):
    print(f"Generating summary for patient: {bcno}")
    try:
        summary = nlp.generate_summary(bcno)
        print(f"Summary generated successfully for {bcno}")
        return {"summary": summary}
    except Exception as e:
        print(f"Error in get_summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
def ask_question(request: QuestionRequest):
    print(f"Question for patient {request.bcno}: {request.question}")
    try:
        answer = nlp.ask_patient_question(request.bcno, request.question)
        print(f"Answer generated for {request.bcno}")
        return {"answer": answer}
    except Exception as e:
        print(f"Error in ask_question: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/config")
def get_config():
    return nlp.config

@app.post("/config")
def save_config(config: Dict[str, Any]):
    try:
        nlp.save_config(config)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
