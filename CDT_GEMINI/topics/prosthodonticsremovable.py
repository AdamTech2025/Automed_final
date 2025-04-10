import os
import sys
from langchain.prompts import PromptTemplate
from llm_services import create_chain, invoke_chain, get_llm_service

# Add the root directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

# Now import modules
from topics.prompt import PROMPT
from subtopics.Prosthodontics_Removable import (
    activate_complete_dentures,
    activate_partial_denture,
    activate_adjustments_to_dentures,
    activate_repairs_to_complete_dentures,
    activate_repairs_to_partial_dentures,
    activate_denture_rebase_procedures,
    activate_denture_reline_procedures,
    activate_interim_prosthesis,
    activate_other_removable_prosthetic_services
)

# Load environment variables

def analyze_prosthodonticsremovable(scenario):
    """
    Analyze a removable prosthodontics scenario and return relevant code ranges.
    
    Args:
        scenario (str): The dental scenario text to analyze
        
    Returns:
        str: The identified removable prosthodontics code range(s)
    """
    try:
        # Create the prompt template
        prompt_template = PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert with over 15 years of expertise in ADA dental codes. 
Your task is to analyze the given scenario and determine the most applicable removable prosthodontics code range(s) based on the following classifications:

## IMPORTANT GUIDELINES:
- You should activate ALL code ranges that have any potential relevance to the scenario
- Even if a code range is only slightly related, include it in your response
- Only exclude a code range if it is DEFINITELY NOT relevant to the scenario
- When in doubt, INCLUDE the code range rather than exclude it
- Multiple code ranges can and should be activated if they have any potential applicability
- Your goal is to ensure no potentially relevant codes are missed

## **Complete Dentures (D5110-D5140)**
**Use when:** Providing full arch prostheses for edentulous patients.
**Check:** Documentation specifies maxillary/mandibular and immediate/conventional status.
**Note:** These address complete tooth loss in an arch with full tissue coverage prostheses.
**Activation trigger:** Scenario mentions OR implies any full denture, complete denture, edentulous treatment, immediate denture, or replacement of all teeth in an arch. INCLUDE this range if there's any indication of complete tooth replacement in either arch.

## **Partial Denture (D5211-D5286)**
**Use when:** Providing removable prostheses for partially edentulous patients.
**Check:** Documentation details the framework material and arch being restored.
**Note:** These replace some but not all teeth in an arch while utilizing remaining natural teeth for support.
**Activation trigger:** Scenario mentions OR implies any partial denture, RPD, removable partial, cast framework prosthesis, or flexible base partial. INCLUDE this range if there's any hint of replacing some but not all teeth with a removable appliance.

## **Adjustments to Dentures (D5410-D5422)**
**Use when:** Modifying existing dentures to improve fit or function.
**Check:** Documentation specifies the type of denture being adjusted.
**Note:** These address minor issues without remaking or significantly altering the prosthesis.
**Activation trigger:** Scenario mentions OR implies any denture adjustment, fit correction, comfort adjustment, occlusal adjustment of prosthesis, or minor modification of denture. INCLUDE this range if there's any suggestion of minor alterations to existing dentures.

## **Repairs to Complete Dentures (D5511-D5520)**
**Use when:** Fixing damaged complete dentures.
**Check:** Documentation identifies the specific damage and repair performed.
**Note:** These restore function to damaged complete dentures without replacement.
**Activation trigger:** Scenario mentions OR implies any denture repair, broken denture, cracked denture base, replacement of broken teeth in denture, or fixing complete denture. INCLUDE this range if there's any indication of repairing damage to a complete denture.

## **Repairs to Partial Dentures (D5611-D5671)**
**Use when:** Fixing damaged partial dentures.
**Check:** Documentation details the specific component repaired or replaced.
**Note:** These restore function to damaged partial dentures by addressing specific components.
**Activation trigger:** Scenario mentions OR implies any partial denture repair, broken clasp, damaged framework, resin base repair, or adding components to existing partial. INCLUDE this range if there's any hint of repairing or modifying components of a partial denture.

## **Denture Rebase Procedures (D5710-D5725)**
**Use when:** Completely replacing the base material of an existing denture.
**Check:** Documentation indicates complete replacement of the base while maintaining the original teeth.
**Note:** These procedures address significant changes in ridge morphology requiring new base adaptation.
**Activation trigger:** Scenario mentions OR implies any denture rebase, replacing entire denture base, new base for existing denture, or complete base replacement. INCLUDE this range if there's any suggestion of replacing the entire base material while keeping the original teeth.

## **Denture Reline Procedures (D5730-D5761)**
**Use when:** Adding new material to the tissue surface of a denture to improve fit.
**Check:** Documentation specifies whether chairside or laboratory reline and type of denture.
**Note:** These procedures add material rather than completely replacing the base.
**Activation trigger:** Scenario mentions OR implies any denture reline, adding material to denture base, improving fit with new lining, chairside or lab reline. INCLUDE this range if there's any indication of adding material to the tissue surface of a denture.

## **Interim Prosthesis (D5810-D5821)**
**Use when:** Providing temporary dentures during treatment phases.
**Check:** Documentation clarifies the interim nature and purpose of the prosthesis.
**Note:** These are not intended as definitive restorations but as transitional appliances.
**Activation trigger:** Scenario mentions OR implies any temporary denture, interim prosthesis, transitional denture, provisional appliance, or temporary tooth replacement. INCLUDE this range if there's any hint of temporary dentures during transition to final prostheses.

