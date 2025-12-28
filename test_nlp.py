import importlib_metadata
import importlib.metadata
importlib.metadata.packages_distributions = importlib_metadata.packages_distributions

from nlp_service import NLPService
from dotenv import load_dotenv
import os

load_dotenv()

def test_nlp():
    nlp = NLPService()
    bcno = "U-0494" # Example BCNo from logs
    print(f"Testing for BCNo: {bcno}")
    
    try:
        context = nlp.get_patient_context(bcno)
        print("Context retrieved successfully.")
        print(f"Context length: {len(context)}")
        # print(context[:500]) # Don't print everything
        
        print("\nTesting Summary Generation...")
        summary = nlp.generate_summary(bcno)
        print("Summary generated:")
        print(summary)
        
        import time
        print("\nWaiting 5 seconds to avoid rate limit...")
        time.sleep(5)
        
        print("\nTesting Q&A...")
        answer = nlp.ask_patient_question(bcno, "What is the diagnosis?")
        print("Answer:")
        print(answer)
        
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    test_nlp()
