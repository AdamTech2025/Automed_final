"""
Module for extracting implant/abutment supported fixed dentures codes.
"""

import os
import sys
from langchain.prompts import PromptTemplate
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file
from subtopics.prompt.prompt import PROMPT



def create_fixed_dentures_extractor():
    """
    Creates a LangChain-based extractor for implant/abutment supported fixed dentures codes.
    """
    template = f"""
    You are a dental coding expert specializing in implant services.
    
    ## **Implant/Abutment Supported Fixed Dentures** 
 
### **Before picking a code, ask:** 
- Is the arch fully edentulous (completely without teeth) or partially edentulous?
- Is the prosthesis for the maxillary (upper) or mandibular (lower) arch?
- Is this intended as a permanent prosthesis or an interim prosthesis?
- What is the timeframe for using this prosthesis (permanent vs. temporary during healing)?
- Are there any special considerations based on the patient's oral anatomy?
- What materials are being used for the prosthesis?
 
---
 
### **Permanent Fixed Dentures for Edentulous Arches**
 
#### **Code: D6114** – *Implant/abutment supported fixed denture for edentulous arch – maxillary* 
**Use when:** Creating a permanent fixed prosthesis for a completely edentulous upper arch that is supported by implants or abutments.
**Check:** Verify that no natural teeth remain in the arch and that sufficient implants have been placed to support the prosthesis.
**Note:** This is a full-arch restoration that provides significant functional and esthetic benefits. Requires precise planning for implant placement and prosthesis design.
 
#### **Code: D6115** – *Implant/abutment supported fixed denture for edentulous arch – mandibular* 
**Use when:** Creating a permanent fixed prosthesis for a completely edentulous lower arch that is supported by implants or abutments.
**Check:** Confirm that the lower arch is completely without teeth and has adequate implant support.
**Note:** Lower arch restorations may require different implant positioning and angulation compared to upper arch due to anatomical differences.
 
---
 
### **Permanent Fixed Dentures for Partially Edentulous Arches**
 
#### **Code: D6116** – *Implant/abutment supported fixed denture for partially edentulous arch – maxillary* 
**Use when:** Creating a permanent fixed prosthesis for a partially edentulous upper arch that is supported by implants or abutments.
**Check:** Verify that some natural teeth remain in the arch and document which teeth are being replaced by the prosthesis.
**Note:** Requires careful planning to ensure proper occlusion between the prosthesis and remaining natural teeth.
 
#### **Code: D6117** – *Implant/abutment supported fixed denture for partially edentulous arch – mandibular* 
**Use when:** Creating a permanent fixed prosthesis for a partially edentulous lower arch that is supported by implants or abutments.
**Check:** Confirm which natural teeth remain and ensure the prosthesis design accommodates them.
**Note:** May require additional considerations for biomechanical forces, especially if posterior teeth are being replaced.
 
---
 
### **Interim Fixed Dentures**
 
#### **Code: D6118** – *Implant/abutment supported interim fixed denture for edentulous arch – mandibular* 
**Use when:** A temporary fixed prosthesis is needed for the lower arch during a healing period or prior to the final prosthesis.
**Check:** Document why an interim prosthesis is necessary and the expected timeline before transitioning to a permanent prosthesis.
**Note:** Used when a period of healing is necessary prior to fabrication and placement of a permanent prosthetic. Materials and design may differ from the final prosthesis.
 
#### **Code: D6119** – *Implant/abutment supported interim fixed denture for edentulous arch – maxillary* 
**Use when:** A temporary fixed prosthesis is needed for the upper arch during a healing period or prior to the final prosthesis.
**Check:** Specify the clinical reason for using an interim prosthesis instead of proceeding directly to the permanent one.
**Note:** Interim prostheses allow for assessment of function, esthetics, and phonetics before finalizing the permanent design. They also protect healing implants while allowing some function.
 
---
 
### **Key Takeaways:** 
- These codes specifically refer to fixed dentures (non-removable prostheses) supported by implants or abutments.
- The codes distinguish between maxillary (upper) and mandibular (lower) arches due to the different functional demands.
- Different codes are used for fully edentulous arches vs. partially edentulous arches.
- Interim prostheses (D6118, D6119) are used during healing periods or while waiting for the fabrication of the final prosthesis.
- Documentation should clearly indicate whether the arch is fully or partially edentulous, and if partially, which teeth remain.
- When coding for a fixed hybrid prosthesis, consider that these typically involve a metal framework with acrylic or composite teeth.
    
    SCENARIO: {{scenario}}
    
    {PROMPT}
    """
    
    prompt = PromptTemplate(template=template, input_variables=["scenario"])
    return create_chain(prompt)

def extract_fixed_dentures_code(scenario):
    """
    Extracts implant/abutment supported fixed dentures code(s) for a given scenario.
    """
    try:
        extractor = create_fixed_dentures_extractor()
        result = invoke_chain(extractor, {"scenario": scenario})
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Error in fixed dentures code extraction: {str(e)}")
        return None

def activate_implant_supported_fixed_dentures(scenario):
    """
    Analyze a dental scenario to determine implant/abutment supported fixed dentures code.
    
    Args:
        scenario (str): The dental scenario to analyze.
        
    Returns:
        str: The identified implant/abutment supported fixed dentures code or empty string if none found.
    """
    try:
        result = extract_fixed_dentures_code(scenario)
        
        # Return empty string if no code found
        if result == "None" or not result or "not applicable" in result.lower():
            return ""
            
        return result
    except Exception as e:
        print(f"Error in activate_implant_supported_fixed_dentures: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = "The patient is receiving a zirconia fixed complete denture for an edentulous maxillary arch supported by six implants. The prosthesis will be screw-retained directly to the implants."
    result = activate_implant_supported_fixed_dentures(scenario)
    print(result) 