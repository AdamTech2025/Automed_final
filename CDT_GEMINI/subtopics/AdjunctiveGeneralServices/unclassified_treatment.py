import os
import sys
from langchain.prompts import PromptTemplate
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file    
from subtopics.prompt.prompt import PROMPT



def create_unclassified_treatment_extractor():
    """
    Creates a LangChain-based extractor for unclassified treatment codes.
    """
    template = f"""
    You are a dental coding expert
    
    ## **Unclassified Treatment** 
 
### **Before picking a code, ask:** 
- Does the procedure or service fit any existing CDT code? 
- Has the procedure been performed using a new or emerging technology? 
- Is the procedure or service experimental or investigational? 
- Is there documentation explaining why a standard code doesn't apply? 
- Is there a clinical narrative that describes the specific treatment in detail? 
 
---
 
### **Detailed Coding Guidelines for Unclassified Treatment** 
 
#### **Code: D9999** – *Unspecified Adjunctive Procedure, By Report* 
**Use when:** A dental procedure is performed that cannot be adequately described by any other existing CDT code. 
**Check:** Ensure that no standard code exists that could adequately describe the procedure. 
**Note:** This code requires a detailed narrative report that explains the nature, extent, and necessity of the procedure and the time, effort, and equipment required. 
 
---
 
### **Common Uses for D9999:** 
- New or evolving dental procedures not yet assigned a specific code 
- Experimental or innovative treatments 
- Use of technology or approaches that significantly modify standard procedures 
- Services that combine elements of multiple procedures in a way not described by existing codes 
 
---
 
### **Key Takeaways:** 
- **D9999 should be a last resort** when no other code accurately describes the procedure. 
- **Always include a detailed report** with clinical documentation and justification. 
- **Check for updates to CDT codes** before using D9999, as new codes are added regularly. 
- **The narrative should explain why** standard codes are insufficient. 
 
This code is subject to greater scrutiny by payers and may require additional documentation for reimbursement.

    SCENARIO: {{scenario}}
    
    {PROMPT}
    """
    
    prompt = PromptTemplate(template=template, input_variables=["scenario"])
    return create_chain(prompt)

def extract_unclassified_treatment_code(scenario):
    """
    Extracts unclassified treatment code(s) for a given scenario.
    """
    try:
        extractor = create_unclassified_treatment_extractor()
        result = invoke_chain(extractor, {"scenario": scenario})
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Error in unclassified treatment code extraction: {str(e)}")
        return None

def activate_unclassified_treatment(scenario):
    """
    Activates the unclassified treatment analysis process and returns results.
    """
    try:
        result = extract_unclassified_treatment_code(scenario)
        return result
    except Exception as e:
        print(f"Error activating unclassified treatment analysis: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = "Dentist performed an experimental laser therapy for gum disease that doesn't fit any existing CDT code. The treatment used a new type of laser frequency and application technique not covered by standard periodontal codes."
    result = activate_unclassified_treatment(scenario)
    print(result) 