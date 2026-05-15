import os
from dotenv import load_dotenv

load_dotenv()

def get_groq_key():
    return os.getenv("GROQ_API_KEY")

def get_tavily_key():
    return os.getenv("TAVILY_API_KEY")
