"""
Module for extracting treatment complications ICD-10 codes.
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
 
def create_treatment_complications_extractor(temperature=0.0):
    """
    Create a LangChain-based treatment complications code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template="""
You are a highly experienced medical coding expert specializing in treatment complications. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

12.1 Complications Related to Dental Implants:
- T85.81XA: Embolism due to internal orthopedic prosthetic devices, implants and grafts, initial encounter
- T85.82XA: Fibrosis due to internal orthopedic prosthetic devices, implants and grafts, initial encounter
- T85.83XA: Hemorrhage due to internal orthopedic prosthetic devices, implants and grafts, initial encounter
- T85.84XA: Pain due to internal orthopedic prosthetic devices, implants and grafts, initial encounter
- T85.85XA: Stenosis due to internal orthopedic prosthetic devices, implants and grafts, initial encounter
- T85.86XA: Thrombosis due to internal orthopedic prosthetic devices, implants and grafts, initial encounter
- T85.89XA: Other specified complication of internal orthopedic prosthetic devices, implants and grafts, initial encounter

12.2 Complications of Surgical and Medical Care:
- M96.0: Pseudarthrosis after fusion or arthrodesis
- M96.1: Postlaminectomy syndrome, not elsewhere classified
- M96.6: Fracture of bone following insertion of orthopedic implant, joint prosthesis, or bone plate

12.3 Postprocedural Complications:
- K91.840: Postprocedural hemorrhage of a digestive system organ or structure following a dental procedure
- K91.841: Postprocedural hemorrhage of a digestive system organ or structure following other procedure
- K91.870: Postprocedural hematoma of a digestive system organ or structure following a dental procedure
- K91.871: Postprocedural hematoma of a digestive system organ or structure following other procedure
- K91.872: Postprocedural seroma of a digestive system organ or structure following a dental procedure
- K91.873: Postprocedural seroma of a digestive system organ or structure following other procedure

12.4 Medication-Related Complications:
- K12.31: Oral mucositis (ulcerative) due to antineoplastic therapy
- K12.32: Oral mucositis (ulcerative) due to other drugs
- K12.33: Oral mucositis (ulcerative) due to radiation
- K12.39: Other oral mucositis (ulcerative)
- T88.6XXA: Anaphylactic reaction due to adverse effect of correct drug or medicament properly administered, initial encounter
- T88.7XXA: Unspecified adverse effect of drug or medicament, initial encounter

12.5 Device-Related Complications:
- K08.52: Decreased vertical dimension of bite due to attrition of teeth
- K08.53: Decreased vertical dimension of bite due to trauma
- K08.54: Decreased vertical dimension of bite due to dietary habit (abrasion)
- K08.0: Exfoliation of teeth due to systemic causes

12.6 Failed Dental Restorative Materials:
- K08.51: Open restoration margins of tooth
- K08.530: Fractured dental restorative material with loss of material
- K08.531: Fractured dental restorative material without loss of material
- K08.539: Fractured dental restorative material, unspecified

Scenario: {{scenario}}

{prompt}
""",
        input_variables=["scenario", "prompt"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template.partial(prompt=PROMPT))

def extract_treatment_complications_code(scenario, temperature=0.0):
    """
    Extract treatment complications code(s) for a given scenario.
    """
    try:
        chain = create_treatment_complications_extractor(temperature)
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
        print(f"Error in extract_treatment_complications_code: {str(e)}")
        return ""

def activate_treatment_complications(scenario):
    """
    Activate treatment complications analysis and return results.
    """
    try:
        return extract_treatment_complications_code(scenario)
    except Exception as e:
        print(f"Error in activate_treatment_complications: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient presents with pain around dental implant that was placed 3 months ago."
    result = activate_treatment_complications(scenario)
    print(result) 