"""
Module for extracting social determinants of health ICD-10 codes.
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
 
def create_social_determinants_extractor(temperature=0.0):
    """
    Create a LangChain-based social determinants of health code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template="""
You are a highly experienced medical coding expert specializing in social determinants of health. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

17.1 Social Determinants of Health:
- Z55.0: Illiteracy and low-level literacy
- Z55.3: Underachievement in school
- Z55.4: Educational maladjustment and discord with teachers and classmates
- Z55.8: Other problems related to education and literacy
- Z56.0: Unemployment, unspecified
- Z56.82: Military deployment status
- Z59.0: Homelessness
- Z59.1: Inadequate housing
- Z59.4: Lack of adequate food and safe drinking water
- Z59.8: Other problems related to housing and economic circumstances
- Z60.2: Problems related to living alone
- Z60.3: Acculturation difficulty
- Z62.810: Personal history of physical and sexual abuse in childhood
- Z62.811: Personal history of psychological abuse in childhood
- Z62.820: Parent-child conflict
- Z62.891: Sibling rivalry
- Z63.72: Alcoholism and drug addiction in family
- Z75.3: Unavailability and inaccessibility of health care facilities
- Z75.4: Unavailability and inaccessibility of other helping agencies

Scenario: {{scenario}}

{prompt}
""",
        input_variables=["scenario", "prompt"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template.partial(prompt=PROMPT))

def extract_social_determinants_code(scenario, temperature=0.0):
    """
    Extract social determinants of health code(s) for a given scenario.
    """
    try:
        chain = create_social_determinants_extractor(temperature)
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
        print(f"Error in extract_social_determinants_code: {str(e)}")
        return ""

def activate_social_determinants(scenario):
    """
    Activate social determinants of health analysis and return results.
    """
    try:
        return extract_social_determinants_code(scenario)
    except Exception as e:
        print(f"Error in activate_social_determinants: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient reports living in an apartment with mold and structural issues."
    result = activate_social_determinants(scenario)
    print(result)
