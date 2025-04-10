import os
import sys
from langchain.prompts import PromptTemplate
from llm_services import create_chain, invoke_chain, get_llm_service
from topics.prompt import PROMPT

# Add the project root to the path so we can import subtopics
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now try to import subtopics, with a fallback mechanism
try:
    # Note: The directory is named 'implantservices' (lowercase) - matching directory structure
    from subtopics.implantservices import (
        activate_pre_surgical,
        activate_surgical_services,
        activate_implant_supported_prosthetics,
        activate_implant_supported_removable_dentures,
        activate_implant_supported_fixed_dentures,
        activate_single_crowns_abutment,
        activate_single_crowns_implant,
        activate_fpd_abutment,
        activate_fpd_implant,
        activate_other_implant_services
    )
except ImportError:
    print("Warning: Could not import subtopics for implantservices. Using fallback functions.")
    
    # Define fallback functions
    

def analyze_implant_services(scenario):
    """
    Analyze an implant services scenario and return relevant code ranges.
    
    Args:
        scenario (str): The dental scenario text to analyze

    Returns:
        str: The identified implant services code range(s)
    """
    try:
        # Create the prompt template
        prompt_template = PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert with over 15 years of expertise in ADA dental codes. 
Your task is to analyze the given scenario and determine the most applicable implant services code range(s) based on the following classifications:


## **Pre-Surgical Services (D6190)**
**Use when:** Performing radiographic/surgical implant index prior to surgery.
**Check:** Documentation specifies the use of radiographic or surgical guides for implant planning.
**Note:** This code is for the planning phase, not the actual implant placement.
**Activation trigger:** Scenario mentions OR implies any implant planning, guide fabrication, treatment planning for implants, or pre-surgical assessment. INCLUDE this range if there's any indication of preparation or planning for dental implant procedures.

## **Surgical Services (D6010-D6199)**
**Use when:** Placing implant bodies, interim abutments, or performing surgical revisions.
**Check:** Documentation details the surgical approach, implant type, and location.
**Note:** Different codes apply based on whether the implant is endosteal, eposteal, or transosteal.
**Activation trigger:** Scenario mentions OR implies any implant placement, implant surgery, bone grafting for implants, or surgical exposure of implants. INCLUDE this range if there's any hint of surgical procedures related to implant placement or preparation.

## **Implant Supported Prosthetics (D6051-D6078)**
**Use when:** Providing restorations that are supported by implants.
**Check:** Documentation specifies the type of prosthesis and its connection to the implants.
**Note:** These codes cover a wide range of prosthetic options from single crowns to full-arch restorations.
**Activation trigger:** Scenario mentions OR implies any implant-supported restoration, implant crown, implant prosthesis, or abutment placement. INCLUDE this range if there's any suggestion of restorations being attached to or supported by implants.

## **Implant Supported Removable Dentures (D6110-D6119)**
**Use when:** Providing removable dentures that are supported or retained by implants.
**Check:** Documentation clarifies whether the denture is maxillary or mandibular and the attachment mechanism.
**Note:** These differ from traditional dentures in their connection to implants for stability.
**Activation trigger:** Scenario mentions OR implies any implant-supported overdenture, implant-retained denture, or removable prosthesis attached to implants. INCLUDE this range if there's any indication of removable dentures that utilize implants for support or retention.

## **Implant Supported Fixed Dentures (D6090-D6095)**
**Use when:** Repairing or modifying existing implant prosthetics.
**Check:** Documentation describes the specific repair or maintenance procedure performed.
**Note:** These services maintain the functionality of existing implant restorations.
**Activation trigger:** Scenario mentions OR implies any repair of implant-supported prosthesis, replacement of broken components, or maintenance of implant restorations. INCLUDE this range if there's any hint of repairs or modifications to existing implant prosthetics.

## **Single Crowns, Abutment Supported (D6058-D6077)**
**Use when:** Providing crown restorations supported by an abutment on an implant.
**Check:** Documentation specifies the material of the crown and nature of the abutment.
**Note:** These differ from implant-supported crowns as they require a separate abutment.
**Activation trigger:** Scenario mentions OR implies any abutment-supported crown, crown attached to an implant abutment, or restorations on implant abutments. INCLUDE this range if there's any indication of crowns that are placed on abutments rather than directly on implants.

