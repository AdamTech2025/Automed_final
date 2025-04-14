"""
Module for extracting implant supported prosthetics codes.
"""

import os
import sys
from langchain.prompts import PromptTemplate
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file
from subtopics.prompt.prompt import PROMPT



def create_implant_supported_prosthetics_extractor():
    """
    Creates a LangChain-based extractor for implant supported prosthetics codes.
    """
    template = f"""
    You are a dental coding expert specializing in implant services.
    
  ## **Implant Supported Prosthetics Components** 
 
### **Before picking a code, ask:** 
- What specific component of an implant-supported prosthesis is being placed?
- Is this a connecting bar, abutment, or attachment?
- If it's an abutment, is it prefabricated or custom-fabricated?
- Is this an interim component or a definitive component?
- Is this a semi-precision component?
- What is the purpose of the component in the overall prosthetic plan?
 
---
 
### **Connecting Components**
 
#### **Code: D6055** – *Connecting bar — implant supported or abutment supported* 
**Use when:** Placing a bar that connects multiple implants or abutments to stabilize a prosthesis.
**Check:** Verify that multiple implants or abutments are being connected with a bar structure.
**Note:** Connecting bars provide excellent stability and retention for removable prostheses (overdentures) and help distribute forces across multiple implants.
 
---
 
### **Abutment Options**
 
#### **Code: D6056** – *Prefabricated abutment — includes modification and placement* 
**Use when:** Placing a manufactured, ready-made abutment on an implant that requires some chair-side modifications.
**Check:** Confirm that the abutment is prefabricated rather than custom-made, and document any modifications.
**Note:** Prefabricated abutments are more economical but may require adjustments to fit properly with the prosthesis and soft tissue contours.
 
#### **Code: D6057** – *Custom fabricated abutment — includes placement* 
**Use when:** Placing a laboratory-made abutment specifically designed for an individual patient.
**Check:** Verify that the abutment was custom-made by a laboratory process for a specific implant and prosthetic plan.
**Note:** Custom abutments provide optimal emergence profiles, angulation correction, and tissue contours but are more expensive and require longer fabrication time.
 
#### **Code: D6051** – *Interim implant abutment placement* 
**Use when:** Placing a temporary abutment during a healing or transitional period.
**Check:** Document why an interim abutment is necessary and distinguish it from a healing cap (which is not an interim abutment).
**Note:** Interim abutments help shape soft tissue and allow temporary restoration during the healing process.
 
---
 
### **Semi-Precision Components**
 
#### **Code: D6191** – *Semi-precision abutment — placement* 
**Use when:** Placing a semi-precision abutment on an implant body.
**Check:** Confirm that this is the initial placement or replacement of a semi-precision abutment.
**Note:** Semi-precision abutments have milled surfaces that allow precise alignment with corresponding attachments on removable prostheses.
 
#### **Code: D6192** – *Semi-precision attachment — placement* 
**Use when:** Attaching a semi-precision component to a removable prosthesis.
**Check:** Document that this involves luting of the initial or replacement semi-precision attachment to the removable prosthesis.
**Note:** Semi-precision attachments provide enhanced retention and stability while allowing removal of the prosthesis for hygiene.
 
---
 
### **Key Takeaways:** 
- These codes focus on the components that support implant prostheses, not the final prostheses themselves.
- Clear distinction must be made between prefabricated components (D6056) and custom-made components (D6057).
- Interim components (D6051) are specifically for use during healing or transition periods.
- Connecting bars (D6055) distribute forces across multiple implants and provide stability for overdentures.
- Semi-precision components (D6191, D6192) involve both an abutment component and a prosthesis attachment component.
- Documentation should specify the exact type of component, materials used, and purpose within the overall treatment plan.
- Remember that healing caps are not considered interim abutments and should not be coded as D6051.
    
    SCENARIO: {{scenario}}
    
    {PROMPT}
    """
    
    prompt = PromptTemplate(template=template, input_variables=["scenario"])
    return create_chain(prompt)

def extract_implant_supported_prosthetics_code(scenario):
    """
    Extracts implant supported prosthetics code(s) for a given scenario.
    """
    try:
        extractor = create_implant_supported_prosthetics_extractor()
        result = invoke_chain(extractor, {"scenario": scenario})
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Error in implant supported prosthetics code extraction: {str(e)}")
        return None

def activate_implant_supported_prosthetics(scenario):
    """
    Analyze a dental scenario to determine implant supported prosthetics code.
    
    Args:
        scenario (str): The dental scenario to analyze.
        
    Returns:
        str: The identified implant supported prosthetics code or empty string if none found.
    """
    try:
        result = extract_implant_supported_prosthetics_code(scenario)
        
        # Return empty string if no code found
        if result == "None" or not result or "not applicable" in result.lower():
            return ""
            
        return result
    except Exception as e:
        print(f"Error in activate_implant_supported_prosthetics: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = "A patient has four implants placed in the mandible. To stabilize the overdenture, a metallic bar connecting all four implants is being fabricated and placed."
    result = activate_implant_supported_prosthetics(scenario)
    print(result) 