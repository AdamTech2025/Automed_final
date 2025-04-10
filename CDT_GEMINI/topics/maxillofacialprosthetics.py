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
from subtopics.Maxillofacial_Prosthetics import (
    activate_general_prosthetics,
    activate_carriers
)

# Load environment variables


# Get model name from environment variable, default to gpt-4o if not set

# Ensure API key is set


def analyze_maxillofacial_prosthetics(scenario):
    """
    Analyze a dental maxillofacial prosthetics scenario and return relevant code ranges.
    
    Args:
        scenario (str): The dental scenario text to analyze
        
    Returns:
        str: The identified maxillofacial prosthetics code range(s)
    """
    try:
        # Create the prompt template
        prompt_template = PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert with over 15 years of expertise in ADA dental codes. 
Your task is to analyze the given scenario and determine the most applicable maxillofacial prosthetics code range(s) based on the following classifications:


## **General Maxillofacial Prosthetics (D5992-D5937)**
**Use when:** Creating or adjusting prosthetic replacements for missing facial or oral structures.
**Check:** Documentation describes the specific prosthesis type and its purpose in restoring function or aesthetics.
**Note:** These prostheses address complex defects resulting from surgery, trauma, or congenital conditions.
**Activation trigger:** Scenario mentions OR implies any facial prosthesis, oral-maxillofacial defect, obturator, speech aid, radiation shield, or post-surgical rehabilitation. INCLUDE this range if there's any indication of specialized prostheses for maxillofacial defects.

## **Carriers (D5986-D5999)**
**Use when:** Fabricating devices for delivery of therapeutic agents or specialized treatments.
**Check:** Documentation specifies the purpose of the carrier and what it's designed to deliver.
**Note:** These include custom trays for medication delivery or protection of tissues.
**Activation trigger:** Scenario mentions OR implies any fluoride carrier, medicament delivery device, specialized tray, or custom carrier for therapeutic agents. INCLUDE this range if there's any hint of devices designed to hold or deliver medications or treatments.

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
        print(f"Analyzing maxillofacial prosthetics scenario: {scenario[:100]}...")
        
        # Use invoke through our LLM service
        result = invoke_chain(chain, {"scenario": scenario})
        
        # Extract the text from the result
        code_range = result.get("text", "").strip()
        
        print(f"Maxillofacial Prosthetics analyze_maxillofacial_prosthetics result: {code_range}")
        return code_range
    except Exception as e:
        print(f"Error in analyze_maxillofacial_prosthetics: {str(e)}")
        return ""

def activate_maxillofacial_prosthetics(scenario):
    """
    Activate maxillofacial prosthetics analysis and return the results with specific subtopic activations.
    
    Args:
        scenario (str): The dental scenario text to analyze
        
    Returns:
        dict: A dictionary containing the code range, subtopic and specific codes
    """
    try:
        # Get the code range from the analysis
        maxillofacial_result = analyze_maxillofacial_prosthetics(scenario)
        if not maxillofacial_result:
            print("No maxillofacial prosthetics result returned")
            return {}
        
        print(f"Maxillofacial Prosthetics Result in activate_maxillofacial_prosthetics: {maxillofacial_result}")
        
        # Process specific maxillofacial prosthetics subtopics based on the result
        specific_codes = []
        activated_subtopics = []
        
        # Check for each subtopic and activate if applicable
        if "D5992-D5937" in maxillofacial_result:
            print("Activating subtopic: General Maxillofacial Prosthetics (D5992-D5937)")
            general_prosthetics_code = activate_general_prosthetics(scenario)
            if general_prosthetics_code:
                specific_codes.append(general_prosthetics_code)
                activated_subtopics.append("General Maxillofacial Prosthetics (D5992-D5937)")
                
        if "D5986-D5999" in maxillofacial_result:
            print("Activating subtopic: Carriers (D5986-D5999)")
            carriers_code = activate_carriers(scenario)
            if carriers_code:
                specific_codes.append(carriers_code)
                activated_subtopics.append("Carriers (D5986-D5999)")
        
        # Choose the primary subtopic (either the first activated or a default)
        primary_subtopic = activated_subtopics[0] if activated_subtopics else "General Maxillofacial Prosthetics (D5992-D5937)"
        
        # Return the results in standardized format
        return {
            "code_range": maxillofacial_result,
            "subtopic": primary_subtopic,
            "activated_subtopics": activated_subtopics,
            "codes": specific_codes
        }
    except Exception as e:
        print(f"Error in maxillofacial prosthetics analysis: {str(e)}")
        return {}

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = input("Enter a dental maxillofacial prosthetics scenario: ")
    result = activate_maxillofacial_prosthetics(scenario)
    print(f"\n=== MAXILLOFACIAL PROSTHETICS ANALYSIS RESULT ===")
    print(f"CODE RANGE: {result.get('code_range', 'None')}")
    print(f"PRIMARY SUBTOPIC: {result.get('subtopic', 'None')}")
    print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
    print(f"SPECIFIC CODES: {', '.join(result.get('codes', []))}")
