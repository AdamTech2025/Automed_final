import os
import sys
from langchain.prompts import PromptTemplate
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file
from subtopics.prompt.prompt import PROMPT



def create_endodontic_therapy_extractor():
    """
    Create a LangChain-based Endodontic Therapy code extractor.
    """
    prompt_template = f"""
You are a highly experienced dental coding expert

Before Picking a Code, Ask:
- What was the primary reason the patient came in? Was it for a routine visit, or did the patient present with pain, swelling, or a specific endodontic issue?
- Which tooth is being treated? Is it an anterior, premolar, or molar tooth?
- Is the procedure a complete root canal, an obstruction treatment, an incomplete therapy, or a repair of a perforation?
- Has the tooth's condition been assessed with radiographs or clinical exams (e.g., pulp vitality, fractures, obstructions)?
- Is the treatment surgical or non-surgical, and was any perforation caused by the same provider?

---

### Endodontic Therapy

#### Code: D3310
**Heading:** Endodontic therapy, anterior tooth (excluding final restoration)  
**When to Use:**  
- The patient has a permanent anterior tooth (incisor or canine) requiring root canal therapy due to pulp necrosis, irreversible pulpitis, or trauma.  
- The procedure includes complete cleaning, shaping, and obturation of the root canal system.  
- Use when the focus is on the endodontic treatment, not the final restoration.  
**What to Check:**  
- Confirm the tooth is an anterior permanent tooth via radiograph or clinical exam.  
- Assess pulp vitality and the presence of periapical pathology (e.g., abscess or radiolucency).  
- Verify the canal is negotiable and no significant obstructions exist (otherwise, see D3331).  
- Check patient history for previous endodontic treatment or trauma.  
**Notes:**  
- Excludes final restoration—use a separate code (e.g., D2950 or D2750) for core buildup or crown.  
- Not for premolars or molars (see D3320 or D3330).  
- Narrative may be needed for insurance if complexity (e.g., curved canals) is a factor.  

#### Code: D3320
**Heading:** Endodontic therapy, premolar tooth (excluding final restoration)  
**When to Use:**  
- The patient has a permanent premolar requiring root canal therapy due to pulp disease or injury.  
- Involves complete endodontic treatment (cleaning, shaping, filling) of one or more canals.  
- Use when the procedure targets the pulp, not the final restoration.  
**What to Check:**  
- Confirm the tooth is a premolar using clinical exam or radiograph.  
- Evaluate the number of canals (typically 1-2) and their accessibility.  
- Check for signs of infection, fracture, or resorption affecting treatment feasibility.  
- Review patient symptoms (e.g., pain, sensitivity) and diagnostic findings.  
**Notes:**  
- Excludes final restoration—code separately for restorative work.  
- Not for anterior teeth or molars (see D3310 or D3330).  
- May require documentation of canal complexity for insurance approval.  

#### Code: D3330
**Heading:** Endodontic therapy, molar tooth (excluding final restoration)  
**When to Use:**  
- The patient has a permanent molar requiring root canal therapy due to pulp pathology.  
- Involves complete treatment of multiple canals (typically 3-4) in the molar.  
- Use when the focus is on endodontic therapy, not the final restoration.  
**What to Check:**  
- Confirm the tooth is a molar via radiograph or exam.  
- Assess the number and condition of canals (e.g., calcification, curvature).  
- Check for periapical pathology or tooth restorability post-treatment.  
- Verify patient medical history for factors affecting treatment (e.g., antibiotics needed).  
**Notes:**  
- Excludes final restoration—use separate codes for crowns or fillings.  
- Not for anterior or premolar teeth (see D3310 or D3320).  
- Higher complexity may justify a narrative for insurance (e.g., extra canals).  

#### Code: D3331
**Heading:** Treatment of root canal obstruction; non-surgical access  
**Description:** In lieu of surgery, the formation of a pathway to achieve an apical seal without surgical intervention because of a non-negotiable root canal blocked by foreign bodies, including but not limited to separated instruments, broken posts, or calcification of 50% or more of the length of the tooth root.  
**When to Use:**  
- The patient has a root canal with a significant obstruction preventing standard endodontic therapy.  
- Non-surgical methods are used to bypass or remove the blockage (e.g., calcification, separated instrument).  
- Use when the goal is to achieve an apical seal without resorting to surgery.  
**What to Check:**  
- Identify the obstruction type (e.g., calcification, foreign body) via radiograph.  
- Confirm the canal is non-negotiable with standard techniques.  
- Assess whether the tooth remains restorable after treatment.  
- Check if surgery is a viable alternative (if so, this code may not apply).  
**Notes:**  
- Not a standalone root canal code—use with D3310, D3320, or D3330 if full therapy is completed.  
- Requires detailed documentation (e.g., X-rays, narrative) for insurance due to complexity.  
- Not for surgical interventions (e.g., apicoectomy).  

#### Code: D3332
**Heading:** Incomplete endodontic therapy; inoperable, unrestorable, or fractured tooth  
**Description:** Considerable time is necessary to determine diagnosis and/or provide initial treatment before the fracture makes the tooth unretainable.  
**When to Use:**  
- The patient undergoes partial root canal therapy, but the procedure is aborted due to inoperability, unrestorability, or a fracture discovered during treatment.  
- Use when significant time is spent before determining the tooth cannot be saved.  
**What to Check:**  
- Confirm the tooth's condition (e.g., fracture, extensive decay) via exam or radiograph.  
- Assess time spent on diagnosis and initial treatment before stopping.  
- Check if the tooth was deemed unrestorable or inoperable mid-procedure.  
- Verify patient symptoms and consent for alternative treatment (e.g., extraction).  
**Notes:**  
- Not for completed root canals (see D3310-D3330).  
- Requires a narrative explaining why therapy was incomplete (e.g., fracture line found).  
- Often followed by extraction or other codes if applicable.  

#### Code: D3333
**Heading:** Internal root repair of perforation defects  
**Description:** Non-surgical seal of perforation caused by resorption and/or decay but not iatrogenic by the same provider.  
**When to Use:**  
- The patient has a perforation in the root (due to resorption or decay) requiring non-surgical repair during endodontic treatment.  
- Use when sealing the defect internally with biocompatible material (e.g., MTA).  
**What to Check:**  
- Confirm the perforation's cause (resorption/decay, not provider error) via radiograph or exam.  
- Assess the perforation's location and size to ensure non-surgical repair is feasible.  
- Check if the same provider caused the perforation (if so, this code doesn't apply).  
- Verify the tooth's prognosis post-repair.  
**Notes:**  
- Not for iatrogenic perforations by the same provider—those are typically not billable.  
- Often used with D3310-D3330 if part of a broader root canal procedure.  
- Requires a narrative and possibly X-rays for insurance justification.  

---

### Key Takeaways:
- **Tooth Type Matters:** D3310 (anterior), D3320 (premolar), and D3330 (molar) depend on tooth location—accuracy is critical.  
- **Scope vs. Volume:** Codes reflect the procedure's focus (e.g., full therapy, obstruction, perforation), not just time spent.  
- **Restoration Exclusion:** All therapy codes exclude final restorations—code separately for crowns or fillings.  
- **Documentation:** Complex cases (e.g., D3331, D3332, D3333) need narratives and evidence for insurance approval.  
- **Non-Surgical Focus:** These codes emphasize non-surgical approaches; surgical options (e.g., apicoectomy) use different codes.

### **Scenario:**
"{{scenario}}"

{PROMPT}
"""
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["scenario"])
    return create_chain(prompt)

def extract_endodontic_therapy_code(scenario):
    """
    Extract Endodontic Therapy code(s) for a given scenario.
    """
    try:
        extractor = create_endodontic_therapy_extractor()
        result = invoke_chain(extractor, {"scenario": scenario})
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Error in endodontic therapy code extraction: {str(e)}")
        return None

def activate_endodontic_therapy(scenario):
    """
    Activate Endodontic Therapy analysis and return results.
    """
    try:
        result = extract_endodontic_therapy_code(scenario)
        return result
    except Exception as e:
        print(f"Error activating endodontic therapy analysis: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = "A patient presents with severe pain in tooth #8 (upper right central incisor). After examination and radiographs, the dentist diagnoses irreversible pulpitis and performs a complete root canal therapy on the tooth."
    result = activate_endodontic_therapy(scenario)
    print(result) 