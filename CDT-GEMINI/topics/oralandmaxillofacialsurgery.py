import os
import sys
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from llm_services import create_chain, invoke_chain, get_llm_service
load_dotenv()

# Add the root directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

# Now import modules
from topics.prompt import PROMPT
from subtopics.OralMaxillofacialSurgery import (
    activate_extractions,
    activate_other_surgical_procedures,
    activate_alveoloplasty,
    activate_vestibuloplasty,
    activate_excision_soft_tissue,
    activate_excision_intra_osseous,
    activate_excision_bone_tissue,
    activate_surgical_incision,
    activate_closed_fractures,
    activate_open_fractures,
    activate_tmj_dysfunctions,
    activate_traumatic_wounds,
    activate_complicated_suturing,
    activate_other_repair_procedures
)

def analyze_oral_maxillofacial_surgery(scenario):
    """
    Analyze an oral and maxillofacial surgery scenario and return relevant code ranges.
    
    Args:
        scenario (str): The dental scenario text to analyze
        
    Returns:
        str: The identified oral and maxillofacial surgery code range(s)
    """
    try:
        # Create the prompt template
        prompt_template = PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert with over 15 years of expertise in ADA dental codes. 
Your task is to analyze the given scenario and determine the most applicable oral and maxillofacial surgery code range(s) based on the following classifications:

## IMPORTANT GUIDELINES:
- You should activate ALL code ranges that have any potential relevance to the scenario
- Even if a code range is only slightly related, include it in your response
- Only exclude a code range if it is DEFINITELY NOT relevant to the scenario
- When in doubt, INCLUDE the code range rather than exclude it
- Multiple code ranges can and should be activated if they have any potential applicability
- Your goal is to ensure no potentially relevant codes are missed

## **Extractions (D7111-D7140)**
**Use when:** Removing teeth through simple non-surgical procedures.
**Check:** Documentation indicates routine extraction without significant bone removal or sectioning.
**Note:** These are straightforward procedures typically performed with elevators and forceps.
**Activation trigger:** Scenario mentions OR implies any simple extraction, removal of erupted tooth, or non-surgical tooth removal. INCLUDE this range if there's any indication of basic tooth extraction without surgical intervention.

## **Surgical Extractions (D7210-D7251)**
**Use when:** Removing teeth that require surgical intervention.
**Check:** Documentation details flap elevation, bone removal, or tooth sectioning.
**Note:** These procedures are more complex than simple extractions and may involve impacted teeth.
**Activation trigger:** Scenario mentions OR implies any surgical extraction, removal of bone, sectioning of tooth, impacted tooth, or complicated extraction. INCLUDE this range if there's any hint of extraction requiring more than elevators and forceps.

## **Other Surgical Procedures (D7260-D7297)**
**Use when:** Performing specialized oral surgical procedures beyond extractions.
**Check:** Documentation specifies the exact procedure and anatomical structures involved.
**Note:** These include oroantral fistula closures, tooth reimplantation, surgical exposure, and biopsies.
**Activation trigger:** Scenario mentions OR implies any specialized oral surgery, fistula, reimplantation, exposure of unerupted teeth, or tissue biopsy. INCLUDE this range if there's any suggestion of oral surgical procedures beyond extractions.

## **Alveoloplasty (D7310-D7321)**
**Use when:** Surgically remodeling and smoothing bone after extractions.
**Check:** Documentation describes ridge preparation and whether performed with extractions or separately.
**Note:** These procedures prepare the ridge for prosthetic placement.
**Activation trigger:** Scenario mentions OR implies any bone recontouring, ridge smoothing, preparation for dentures, or alveolar ridge modification. INCLUDE this range if there's any suggestion of bone remodeling related to tooth extraction sites.

## **Vestibuloplasty (D7340-D7350)**
**Use when:** Surgically modifying the vestibular depth and soft tissues.
**Check:** Documentation specifies the surgical approach and graft materials if used.
**Note:** These procedures increase the vestibular depth for prosthetic stability.
**Activation trigger:** Scenario mentions OR implies any vestibular extension, soft tissue modification for dentures, ridge extension, or tissue grafting for prosthetic purposes. INCLUDE this range if there's any indication of surgical alteration of vestibular tissues.

