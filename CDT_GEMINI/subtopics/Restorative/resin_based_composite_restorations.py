"""
Module for extracting resin-based composite restorations codes.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from subtopics.prompt.prompt import PROMPT
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file


# Load environment variables
load_dotenv()

# Get model name from environment variable, default to gpt-4o if not set
 
def create_resin_based_composite_restorations_extractor(temperature=0.0):
    """
    Create a LangChain-based resin-based composite restorations code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert

### Before picking a code, ask:
- What was the primary reason the patient came in? Was it to restore a carious lesion, erosion, or trauma, or for a cosmetic concern?
- Is the restoration on an anterior or posterior tooth, and how many surfaces are involved?
- Does the restoration involve the incisal angle (anterior) or full crown coverage?
- Is the lesion into the dentin (posterior), or is this a preventive procedure (which wouldn’t apply)?
- Are there any complicating factors (e.g., patient preference, occlusion issues) that might affect coding?

---

### Restorative Dental Codes: Resin-Based Composite Restorations — Direct

#### Code: D2330 - Resin-Based Composite — One Surface, Anterior
- **When to use:**
  - Direct placement of a resin-based composite restoration on one surface of an anterior tooth.
  - Typically for small caries, erosion, or minor defects (e.g., facial surface).
- **What to check:**
  - Confirm the restoration is on an anterior tooth (incisors/canines) and involves only one surface (e.g., facial, lingual).
  - Verify the procedure includes caries removal, preparation, and composite placement.
  - Ensure no incisal angle involvement or additional surfaces affected.
- **Notes:**
  - Per-tooth code—specify tooth number and surface (e.g., F for facial) in documentation.
  - Used for esthetic restorations; patient may request composite over amalgam.
  - If decay extends to another surface, use D2331 instead.

#### Code: D2331 - Resin-Based Composite — Two Surfaces, Anterior
- **When to use:**
  - Direct placement of a resin-based composite restoration on two surfaces of an anterior tooth.
  - For moderate caries or damage spanning two surfaces (e.g., mesial and facial).
- **What to check:**
  - Confirm two surfaces are restored on an anterior tooth (e.g., mesial and incisal, or facial and lingual).
  - Verify preparation and composite placement across both surfaces.
  - Check that the incisal angle isn’t involved (use D2335 if it is).
- **Notes:**
  - Per-tooth code—document tooth number and surfaces (e.g., MF).
  - Common for proximal caries with facial extension in anterior teeth.
  - Ensure accurate surface count to avoid under- or over-coding.

#### Code: D2332 - Resin-Based Composite — Three Surfaces, Anterior
- **When to use:**
  - Direct placement of a resin-based composite restoration on three surfaces of an anterior tooth.
  - For larger caries or defects affecting three surfaces (e.g., mesial, facial, distal).
- **What to check:**
  - Confirm three surfaces are restored on an anterior tooth (e.g., MFD).
  - Verify the extent of decay or damage and composite application across all surfaces.
  - Ensure the incisal angle isn’t involved (use D2335 if it is).
- **Notes:**
  - Per-tooth code—list tooth number and surfaces in documentation.
  - Often used for extensive anterior restorations without incisal angle loss.
  - Check occlusion post-restoration to ensure function and esthetics.

#### Code: D2335 - Resin-Based Composite — Four or More Surfaces or Involving Incisal Angle (Anterior)
- **When to use:**
  - Direct placement of a resin-based composite restoration on four or more surfaces, or involving the incisal angle, of an anterior tooth.
  - Incisal angle defined as the junction of the incisal edge with mesial or distal surfaces.
- **What to check:**
  - Confirm four or more surfaces (e.g., MFDL) or incisal angle involvement (e.g., fractured incisal edge).
  - Verify the tooth is anterior and the procedure restores significant structure or esthetics.
  - Assess if the restoration approaches a crown (use D2390 if full coverage).
- **Notes:**
  - Per-tooth code—document tooth number, surfaces, and incisal involvement.
  - Common for trauma or extensive caries affecting the incisal edge.
  - If full tooth coverage is achieved, consider D2390 instead.

#### Code: D2390 - Resin-Based Composite Crown, Anterior
- **When to use:**
  - Direct placement of a full resin-based composite crown on an anterior tooth.
  - Provides complete coverage for severe decay, trauma, or esthetic needs.
- **What to check:**
  - Confirm the restoration covers the entire anterior tooth (all surfaces).
  - Verify the procedure involves extensive preparation and composite buildup.
  - Assess if the tooth’s structure is too compromised for lesser codes (e.g., D2335).
