from mcp.server.fastmcp import FastMCP
import sqlite3
import pandas as pd
import os
import google.genai as genai
from dotenv import load_dotenv
from typing import List, Optional

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("BrCa AI Analysis")

# Database configuration
DB_NAME = "patient_data.db"

# AI configuration
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    client = genai.Client(api_key=api_key)
    # Using the verified working model name from nlp_service.py
    model_name = 'gemini-3-flash-preview'
else:
    client = None
    print("Warning: GOOGLE_API_KEY not found in environment variables.")

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def get_patient_context(bcno: str) -> str:
    """Helper to get patient context for AI tools."""
    conn = get_db_connection()
    # Fixed table list from nlp_service.py
    tables = ["PatientCaseSummaryReport"]
    context = ""
    for table in tables:
        query = f"SELECT * FROM {table} WHERE BCNo LIKE ?"
        df = pd.read_sql_query(query, conn, params=(bcno,))
        if not df.empty:
            context += f"\n### Table: {table}\n"
            context += df.head(20).to_string(index=False)
            context += "\n"
    conn.close()
    return context[:10000]

@mcp.tool()
def list_patients(search: Optional[str] = None) -> List[dict]:
    """
    Search for patients by name or BCNo. Returns a list of patient summaries.
    
    Args:
        search: Optional search term (name or BCNo). If None, returns the first 100 patients.
    """
    conn = get_db_connection()
    if search:
        query = """
        SELECT * 
        FROM PatientCaseSummaryReport
        WHERE PatientName LIKE ? OR BCNo LIKE ?
        LIMIT 100
        """
        params = (f"%{search}%", f"%{search}%")
        df = pd.read_sql_query(query, conn, params=params)
    else:
        query = """
        SELECT * 
        FROM PatientCaseSummaryReport
        LIMIT 100
        """
        df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient="records")

@mcp.tool()
def get_patient_details(bcno: str) -> dict:
    """
    Retrieve comprehensive data for a specific patient across all clinical categories.
    
    Args:
        bcno: The unique Patient ID (BCNo).
    """
    conn = get_db_connection()
    tables = ["PatientCaseSummaryReport"]
    details = {}
    for table in tables:
        query = f"SELECT * FROM {table} WHERE BCNo = ?"
        df = pd.read_sql_query(query, conn, params=(bcno,))
        details[table] = df.to_dict(orient="records")
    conn.close()
    return details

@mcp.tool()
def generate_summary(bcno: str) -> str:
    """
    Generate an AI-powered clinical summary for a doctor.
    
    Args:
        bcno: The unique Patient ID (BCNo).
    """
    if not client:
        return "AI model not initialized. Check GOOGLE_API_KEY."
    
    context = get_patient_context(bcno)
    if not context:
        return f"Patient data for {bcno} not found."
    
    prompt = f"You are a medical expert in Breast Cancer. Summarize the following patient data for a doctor. Focus on clinical diagnosis, stage, relevant investigations, and surgery details.\nPatient Data:\n{context}"
    
    try:
        response = client.models.generate_content(model=model_name, contents=prompt)
        return response.text
    except Exception as e:
        if "429" in str(e):
            return "The AI service is currently at its limit (Quota Exceeded). Please wait a minute and try again."
        return f"Error generating summary: {str(e)}"

@mcp.tool()
def ask_patient_question(bcno: str, question: str) -> str:
    """
    Answer specific medical questions based on the provided patient data.
    
    Args:
        bcno: The unique Patient ID (BCNo).
        question: The doctor's question about the patient.
    """
    if not client:
        return "AI model not initialized. Check GOOGLE_API_KEY."

    context = get_patient_context(bcno)
    if not context:
        return f"Patient data for {bcno} not found."
        
    prompt = f"You are a medical assistant for Breast Cancer doctors. Answer the doctor's question based on the provided patient data. If the data is not available, state that.\nPatient Data:\n{context}\n\nQuestion: {question}"
    
    try:
        response = client.models.generate_content(model=model_name, contents=prompt)
        return response.text
    except Exception as e:
        if "429" in str(e):
            return "The AI service is currently at its limit (Quota Exceeded). Please try again in 1 minute."
        return f"Error answering question: {str(e)}"

if __name__ == "__main__":
    mcp.run()