from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

class GroqLLM:
    def __init__(self):
        load_dotenv()
    
    def get_llm(self):
        try:
            os.environ['GROQ_API_KEY'] = self.groq_api_key = os.getenv('GROQ_API_KEY')
            llm = ChatGroq(api_key = self.groq_api_key,model = 'openai/gpt-oss-120b')
            print("Model is succefully loaded")
            return llm
        except Exception as e:
            raise ValueError(f"Could not load model, error occured with exception: {e}")
        