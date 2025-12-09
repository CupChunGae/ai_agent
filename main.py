import os
import argparse
from google import genai
from dotenv import load_dotenv
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("Check API key is correct")

client = genai.Client(api_key = api_key)
def main():
    parser = argparse.ArgumentParser(description="Gemini")
    parser.add_argument("prompt", type=str, help="User prompt")
    args = parser.parse_args()
    messages = [types.Content(role = "user", parts = [types.Part(text = args.user_prompt)])]
    
    response = client.models.generate_content(model = "gemini-2.5-flash", contents = messages)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)


if __name__ == "__main__":
    main()
