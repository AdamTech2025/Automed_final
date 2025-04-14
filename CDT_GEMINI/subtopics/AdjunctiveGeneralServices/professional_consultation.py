import os
import os
import sys
from langchain.prompts import PromptTemplate
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file
from subtopics.prompt.prompt import PROMPT



def create_professional_consultation_extractor():
    """
    Creates a LangChain-based extractor for professional consultation codes.
    """
    template = f"""
    You are a dental coding expert
    
   Before picking a code, ask:** 
- Is the consultation being provided by a dentist or a medical health care professional? 
- Is the consultation for diagnostic purposes, or is it related to a broader medical concern affecting dental treatment? 
- Is this a one-time consultation, or will it require ongoing collaboration with another provider? 
- Will the consulted practitioner be initiating additional diagnostic or therapeutic services? 
- Does the consultation include a full oral evaluation, or is it limited to discussion and advice? 
 
---
 
### **Detailed Coding Guidelines for Professional Consultation** 
 
#### **Code: D9310** – *Consultation - Diagnostic Service Provided by a Dentist or Physician Other Than the Requesting Dentist or Physician* 
**Use when:** A patient is referred to another dentist or physician for their professional opinion or advice regarding a specific dental problem. 
**Check:** Ensure that the consultation is formally requested by another provider and that the consulting practitioner provides a documented evaluation. 
**Note:** This code includes an oral evaluation but does not cover additional treatment or procedures initiated by the consultant. If further diagnostic or therapeutic services are required, they must be billed separately. 
 
#### **Code: D9311** – *Consultation with a Medical Health Care Professional* 
**Use when:** A dentist consults with a medical professional (e.g., physician, specialist) regarding a patient's medical condition that may impact dental treatment. 
**Check:** Ensure the consultation is medically necessary and directly related to the patient's dental care plan. 
**Note:** Common cases include discussions about patients with cardiovascular conditions, diabetes, bleeding disorders, or immunosuppressive conditions that may require adjustments in dental treatment. Documentation of the consultation, including any recommendations made by the medical provider, is essential. 
 
---
 
### **Key Takeaways:** 
- **D9310** is used when a dentist or physician provides a second opinion or diagnosis at the request of another provider. This includes an oral evaluation. 
- **D9311** is used when a treating dentist consults with a medical provider to assess how a patient's medical condition may affect planned dental procedures. 
- **Ensure proper documentation** of the consultation request, findings, and recommendations to justify the billing of these codes. 
- **Additional procedures or treatments** initiated as a result of the consultation must be coded separately. 
 
By using these codes appropriately, dental providers can ensure accurate billing and seamless interdisciplinary coordination for comprehensive patient care.


    SCENARIO: {{scenario}}
    
    {PROMPT}
    """
    
    prompt = PromptTemplate(template=template, input_variables=["scenario"])
    return create_chain(prompt)

def extract_professional_consultation_code(scenario):
    """
    Extracts professional consultation code(s) for a given scenario.
    """
    try:
        extractor = create_professional_consultation_extractor()
        result = invoke_chain(extractor, {"scenario": scenario})
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Error in professional consultation code extraction: {str(e)}")
        return None

def activate_professional_consultation(scenario):
    """
    Activates the professional consultation analysis process and returns results.
    """
    try:
        result = extract_professional_consultation_code(scenario)
        return result
    except Exception as e:
        print(f"Error activating professional consultation analysis: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = "Family dentist refers patient to oral surgeon for evaluation of a suspicious lesion on the tongue. The oral surgeon conducts a comprehensive examination, documents findings, and provides treatment recommendations."
    result = activate_professional_consultation(scenario)
    print(result) 