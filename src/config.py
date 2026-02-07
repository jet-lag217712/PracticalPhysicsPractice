import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY_1 = os.getenv("GROQ_API_KEY_1")
GROQ_API_KEY_2 = os.getenv("GROQ_API_KEY_2")
GROQ_API_KEY_3 = os.getenv("GROQ_API_KEY_3")
GROQ_API_KEY_4 = os.getenv("GROQ_API_KEY_4")
GROQ_API_KEYS = [GROQ_API_KEY_1, GROQ_API_KEY_2, GROQ_API_KEY_3, GROQ_API_KEY_4]

GOOGLE_API_KEY_1 = os.getenv("GOOGLE_API_KEY_1")
GOOGLE_API_KEY_2 = os.getenv("GOOGLE_API_KEY_2")
GOOGLE_API_KEYS = [GOOGLE_API_KEY_1,GOOGLE_API_KEY_2]

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
AUTH = [EMAIL,PASSWORD]