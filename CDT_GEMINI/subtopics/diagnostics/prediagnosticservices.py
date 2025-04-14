import os
import sys
from langchain.prompts import PromptTemplate
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file
from subtopics.prompt.prompt import PROMPT


def create_prediagnostic_services_extractor():
    """
    Create a LangChain-based Prediagnostic Services extractor.
    """
    template = f"""
You are a highly experienced medical coding expert, 


## Pre-Diagnostic Services - Detailed Guidelines

### **D0190 - Screening of a Patient**
**When to Use:**
- When conducting a general screening to determine if a patient needs further dental evaluation.
- Includes state or federally mandated screenings.

**What to Check:**
- Ensure it is a preliminary evaluation and does not include a full diagnosis.
- Used to determine the necessity of a comprehensive dental exam.

**Notes:**
- Not a substitute for a complete dental examination.
- Typically used in community health screenings or school programs.

---

### **D0191 - Assessment of a Patient**
**When to Use:**
- When performing a limited clinical inspection to identify signs of oral or systemic disease, malformation, or injury.
- Used to determine the need for a referral for diagnosis and treatment.

**What to Check:**
- Ensure findings are documented.
- Should be used for preliminary assessments and not as a full diagnostic evaluation.

**Notes:**
- Helps identify patients who may require specialized care or further testing.
- Can be used in triage situations.

---

### **General Guidelines for Selecting Codes:**
1. **Determine Purpose:** Screening (D0190) is for general identification of patients needing further care, while assessment (D0191) is a more focused inspection for specific concerns.
2. **Check Documentation Requirements:** Record findings properly to justify further diagnostic procedures or referrals.
3. **Understand Limitations:** These codes do not include full diagnostic evaluations or treatment planning.

### *Scenario:*
{{scenario}}

{PROMPT}
"""
    
    prompt = PromptTemplate(template=template, input_variables=["scenario"])
    return create_chain(prompt)

def extract_prediagnostic_services_code(scenario):
    """
    Extract Prediagnostic Services code(s) for a given scenario.
    """
    try:
        extractor = create_prediagnostic_services_extractor()
        result = invoke_chain(extractor, {"scenario": scenario})
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Error in prediagnostic services code extraction: {str(e)}")
        return None

def activate_prediagnostic_services(scenario):
    """
    Activate Prediagnostic Services analysis and return results.
    """
    try:
        result = extract_prediagnostic_services_code(scenario)
        return result
    except Exception as e:
        print(f"Error activating prediagnostic services analysis: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = "A school nurse conducts quick dental checks on elementary students to identify children who may need to visit a dentist."
    result = activate_prediagnostic_services(scenario)
    print(result)