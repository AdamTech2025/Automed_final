"""
Module for extracting dental encounters ICD-10 codes.
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
 
def create_dental_encounters_extractor(temperature=0.0):
    """
    Create a LangChain-based dental encounters code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template="""
You are a highly experienced medical coding expert specializing in dental encounters and examinations. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

1.1 Routine Dental Examinations:
- Z01.20: Encounter for dental examination and cleaning without abnormal findings
- Z01.21: Encounter for dental examination and cleaning with abnormal findings

1.2 Special Screening Examinations:
- Z13.84: Encounter for screening for dental disorders

1.3 Orthodontic-Related Encounters:
- Z46.4: Encounter for fitting and adjustment of orthodontic device

1.4 Dental Prosthesis-Related Encounters:
- Z45.81: Encounter for adjustment or removal of breast implant
- Z45.82: Encounter for adjustment or removal of myringotomy device (stent) (tube)
- Z45.89: Encounter for adjustment and management of other implanted devices
- Z46.3: Encounter for fitting and adjustment of dental prosthetic device

1.5 Dental Procedure Follow-ups:
- Z09: Encounter for follow-up examination after completed treatment for conditions other than malignant neoplasm

1.6 Encounters for Other Specified Aftercare:
- Z51.89: Encounter for other specified aftercare

1.7 Counseling:
- Z71.89: Other specified counseling

1.8 Fear of Dental Treatment:
- Z64.4: Discord with counselors

1.9 Problems Related to Care:
- Z74.0: Reduced mobility
- Z74.1: Need for assistance with personal care
- Z74.3: Need for continuous supervision
- Z76.5: Malingerer [conscious simulation]
- Z91.89: Other specified personal risk factors, not elsewhere classified

1.10 Problems Related to Medical Facilities and Other Health Care:
- Z75.3: Unavailability and inaccessibility of health care facilities
- Z75.4: Unavailability and inaccessibility of other helping agencies

Scenario: {scenario}

{prompt}
""",
        input_variables=["scenario", "prompt"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template.partial(prompt=PROMPT))

def extract_dental_encounters_code(scenario, temperature=0.0):
    """
    Extract dental encounters code(s) for a given scenario.
    """
    try:
        chain = create_dental_encounters_extractor(temperature)
        result = chain.invoke({"scenario": scenario})
        # Try to extract the result based on different possible structures
        if isinstance(result, dict) and "text" in result:
            result_text = result["text"]
        elif isinstance(result, dict) and "output_text" in result:
            result_text = result["output_text"]
        elif hasattr(result, "content"):
            result_text = result.content
        else:
            result_text = str(result)
            
        print(f"Dental encounters code result: {result_text}")
        return result_text.strip()
    except Exception as e:
        print(f"Error in extract_dental_encounters_code: {str(e)}")
        return ""

def activate_dental_encounters(scenario):
    """
    Activate dental encounters analysis and return results.
    """
    try:
        return extract_dental_encounters_code(scenario)
    except Exception as e:
        print(f"Error in activate_dental_encounters: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient presents for 6-month routine dental check-up and cleaning. No abnormal findings."
    result = activate_dental_encounters(scenario)
    print(result)
