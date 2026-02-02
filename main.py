import os

from groq import Groq
from dotenv import load_dotenv

# Gets API Key
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Groq Initialize
client = Groq(api_key=API_KEY)

output = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
      {
        "role": "system",
        "content": "Output ONLY the correct answer number"
      },
      {
        "role": "user",
        "content": """
        
        """
      }
    ],
    temperature=1,
    max_completion_tokens=512,
    top_p=1,
    stream=False,
    stop=None
)

answer = output.choices[0].message.content
answer = int(answer)
print(answer-1)