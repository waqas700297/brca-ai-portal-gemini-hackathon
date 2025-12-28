from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import importlib_metadata
import importlib.metadata
importlib.metadata.packages_distributions = importlib_metadata.packages_distributions

load_dotenv()

def test_simple_ai():
    api_key = os.getenv("GOOGLE_API_KEY")
    # Try different model names
    models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro", "gemini-1.5-flash-latest"]
    
    for model_name in models:
        print(f"\n--- Testing model: {model_name} ---")
        try:
            llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)
            res = llm.invoke("Hello, are you working?")
            print(f"Success! Response: {res.content}")
            return model_name
        except Exception as e:
            print(f"Failed: {e}")
    return None

if __name__ == "__main__":
    test_simple_ai()