- **Notes:**
  - Per-tooth code—specify tooth number and full coverage in documentation.
  - Not for partial restorations—use D2330-D2335 for fewer surfaces.
  - Often a temporary or esthetic solution; may precede a lab-fabricated crown.

#### Code: D2391 - Resin-Based Composite — One Surface, Posterior
- **When to use:**
  - Direct placement of a resin-based composite restoration on one surface of a posterior tooth.
  - Used to restore a carious lesion or deep erosion into the dentin (not preventive).
- **What to check:**
  - Confirm the restoration is on a posterior tooth (premolars/molars) and involves one surface (e.g., occlusal).
  - Verify the lesion extends into dentin, not just enamel (preventive uses D1355).
  - Ensure preparation, composite placement, and finishing are completed.
- **Notes:**
  - Per-tooth code—document tooth number and surface (e.g., O for occlusal).
  - Not for sealants or preventive measures—must address active pathology.
  - Patient may prefer composite over amalgam for esthetics.

#### Code: D2392 - Resin-Based Composite — Two Surfaces, Posterior
- **When to use:**
  - Direct placement of a resin-based composite restoration on two surfaces of a posterior tooth.
  - For caries or erosion into dentin affecting two surfaces (e.g., occlusal and mesial).
- **What to check:**
  - Confirm two surfaces are restored on a posterior tooth (e.g., MO, DO).
  - Verify dentin involvement and composite application across both surfaces.
  - Check radiographs or clinical notes to confirm surface count.
- **Notes:**
  - Per-tooth code—list tooth number and surfaces in documentation.
  - Common for proximal caries with occlusal extension in molars.
  - Ensure occlusion is adjusted post-restoration.

#### Code: D2393 - Resin-Based Composite — Three Surfaces, Posterior
- **When to use:**
  - Direct placement of a resin-based composite restoration on three surfaces of a posterior tooth.
  - For larger caries or erosion into dentin affecting three surfaces (e.g., MOD).
- **What to check:**
  - Confirm three surfaces are restored on a posterior tooth (e.g., mesial, occlusal, distal).
  - Verify dentin involvement and full restoration process.
  - Assess if additional surfaces are involved (use D2394 if four or more).
- **Notes:**
  - Per-tooth code—document tooth number and surfaces (e.g., MOD).
  - Frequent in posterior teeth with extensive decay.
  - Check for wear resistance and occlusal harmony.

#### Code: D2394 - Resin-Based Composite — Four or More Surfaces, Posterior
- **When to use:**
  - Direct placement of a resin-based composite restoration on four or more surfaces of a posterior tooth.
  - For extensive caries or erosion into dentin involving most or all surfaces (e.g., MODB).
- **What to check:**
  - Confirm four or more surfaces are restored on a posterior tooth (e.g., MODBL).
  - Verify dentin involvement and comprehensive composite placement.
  - Assess if the restoration approaches a crown or buildup (consider D2950 with narrative).
- **Notes:**
  - Per-tooth code—specify tooth number and all surfaces in documentation.
  - Rare but used for severely damaged posterior teeth.
  - Ensure durability and occlusion are addressed post-restoration.

---

### Key Takeaways:
- *Anterior vs. Posterior:* Codes split by tooth location (D2330-D2335, D2390 for anterior; D2391-D2394 for posterior)—identify correctly.
- *Surface Count Drives Coding:* Number of surfaces restored dictates the code—count precisely, including incisal angle for anterior teeth.
- *Dentin Involvement (Posterior):* Posterior codes (D2391-D2394) require caries or erosion into dentin—not for preventive use.
- *Patient Education:* Discuss composite benefits (esthetics) and care, though not billable under these codes.
- *Documentation Precision:* Record tooth number, surfaces, dentin involvement (posterior), and clinical justification to support claims and audits.



Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_resin_based_composite_restorations_code(scenario, temperature=0.0):
    """
    Extract resin-based composite restorations code(s) for a given scenario.
    """
    try:
        chain = create_resin_based_composite_restorations_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Resin-based composite restorations code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_resin_based_composite_restorations_code: {str(e)}")
        return ""

def activate_resin_based_composite_restorations(scenario):
    """
    Activate resin-based composite restorations analysis and return results.
    """
    try:
        return extract_resin_based_composite_restorations_code(scenario)
    except Exception as e:
        print(f"Error in activate_resin_based_composite_restorations: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient has a cavity on the mesial and distal surfaces of tooth #8 and needs a composite filling."
    result = activate_resin_based_composite_restorations(scenario)
    print(result) 