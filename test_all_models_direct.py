import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def test_all_models():
    models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            models.append(m.name)
    
    print(f"Found {len(models)} models. Testing top ones...")
    
    for model_path in models[:10]: # Test first 10
        print(f"\nTesting: {model_path}")
        try:
            model = genai.GenerativeModel(model_path)
            response = model.generate_content("Hi")
            print(f"SUCCESS with {model_path}: {response.text}")
            return model_path
        except Exception as e:
            print(f"FAILED {model_path}: {e}")
            if "429" in str(e):
                print("Quota limit hit, waiting...")
                time.sleep(5)
    return None

if __name__ == "__main__":
    test_all_models()
