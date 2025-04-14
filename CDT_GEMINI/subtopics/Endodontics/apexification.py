import os
import sys
from langchain.prompts import PromptTemplate
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file
from subtopics.prompt.prompt import PROMPT



def create_apexification_extractor():
    """
    Create a LangChain-based Apexification/Recalcification code extractor.
    """
    prompt_template = f"""
You are a highly experienced dental coding expert

Before Picking a Code, Ask:
- What was the primary reason the patient came in? Did they present with symptoms (e.g., pain, swelling) tied to a previously treated root canal, or was it discovered during a routine visit?
- Which tooth is being retreated? Is it an anterior, premolar, or molar tooth?
- Has the prior root canal failed due to issues like persistent infection, poor sealing, or new pathology?
- Are there diagnostic tools (e.g., radiographs, clinical exams) confirming the need for retreatment?
- Is the tooth still restorable, or does its condition suggest a different approach (e.g., extraction)?

---

### Apexification/Recalcification (Endodontic Retreatment with Provided Codes)
#### **Code:** D3351  
**Heading:** Apexification/Recalcification – Initial Visit  
**When to Use:**  
- The patient has an immature permanent tooth or an open apex that requires apical closure.  
- Used in cases involving root resorption, perforations, or other anomalies requiring calcific barrier formation.  
- Typically indicated when performing endodontic treatment on a non-vital tooth with an incompletely formed apex.  
- May also apply when repairing perforations or managing resorptive defects with medicament therapy.  

**What to Check:**  
- Confirm the presence of an open apex or apical pathology via radiographic evidence.  
- Assess the tooth's vitality and pulpal status (usually necrotic pulp in young permanent teeth).  
- Evaluate whether the root is restorable and the prognosis is favorable with apexification.  
- Document clinical signs (e.g., sinus tract, swelling) and diagnostic testing (cold test, percussion).  

**Notes:**  
- Includes opening the tooth, canal debridement, placement of the first medicament (e.g., calcium hydroxide, MTA), and necessary radiographs.  
- Often represents the **first stage of root canal therapy** for immature teeth.  
- Follow-up visits for additional medicament replacement may require **D3352**, and the final visit for closure is coded with **D3353**.  
- Document material used and rationale clearly for insurance—especially in trauma or developmental cases.  


### Key Takeaways:
- **Tooth Location Drives Coding:** D3346 (anterior), D3347 (premolar), and D3348 (molar) are specific to tooth type—precision is critical.  
- **Evidence of Failure:** Retreatment codes require proof of prior root canal issues (e.g., imaging, symptoms).  
- **Non-Surgical Only:** These codes apply to non-surgical retreatments; surgical options have separate codes.  
- **Restoration Separate:** Final restorations aren't included—code them independently.  
- **Insurance Prep:** Expect to provide narratives and X-rays to support retreatment claims.


Scenario:
"{{scenario}}"

{PROMPT}
"""
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["scenario"])
    return create_chain(prompt)

def extract_apexification_code(scenario):
    """
    Extract Apexification/Recalcification code for a given scenario.
    """
    try:
        extractor = create_apexification_extractor()
        result = invoke_chain(extractor, {"scenario": scenario})
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Error in apexification code extraction: {str(e)}")
        return None

def activate_apexification(scenario):
    """
    Activate Apexification/Recalcification analysis and return results.
    """
    try:
        result = extract_apexification_code(scenario)
        return result
    except Exception as e:
        print(f"Error activating apexification analysis: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = "A 9-year-old patient presents with a traumatic injury to tooth #8 (maxillary right central incisor). Radiographs show an immature root with an open apex. The dentist performs the initial visit for apexification by removing the necrotic pulp, debriding the canal, and placing calcium hydroxide to stimulate calcific barrier formation."
    result = activate_apexification(scenario)
    print(result) 