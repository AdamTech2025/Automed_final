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
from subtopics.Orthodontics import (
    activate_limited_orthodontic_treatment,
    activate_comprehensive_orthodontic_treatment,
    activate_minor_treatment_harmful_habits,
    activate_other_orthodontic_services
)

# Load environment variables



def analyze_orthodontic(scenario):
    """
    Analyze an orthodontic scenario and return relevant code ranges.
    
    Args:
        scenario (str): The dental scenario text to analyze
        
    Returns:
        str: The identified orthodontic code range(s)
    """
    try:
        # Create the prompt template
        prompt_template = PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert with over 15 years of expertise in ADA dental codes. 
Your task is to analyze the given scenario and determine the most applicable orthodontic code range(s) based on the following classifications:


## **Limited Orthodontic Treatment (D8010-D8040)**
**Use when:** Providing partial correction or addressing a specific orthodontic problem.
**Check:** Documentation specifies which dentition stage (primary, transitional, adolescent, adult) is being treated.
**Note:** These procedures focus on limited treatment goals rather than comprehensive correction.
**Activation trigger:** Scenario mentions OR implies any partial orthodontic treatment, minor tooth movement, single arch treatment, or interceptive orthodontics. INCLUDE this range if there's any indication of focused orthodontic care rather than full correction.

## **Comprehensive Orthodontic Treatment (D8070-D8090)**
**Use when:** Providing complete orthodontic correction for the entire dentition.
**Check:** Documentation identifies the dentition stage (transitional, adolescent, adult) being treated.
**Note:** These involve full banding/bracketing of the dentition with regular adjustments.
**Activation trigger:** Scenario mentions OR implies any full orthodontic treatment, complete braces, comprehensive correction, full arch treatment, or extensive alignment. INCLUDE this range if there's any hint of complete orthodontic care addressing overall occlusion.

## **Minor Treatment to Control Harmful Habits (D8210-D8220)**
**Use when:** Correcting deleterious oral habits through appliance therapy.
**Check:** Documentation specifies the habit being addressed and type of appliance used.
**Note:** These procedures target specific habits rather than overall malocclusion.
**Activation trigger:** Scenario mentions OR implies any thumb-sucking, tongue thrusting, habit appliance, habit breaking, or interceptive treatment for parafunctional habits. INCLUDE this range if there's any suggestion of treating harmful oral habits through specialized appliances.

## **Other Orthodontic Services (D8660-D8999)**
**Use when:** Providing supplementary orthodontic services or treatments not specified elsewhere.
**Check:** Documentation details the specific service provided and its purpose.
**Note:** These include consultations, retention, repairs, and additional orthodontic services.
**Activation trigger:** Scenario mentions OR implies any pre-orthodontic visit, retainer placement, bracket repair, adjustment visit, or specialized orthodontic service. INCLUDE this range if there's any indication of orthodontic care beyond the initial appliance placement.

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
        print(f"Analyzing orthodontic scenario: {scenario[:100]}...")
        
        # Use invoke through our LLM service
        result = invoke_chain(chain, {"scenario": scenario})
        
        # Extract the text from the result
        code_range = result.get("text", "").strip()
        
        print(f"Orthodontic analyze_orthodontic result: {code_range}")
        return code_range
    except Exception as e:
        print(f"Error in analyze_orthodontic: {str(e)}")
        return ""

def activate_orthodontic(scenario):
    """
    Activate orthodontic analysis and return the results with specific subtopic activations.
    
    Args:
        scenario (str): The dental scenario text to analyze
        
    Returns:
        dict: A dictionary containing the code range, subtopic and specific codes
    """
    try:
        # Get the code range from the analysis
        orthodontic_result = analyze_orthodontic(scenario)
        if not orthodontic_result:
            print("No orthodontic result returned")
            return {}
        
        print(f"Orthodontic Result in activate_orthodontic: {orthodontic_result}")
        
        # Process specific orthodontic subtopics based on the result
        specific_codes = []
        activated_subtopics = []
        
        # Check for each subtopic and activate if applicable
        if "D8010-D8040" in orthodontic_result:
            print("Activating subtopic: Limited Orthodontic Treatment (D8010-D8040)")
            limited_treatment_code = activate_limited_orthodontic_treatment(scenario)
            if limited_treatment_code:
                specific_codes.append(limited_treatment_code)
                activated_subtopics.append("Limited Orthodontic Treatment (D8010-D8040)")
                
        if "D8070-D8090" in orthodontic_result:
            print("Activating subtopic: Comprehensive Orthodontic Treatment (D8070-D8090)")
            comprehensive_treatment_code = activate_comprehensive_orthodontic_treatment(scenario)
            if comprehensive_treatment_code:
                specific_codes.append(comprehensive_treatment_code)
                activated_subtopics.append("Comprehensive Orthodontic Treatment (D8070-D8090)")
                
        if "D8210-D8220" in orthodontic_result:
            print("Activating subtopic: Minor Treatment to Control Harmful Habits (D8210-D8220)")
            harmful_habits_code = activate_minor_treatment_harmful_habits(scenario)
            if harmful_habits_code:
                specific_codes.append(harmful_habits_code)
                activated_subtopics.append("Minor Treatment to Control Harmful Habits (D8210-D8220)")
                
        if "D8660-D8999" in orthodontic_result:
            print("Activating subtopic: Other Orthodontic Services (D8660-D8999)")
            other_services_code = activate_other_orthodontic_services(scenario)
            if other_services_code:
                specific_codes.append(other_services_code)
                activated_subtopics.append("Other Orthodontic Services (D8660-D8999)")
        
        # Choose the primary subtopic (either the first activated or a default)
        primary_subtopic = activated_subtopics[0] if activated_subtopics else "Comprehensive Orthodontic Treatment (D8070-D8090)"
        
        # Return the results in standardized format
        return {
            "code_range": orthodontic_result,
            "subtopic": primary_subtopic,
            "activated_subtopics": activated_subtopics,
            "codes": specific_codes
        }
    except Exception as e:
        print(f"Error in orthodontic analysis: {str(e)}")
        return {}

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = input("Enter an orthodontic scenario: ")
    result = activate_orthodontic(scenario)
    print(f"\n=== ORTHODONTIC ANALYSIS RESULT ===")
    print(f"CODE RANGE: {result.get('code_range', 'None')}")
    print(f"PRIMARY SUBTOPIC: {result.get('subtopic', 'None')}")
    print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
    print(f"SPECIFIC CODES: {', '.join(result.get('codes', []))}")
