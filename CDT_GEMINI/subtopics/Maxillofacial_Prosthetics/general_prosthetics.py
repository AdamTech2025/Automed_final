"""
Module for extracting general maxillofacial prosthetics codes.
"""

import os
import sys
from langchain.prompts import PromptTemplate
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file
from subtopics.prompt.prompt import PROMPT


def create_general_prosthetics_extractor():
    """
    Creates a LangChain-based extractor for general maxillofacial prosthetics codes.
    """
    template = f"""
You are a dental coding expert 

GBefore picking a code, ask:
What was the primary reason the patient came in?
Is the prosthesis initial, a replacement, or a modification?
Is the prosthesis intraoral or extraoral?
What anatomical structure is being restored (e.g., ear, nose, palate, eye)?
Are there changes to the tissue bed that may affect prosthesis retention or fit?

Code: D5992
When to use: When a maxillofacial prosthetic appliance requires adjustment that is not routine maintenance.
What to check: Confirm that the adjustment is not just cleaning or maintenance, but involves adaptation due to tissue or functional change.
Notes: Requires narrative and report documentation.
Code: D5993
When to use: For professional cleaning and maintenance of a maxillofacial prosthesis without actual adjustments.
What to check: Ensure it's a cleaning/maintenance service and not an adjustment.
Notes: Applies to both intraoral and extraoral prostheses. Use only when there's no alteration to prosthesis design or fit.
Code: D5914
When to use: When fabricating an initial auricular (ear) prosthesis.
What to check: Confirm this is the first prosthesis and a mold is being created.
Notes: Subsequent prostheses can be made from this mold unless tissue bed changes.
Code: D5927
When to use: For replacement of an auricular prosthesis using an existing mold.
What to check: Verify no changes in tissue bed, and mold is still usable.
Notes: If a new mold is required, use D5914 instead.
Code: D5987
When to use: When providing a commissure (lip) splint to assist in lip movement or separation.
What to check: Confirm indication includes contractures or restrictions due to surgery or trauma.
Notes: Often needed post-oncologic or reconstructive surgeries.
Code: D5924
When to use: For fabrication of a cranial (skull) prosthesis implant.
What to check: Permanent placement and biocompatibility requirements.
Notes: Not removable. Typically post-cranioplasty.
Code: D5925
When to use: When augmenting facial structures surgically using implants.
What to check: Surgical planning documentation and need for custom prosthesis.
Notes: Often custom-made; rarely prefabricated due to anatomical variation.
Code: D5912
When to use: For full-face impressions to create a complete facial moulage.
What to check: Need for total facial structure recording.
Notes: Impression not reusable.
Code: D5911
When to use: For partial or sectional facial impressions.
What to check: Determine which facial regions are included and whether multiple sections will be combined.
Notes: Allows custom segment capture.
Code: D5919
When to use: When fabricating a new removable facial prosthesis.
What to check: Confirm tissue loss due to trauma, surgery, or congenital factors.
Notes: May need future modification depending on leakage or movement.
Code: D5929
When to use: For replacing an existing facial prosthesis using an original mold.
What to check: Ensure no further tissue change has occurred.
Notes: Faster and more cost-effective if mold is intact.
Code: D5951
When to use: In infants with cleft palate to aid feeding.
What to check: Confirm use is temporary pending surgical repair.
Notes: Important for sucking/swallowing function.
Code: D5934
When to use: When guiding a resected mandible with a flange-based prosthesis.
What to check: Confirm post-resection anatomy and ability to support prosthesis.
Notes: Improves occlusal contact and mastication.
Code: D5935
When to use: Same as above but without guide flange.
What to check: Determine limitations or patient tolerance for flanges.
Notes: Less directional control than D5934.
Code: D5913
When to use: For initial nasal prosthesis fabrication.
What to check: Confirm new mold required.
Notes: Needed when no previous prosthesis or mold exists.
Code: D5926
When to use: When replacing a nasal prosthesis using an existing mold.
What to check: No changes in anatomy.
Notes: Allows multiple reproductions from same mold.
Code: D5922
When to use: To close a hole in the nasal septum.
What to check: Septal wall defect and type of prosthetic material.
Notes: May need frequent replacement due to degradation.
Code: D5932
When to use: For a long-term definitive obturator replacing maxilla/tissue.
What to check: Ensure tissues are stable and not expected to change.
Notes: Final stage prosthesis.
Code: D5936
When to use: Following healing after maxillary resection, as a temporary prosthesis.
What to check: Healing completion, no planned surgical revisions.
Notes: Interim use before definitive prosthesis.
Code: D5933
When to use: When modifying an existing obturator (surgical, interim, or definitive).
What to check: Determine reason for adjustment — fit, seal, or tissue adaptation.
Notes: Avoids full remake.
Code: D5931
When to use: Immediately post-surgery for maxillary defects.
What to check: Confirm prosthesis is temporary and placed during/after surgery.
Notes: Multiple adjustments may be required.
Code: D5916
When to use: For permanent ocular (eye) prosthesis.
What to check: Confirm trauma/surgery resulted in eye loss.
Notes: Requires periodic cleaning and adaptation.
Code: D5923
When to use: Temporary ocular replacement post-trauma/surgery.
What to check: Indication is for healing phase, not aesthetics.
Notes: Clear acrylic, used before permanent eye is made.
Code: D5915
When to use: For full orbital prosthesis restoration (eye + surrounding structures).
What to check: Need for complete replacement including skin, muscle, eyelid.
Notes: Requires new mold unless unchanged.
Code: D5928
When to use: To replace an existing orbital prosthesis from the same mold.
What to check: Confirm fit and tissue bed stability.
Notes: Faster and more cost-effective.
Code: D5954
When to use: For augmenting hard/soft palate to support tongue function.
What to check: Confirm need for speech or swallowing improvement.
Notes: Removable; may also be called speech prosthesis.
Code: D5955
When to use: For permanent elevation of soft palate.
What to check: Ensure patient tolerated interim prosthesis well.
Notes: Long-term use.
Code: D5958
When to use: To evaluate use of palatal lift for speech/swallowing.
What to check: For diagnostic and short-term therapeutic use.
Notes: Assesses functional improvement.
Code: D5959
When to use: Adjusting an existing palatal lift prosthesis.
What to check: Confirm the issue is with fit, retention, or comfort.
Notes: Avoids remake.
Code: D5985
When to use: For targeting radiation in oral cancer treatment.
What to check: Used during split-course irradiation.
Notes: Ensures precise radiation delivery.
Code: D5984
When to use: To protect tissues during radiation therapy.
What to check: Positioning and shielding requirements.
Notes: Often includes lead.
Code: D5953
When to use: In adult cleft patients to support speech.
What to check: Check for cleft palate or velopharyngeal insufficiency.
Notes: Often used with crown-supported attachments.
Code: D5960
When to use: When revising a pediatric/adult speech prosthesis.
What to check: Determine if only a section of the prosthesis needs modification.
Notes: Increases device longevity.
Code: D5952
When to use: Temporary speech aid in pediatric cleft patients.
What to check: Check for erupted deciduous teeth for retention.
Notes: Helps speech until further growth.
Code: D5988
When to use: For stabilization and occlusal support post-jaw fracture or trauma.
What to check: Confirm it's being used for healing and stabilization.
Notes: May include arch bars or existing dentures.
Code: D5982
When to use: To apply pressure and aid soft tissue healing.
What to check: Indications for surgical stent.
Notes: Can be made with soft liner or compound.
Code: D5937
When to use: For managing trismus (restricted jaw opening).
What to check: Not to be used for TMJ-related conditions.
Notes: Focused on increasing oral aperture width.

Key Takeaways:
Replacement vs. Initial: Always determine whether the prosthesis is new or a replacement.
Mold Reusability: Many prostheses rely on the original mold. Check for tissue changes before reuse.
Indication Specificity: Codes are highly specific; use exact anatomical and functional justification.
Documentation Required: Many of these codes require narrative reports and case-specific justification.
Follow-Up Plans: Account for ongoing care, modifications, and patient tolerance in planning treatment and choosing the code.

Scenario:
"{{scenario}}"

{PROMPT}
"""
    
    prompt = PromptTemplate(template=template, input_variables=["scenario"])
    return create_chain(prompt)

def extract_general_prosthetics_code(scenario):
    """
    Extracts general maxillofacial prosthetics code(s) for a given scenario.
    """
    try:
        extractor = create_general_prosthetics_extractor()
        result = invoke_chain(extractor, {"scenario": scenario})
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Error in general prosthetics code extraction: {str(e)}")
        return None

def activate_general_prosthetics(scenario):
    """
    Analyze a dental scenario to determine general maxillofacial prosthetics code.
    
    Args:
        scenario (str): The dental scenario to analyze.
        
    Returns:
        str: The identified general maxillofacial prosthetics code or empty string if none found.
    """
    try:
        result = extract_general_prosthetics_code(scenario)
        
        # Return empty string if no code found
        if result == "None" or not result or "not applicable" in result.lower():
            return ""
            
        return result
    except Exception as e:
        print(f"Error in activate_general_prosthetics: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = "A 57-year-old male patient who had a partial maxillectomy due to oral cancer 3 months ago requires a definitive obturator prosthesis. The surgical site has completely healed, and the patient has been using an interim obturator which is no longer fitting properly."
    result = activate_general_prosthetics(scenario)
    print(result) 