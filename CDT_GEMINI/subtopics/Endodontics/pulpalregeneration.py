import os
import sys
from langchain.prompts import PromptTemplate
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file
from subtopics.prompt.prompt import PROMPT



def create_pulpal_regeneration_extractor():
    """
    Create a LangChain-based Pulpal Regeneration code extractor.
    """
    prompt_template = f"""
You are a highly experienced dental coding expert 


### Before Picking a Code, Ask:
- What was the primary reason the patient came in? Did they present with a specific issue (e.g., trauma, immature tooth with necrotic pulp) requiring pulpal regeneration, or was it identified during an exam?
- Is this the initial visit, an interim medication replacement, or the completion of the regeneration process?
- Does the tooth have an open apex or immature root development necessitating regenerative treatment?
- Are diagnostic tools (e.g., radiographs, pulp vitality tests) confirming the need for pulpal regeneration?
- Is the tooth a candidate for regeneration (e.g., young patient, no extensive damage), or is traditional root canal therapy more appropriate?

---

### Pulpal Regeneration

#### Code: D3355
**Heading:** Pulpal regeneration — initial visit  
**Description:** Includes opening tooth, preparation of canal spaces, placement of medication.  
**When to Use:**  
- The patient has a permanent tooth with an immature apex and necrotic pulp (often due to trauma or caries), requiring the start of regenerative endodontic treatment.  
- The procedure involves accessing the tooth, cleaning canal spaces, and placing medication (e.g., antibiotic paste) to stimulate regeneration.  
- Use for the first visit of a multi-step pulpal regeneration process.  
**What to Check:**  
- Confirm the tooth is permanent with an open apex via radiograph (e.g., wide canal, thin walls).  
- Assess pulp status (e.g., necrotic but not fully infected beyond regeneration potential).  
- Check patient age (typically younger patients, e.g., 6-18) and tooth condition for regeneration viability.  
- Verify no contraindications (e.g., severe root damage, patient allergies to medications).  
**Notes:**  
- This is the initial step only—subsequent visits use D3356 or D3357 as needed.  
- Requires detailed documentation (e.g., X-rays, clinical findings) for insurance due to specialized nature.  
- Not for mature teeth or standard root canal therapy (see D3310-D3330).  

#### Code: D3356
**Heading:** Pulpal regeneration — interim medication replacement  
**When to Use:**  
- The patient returns for a follow-up visit after the initial pulpal regeneration (D3355) to replace or adjust intracanal medication.  
- Involves removing old medication, irrigating the canal, and placing new medication to promote continued regeneration.  
- Use for interim visits between the initial and final stages of treatment.  
**What to Check:**  
- Confirm prior D3355 was performed and the tooth remains a candidate for regeneration.  
- Assess canal condition (e.g., signs of healing, no persistent infection) via exam or radiograph.  
- Check patient symptoms (e.g., reduced pain, no swelling) and response to initial treatment.  
- Verify the need for additional medication rather than completion (D3357).  
**Notes:**  
- May be used multiple times if several interim visits are required—document each instance.  
- Not a standalone code—must follow D3355 and precede D3357 in the regeneration sequence.  
- Narrative may be needed to explain the number of interim visits for insurance approval.  

#### Code: D3357
**Heading:** Pulpal regeneration — completion of treatment  
**Description:** Does not include final restoration.  
**When to Use:**  
- The patient has completed the regenerative process, and the final visit seals the canal with a biocompatible material (e.g., MTA) to encourage root development.  
- Use when the pulpal regeneration treatment concludes, confirming apex closure or dentin thickening.  
- Applied after initial (D3355) and any interim (D3356) visits.  
**What to Check:**  
- Confirm prior D3355 and D3356 (if applicable) were performed and regeneration goals are met.  
- Assess radiographic evidence of root maturation (e.g., apex closure, wall thickening).  
- Check for resolution of symptoms and absence of infection or inflammation.  
- Verify the tooth's stability and readiness for final restoration (coded separately).  
**Notes:**  
- Excludes final restoration—use separate codes (e.g., D2950, D2750) for core buildup or crown.  
- Requires pre- and post-treatment X-rays and a narrative for insurance to document success.  
- Not for incomplete treatments or cases requiring extraction.  

---

### Key Takeaways:
- **Multi-Step Process:** D3355 (initial), D3356 (interim), and D3357 (completion) reflect distinct stages—use them sequentially.  
- **Immature Teeth Only:** Pulpal regeneration targets permanent teeth with open apices, not mature roots.  
- **Regeneration vs. Therapy:** These codes differ from standard root canal codes (D3310-D3330) by aiming to regenerate tissue.  
- **Restoration Separate:** Final restorations are not included—code them independently.  
- **Documentation Critical:** Insurance often requires detailed records (e.g., X-rays, medication used) due to the procedure's complexity.



### **Scenario:**
"{{scenario}}"

{PROMPT}
"""
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["scenario"])
    return create_chain(prompt)

def extract_pulpal_regeneration_code(scenario):
    """
    Extract Pulpal Regeneration code(s) for a given scenario.
    """
    try:
        extractor = create_pulpal_regeneration_extractor()
        result = invoke_chain(extractor, {"scenario": scenario})
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Error in pulpal regeneration code extraction: {str(e)}")
        return None

def activate_pulpal_regeneration(scenario):
    """
    Activate Pulpal Regeneration analysis and return results.
    """
    try:
        result = extract_pulpal_regeneration_code(scenario)
        return result
    except Exception as e:
        print(f"Error activating pulpal regeneration analysis: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = "A 12-year-old patient comes in with a necrotic pulp in an immature permanent tooth. The dentist performs the first step of pulpal regeneration, including opening the tooth, preparing the canal, and placing medication."
    result = activate_pulpal_regeneration(scenario)
    print(result) 