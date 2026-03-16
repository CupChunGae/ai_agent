import os
import argparse
from google import genai
from dotenv import load_dotenv
from google.genai import types
from prompts import system_prompt
from functions.call_functions import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("Check if API key is correct")

client = genai.Client(api_key = api_key)
def main():
    parser = argparse.ArgumentParser(description="Gemini")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    for _ in range(20):
    
        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = messages,
            config = types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0)
            ,)
        
        if response.candidates is not None:
            for candidate in response.candidates:
                if candidate.content and candidate.content.parts:
                    #print(f"DEBUG candidate content: {candidate.content}")
                    messages.append(candidate.content)
        
        if args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        function_results = []
        
        if response.function_calls is not None:
            for item in response.function_calls:
                function_call_result = call_function(item, args.verbose)
                if not function_call_result.parts:
                    raise Exception (".parts list is empty.")
                
                if function_call_result.parts[0].function_response is None:
                    raise Exception ("Missing FunctionResponse Object")
                
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception ("function_response.response is missing.")
                
                function_results.append(function_call_result.parts[0])
                
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        
        messages.append(types.Content(role="user", parts=function_results))
    
        #print(f"DEBUG function_calls: {response.function_calls}")
        #print(f"DEBUG text: {response.text}")    
        if not response.function_calls:
            for candidate in reversed(response.candidates):
                if candidate.content and candidate.content.parts:
                    final_text = response.candidates[-1].content.parts[0].text
                    if final_text:
                        print("Final response: ")
                        print(final_text)
                        return
                    
    print("Max attempts reached without finishing")


if __name__ == "__main__":
    main()
