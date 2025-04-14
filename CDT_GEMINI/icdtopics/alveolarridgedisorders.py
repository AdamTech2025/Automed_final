"""
Module for extracting alveolar ridge disorders ICD-10 codes.
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
 
def create_alveolar_ridge_disorders_extractor(temperature=0.0):
    """
    Create a LangChain-based alveolar ridge disorders code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template="""
You are a highly experienced medical coding expert specializing in alveolar ridge disorders. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

6.1 Atrophy of Alveolar Ridge:
- K08.20: Unspecified atrophy of edentulous alveolar ridge
- K08.21: Minimal atrophy of the mandible
- K08.22: Moderate atrophy of the mandible
- K08.23: Severe atrophy of the mandible
- K08.24: Minimal atrophy of maxilla
- K08.25: Moderate atrophy of the maxilla
- K08.26: Severe atrophy of the maxilla

6.2 Alveolar Anomalies:
- M26.71: Alveolar maxillary hyperplasia
- M26.72: Alveolar mandibular hyperplasia
- M26.73: Alveolar maxillary hypoplasia
- M26.74: Alveolar mandibular hypoplasia
- M26.79: Other specified alveolar anomalies

Scenario: {{scenario}}

{prompt}
""",
        input_variables=["scenario", "prompt"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template.partial(prompt=PROMPT))

def extract_alveolar_ridge_disorders_code(scenario, temperature=0.0):
    """
    Extract alveolar ridge disorders code(s) for a given scenario.
    """
    try:
        chain = create_alveolar_ridge_disorders_extractor(temperature)
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
        print(f"Error in extract_alveolar_ridge_disorders_code: {str(e)}")
        return ""

def activate_alveolar_ridge_disorders(scenario):
    """
    Activate alveolar ridge disorders analysis and return results.
    """
    try:
        return extract_alveolar_ridge_disorders_code(scenario)
    except Exception as e:
        print(f"Error in activate_alveolar_ridge_disorders: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient presents with moderate bone loss in the upper jaw following tooth loss."
    result = activate_alveolar_ridge_disorders(scenario)
    print(result)
