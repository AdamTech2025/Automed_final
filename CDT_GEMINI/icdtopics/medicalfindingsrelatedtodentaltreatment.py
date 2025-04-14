"""
Module for extracting medical findings related to dental treatment ICD-10 codes.
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
 
def create_medical_findings_dental_treatment_extractor(temperature=0.0):
    """
    Create a LangChain-based medical findings related to dental treatment code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template="""
You are a highly experienced medical coding expert specializing in medical findings related to dental treatment. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

12.1 Medical Findings:
- Z01.20: Encounter for dental examination and cleaning without abnormal findings
- Z01.21: Encounter for dental examination and cleaning with abnormal findings
- Z13.84: Encounter for screening for dental disorders
- Z29.3: Encounter for prophylactic fluoride administration
- Z41.8: Encounter for other procedures for purposes other than remedying health state
- Z46.3: Encounter for fitting and adjustment of dental prosthetic device
- Z46.4: Encounter for fitting and adjustment of orthodontic device

12.2 Dental Treatment Complications:
- T88.52XA: Failed moderate sedation during procedure, initial encounter
- T88.52XD: Failed moderate sedation during procedure, subsequent encounter
- T88.52XS: Failed moderate sedation during procedure, sequela
- Y65.53: Performance of wrong procedure (operation) on correct patient
- Y69: Unspecified misadventure during surgical and medical care
- Y84.8: Other medical procedures as the cause of abnormal reaction

12.3 Dental Treatment History:
- Z87.828: Personal history of other (healed) physical injury and trauma
- Z91.89: Other specified personal risk factors, not elsewhere classified
- Z92.89: Personal history of other medical treatment
- Z98.818: Personal history of other surgery
- Z98.89: Other specified postprocedural states

12.4 Dental Treatment Observations:
- R68.89: Other general symptoms and signs
- R69: Illness, unspecified
- Z71.89: Other specified counseling
- Z72.89: Other problems related to lifestyle
- Z91.849: Other risk factors, not elsewhere classified

Scenario: {{scenario}}

{prompt}
""",
        input_variables=["scenario", "prompt"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template.partial(prompt=PROMPT))

def extract_medical_findings_dental_treatment_code(scenario, temperature=0.0):
    """
    Extract medical findings related to dental treatment code(s) for a given scenario.
    """
    try:
        chain = create_medical_findings_dental_treatment_extractor(temperature)
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
        print(f"Error in extract_medical_findings_dental_treatment_code: {str(e)}")
        return ""

def activate_medical_findings(scenario):
    """
    Activate medical findings related to dental treatment analysis and return results.
    """
    try:
        return extract_medical_findings_dental_treatment_code(scenario)
    except Exception as e:
        print(f"Error in activate_medical_findings: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient presents for routine dental examination and cleaning, no abnormal findings noted."
    result = activate_medical_findings(scenario)
    print(result)
