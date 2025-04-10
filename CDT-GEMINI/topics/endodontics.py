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

# Now try to import subtopics, with a fallback mechanism
try:
    # Note: The directory is named 'Endodontics' (capitalized) - matching directory structure
    from subtopics.Endodontics import (
        activate_pulp_capping,
        activate_pulpotomy,
        activate_primary_teeth_therapy,
        activate_endodontic_therapy,
        activate_endodontic_retreatment,
        activate_apexification,
        activate_pulpal_regeneration,
        activate_apicoectomy,
        activate_other_endodontic
    )
except ImportError:
    print("Warning: Could not import subtopics for Endodontics. Using fallback functions.")
    

def analyze_endodontic(scenario):
    """
    Analyze a dental endodontic scenario and return relevant code ranges.
    
    Args:
        scenario (str): The dental scenario text to analyze
        
    Returns:
        str: The identified endodontic code range(s)
    """
    try:
        # Create the prompt template
        prompt_template = PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert with over 15 years of expertise in ADA dental codes. 
Your task is to analyze the given scenario and determine the most applicable endodontic code range(s) based on the following classifications:


## **Pulp Capping (D3110-D3120)**
**Use when:** Protecting exposed or nearly exposed pulp to preserve vitality.
**Check:** Documentation specifies direct or indirect pulp capping and materials used.
**Note:** These procedures aim to promote healing and prevent the need for root canal therapy.
**Activation trigger:** Scenario mentions OR implies any deep decay, pulp exposure, protective material placement, or efforts to maintain pulp vitality. INCLUDE this range if there's any indication of protecting the pulp from exposure or further damage.

## **Pulpotomy (D3220-D3222)**
**Use when:** Removing the coronal portion of pulp tissue while preserving radicular pulp.
**Check:** Documentation clearly indicates partial pulp removal and reason for procedure.
**Note:** Often performed on primary teeth or as an emergency procedure in permanent teeth.
**Activation trigger:** Scenario mentions OR implies any partial pulp removal, emergency pulpal treatment, or treatment of traumatic exposures. INCLUDE this range if there's any suggestion of coronal pulp removal or pain relief through pulp therapy.

## **Endodontic Therapy on Primary Teeth (D3230-D3240)**
**Use when:** Providing pulp therapy specifically for primary teeth.
**Check:** Documentation identifies primary teeth and specifies the pulpal treatment performed.
**Note:** These procedures are designed specifically for primary dentition with consideration for eventual exfoliation.
**Activation trigger:** Scenario mentions OR implies any primary tooth pulp treatment, pulpectomy in baby teeth, or root canal in deciduous teeth. INCLUDE this range if there's any indication of pulp therapy in a primary tooth.

## **Endodontic Therapy (D3310-D3333)**
**Use when:** Performing complete root canal treatment for permanent teeth.
**Check:** Documentation specifies the tooth treated and details of canal preparation and obturation.
**Note:** Different codes apply based on the tooth type (anterior, premolar, or molar).
**Activation trigger:** Scenario mentions OR implies any root canal treatment, pulpectomy, canal preparation, obturation, or treatment of irreversible pulpitis or necrosis. INCLUDE this range if there's any hint that complete endodontic therapy is needed or being performed.

## **Endodontic Retreatment (D3346-D3348)**
**Use when:** Redoing previously treated root canals that have failed.
**Check:** Documentation confirms previous endodontic treatment and reason for retreatment.
**Note:** These procedures involve removing previous filling materials and addressing issues like missed canals.
**Activation trigger:** Scenario mentions OR implies any failed root canal, persistent infection, retreatment, revision, or removal of previous canal fillings. INCLUDE this range if there's any suggestion that a tooth with previous endodontic treatment requires additional therapy.

## **Apexification/Recalcification (D3351)**
**Use when:** Treating immature permanent teeth with open apices.
**Check:** Documentation describes the tooth's developmental stage and material placement.
**Note:** These procedures promote apical closure in non-vital immature teeth.
**Activation trigger:** Scenario mentions OR implies any open apex, immature tooth with pulp necrosis, apical barrier placement, or calcium hydroxide/MTA procedures. INCLUDE this range if there's any indication of treating a non-vital tooth with incomplete root development.

## **Pulpal Regeneration (D3355-D3357)**
**Use when:** Attempting to regenerate pulp-dentin complex in immature necrotic teeth.
**Check:** Documentation details regenerative approach and materials used.
**Note:** These biologically-based procedures aim to continue root development.
**Activation trigger:** Scenario mentions OR implies any regenerative endodontic procedure, revascularization, blood clot induction, or stem cell approaches for immature teeth. INCLUDE this range if there's any suggestion of regenerative approaches rather than traditional apexification.

## **Apicoectomy/Periradicular Services (D3410-D3470)**
**Use when:** Performing surgical endodontic procedures to resolve periapical pathology.
**Check:** Documentation specifies the surgical approach, access, and root-end management.
**Note:** These procedures address cases where conventional root canal treatment is insufficient.
**Activation trigger:** Scenario mentions OR implies any periapical surgery, root-end resection, apicoectomy, retrograde filling, or persistent periapical pathology. INCLUDE this range if there's any indication that surgical intervention for endodontic issues is needed.