## **Excision of Soft Tissue Lesions (D7410-D7465)**
**Use when:** Removing lesions or abnormal tissues from oral structures.
**Check:** Documentation details size, location, and pathology results of excised tissue.
**Note:** These procedures address pathological conditions requiring removal.
**Activation trigger:** Scenario mentions OR implies any tissue biopsy, lesion removal, excision of abnormal tissue, or removal of cysts or tumors. INCLUDE this range if there's any hint of removing pathological tissue from the oral cavity.

## **Excision of Intra-Osseous Lesions (D7440-D7461)**
**Use when:** Removing lesions within the bone.
**Check:** Documentation specifies the exact procedure, lesion type, and extent of bone involvement.
**Note:** These address pathological conditions within the jawbones.
**Activation trigger:** Scenario mentions OR implies any bony lesion, intraosseous cyst, jaw tumor, or pathology within bone. INCLUDE this range if there's any indication of lesions or pathology within the jawbones requiring surgical removal.

## **Excision of Bone Tissue (D7471-D7490)**
**Use when:** Removing excess bone or bony growths.
**Check:** Documentation identifies the specific bony structure and reason for removal.
**Note:** These procedures address non-pathological bony overgrowths or interferences.
**Activation trigger:** Scenario mentions OR implies any tori, exostosis, excessive bone, bony protuberance, or bone removal for prosthetic purposes. INCLUDE this range if there's any suggestion of removing excess bone not related to pathology.

## **Surgical Incision (D7510-D7560)**
**Use when:** Creating surgical openings to drain infections or remove foreign bodies.
**Check:** Documentation describes the reason for incision and what was drained or removed.
**Note:** These procedures address acute conditions requiring immediate drainage.
**Activation trigger:** Scenario mentions OR implies any incision and drainage, abscess treatment, swelling, infection, or foreign body removal. INCLUDE this range if there's any suggestion of creating a surgical opening for therapeutic purposes.

## **Treatment of Fractures (D7610-D7780)**
**Use when:** Managing facial or jaw fractures through surgical intervention.
**Check:** Documentation specifies fracture type, location, and fixation method.
**Note:** These procedures restore function and proper alignment after trauma.
**Activation trigger:** Scenario mentions OR implies any jaw fracture, facial trauma, bone plating, fixation of fragments, or fracture reduction. INCLUDE this range if there's any indication of treating broken facial or jaw bones.

## **Reduction of Dislocation (D7810-D7880)**
**Use when:** Correcting dislocated temporomandibular joint or managing TMJ dysfunction.
**Check:** Documentation details the condition and specific intervention performed.
**Note:** These procedures address joint-related conditions affecting function.
**Activation trigger:** Scenario mentions OR implies any TMJ disorder, jaw joint problems, clicking, locking, disc displacement, or joint manipulation. INCLUDE this range if there's any hint of temporomandibular joint issues requiring intervention.

## **Repair of Traumatic Wounds (D7910-D7912)**
**Use when:** Suturing or otherwise closing traumatic wounds.
**Check:** Documentation specifies wound size, complexity, and repair technique.
**Note:** These procedures address soft tissue injuries from trauma.
**Activation trigger:** Scenario mentions OR implies any laceration, soft tissue injury, suturing, wound closure, or traumatic tissue damage. INCLUDE this range if there's any suggestion of repairing damaged oral tissues after injury.

## **Complicated Suturing (D7911-D7912)**
**Use when:** Closing complex wounds requiring advanced techniques.
**Check:** Documentation details the complexity factors and closure method.
**Note:** These are more involved than simple suturing procedures.
**Activation trigger:** Scenario mentions OR implies any complex laceration, extensive tissue damage, complicated wound closure, or wounds requiring layered repair. INCLUDE this range if there's any indication of complex wound management beyond simple suturing.