## **Single Crowns, Implant Supported (D6065-D6067)**
**Use when:** Providing crown restorations attached directly to the implant.
**Check:** Documentation identifies the crown material and direct implant connection.
**Note:** These connect directly to the implant without a separate abutment component.
**Activation trigger:** Scenario mentions OR implies any implant-supported crown, crown screwed directly to implant, or single-unit restoration on implant. INCLUDE this range if there's any suggestion of crowns connected directly to implants without intermediate abutments.

## **Fixed Partial Denture (FPD), Abutment Supported (D6071-D6074)**
**Use when:** Providing fixed bridges supported by implant abutments.
**Check:** Documentation details the span of the bridge and abutment specifications.
**Note:** These use abutments on implants as the support for a multi-unit fixed bridge.
**Activation trigger:** Scenario mentions OR implies any implant-supported bridge with abutments, multi-unit restoration on implant abutments, or fixed prosthesis on implant abutments. INCLUDE this range if there's any indication of bridges supported by abutments placed on implants.

## **Fixed Partial Denture (FPD), Implant Supported (D6075)**
**Use when:** Providing fixed bridges attached directly to implants without separate abutments.
**Check:** Documentation specifies the direct connection between the bridge and implants.
**Note:** These prostheses connect directly to the implant platform.
**Activation trigger:** Scenario mentions OR implies any implant-supported bridge without abutments, bridge screwed directly to implants, or multi-unit prosthesis directly on implants. INCLUDE this range if there's any hint of bridges connected directly to implants without intermediate abutments.

## **Other Implant Services (D6080-D6199)**
**Use when:** Providing specialized implant services not covered by other categories.
**Check:** Documentation provides detailed narrative explaining the specialized service.
**Note:** These include maintenance, repairs, and specialized modifications to implant prosthetics.
**Activation trigger:** Scenario mentions OR implies any implant maintenance, specialized implant procedure, implant modification, peri-implantitis treatment, or unusual implant service. INCLUDE this range if there's any suggestion of implant-related services that don't clearly fit other categories.

### **Scenario:**
{{scenario}}
{PROMPT}

