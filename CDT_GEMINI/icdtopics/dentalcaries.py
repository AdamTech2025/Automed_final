"""
Module for extracting dental caries ICD-10 codes.
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
 
def create_dental_caries_extractor(temperature=0.0):
    """
    Create a LangChain-based dental caries code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template="""
You are a highly experienced medical coding expert specializing in dental caries. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

Dental Caries ICD-10 codes include:
2.1 Risk Factors
- Z91.841: Risk for dental caries, low
- Z91.842: Risk for dental caries, moderate
- Z91.843: Risk for dental caries, high

2.2 Caries
- K02.3: Arrested dental caries (decay and cavities) (includes coronal and root caries)
- K02.51: Dental caries on pit and fissure surface limited to enamel
- K02.52: Dental caries on pit and fissure surface penetrating into dentin
- K02.53: Dental caries on pit and fissure surface penetrating into pulp
- K02.61: Dental caries on smooth surface limited to enamel
- K02.62: Dental caries on smooth surface penetrating into dentin
- K02.63: Dental caries on smooth surface penetrating into pulp

2.2 Permanent Dentition:
- K02.7: Dental root caries
- K02.3: Arrested dental caries
- K02.9: Dental caries, unspecified

Scenario: {scenario}

{prompt}
""",
        input_variables=["scenario", "prompt"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template.partial(prompt=PROMPT))

def extract_dental_caries_code(scenario, temperature=0.0):
    """
    Extract dental caries code(s) for a given scenario.
    """
    try:
        chain = create_dental_caries_extractor(temperature)
        result = chain.invoke({"scenario": scenario})
        result_text = ""
        
        # LangChain 0.1.x format: should return dict with keys that might include 'text' or 'output_text'
        if isinstance(result, dict):
            if "text" in result:
                result_text = result["text"]
            elif "output_text" in result:
                result_text = result["output_text"]
            else:
                result_text = str(result)
        # New version may return an object with content attribute
        elif hasattr(result, "content"):
            result_text = result.content
        else:
            result_text = str(result)
            
        print(f"Dental caries code result: {result_text}")
        return result_text.strip()
    except Exception as e:
        print(f"Error in extract_dental_caries_code: {str(e)}")
        return ""

def activate_dental_caries(scenario):
    """
    Activate dental caries analysis and return results.
    """
    try:
        return extract_dental_caries_code(scenario)
    except Exception as e:
        print(f"Error in activate_dental_caries: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient presents with deep cavity on a primary molar penetrating into the pulp."
    result = activate_dental_caries(scenario)
    print(result)
