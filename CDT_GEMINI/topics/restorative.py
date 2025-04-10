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
from subtopics.Restorative import (
    activate_amalgam_restorations,
    activate_resin_based_composite_restorations,
    activate_gold_foil_restorations,
    activate_inlays_and_onlays,
    activate_crowns,
    activate_other_restorative_services
)

# Load environment variables

def analyze_restorative(scenario):
    """
    Analyze a restorative scenario and return relevant code ranges.
    
    Args:
        scenario (str): The dental scenario text to analyze
        
    Returns:
        str: The identified restorative code range(s)
    """
    try:
        # Create the prompt template
        prompt_template = PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert with over 15 years of expertise in ADA dental codes. 
Your task is to analyze the given scenario and determine the most applicable restorative code range(s) based on the following classifications:


## **Amalgam Restorations (D2140-D2161)**
**Use when:** Placing silver-colored metal alloy fillings.
**Check:** Documentation specifies the number of surfaces involved and tooth location.
**Note:** These durable restorations are typically used for posterior teeth.
**Activation trigger:** Scenario mentions OR implies any amalgam filling, silver filling, metallic restoration, posterior filling, or direct restoration with amalgam. INCLUDE this range if there's any indication of silver-colored fillings being placed.

## **Resin-Based Composite Restorations (D2330-D2394)**
**Use when:** Placing tooth-colored fillings made of composite resin.
**Check:** Documentation details the number of surfaces involved and tooth location.
**Note:** These esthetic restorations can be used in anterior or posterior teeth.
**Activation trigger:** Scenario mentions OR implies any composite filling, tooth-colored restoration, resin restoration, bonded filling, or esthetic direct restoration. INCLUDE this range if there's any hint of tooth-colored fillings being placed.

## **Gold Foil Restorations (D2410-D2430)**
**Use when:** Placing pure gold restorations through direct techniques.
**Check:** Documentation identifies the number of surfaces and specific gold foil technique.
**Note:** These are specialized, less common restorations using pure gold.
**Activation trigger:** Scenario mentions OR implies any gold foil, direct gold restoration, or traditional gold filling technique. INCLUDE this range if there's any suggestion of pure gold being used in a direct restoration technique.

## **Inlays and Onlays (D2510-D2664)**
**Use when:** Providing laboratory-fabricated partial coverage restorations.
**Check:** Documentation specifies the material used and extent of cuspal coverage.
**Note:** These indirect restorations offer precision fit for moderate to large lesions.
**Activation trigger:** Scenario mentions OR implies any inlay, onlay, indirect restoration, laboratory-fabricated partial coverage, or precision-fitted restoration. INCLUDE this range if there's any indication of indirect partial coverage restorations.

## **Crowns (D2710-D2799)**
**Use when:** Providing full-coverage restorations for damaged teeth.
**Check:** Documentation details the crown material and reason for full coverage.
**Note:** These restore severely damaged teeth requiring complete coronal protection.
**Activation trigger:** Scenario mentions OR implies any crown, full coverage restoration, cap, coronal coverage, or complete tooth restoration. INCLUDE this range if there's any hint of full coverage restorations being provided.

## **Other Restorative Services (D2910-D2999)**
**Use when:** Providing additional services related to restorations.
**Check:** Documentation specifies the exact service and its purpose.
**Note:** These include repairs, recementations, cores, posts, and specialized services.
**Activation trigger:** Scenario mentions OR implies any core buildup, post and core, resin infiltration, temporary restoration, crown repair, veneer, reattachment of fragment, or specialized restorative service. INCLUDE this range if there's any suggestion of restorative services beyond standard fillings or crowns.

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
        print(f"Analyzing restorative scenario: {scenario[:100]}...")
        
        # Use invoke through our LLM service
        result = invoke_chain(chain, {"scenario": scenario})
        
        # Extract the text from the result
        code_range = result.get("text", "").strip()
        
        print(f"Restorative analyze_restorative result: {code_range}")
        return code_range
    except Exception as e:
        print(f"Error in analyze_restorative: {str(e)}")
        return ""

def activate_restorative(scenario):
    """
    Activate restorative analysis and return the results with specific subtopic activations.
    
    Args:
        scenario (str): The dental scenario text to analyze
        
    Returns:
        dict: A dictionary containing the code range, subtopic and specific codes
    """
    try:
        # Get the code range from the analysis
        restorative_result = analyze_restorative(scenario)
        if not restorative_result:
            print("No restorative result returned")
            return {}
        
        print(f"Restorative Result in activate_restorative: {restorative_result}")
        
        # Process specific restorative subtopics based on the result
        specific_codes = []
        activated_subtopics = []
        
        # Check for each subtopic and activate if applicable
        if "D2140-D2161" in restorative_result:
            print("Activating subtopic: Amalgam Restorations (D2140-D2161)")
            amalgam_code = activate_amalgam_restorations(scenario)
            if amalgam_code:
                specific_codes.append(amalgam_code)
                activated_subtopics.append("Amalgam Restorations (D2140-D2161)")
                
        if "D2330-D2394" in restorative_result:
            print("Activating subtopic: Resin-Based Composite Restorations (D2330-D2394)")
            composite_code = activate_resin_based_composite_restorations(scenario)
            if composite_code:
                specific_codes.append(composite_code)
                activated_subtopics.append("Resin-Based Composite Restorations (D2330-D2394)")
                
        if "D2410-D2430" in restorative_result:
            print("Activating subtopic: Gold Foil Restorations (D2410-D2430)")
            gold_foil_code = activate_gold_foil_restorations(scenario)
            if gold_foil_code:
                specific_codes.append(gold_foil_code)
                activated_subtopics.append("Gold Foil Restorations (D2410-D2430)")
                
        if "D2510-D2664" in restorative_result:
            print("Activating subtopic: Inlays and Onlays (D2510-D2664)")
            inlay_code = activate_inlays_and_onlays(scenario)
            if inlay_code:
                specific_codes.append(inlay_code)
                activated_subtopics.append("Inlays and Onlays (D2510-D2664)")
                
        if "D2710-D2799" in restorative_result:
            print("Activating subtopic: Crowns (D2710-D2799)")
            crown_code = activate_crowns(scenario)
            if crown_code:
                specific_codes.append(crown_code)
                activated_subtopics.append("Crowns (D2710-D2799)")
                
        if "D2910-D2999" in restorative_result:
            print("Activating subtopic: Other Restorative Services (D2910-D2999)")
            other_code = activate_other_restorative_services(scenario)
            if other_code:
                specific_codes.append(other_code)
                activated_subtopics.append("Other Restorative Services (D2910-D2999)")
        
        # Choose the primary subtopic (either the first activated or a default)
        primary_subtopic = activated_subtopics[0] if activated_subtopics else "Resin-Based Composite Restorations (D2330-D2394)"
        
        # Format detailed results if specific codes were found
        return {
            "code_range": restorative_result,
            "subtopic": primary_subtopic,
            "activated_subtopics": activated_subtopics,
            "codes": specific_codes
        }
    except Exception as e:
        print(f"Error in restorative analysis: {str(e)}")
        return {}

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = input("Enter a restorative dental scenario: ")
    result = activate_restorative(scenario)
    print(f"\n=== RESTORATIVE ANALYSIS RESULT ===")
    print(f"CODE RANGE: {result.get('code_range', 'None')}")
    print(f"PRIMARY SUBTOPIC: {result.get('subtopic', 'None')}")
    print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
    print(f"SPECIFIC CODES: {', '.join(result.get('codes', []))}")

