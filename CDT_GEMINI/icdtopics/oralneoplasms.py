"""
Module for extracting oral neoplasms ICD-10 codes.
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
 
def create_oral_neoplasms_extractor(temperature=0.0):
    """
    Create a LangChain-based oral neoplasms code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template="""
You are a highly experienced medical coding expert specializing in oral neoplasms. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

13.1 Malignant Neoplasms:
- C00.0: Malignant neoplasm of external upper lip
- C00.1: Malignant neoplasm of external lower lip
- C00.2: Malignant neoplasm of external lip, unspecified
- C00.3: Malignant neoplasm of upper lip, inner aspect
- C00.4: Malignant neoplasm of lower lip, inner aspect
- C00.5: Malignant neoplasm of lip, unspecified, inner aspect
- C00.6: Malignant neoplasm of commissure of lip, unspecified
- C00.8: Malignant neoplasm of overlapping sites of lip
- C00.9: Malignant neoplasm of lip, unspecified

13.2 Benign Neoplasms:
- D10.0: Benign neoplasm of lip
- D10.1: Benign neoplasm of tongue
- D10.2: Benign neoplasm of floor of mouth
- D10.30: Benign neoplasm of unspecified part of mouth
- D10.39: Benign neoplasm of other parts of mouth
- D10.4: Benign neoplasm of tonsil
- D10.5: Benign neoplasm of other parts of oropharynx
- D10.6: Benign neoplasm of nasopharynx
- D10.7: Benign neoplasm of hypopharynx
- D10.9: Benign neoplasm of pharynx, unspecified

13.3 Neoplasms of Uncertain Behavior:
- D37.01: Neoplasm of uncertain behavior of lip
- D37.02: Neoplasm of uncertain behavior of tongue
- D37.04: Neoplasm of uncertain behavior of minor salivary glands
- D37.05: Neoplasm of uncertain behavior of pharynx
- D37.09: Neoplasm of uncertain behavior of other specified sites of the oral cavity

Scenario: {{scenario}}

{prompt}
""",
        input_variables=["scenario", "prompt"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template.partial(prompt=PROMPT))

def extract_oral_neoplasms_code(scenario, temperature=0.0):
    """
    Extract oral neoplasms code(s) for a given scenario.
    """
    try:
        chain = create_oral_neoplasms_extractor(temperature)
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
        print(f"Error in extract_oral_neoplasms_code: {str(e)}")
        return ""

def activate_oral_neoplasms(scenario):
    """
    Activate oral neoplasms analysis and return results.
    """
    try:
        return extract_oral_neoplasms_code(scenario)
    except Exception as e:
        print(f"Error in activate_oral_neoplasms: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient presents with a benign growth on the tongue."
    result = activate_oral_neoplasms(scenario)
    print(result)
