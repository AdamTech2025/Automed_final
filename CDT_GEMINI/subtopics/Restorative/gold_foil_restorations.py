"""
Module for extracting gold foil restorations codes.
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
 
def create_gold_foil_restorations_extractor(temperature=0.0):
    """
    Create a LangChain-based gold foil restorations code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert


### Before picking a code, ask:
- What was the primary reason the patient came in? Was it to restore a carious lesion or defect with gold foil, or for another concern?
- How many surfaces of the tooth are involved in the gold foil restoration?
- Is the restoration on an anterior or posterior tooth, and does the patient prefer gold foil for durability or esthetics?
- Are there any complicating factors (e.g., small lesion size, patient sensitivity) that might affect the choice of gold foil over other materials?
- Does the procedure include final finishing, and is it the definitive restoration?

---

### Restorative Dental Codes: Gold Foil Restorations

#### Code: D2410 - Gold Foil — One Surface
- **When to use:**
  - Direct placement of a gold foil restoration on one surface of a tooth.
  - Typically for small caries or defects limited to a single surface (e.g., occlusal or facial).
- **What to check:**
  - Confirm the restoration involves only one surface (e.g., occlusal, buccal, lingual).
  - Verify the use of gold foil (not amalgam or composite) and the tooth’s condition (e.g., minimal caries).
  - Ensure the procedure includes preparation, gold foil condensation, and finishing.
  - Check that the lesion size and location suit gold foil’s conservative approach.
- **Notes:**
  - Per-tooth code—specify tooth number and surface in documentation.
  - Rare today due to labor-intensive technique; often chosen for durability or patient preference.
  - If decay extends to another surface, use D2420 instead.
  - Finishing (e.g., burnishing) is included—do not bill separately.

#### Code: D2420 - Gold Foil — Two Surfaces
- **When to use:**
  - Direct placement of a gold foil restoration on two surfaces of a tooth.
  - For moderate caries or damage involving two distinct surfaces (e.g., occlusal and mesial).
- **What to check:**
  - Confirm two surfaces are restored (e.g., occlusal and proximal, or buccal and lingual).
  - Verify gold foil is the material used and spans both surfaces after preparation.
  - Assess clinical notes or radiographs to validate surface involvement.
  - Ensure the procedure includes condensation and finishing across both surfaces.
- **Notes:**
  - Per-tooth code—document tooth number and surfaces (e.g., MO, DO).
  - Less common than amalgam or composite; requires skilled technique.
  - If a third surface is involved, use D2430 instead.
  - Includes final finishing as part of the restoration process.

#### Code: D2430 - Gold Foil — Three Surfaces
- **When to use:**
  - Direct placement of a gold foil restoration on three surfaces of a tooth.
  - For larger caries or defects affecting three surfaces (e.g., mesial, occlusal, distal).
- **What to check:**
  - Confirm three surfaces are restored (e.g., MOD, or occlusal, buccal, lingual).
  - Verify gold foil application and the extent of decay or damage across all surfaces.
  - Ensure the full procedure (preparation, condensation, finishing) is completed.
  - Check that no additional surfaces are involved beyond three.
- **Notes:**
  - Per-tooth code—list tooth number and surfaces (e.g., MOD) in documentation.
  - Highly technique-sensitive; used rarely due to modern alternatives.
  - If restoration exceeds three surfaces, consider other materials or codes with narrative.
  - Finishing is integral—ensure proper contour and occlusion are documented.

---

### Key Takeaways:
- *Surface Count Drives Coding:* Codes escalate from D2410 to D2430 based on the number of surfaces restored—count accurately.
- *Gold Foil Specificity:* These codes are exclusive to gold foil restorations—don’t confuse with amalgam (D2140-D2161) or composite (D2330-D2394).
- *Conservative Use:* Gold foil is suited for small, precise restorations—larger defects may warrant alternative materials.
- *Patient Education:* Discuss gold foil’s longevity and esthetic trade-offs, though not billable under these codes.
- *Documentation Precision:* Specify tooth number, surfaces restored, and clinical justification (e.g., caries size) to support claims and audits.


Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_gold_foil_restorations_code(scenario, temperature=0.0):
    """
    Extract gold foil restorations code(s) for a given scenario.
    """
    try:
        chain = create_gold_foil_restorations_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Gold foil restorations code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_gold_foil_restorations_code: {str(e)}")
        return ""

def activate_gold_foil_restorations(scenario):
    """
    Activate gold foil restorations analysis and return results.
    """
    try:
        return extract_gold_foil_restorations_code(scenario)
    except Exception as e:
        print(f"Error in activate_gold_foil_restorations: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient requests a gold foil restoration on the occlusal surface of tooth #14."
    result = activate_gold_foil_restorations(scenario)
    print(result) 