## **Other Repair Procedures (D7920-D7999)**
**Use when:** Performing specialized surgical procedures not covered by other categories.
**Check:** Documentation provides detailed narrative explaining the unusual or specialized procedure.
**Note:** These include skin grafts, sinus procedures, frenectomies, and other specialized surgeries.
**Activation trigger:** Scenario mentions OR implies any frenectomy, sinus procedures, skin grafts, bone replacement, specialized surgical interventions, or unusual maxillofacial procedures. INCLUDE this range if there's any hint of specialized surgical procedures not clearly fitting other categories.

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
        print(f"Analyzing oral and maxillofacial surgery scenario: {scenario[:100]}...")
        
        # Use invoke through our LLM service
        result = invoke_chain(chain, {"scenario": scenario})
        
        # Extract the text from the result
        code_range = result.get("text", "").strip()
        
        print(f"Oral & Maxillofacial Surgery analyze_oral_maxillofacial_surgery result: {code_range}")
        return code_range
    except Exception as e:
        print(f"Error in analyze_oral_maxillofacial_surgery: {str(e)}")
        return ""

def activate_oral_maxillofacial_surgery(scenario):
    """
    Activate oral and maxillofacial surgery analysis and return the results with specific subtopic activations.
    
    Args:
        scenario (str): The dental scenario text to analyze
        
    Returns:
        dict: A dictionary containing the code range, subtopic and specific codes
    """
    try:
        # Get the code range from the analysis
        oral_surgery_result = analyze_oral_maxillofacial_surgery(scenario)
        if not oral_surgery_result:
            print("No oral and maxillofacial surgery result returned")
            return {}
        
        print(f"Oral & Maxillofacial Surgery Result in activate_oral_maxillofacial_surgery: {oral_surgery_result}")
        
        # Process specific oral and maxillofacial surgery subtopics based on the result
        specific_codes = []
        activated_subtopics = []
        
        # Check for each subtopic and activate if applicable
        if "D7111-D7251" in oral_surgery_result:
            print("Activating subtopic: Extractions (D7111-D7251)")
            extractions_code = activate_extractions(scenario)
            if extractions_code:
                specific_codes.append(extractions_code)
                activated_subtopics.append("Extractions (D7111-D7251)")
                
        if "D7260-D7297" in oral_surgery_result:
            print("Activating subtopic: Other Surgical Procedures (D7260-D7297)")
            other_surgical_code = activate_other_surgical_procedures(scenario)
            if other_surgical_code:
                specific_codes.append(other_surgical_code)
                activated_subtopics.append("Other Surgical Procedures (D7260-D7297)")
                
        # For sialoliths, also check other surgical procedures even if not explicitly in the result
        if "sialolith" in scenario.lower() and "D7260-D7297" not in oral_surgery_result:
            print("Activating subtopic: Other Surgical Procedures (D7260-D7297) - Sialolithotomy")
            other_surgical_code = activate_other_surgical_procedures(scenario)
            if other_surgical_code:
                specific_codes.append(other_surgical_code)
                activated_subtopics.append("Other Surgical Procedures (D7260-D7297) - Sialolithotomy")
                
        if "D7310-D7321" in oral_surgery_result:
            print("Activating subtopic: Alveoloplasty (D7310-D7321)")
            alveoloplasty_code = activate_alveoloplasty(scenario)
            if alveoloplasty_code:
                specific_codes.append(alveoloplasty_code)
                activated_subtopics.append("Alveoloplasty (D7310-D7321)")
                
        if "D7340-D7350" in oral_surgery_result:
            print("Activating subtopic: Vestibuloplasty (D7340-D7350)")
            vestibuloplasty_code = activate_vestibuloplasty(scenario)
            if vestibuloplasty_code:
                specific_codes.append(vestibuloplasty_code)
                activated_subtopics.append("Vestibuloplasty (D7340-D7350)")
                
        if "D7410-D7465" in oral_surgery_result:
            print("Activating subtopic: Excision of Soft Tissue Lesions (D7410-D7465)")
            soft_tissue_code = activate_excision_soft_tissue(scenario)
            if soft_tissue_code:
                specific_codes.append(soft_tissue_code)
                activated_subtopics.append("Excision of Soft Tissue Lesions (D7410-D7465)")
                
        if "D7440-D7461" in oral_surgery_result:
            print("Activating subtopic: Excision of Intra-Osseous Lesions (D7440-D7461)")
            intra_osseous_code = activate_excision_intra_osseous(scenario)
            if intra_osseous_code:
                specific_codes.append(intra_osseous_code)
                activated_subtopics.append("Excision of Intra-Osseous Lesions (D7440-D7461)")
                
        if "D7471-D7490" in oral_surgery_result:
            print("Activating subtopic: Excision of Bone Tissue (D7471-D7490)")
            bone_tissue_code = activate_excision_bone_tissue(scenario)
            if bone_tissue_code:
                specific_codes.append(bone_tissue_code)
                activated_subtopics.append("Excision of Bone Tissue (D7471-D7490)")
                
        if "D7509-D7560" in oral_surgery_result:
            print("Activating subtopic: Surgical Incision (D7509-D7560)")
            surgical_incision_code = activate_surgical_incision(scenario)
            if surgical_incision_code:
                specific_codes.append(surgical_incision_code)
                activated_subtopics.append("Surgical Incision (D7509-D7560)")
                
        if "D7610-D7680" in oral_surgery_result:
            print("Activating subtopic: Treatment of Closed Fractures (D7610-D7680)")
            closed_fractures_code = activate_closed_fractures(scenario)
            if closed_fractures_code:
                specific_codes.append(closed_fractures_code)
                activated_subtopics.append("Treatment of Closed Fractures (D7610-D7680)")
                
        if "D7710-D7780" in oral_surgery_result:
            print("Activating subtopic: Treatment of Open Fractures (D7710-D7780)")
            open_fractures_code = activate_open_fractures(scenario)
            if open_fractures_code:
                specific_codes.append(open_fractures_code)
                activated_subtopics.append("Treatment of Open Fractures (D7710-D7780)")
                
        if "D7810-D7899" in oral_surgery_result:
            print("Activating subtopic: TMJ Dysfunctions (D7810-D7899)")
            tmj_code = activate_tmj_dysfunctions(scenario)
            if tmj_code:
                specific_codes.append(tmj_code)
                activated_subtopics.append("TMJ Dysfunctions (D7810-D7899)")
                
        if "D7910" in oral_surgery_result:
            print("Activating subtopic: Repair of Traumatic Wounds (D7910)")
            traumatic_wounds_code = activate_traumatic_wounds(scenario)
            if traumatic_wounds_code:
                specific_codes.append(traumatic_wounds_code)
                activated_subtopics.append("Repair of Traumatic Wounds (D7910)")
                
        if "D7911-D7912" in oral_surgery_result:
            print("Activating subtopic: Complicated Suturing (D7911-D7912)")
            complicated_suturing_code = activate_complicated_suturing(scenario)
            if complicated_suturing_code:
                specific_codes.append(complicated_suturing_code)
                activated_subtopics.append("Complicated Suturing (D7911-D7912)")
                
        if "D7920-D7999" in oral_surgery_result:
            print("Activating subtopic: Other Repair Procedures (D7920-D7999)")
            other_repair_code = activate_other_repair_procedures(scenario)
            if other_repair_code:
                specific_codes.append(other_repair_code)
                activated_subtopics.append("Other Repair Procedures (D7920-D7999)")
        
        # Choose the primary subtopic (either the first activated or a default)
        primary_subtopic = activated_subtopics[0] if activated_subtopics else "Extractions (D7111-D7251)"
        
        # Return the results in standardized format
        return {
            "code_range": oral_surgery_result,
            "subtopic": primary_subtopic,
            "activated_subtopics": activated_subtopics,
            "codes": specific_codes
        }
    except Exception as e:
        print(f"Error in oral and maxillofacial surgery analysis: {str(e)}")
        return {}

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = input("Enter an oral and maxillofacial surgery scenario: ")
    result = activate_oral_maxillofacial_surgery(scenario)
    print(f"\n=== ORAL & MAXILLOFACIAL SURGERY ANALYSIS RESULT ===")
    print(f"CODE RANGE: {result.get('code_range', 'None')}")
    print(f"PRIMARY SUBTOPIC: {result.get('subtopic', 'None')}")
    print(f"ACTIVATED SUBTOPICS: {', '.join(result.get('activated_subtopics', []))}")
    print(f"SPECIFIC CODES: {', '.join(result.get('codes', []))}")