## **Other Removable Prosthetic Services (D5765-D5899)**
**Use when:** Providing specialized prosthetic services not covered in other categories.
**Check:** Documentation details the specific service and its therapeutic purpose.
**Note:** These include tissue conditioning, precision attachment, and other advanced procedures.
**Activation trigger:** Scenario mentions OR implies any tissue conditioning, precision attachment, specialized denture procedure, overdenture, or unusual prosthetic technique. INCLUDE this range if there's any suggestion of specialized removable prosthetic services beyond standard dentures and partials.

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
        print(f"Analyzing removable prosthodontics scenario: {scenario[:100]}...")
        
        # Use invoke through our LLM service
        result = invoke_chain(chain, {"scenario": scenario})
        
        # Extract the text from the result
        code_range = result.get("text", "").strip()
        
        print(f"Prosthodontics Removable analyze_prosthodonticsremovable result: {code_range}")
        return code_range
    except Exception as e:
        print(f"Error in analyze_prosthodonticsremovable: {str(e)}")
        return ""

def activate_prosthodonticsremovable(scenario):
    """
    Activate removable prosthodontics analysis and return the results with specific subtopic activations.
    
    Args:
        scenario (str): The dental scenario text to analyze
        
    Returns:
        dict: A dictionary containing the code range, subtopic and specific codes
    """
    try:
        # Get the code range from the analysis
        code_range = analyze_prosthodonticsremovable(scenario)
        if not code_range:
            print("No removable prosthodontics result returned")
            return {}
            
        print(f"Removable Prosthodontics Result in activate_prosthodonticsremovable: {code_range}")
        
        # Process specific prosthodontics subtopics based on the result
        specific_codes = []
        activated_subtopics = []
        
        # Check for each subtopic and activate if applicable
        if "D5110-D5140" in code_range:
            print("Activating subtopic: Complete Dentures (D5110-D5140)")
            complete_dentures_code = activate_complete_dentures(scenario)
            if complete_dentures_code:
                specific_codes.append(complete_dentures_code)
                activated_subtopics.append("Complete Dentures (D5110-D5140)")
        
        if "D5211-D5286" in code_range:
            print("Activating subtopic: Partial Denture (D5211-D5286)")
            partial_denture_code = activate_partial_denture(scenario)
            if partial_denture_code:
                specific_codes.append(partial_denture_code)
                activated_subtopics.append("Partial Denture (D5211-D5286)")
        
        if "D5410-D5422" in code_range:
            print("Activating subtopic: Adjustments to Dentures (D5410-D5422)")
            adjustments_code = activate_adjustments_to_dentures(scenario)
            if adjustments_code:
                specific_codes.append(adjustments_code)
                activated_subtopics.append("Adjustments to Dentures (D5410-D5422)")
        
        if "D5511-D5520" in code_range:
            print("Activating subtopic: Repairs to Complete Dentures (D5511-D5520)")
            repairs_complete_code = activate_repairs_to_complete_dentures(scenario)
            if repairs_complete_code:
                specific_codes.append(repairs_complete_code)
                activated_subtopics.append("Repairs to Complete Dentures (D5511-D5520)")
        
        if "D5611-D5671" in code_range:
            print("Activating subtopic: Repairs to Partial Dentures (D5611-D5671)")
            repairs_partial_code = activate_repairs_to_partial_dentures(scenario)
            if repairs_partial_code:
                specific_codes.append(repairs_partial_code)
                activated_subtopics.append("Repairs to Partial Dentures (D5611-D5671)")
                
        if "D5710-D5725" in code_range:
            print("Activating subtopic: Denture Rebase Procedures (D5710-D5725)")
            rebase_code = activate_denture_rebase_procedures(scenario)
            if rebase_code:
                specific_codes.append(rebase_code)
                activated_subtopics.append("Denture Rebase Procedures (D5710-D5725)")
                
        if "D5730-D5761" in code_range:
            print("Activating subtopic: Denture Reline Procedures (D5730-D5761)")
            reline_code = activate_denture_reline_procedures(scenario)
            if reline_code:
                specific_codes.append(reline_code)
                activated_subtopics.append("Denture Reline Procedures (D5730-D5761)")
                
        if "D5810-D5821" in code_range:
            print("Activating subtopic: Interim Prosthesis (D5810-D5821)")
            interim_code = activate_interim_prosthesis(scenario)
            if interim_code:
                specific_codes.append(interim_code)
                activated_subtopics.append("Interim Prosthesis (D5810-D5821)")
                
        if "D5765-D5899" in code_range:
            print("Activating subtopic: Other Removable Prosthetic Services (D5765-D5899)")
            other_services_code = activate_other_removable_prosthetic_services(scenario)
            if other_services_code:
                specific_codes.append(other_services_code)
                activated_subtopics.append("Other Removable Prosthetic Services (D5765-D5899)")
        
        # Choose the primary subtopic (either the first activated or a default)
        primary_subtopic = activated_subtopics[0] if activated_subtopics else "Complete Dentures (D5110-D5140)"
        
        # Return the results in standardized format
        return {
            "code_range": code_range,
            "subtopic": primary_subtopic,
            "activated_subtopics": activated_subtopics,
            "codes": specific_codes
        }
    except Exception as e:
        print(f"Error in removable prosthodontics analysis: {str(e)}")
        return {}

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = input("Enter a removable prosthodontics dental scenario: ")
    result = activate_prosthodonticsremovable(scenario)
    print(f"\n=== REMOVABLE PROSTHODONTICS ANALYSIS RESULT ===")
    print(f"CODE RANGE: {result.get('code_range', 'None')}")
    print(f"PRIMARY SUBTOPIC: {result.get('subtopic', 'None')}")
    print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
    print(f"SPECIFIC CODES: {', '.join(result.get('codes', []))}")
