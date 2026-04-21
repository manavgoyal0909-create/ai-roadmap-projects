from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

# Connect to Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Make your first AI call
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "What is artificial intelligence in 2 lines?"}
    ]
)

# Print the response
print("AI Response:")
print(response.choices[0].message.content)