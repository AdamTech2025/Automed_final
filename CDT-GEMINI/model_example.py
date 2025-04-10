"""
Example script demonstrating how to use different models in different files.

This file shows how you can set a specific model for a particular file,
which will only affect the LLM calls made from this file.
"""

import os
from dotenv import load_dotenv
from llm_services import get_llm_service, set_model_for_file, set_temperature_for_file

# Load environment variables
load_dotenv()

def main():
    # Get the default LLM service and show current settings
    llm_service = get_llm_service()
    print(f"Default model: {llm_service.gemini_model}")
    print(f"Default temperature: {llm_service.temperature}")
    
    # Change the model for this file only
    if set_model_for_file("gemini-1.5-flash"):
        print("Successfully changed model to gemini-1.5-flash")
    
    # Change the temperature for this file only
    if set_temperature_for_file(0.7):
        print("Successfully changed temperature to 0.7")
    
    # Show updated settings
    llm_service = get_llm_service()
    print(f"Updated model: {llm_service.gemini_model}")
    print(f"Updated temperature: {llm_service.temperature}")
    
    print("\nUsage instructions:")
    print("1. Import set_model_for_file from llm_services")
    print("2. Call set_model_for_file('your-model-name') at the top of your file")
    print("3. All LLM calls from this file will use the specified model")
    print("4. Other files will continue to use the default model from .env")
    print("5. You can also use set_temperature_for_file(0.5) to change temperature")

if __name__ == "__main__":
    main() 