RESPOND WITH ALL APPLICABLE CODE RANGES from the options above, even if they are only slightly relevant.
List them in order of relevance, with the most relevant first.
""",
            input_variables=["scenario"]
        )
        
        # Create the chain using our LLM service
        chain = create_chain(prompt_template)
        
        # Use the provided scenario directly
        print(f"Analyzing implant services scenario: {scenario[:100]}...")
        
        # Use invoke through our LLM service
        result = invoke_chain(chain, {"scenario": scenario})
        
        # Extract the text from the result
        code_range = result.get("text", "").strip()
        
        print(f"Implant Services analyze_implant_services result: {code_range}")
        return code_range
    except Exception as e:
        print(f"Error in analyze_implant_services: {str(e)}")
        return ""

def activate_implant_services(scenario):
    """
    Activate implant services analysis and return the results with specific subtopic activations.
    
    Args:
        scenario (str): The dental scenario text to analyze
        
    Returns:
        dict: A dictionary containing the code range, subtopic and specific codes
    """
    try:
        # Get the code range from the analysis
        implant_result = analyze_implant_services(scenario)
        if not implant_result:
            print("No implant services result returned")
            return {}
        
        print(f"Implant Services Result in activate_implant_services: {implant_result}")
        
        # Process specific implant services subtopics based on the result
        specific_codes = []
        activated_subtopics = []
        
        # Check for each subtopic and activate if applicable
        if "D6190" in implant_result:
            print("Activating subtopic: Pre-Surgical Services (D6190)")
            pre_surgical_code = activate_pre_surgical(scenario)
            if pre_surgical_code:
                specific_codes.append(pre_surgical_code)
                activated_subtopics.append("Pre-Surgical Services (D6190)")
                
        if "D6010-D6107" in implant_result:
            print("Activating subtopic: Surgical Services (D6010-D6107)")
            surgical_code = activate_surgical_services(scenario)
            if surgical_code:
                specific_codes.append(surgical_code)
                activated_subtopics.append("Surgical Services (D6010-D6107)")
                
        if "D6055-D6192" in implant_result:
            print("Activating subtopic: Implant Supported Prosthetics (D6055-D6192)")
            prosthetics_code = activate_implant_supported_prosthetics(scenario)
            if prosthetics_code:
                specific_codes.append(prosthetics_code)
                activated_subtopics.append("Implant Supported Prosthetics (D6055-D6192)")
                
        if "D6110-D6113" in implant_result:
            print("Activating subtopic: Implant/Abutment Supported Removable Dentures (D6110-D6113)")
            removable_code = activate_implant_supported_removable_dentures(scenario)
            if removable_code:
                specific_codes.append(removable_code)
                activated_subtopics.append("Implant/Abutment Supported Removable Dentures (D6110-D6113)")
                
        if "D6114-D6119" in implant_result:
            print("Activating subtopic: Implant/Abutment Supported Fixed Dentures (D6114-D6119)")
            fixed_code = activate_implant_supported_fixed_dentures(scenario)
            if fixed_code:
                specific_codes.append(fixed_code)
                activated_subtopics.append("Implant/Abutment Supported Fixed Dentures (D6114-D6119)")
                
        if "D6058-D6094" in implant_result:
            print("Activating subtopic: Single Crowns, Abutment Supported (D6058-D6094)")
            abutment_crown_code = activate_single_crowns_abutment(scenario)
            if abutment_crown_code:
                specific_codes.append(abutment_crown_code)
                activated_subtopics.append("Single Crowns, Abutment Supported (D6058-D6094)")
                
        if "D6065-D6088" in implant_result:
            print("Activating subtopic: Single Crowns, Implant Supported (D6065-D6088)")
            implant_crown_code = activate_single_crowns_implant(scenario)
            if implant_crown_code:
                specific_codes.append(implant_crown_code)
                activated_subtopics.append("Single Crowns, Implant Supported (D6065-D6088)")
                
        if "D6068-D6194" in implant_result:
            print("Activating subtopic: Fixed Partial Denture Retainer, Abutment Supported (D6068-D6194)")
            fpd_abutment_code = activate_fpd_abutment(scenario)
            if fpd_abutment_code:
                specific_codes.append(fpd_abutment_code)
                activated_subtopics.append("Fixed Partial Denture Retainer, Abutment Supported (D6068-D6194)")
                
        if "D6075-D6123" in implant_result:
            print("Activating subtopic: Fixed Partial Denture Retainer, Implant Supported (D6075-D6123)")
            fpd_implant_code = activate_fpd_implant(scenario)
            if fpd_implant_code:
                specific_codes.append(fpd_implant_code)
                activated_subtopics.append("Fixed Partial Denture Retainer, Implant Supported (D6075-D6123)")
                
        if "D6080-D6199" in implant_result:
            print("Activating subtopic: Other Implant Services (D6080-D6199)")
            other_code = activate_other_implant_services(scenario)
            if other_code:
                specific_codes.append(other_code)
                activated_subtopics.append("Other Implant Services (D6080-D6199)")
        
        # Choose the primary subtopic (either the first activated or a default)
        primary_subtopic = activated_subtopics[0] if activated_subtopics else "Surgical Services (D6010-D6107)"
        
        # Return the results in standardized format
        return {
            "code_range": implant_result,
            "subtopic": primary_subtopic,
            "activated_subtopics": activated_subtopics,
            "codes": specific_codes
        }
    except Exception as e:
        print(f"Error in implant services analysis: {str(e)}")
        return {}

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = input("Enter an implant services dental scenario: ")
    result = activate_implant_services(scenario)
    print(f"\n=== IMPLANT SERVICES ANALYSIS RESULT ===")
    print(f"CODE RANGE: {result.get('code_range', 'None')}")
    print(f"PRIMARY SUBTOPIC: {result.get('subtopic', 'None')}")
    print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
    print(f"SPECIFIC CODES: {', '.join(result.get('codes', []))}")


