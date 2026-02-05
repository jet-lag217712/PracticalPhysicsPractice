import os
from dotenv import load_dotenv

load_dotenv()
API_KEY_1 = os.getenv("API_KEY_1")
API_KEY_2 = os.getenv("API_KEY_2")

API_KEYS = [API_KEY_1, API_KEY_2]