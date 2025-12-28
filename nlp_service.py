import importlib_metadata
import importlib.metadata
importlib.metadata.packages_distributions = importlib_metadata.packages_distributions

import os
import google.generativeai as genai
import sqlite3
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class NLPService:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            print("Warning: GOOGLE_API_KEY not found in environment variables.")
        genai.configure(api_key=self.api_key)
        # Using the direct library and the verified working model name from test_output.txt
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')

    def get_patient_context(self, bcno):
        conn = sqlite3.connect("patient_data.db")
        tables = ["patients", "clinicaldiagnosis", "examinations", "familyhistory", "investigations", "pasthistory", "surgery"]
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

    def generate_summary(self, bcno):
        context = self.get_patient_context(bcno)
        if not context:
            return "Patient data not found."
        
        prompt = f"You are a medical expert in Breast Cancer. Summarize the following patient data for a doctor. Focus on clinical diagnosis, stage, relevant investigations, and surgery details.\nPatient Data:\n{context}"
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e):
                return "The AI service is currently at its limit (Quota Exceeded). Please wait a minute and try again."
            return f"Error generating summary: {str(e)}"

    def ask_patient_question(self, bcno, question):
        context = self.get_patient_context(bcno)
        if not context:
            return "Patient data not found."
            
        prompt = f"You are a medical assistant for Breast Cancer doctors. Answer the doctor's question based on the provided patient data. If the data is not available, state that.\nPatient Data:\n{context}\n\nQuestion: {question}"
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e):
                return "The AI service is currently at its limit (Quota Exceeded). Please try again in 1 minute."
            return f"Error answering question: {str(e)}"
