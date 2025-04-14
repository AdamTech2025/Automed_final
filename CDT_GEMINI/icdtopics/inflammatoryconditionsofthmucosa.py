"""
Module for extracting inflammatory conditions of the oral mucosa ICD-10 codes.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from icdtopics.prompt import PROMPT

# Load environment variables
load_dotenv()

# Get model name from environment variable, default to gpt-4o if not set
 
def create_inflammatory_mucosa_conditions_extractor(temperature=0.0):
    """
    Create a LangChain-based inflammatory conditions of the oral mucosa code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template="""
You are a highly experienced medical coding expert specializing in inflammatory conditions of the oral mucosa. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

8.1 Inflammatory Conditions of the Oral Mucosa:
- K12.0: Recurrent oral aphthae
- K12.1: Other forms of stomatitis
- K12.2: Cellulitis and abscess of mouth
- K12.30: Oral mucositis (ulcerative), unspecified
- K12.31: Oral mucositis (ulcerative) due to antineoplastic therapy
- K12.32: Oral mucositis (ulcerative) due to other drugs
- K12.33: Oral mucositis (ulcerative) due to radiation
- K12.39: Other oral mucositis (ulcerative)

Scenario: {{scenario}}

{prompt}
""",
        input_variables=["scenario", "prompt"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template.partial(prompt=PROMPT))

def extract_inflammatory_mucosa_conditions_code(scenario, temperature=0.0):
    """
    Extract inflammatory conditions of the oral mucosa code(s) for a given scenario.
    """
    try:
        chain = create_inflammatory_mucosa_conditions_extractor(temperature)
        result = chain.invoke({"scenario": scenario})
        # Handle different return formats from LangChain
        if isinstance(result, dict):
            if "text" in result:
                result_text = result["text"]
            elif "output_text" in result:
                result_text = result["output_text"]
            else:
                result_text = str(result)
        elif hasattr(result, "content"):
            result_text = result.content
        else:
            result_text = str(result)
        
        print(f"Result: {result_text}")
        return result_text.strip()
    except Exception as e:
        print(f"Error in extract_inflammatory_mucosa_conditions_code: {str(e)}")
        return ""

def activate_inflammatory_mucosa_conditions(scenario):
    """
    Activate inflammatory conditions of the oral mucosa analysis and return results.
    """
    try:
        return extract_inflammatory_mucosa_conditions_code(scenario)
    except Exception as e:
        print(f"Error in activate_inflammatory_mucosa_conditions: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient presents with recurrent canker sores in the mouth."
    result = activate_inflammatory_mucosa_conditions(scenario)
    print(result)
