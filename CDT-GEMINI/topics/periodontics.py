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
from subtopics.Periodontics import (
    activate_surgical_services,
    activate_non_surgical_services,
    activate_other_periodontal_services,
)

def analyze_periodontic(scenario):
    """
    Analyze a periodontic scenario and return relevant code ranges.
    
    Args:
        scenario (str): The dental scenario text to analyze
        
    Returns:
        str: The identified periodontic code range(s)
    """
    try:
        # Create the prompt template
        prompt_template = PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert with over 15 years of expertise in ADA dental codes. 
Your task is to analyze the given scenario and determine the most applicable periodontal code range(s) based on the following classifications:


## **Surgical Services (D4210-D4286)**
**Use when:** Performing invasive periodontal procedures involving incisions and flap elevation.
**Check:** Documentation details the specific surgical approach, tissues involved, and treatment goals.
**Note:** These procedures address moderate to severe periodontal disease through surgical intervention.
**Activation trigger:** Scenario mentions OR implies any gum surgery, periodontal surgery, flap procedure, gingivectomy, graft placement, or surgical treatment of periodontal disease. INCLUDE this range if there's any indication of invasive treatment of gum or periodontal tissues.

## **Non-Surgical Periodontal Services (D4322-D4381)**
**Use when:** Providing non-invasive treatment for periodontal disease.
**Check:** Documentation specifies the extent of treatment and instruments/methods used.
**Note:** These procedures treat periodontal disease without surgical intervention.
**Activation trigger:** Scenario mentions OR implies any scaling and root planing, deep cleaning, periodontal debridement, non-surgical periodontal therapy, or treatment of gum disease without surgery. INCLUDE this range if there's any hint of non-surgical treatment of periodontal conditions.

## **Other Periodontal Services (D4910-D4999)**
**Use when:** Providing specialized periodontal care beyond routine treatment.
**Check:** Documentation details the specific service and its therapeutic purpose.
**Note:** These include maintenance treatments following active therapy and specialized interventions.
**Activation trigger:** Scenario mentions OR implies any periodontal maintenance, antimicrobial delivery, gingival irrigation, local drug delivery, or follow-up periodontal care. INCLUDE this range if there's any suggestion of ongoing periodontal management or specialized treatments.

### **Scenario:**
{{scenario}}
{PROMPT}

RESPOND WITH ALL APPLICABLE CODE RANGES from the options above, even if they are only slightly relevant.
List them in order of relevance, with the most relevant first.
Example: "D4322-D4381, D4910-D4999, D4210-D4286"
""",
            input_variables=["scenario"]
        )
        
        # Create the chain using our LLM service
        chain = create_chain(prompt_template)
        
        # Use the provided scenario directly
        print(f"Analyzing periodontic scenario: {scenario[:100]}...")
        
        # Use invoke through our LLM service
        result = invoke_chain(chain, {"scenario": scenario})
        
        # Extract the text from the result
        code_range = result.get("text", "").strip()
        
        print(f"Periodontic analyze_periodontic result: {code_range}")
        return code_range
    except Exception as e:
        print(f"Error in analyze_periodontic: {str(e)}")
        return ""

def activate_periodontic(scenario):
    """
    Activate periodontic analysis and return the results with specific subtopic activations.
    
    Args:
        scenario (str): The dental scenario text to analyze
        
    Returns:
        dict: A dictionary containing the code range, subtopic and specific codes
    """
    try:
        # Get the code range from the analysis
        periodontic_result = analyze_periodontic(scenario)
        if not periodontic_result:
            print("No periodontic result returned")
            return {}
        
        print(f"Periodontic Result in activate_periodontic: {periodontic_result}")
        
        # Process specific periodontic subtopics based on the result
        specific_codes = []
        activated_subtopics = []
        
        # Check for each subtopic and activate if applicable
        if "D4210-D4286" in periodontic_result:
            print("Activating subtopic: Surgical Services (D4210-D4286)")
            surgical_code = activate_surgical_services(scenario)
            if surgical_code:
                specific_codes.append(surgical_code)
                activated_subtopics.append("Surgical Services (D4210-D4286)")
                
        if "D4322-D4381" in periodontic_result:
            print("Activating subtopic: Non-Surgical Services (D4322-D4381)")
            non_surgical_code = activate_non_surgical_services(scenario)
            if non_surgical_code:
                specific_codes.append(non_surgical_code)
                activated_subtopics.append("Non-Surgical Services (D4322-D4381)")
                
        if "D4910-D4999" in periodontic_result:
            print("Activating subtopic: Other Periodontal Services (D4910-D4999)")
            other_code = activate_other_periodontal_services(scenario)
            if other_code:
                specific_codes.append(other_code)
                activated_subtopics.append("Other Periodontal Services (D4910-D4999)")
        
        # Choose the primary subtopic (either the first activated or a default)
        primary_subtopic = activated_subtopics[0] if activated_subtopics else "Non-Surgical Services (D4322-D4381)"
        
        # Return the results in standardized format
        return {
            "code_range": periodontic_result,
            "subtopic": primary_subtopic,
            "activated_subtopics": activated_subtopics,
            "codes": specific_codes
        }
    except Exception as e:
        print(f"Error in periodontic analysis: {str(e)}")
        return {}

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = input("Enter a periodontic scenario: ")
    result = activate_periodontic(scenario)
    print(f"\n=== PERIODONTIC ANALYSIS RESULT ===")
    print(f"CODE RANGE: {result.get('code_range', 'None')}")
    print(f"PRIMARY SUBTOPIC: {result.get('subtopic', 'None')}")
    print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
    print(f"SPECIFIC CODES: {', '.join(result.get('codes', []))}")
