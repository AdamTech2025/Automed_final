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
from subtopics.Preventive import (
    activate_dental_prophylaxis,
    activate_topical_fluoride,
    activate_other_preventive_services,
    activate_space_maintenance,
    activate_space_maintainers,
    activate_vaccinations
)

def analyze_preventive(scenario):
    """
    Analyze a preventive scenario and return relevant code ranges.
    
    Args:
        scenario (str): The dental scenario text to analyze
        
    Returns:
        str: The identified preventive code range(s)
    """
    try:
        # Create the prompt template
        prompt_template = PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert with over 15 years of expertise in ADA dental codes. 
Your task is to analyze the given scenario and determine the most applicable preventive code range(s) based on the following classifications:

## **Dental Prophylaxis (D1110-D1120)**
**Use when:** Providing routine dental cleaning to remove plaque, calculus, and extrinsic stains from the tooth surfaces and implant abutments to maintain oral health and prevent periodontal disease.
**Check:** Documentation specifies whether the patient is an adult (D1110) with permanent/transitional dentition or a child (D1120) with primary/transitional dentition.
**Note:** Adult prophylaxis (D1110) is typically for patients 14 years and older, while child prophylaxis (D1120) is for patients under 14 years old. These services are distinct from therapeutic periodontal procedures like scaling and root planing.
**Activation trigger:** Scenario mentions OR implies any routine cleaning, dental prophylaxis, removal of plaque/calculus/stains, hygiene appointment, recall visit, regular 6-month checkup with cleaning, maintenance cleaning, or preventive oral hygiene care. INCLUDE this range if there is any indication of professional cleaning or patients coming in for their routine preventive appointment.

## **Topical Fluoride Treatment (D1206-D1208)**
**Use when:** Applying professional fluoride treatments to prevent tooth decay, strengthen enamel, and promote remineralization of early carious lesions.
**Check:** Documentation indicates whether fluoride varnish (D1206) or topical application of fluoride excluding varnish (D1208) was provided, along with the risk assessment supporting the need for fluoride.
**Note:** Fluoride treatments are not limited to children and are indicated for patients with moderate to high caries risk, exposed root surfaces, xerostomia, active orthodontic treatment, or other risk factors for dental caries.
**Activation trigger:** Scenario mentions OR implies any professional fluoride application, fluoride varnish, fluoride gel/foam, fluoride treatment, caries prevention measures, remineralization therapy, or treatment for sensitive teeth with fluoride. INCLUDE this range if there's any hint of professional topical fluoride being applied or considered for caries prevention.

## **Other Preventive Services (D1310-D1355)**
**Use when:** Providing preventive services beyond basic cleaning and fluoride, such as oral hygiene instruction, nutritional counseling, tobacco cessation counseling, sealants, or caries arresting medicaments.
**Check:** Documentation clearly describes the specific preventive service, patient education, counseling provided, or the teeth sealed with preventive resin materials.
**Note:** These codes (D1310-D1355) cover a wide range of preventive interventions designed to reduce risk factors for oral disease, including educational, behavioral, and minimally invasive clinical procedures aimed at preventing future disease rather than treating existing conditions.
**Activation trigger:** Scenario mentions OR implies any oral hygiene instructions, nutritional or tobacco counseling, application of sealants to pits and fissures, silver diamine fluoride application, interim caries arresting medicament, oral cancer screening, caries risk assessment, or other non-restorative prevention procedures. INCLUDE this range if there's any suggestion of preventive care beyond routine cleaning and fluoride treatments.

## **Space Maintenance (D1510-D1555)**
**Use when:** Placing, repairing, or removing appliances designed to maintain space for erupting permanent teeth following premature loss of primary teeth.
**Check:** Documentation describes the type of space maintainer (fixed or removable), its location (unilateral or bilateral, maxillary or mandibular), and whether it's an initial placement, repair, or removal procedure.
**Note:** These devices (D1510-D1555) are critical in pediatric dentistry to preserve arch length and prevent malocclusion following early loss of primary teeth. Different codes apply based on design features, with special consideration for distal shoe appliances that guide unerupted first permanent molars.
**Activation trigger:** Scenario mentions OR implies any space maintainer placement, space maintenance following extraction or premature loss of primary teeth, band and loop appliance, lingual arch, transpalatal arch, distal shoe appliance, recementation of space maintainer, or removal of space maintainer. INCLUDE this range if there's any indication of managing space in a developing dentition after tooth loss.

