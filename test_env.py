from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("GROQ_API_KEY")

if key:
    print("✅ Key loaded successfully!")
    print(f"First 8 characters: {key[:8]}...")
else:
    print("❌ Key not found - check your .env file")