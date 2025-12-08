import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ,get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("Check API key is correct")

client = genai.Client(api_key = api_key)
def main():
    print("Hello from ai-agent!")


if __name__ == "__main__":
    main()
