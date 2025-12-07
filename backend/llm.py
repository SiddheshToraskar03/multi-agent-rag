# backend/llm.py

import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    raise ValueError(
        "GEMINI_API_KEY is not set. "
        "Please set it in a .env file or as an environment variable. "
        "Create a .env file in the project root with: GEMINI_API_KEY=your-api-key"
    )


def call_llm(system_prompt: str, user_prompt: str) -> str:
    """
    Call Gemini API with system and user prompts.
    
    Args:
        system_prompt: System instruction prompt
        user_prompt: User question/input prompt
        
    Returns:
        Generated text response from Gemini
    """
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Combine system and user prompts
    full_prompt = f"{system_prompt}\n\n{user_prompt}"
    
    response = model.generate_content(full_prompt)
    return response.text