## **Other Endodontic Procedures (D3910-D3999)**
**Use when:** Performing specialized endodontic services not covered by other categories.
**Check:** Documentation provides detailed narrative explaining the unusual or specialized procedure.
**Note:** These include procedures like tooth isolation, hemisection, or internal bleaching.
**Activation trigger:** Scenario mentions OR implies any specialized endodontic service, surgical exposure of root, internal bleaching, canal preparation for post, hemisection, or unclassified endodontic procedures. INCLUDE this range if there's any hint of endodontic procedures that don't clearly fit other categories.

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
        print(f"Analyzing endodontic scenario: {scenario[:100]}...")
        
        # Use invoke through our LLM service
        result = invoke_chain(chain, {"scenario": scenario})
        
        # Extract the text from the result
        code_range = result.get("text", "").strip()
        
        print(f"Endodontics analyze_endodontic result: {code_range}")
        return code_range
    except Exception as e:
        print(f"Error in analyze_endodontic: {str(e)}")
        return ""

def activate_endodontic(scenario):
    """
    Activate endodontic analysis and return the results with specific subtopic activations.
    
    Args:
        scenario (str): The dental scenario text to analyze
        
    Returns:
        dict: A dictionary containing the code range, subtopic and specific codes
    """
    try:
        # Get the code range from the analysis
        endodontic_result = analyze_endodontic(scenario)
        if not endodontic_result:
            print("No endodontic result returned")
            return {}
        
        print(f"Endodontic Result in activate_endodontic: {endodontic_result}")
        
        # Process specific endodontic subtopics based on the result
        specific_codes = []
        activated_subtopics = []
        
        # Check for each subtopic and activate if applicable
        if "D3110-D3120" in endodontic_result:
            print("Activating subtopic: Pulp Capping (D3110-D3120)")
            pulp_capping_code = activate_pulp_capping(scenario)
            if pulp_capping_code:
                specific_codes.append(pulp_capping_code)
                activated_subtopics.append("Pulp Capping (D3110-D3120)")
                
        if "D3220-D3222" in endodontic_result:
            print("Activating subtopic: Pulpotomy (D3220-D3222)")
            pulpotomy_code = activate_pulpotomy(scenario)
            if pulpotomy_code:
                specific_codes.append(pulpotomy_code)
                activated_subtopics.append("Pulpotomy (D3220-D3222)")
                
        if "D3230-D3240" in endodontic_result:
            print("Activating subtopic: Endodontic Therapy on Primary Teeth (D3230-D3240)")
            primary_teeth_code = activate_primary_teeth_therapy(scenario)
            if primary_teeth_code:
                specific_codes.append(primary_teeth_code)
                activated_subtopics.append("Endodontic Therapy on Primary Teeth (D3230-D3240)")
                
        if "D3310-D3333" in endodontic_result:
            print("Activating subtopic: Endodontic Therapy (D3310-D3333)")
            endodontic_therapy_code = activate_endodontic_therapy(scenario)
            if endodontic_therapy_code:
                specific_codes.append(endodontic_therapy_code)
                activated_subtopics.append("Endodontic Therapy (D3310-D3333)")
                
        if "D3346-D3348" in endodontic_result:
            print("Activating subtopic: Endodontic Retreatment (D3346-D3348)")
            retreatment_code = activate_endodontic_retreatment(scenario)
            if retreatment_code:
                specific_codes.append(retreatment_code)
                activated_subtopics.append("Endodontic Retreatment (D3346-D3348)")
                
        if "D3351" in endodontic_result:
            print("Activating subtopic: Apexification/Recalcification (D3351)")
            apexification_code = activate_apexification(scenario)
            if apexification_code:
                specific_codes.append(apexification_code)
                activated_subtopics.append("Apexification/Recalcification (D3351)")
                
        if "D3355-D3357" in endodontic_result:
            print("Activating subtopic: Pulpal Regeneration (D3355-D3357)")
            regeneration_code = activate_pulpal_regeneration(scenario)
            if regeneration_code:
                specific_codes.append(regeneration_code)
                activated_subtopics.append("Pulpal Regeneration (D3355-D3357)")
                
        if "D3410-D3470" in endodontic_result:
            print("Activating subtopic: Apicoectomy/Periradicular Services (D3410-D3470)")
            apicoectomy_code = activate_apicoectomy(scenario)
            if apicoectomy_code:
                specific_codes.append(apicoectomy_code)
                activated_subtopics.append("Apicoectomy/Periradicular Services (D3410-D3470)")
                
        if "D3910-D3999" in endodontic_result:
            print("Activating subtopic: Other Endodontic Procedures (D3910-D3999)")
            other_code = activate_other_endodontic(scenario)
            if other_code:
                specific_codes.append(other_code)
                activated_subtopics.append("Other Endodontic Procedures (D3910-D3999)")
        
        # Choose the primary subtopic (either the first activated or a default)
        primary_subtopic = activated_subtopics[0] if activated_subtopics else "Endodontic Procedures"
        
        # Return the results in standardized format
        return {
            "code_range": endodontic_result,
            "subtopic": primary_subtopic,
            "activated_subtopics": activated_subtopics,
            "codes": specific_codes
        }
    except Exception as e:
        print(f"Error in endodontic analysis: {str(e)}")
        return {}

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = input("Enter an endodontic dental scenario: ")
    result = activate_endodontic(scenario)
    print(f"\n=== ENDODONTIC ANALYSIS RESULT ===")
    print(f"CODE RANGE: {result.get('code_range', 'None')}")
    print(f"PRIMARY SUBTOPIC: {result.get('subtopic', 'None')}")
    print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
    print(f"SPECIFIC CODES: {', '.join(result.get('codes', []))}")

