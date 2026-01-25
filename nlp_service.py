import os
import json
import google.generativeai as genai
import requests
import sqlite3
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

CONFIG_FILE = "ai_config.json"

DEFAULT_SUMMARY_PROMPT = "You are a medical expert in Breast Cancer. Summarize the following patient data for a doctor. Focus on clinical diagnosis, stage, relevant investigations, and surgery details."

class NLPService:
    def __init__(self):
        self.config = self.load_config()
        self.setup_clients()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    config = json.load(f)
                    
                    # Migrate old config / Ensure 'prompts' section exists
                    if "prompts" not in config:
                        config["prompts"] = {
                            "summary_prompt": DEFAULT_SUMMARY_PROMPT
                        }
                        self.save_config(config)
                    elif "summary_prompt" not in config["prompts"]:
                         config["prompts"]["summary_prompt"] = DEFAULT_SUMMARY_PROMPT
                         self.save_config(config)

                    # Sync with environment variable if API key is missing or is a placeholder
                    api_key_val = config["providers"]["google"].get("apiKey")
                    if not api_key_val or api_key_val == "GOOGLE_API_KEY":
                        env_key = os.getenv("GOOGLE_API_KEY")
                        if env_key:
                            config["providers"]["google"]["apiKey"] = env_key
                            self.save_config(config)
                    return config
            except Exception as e:
                print(f"Error loading config: {e}")
        
        # Default config fallback
        default_config = {
            "selectedModel": "gemini-3-flash-preview",
            "providers": {
                "google": {"apiKey": os.getenv("GOOGLE_API_KEY") or "", "models": ["gemini-3-flash-preview", "gemini-3-pro-preview"]}
            },
            "prompts": {
                "summary_prompt": DEFAULT_SUMMARY_PROMPT
            }
        }
        return default_config

    def save_config(self, config):
        self.config = config
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
        self.setup_clients()

    def setup_clients(self):
        # Google Setup
        google_config = self.config["providers"]["google"]
        if google_config["apiKey"]:
            genai.configure(api_key=google_config["apiKey"])

    def get_patient_context(self, bcno):
        conn = sqlite3.connect("patient_data.db")
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

    def _generate_content(self, prompt):
        selected = self.config["selectedModel"]
        provider, model_name = selected.split(":")

        if provider == "google":
            model = genai.GenerativeModel(f"models/{model_name}")
            response = model.generate_content(prompt)
            return response.text
        return "Error: Unknown provider selected."

    def generate_summary(self, bcno):
        context = self.get_patient_context(bcno)
        if not context:
            return "Patient data not found."
        
        summary_instruction = self.config.get("prompts", {}).get("summary_prompt", DEFAULT_SUMMARY_PROMPT)
        prompt = f"{summary_instruction}\nPatient Data:\n{context}"
        
        try:
            return self._generate_content(prompt)
        except Exception as e:
            if "429" in str(e):
                return "The AI service is currently at its limit (Quota Exceeded). Please wait for some time and try again."
            return f"Error generating summary: {str(e)}"

    def ask_patient_question(self, bcno, question):
        context = self.get_patient_context(bcno)
        if not context:
            return "Patient data not found."
            
        prompt = f"You are a medical assistant for Breast Cancer doctors. Answer the doctor's question based on the provided patient data. If the data is not available, state that.\nPatient Data:\n{context}\n\nQuestion: {question}"
        
        try:
            return self._generate_content(prompt)
        except Exception as e:
            if "429" in str(e):
                return "The AI service is currently at its limit (Quota Exceeded). Please wait for some time and try again."
            return f"Error answering question: {str(e)}"