## **Vaccinations (D1701-D1707)**
**Use when:** Administering vaccines in the dental setting to prevent diseases with oral manifestations or connection to oral health.
**Check:** Documentation confirms the type of vaccine administered, patient consent, and compliance with state regulations allowing dentists to administer vaccines.
**Note:** These codes (D1701-D1707) represent an expanding area of dental practice focused on preventing diseases with oral connections, such as HPV-related oropharyngeal cancers. Not all jurisdictions permit dentists to administer vaccines.
**Activation trigger:** Scenario mentions OR implies any administration of vaccines by dental providers, HPV vaccination, vaccine administration to prevent oral disease, dental practice-based immunization, or counseling related to vaccines that prevent oral or oropharyngeal conditions. INCLUDE this range if there's any reference to vaccination services provided in a dental setting.

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
        print(f"Analyzing preventive scenario: {scenario[:100]}...")
        
        # Use invoke through our LLM service
        result = invoke_chain(chain, {"scenario": scenario})
        
        # Extract the text from the result
        code_range = result.get("text", "").strip()
        
        print(f"Preventive analyze_preventive result: {code_range}")
        return code_range
    except Exception as e:
        print(f"Error in analyze_preventive: {str(e)}")
        return ""

def activate_preventive(scenario):
    """
    Activate preventive analysis and return the results with specific subtopic activations.
    
    Args:
        scenario (str): The dental scenario text to analyze
        
    Returns:
        dict: A dictionary containing the code range, subtopic and specific codes
    """
    try:
        # Get the code range from the analysis
        preventive_result = analyze_preventive(scenario)
        if not preventive_result:
            print("No preventive result returned")
            return {}
        
        print(f"Preventive Result in activate_preventive: {preventive_result}")
        
        # Process specific preventive subtopics based on the result
        specific_codes = []
        activated_subtopics = []
        
        # Check for each subtopic and activate if applicable
        if "D1110-D1120" in preventive_result:
            print("Activating subtopic: Dental Prophylaxis (D1110-D1120)")
            prophylaxis_code = activate_dental_prophylaxis(scenario)
            if prophylaxis_code:
                specific_codes.append(prophylaxis_code)
                activated_subtopics.append("Dental Prophylaxis (D1110-D1120)")
                
        if "D1206-D1208" in preventive_result:
            print("Activating subtopic: Topical Fluoride Treatment (D1206-D1208)")
            fluoride_code = activate_topical_fluoride(scenario)
            if fluoride_code:
                specific_codes.append(fluoride_code)
                activated_subtopics.append("Topical Fluoride Treatment (D1206-D1208)")
                
        if "D1310-D1355" in preventive_result:
            print("Activating subtopic: Other Preventive Services (D1310-D1355)")
            other_code = activate_other_preventive_services(scenario)
            if other_code:
                specific_codes.append(other_code)
                activated_subtopics.append("Other Preventive Services (D1310-D1355)")
                
        if "D1510-D1555" in preventive_result:
            print("Activating subtopic: Space Maintenance (D1510-D1555)")
            maintenance_code = activate_space_maintenance(scenario)
            if maintenance_code:
                specific_codes.append(maintenance_code)
                activated_subtopics.append("Space Maintenance (D1510-D1555)")
                
        if "D1510-D1575" in preventive_result:
            print("Activating subtopic: Space Maintainers (D1510-D1575)")
            maintainers_code = activate_space_maintainers(scenario)
            if maintainers_code:
                specific_codes.append(maintainers_code)
                activated_subtopics.append("Space Maintainers (D1510-D1575)")
                
        if "D1701-D1707" in preventive_result:
            print("Activating subtopic: Vaccinations (D1701-D1707)")
            vaccination_code = activate_vaccinations(scenario)
            if vaccination_code:
                specific_codes.append(vaccination_code)
                activated_subtopics.append("Vaccinations (D1701-D1707)")
        
        # Choose the primary subtopic (either the first activated or a default)
        primary_subtopic = activated_subtopics[0] if activated_subtopics else "Dental Prophylaxis (D1110-D1120)"
        
        # Format detailed results if specific codes were found
        if specific_codes:
            # Return a dictionary with the required fields
            return {
                "code_range": preventive_result,
                "subtopic": primary_subtopic,
                "activated_subtopics": activated_subtopics,  # Add this for clarity about which subtopics were activated
                "codes": specific_codes
            }
            
        # Return a dictionary even if no specific codes were found
        return {
            "code_range": preventive_result,
            "subtopic": primary_subtopic,
            "activated_subtopics": activated_subtopics,
            "codes": []
        }
    except Exception as e:
        print(f"Error in preventive analysis: {str(e)}")
        return {}

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = input("Enter a preventive dental scenario: ")
    result = activate_preventive(scenario)
    print(f"\n=== PREVENTIVE ANALYSIS RESULT ===")
    print(f"CODE RANGE: {result.get('code_range', 'None')}")
    print(f"PRIMARY SUBTOPIC: {result.get('subtopic', 'None')}")
    print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
    print(f"SPECIFIC CODES: {', '.join(result.get('codes', []))}")