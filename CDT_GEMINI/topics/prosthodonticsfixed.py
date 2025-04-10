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
from subtopics.Prosthodontics_Fixed import (
    activate_fixed_partial_denture_pontics,
    activate_fixed_partial_denture_retainers_inlays_onlays,
    activate_fixed_partial_denture_retainers_crowns,
    activate_other_fixed_partial_denture_services
)

# Load environment variables

def analyze_prosthodonticsfixed(scenario):
    """
    Analyze a fixed prosthodontics scenario and return relevant code ranges.
    
    Args:
        scenario (str): The dental scenario text to analyze
        
    Returns:
        str: The identified fixed prosthodontics code range(s)
    """
    try:
        # Create the prompt template
        prompt_template = PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert with over 15 years of expertise in ADA dental codes. 
Your task is to analyze the given scenario and determine the most applicable fixed prosthodontics code range(s) based on the following classifications:


## **Fixed Partial Denture Pontics (D6205-D6253)**
**Use when:** Providing artificial replacement teeth in a fixed bridge.
**Check:** Documentation specifies pontic material and design for the edentulous area.
**Note:** These are the artificial teeth in a bridge that replace missing natural teeth.
**Activation trigger:** Scenario mentions OR implies any bridge pontic, artificial tooth in a bridge, tooth replacement in fixed prosthesis, or pontic design/material. INCLUDE this range if there's any indication of replacement teeth in a fixed bridge.

## **Fixed Partial Denture Retainers — Inlays/Onlays (D6545-D6634)**
**Use when:** Using inlays or onlays as the retaining elements for a fixed bridge.
**Check:** Documentation details the inlay/onlay material and design as a bridge retainer.
**Note:** These are more conservative than full crowns but still provide retention for the bridge.
**Activation trigger:** Scenario mentions OR implies any inlay retainer, onlay abutment, partial coverage retainer for bridge, or conservative bridge attachment. INCLUDE this range if there's any hint of inlays or onlays being used to support a fixed bridge.

## **Fixed Partial Denture Retainers — Crowns (D6710-D6793)**
**Use when:** Using full coverage crowns as the retaining elements for a fixed bridge.
**Check:** Documentation specifies crown material and design as bridge abutments.
**Note:** These provide maximum retention but require more tooth reduction.
**Activation trigger:** Scenario mentions OR implies any crown retainer, abutment crown, full coverage bridge support, or crown preparation for bridge. INCLUDE this range if there's any suggestion of full crowns being used to support a fixed bridge.

## **Other Fixed Partial Denture Services (D6920-D6999)**
**Use when:** Providing additional services related to fixed bridges.
**Check:** Documentation details the specific service and its purpose for the bridge.
**Note:** These include repairs, recementations, and specialized bridge components.
**Activation trigger:** Scenario mentions OR implies any bridge repair, recementation, stress breaker, precision attachment, or maintenance of existing bridge. INCLUDE this range if there's any indication of services for fixed bridges beyond the initial fabrication.

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
        print(f"Analyzing fixed prosthodontics scenario: {scenario[:100]}...")
        
        # Use invoke through our LLM service
        result = invoke_chain(chain, {"scenario": scenario})
        
        # Extract the text from the result
        code_range = result.get("text", "").strip()
        
        print(f"Prosthodontics Fixed analyze_prosthodonticsfixed result: {code_range}")
        return code_range
    except Exception as e:
        print(f"Error in analyze_prosthodonticsfixed: {str(e)}")
        return ""

def activate_prosthodonticsfixed(scenario):
    """
    Activate fixed prosthodontics analysis and return the results with specific subtopic activations.
    
    Args:
        scenario (str): The dental scenario text to analyze
        
    Returns:
        dict: A dictionary containing the code range, subtopic and specific codes
    """
    try:
        # Get the code range from the analysis
        prosthodontics_result = analyze_prosthodonticsfixed(scenario)
        if not prosthodontics_result:
            print("No prosthodontics result returned")
            return {}
        
        print(f"Prosthodontics Fixed Result in activate_prosthodonticsfixed: {prosthodontics_result}")
        
        # Process specific prosthodontics subtopics based on the result
        specific_codes = []
        activated_subtopics = []
        
        # Check for each subtopic and activate if applicable
        if "D6205-D6253" in prosthodontics_result:
            print("Activating subtopic: Fixed Partial Denture Pontics (D6205-D6253)")
            pontics_code = activate_fixed_partial_denture_pontics(scenario)
            if pontics_code:
                specific_codes.append(pontics_code)
                activated_subtopics.append("Fixed Partial Denture Pontics (D6205-D6253)")
                
        if "D6545-D6634" in prosthodontics_result:
            print("Activating subtopic: Fixed Partial Denture Retainers — Inlays/Onlays (D6545-D6634)")
            inlays_onlays_code = activate_fixed_partial_denture_retainers_inlays_onlays(scenario)
            if inlays_onlays_code:
                specific_codes.append(inlays_onlays_code)
                activated_subtopics.append("Fixed Partial Denture Retainers — Inlays/Onlays (D6545-D6634)")
                
        if "D6710-D6793" in prosthodontics_result:
            print("Activating subtopic: Fixed Partial Denture Retainers — Crowns (D6710-D6793)")
            crowns_code = activate_fixed_partial_denture_retainers_crowns(scenario)
            if crowns_code:
                specific_codes.append(crowns_code)
                activated_subtopics.append("Fixed Partial Denture Retainers — Crowns (D6710-D6793)")
                
        if "D6920-D6999" in prosthodontics_result:
            print("Activating subtopic: Other Fixed Partial Denture Services (D6920-D6999)")
            other_code = activate_other_fixed_partial_denture_services(scenario)
            if other_code:
                specific_codes.append(other_code)
                activated_subtopics.append("Other Fixed Partial Denture Services (D6920-D6999)")
        
        # Choose the primary subtopic (either the first activated or a default)
        primary_subtopic = activated_subtopics[0] if activated_subtopics else "Fixed Partial Denture Pontics (D6205-D6253)"
        
        # Return the results in standardized format
        return {
            "code_range": prosthodontics_result,
            "subtopic": primary_subtopic,
            "activated_subtopics": activated_subtopics,
            "codes": specific_codes
        }
    except Exception as e:
        print(f"Error in prosthodontics fixed analysis: {str(e)}")
        return {}

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = input("Enter a fixed prosthodontics dental scenario: ")
    result = activate_prosthodonticsfixed(scenario)
    print(f"\n=== FIXED PROSTHODONTICS ANALYSIS RESULT ===")
    print(f"CODE RANGE: {result.get('code_range', 'None')}")
    print(f"PRIMARY SUBTOPIC: {result.get('subtopic', 'None')}")
    print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
    print(f"SPECIFIC CODES: {', '.join(result.get('codes', []))}")