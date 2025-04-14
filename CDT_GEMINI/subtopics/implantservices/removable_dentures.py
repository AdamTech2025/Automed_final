"""
Module for extracting implant/abutment supported removable dentures codes.
"""

import os
import sys
from langchain.prompts import PromptTemplate
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file
from subtopics.prompt.prompt import PROMPT



def create_removable_dentures_extractor():
    """
    Creates a LangChain-based extractor for implant/abutment supported removable dentures codes.
    """
    template = f"""
    You are a dental coding expert specializing in implant services.
    
  ## **Implant/Abutment Supported Removable Dentures** 
 
### **Before picking a code, ask:** 
- Is the arch fully edentulous (completely without teeth) or partially edentulous?
- Is the prosthesis for the maxillary (upper) or mandibular (lower) arch?
- Is the removable denture supported by implants, abutments, or both?
- What type of attachments or retention systems are being utilized?
- How many implants are supporting the removable prosthesis?
- What are the patient's functional and esthetic requirements for the prosthesis?
 
---
 
### **Removable Dentures for Edentulous Arches**
 
#### **Code: D6110** – *Implant/abutment supported removable denture for edentulous arch – maxillary* 
**Use when:** Creating a removable prosthesis for a completely edentulous upper arch that is supported by implants or abutments and can be removed by the patient.
**Check:** Verify that no natural teeth remain in the upper arch and document the number and position of supporting implants or abutments.
**Note:** This prosthesis offers significant improvement in stability, retention and function compared to conventional dentures while still allowing removal for cleaning and maintenance, making it an excellent option for patients with compromised bone volume who cannot receive a fixed prosthesis but desire improved function and confidence over traditional removable appliances.
**Documentation Requirements:** Records should specify the type of retention system used (such as locator attachments, ball attachments, or bar-clip systems), number of implants supporting the denture, materials used for the denture base and teeth, and any special considerations addressed in the design.
**Clinical Indications:** Particularly beneficial for patients with significant ridge resorption, concerns about oral hygiene maintenance, limited financial resources for a fixed option, or preference for a removable appliance with enhanced stability.
 
#### **Code: D6111** – *Implant/abutment supported removable denture for edentulous arch – mandibular* 
**Use when:** Creating a removable prosthesis for a completely edentulous lower arch that is supported by implants or abutments and can be removed by the patient.
**Check:** Confirm that the lower arch is completely without teeth and document the supporting implants or abutments.
**Note:** Lower implant-supported overdentures offer particularly significant quality-of-life improvements due to the inherent instability of conventional mandibular dentures, with even two implants providing substantial enhancement in retention, stability, and chewing efficiency while preserving alveolar bone and improving patient comfort, function, and psychological well-being.
**Clinical Considerations:** The mandibular overdenture is often considered a standard of care for the edentulous mandible, as it provides dramatic improvement in stability with relatively few implants (typically 2-4) while remaining cost-effective and allowing for excellent hygiene access.
**Attachment Selection:** Documentation should include rationale for attachment system selection, considering factors such as implant position, interarch space, retention needs, and patient dexterity for maintenance.
 
---
 
### **Removable Dentures for Partially Edentulous Arches**
 
#### **Code: D6112** – *Implant/abutment supported removable denture for partially edentulous arch – maxillary* 
**Use when:** Creating a removable prosthesis for a partially edentulous upper arch that is supported by both implants/abutments and natural teeth.
**Check:** Document which natural teeth remain and the position of supporting implants or abutments.
**Note:** This hybrid prosthesis combines the stability of implant support with the proprioception and additional stability of natural teeth, creating a versatile restoration that distributes forces appropriately between implants and natural teeth while allowing removal for hygiene access and maintenance of both the prosthesis and remaining dentition.
**Design Considerations:** The prosthesis requires careful planning for force distribution between implants and natural teeth, with specialized attachment systems designed to account for the different resilience of each support type.
**Biomechanical Factors:** Documentation should address how the design accommodates the differential support provided by the rigid implants versus the periodontal ligament-supported natural teeth to prevent overloading of either support system.
 
#### **Code: D6113** – *Implant/abutment supported removable denture for partially edentulous arch – mandibular* 
**Use when:** Creating a removable prosthesis for a partially edentulous lower arch that is supported by both implants/abutments and natural teeth.
**Check:** Specify which natural teeth remain and how the implants or abutments are integrated into the support system.
**Note:** Lower partial dentures with implant support show significant improvement in stability and patient satisfaction compared to conventional removable partial dentures, particularly in distal extension cases where posterior implant support eliminates the common problems of movement and food entrapment under the denture base.
**Strategic Implant Placement:** Documentation should detail the strategic positioning of implants, often placed in posterior edentulous areas to eliminate movement and provide cross-arch stabilization.
**Attachment Selection:** For partially edentulous cases, attachment selection must consider the integration with any clasps or other retention elements engaging the natural teeth, creating a unified retention system that functions harmoniously.
 
---
 
### **Key Takeaways:** 
- These codes are specifically for removable dentures supported by implants or abutments, not conventional dentures.
- The distinctions between codes are based on whether the arch is fully or partially edentulous and whether it's maxillary or mandibular.
- Documentation should specify the type of attachments or retention systems used to connect the denture to the implants/abutments.
- These prostheses offer significant advantages over conventional removable dentures in terms of stability, function, and bone preservation.
- The design must consider the biomechanics of implant-supported removable prostheses, including attachment wear and maintenance requirements.
- For partially edentulous arches, the integration between implant support and natural teeth support requires special consideration.
- Patient education regarding home care and maintenance of both the prosthesis and the supporting elements is essential.
    
    SCENARIO: {{scenario}}
    
    {PROMPT}
    """
    
    prompt = PromptTemplate(template=template, input_variables=["scenario"])
    return create_chain(prompt)

def extract_removable_dentures_code(scenario):
    """
    Extracts implant/abutment supported removable dentures code(s) for a given scenario.
    """
    try:
        extractor = create_removable_dentures_extractor()
        result = invoke_chain(extractor, {"scenario": scenario})
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Error in removable dentures code extraction: {str(e)}")
        return None

def activate_implant_supported_removable_dentures(scenario):
    """
    Analyze a dental scenario to determine implant/abutment supported removable dentures code.
    
    Args:
        scenario (str): The dental scenario to analyze.
        
    Returns:
        str: The identified implant/abutment supported removable dentures code or empty string if none found.
    """
    try:
        result = extract_removable_dentures_code(scenario)
        
        # Return empty string if no code found
        if result == "None" or not result or "not applicable" in result.lower():
            return ""
            
        return result
    except Exception as e:
        print(f"Error in activate_implant_supported_removable_dentures: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = "A completely edentulous patient has four implants placed in their mandible. After successful integration, the dentist is now fabricating a removable overdenture that will attach to the implants using locator attachments."
    result = activate_implant_supported_removable_dentures(scenario)
    print(result) 