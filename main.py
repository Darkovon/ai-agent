import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    args = sys.argv[1:]
    if not args:
        print("Error: please provide prompt")
        sys.exit(1)

    if "--verbose" in args:
        args.remove("--verbose")
        user_prompt = " ".join(args)
        messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]
        generate_content(client, messages, user_prompt, True)
    else:
        user_prompt = " ".join(args)
        messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]
        generate_content(client, messages)

def generate_content(client, messages, user_prompt="", flags=False):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    if flags:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()
