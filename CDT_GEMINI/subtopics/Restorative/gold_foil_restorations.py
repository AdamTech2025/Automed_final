"""
Module for extracting gold foil restorations codes.
"""

import os
import sys
from langchain.prompts import PromptTemplate
from llm_services import LLMService, get_service, set_model, set_temperature

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

# Import modules
from subtopics.prompt.prompt import PROMPT

class GoldFoilRestorationsServices:
    """Class to analyze and extract gold foil restorations codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing gold foil restorations services."""
        return PromptTemplate(
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
  - Verify the use of gold foil (not amalgam or composite) and the tooth's condition (e.g., minimal caries).
  - Ensure the procedure includes preparation, gold foil condensation, and finishing.
  - Check that the lesion size and location suit gold foil's conservative approach.
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
- *Gold Foil Specificity:* These codes are exclusive to gold foil restorations—don't confuse with amalgam (D2140-D2161) or composite (D2330-D2394).
- *Conservative Use:* Gold foil is suited for small, precise restorations—larger defects may warrant alternative materials.
- *Patient Education:* Discuss gold foil's longevity and esthetic trade-offs, though not billable under these codes.
- *Documentation Precision:* Specify tooth number, surfaces restored, and clinical justification (e.g., caries size) to support claims and audits.

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_gold_foil_restorations_code(self, scenario: str) -> str:
        """Extract gold foil restorations code(s) for a given scenario."""
        try:
            print(f"Analyzing gold foil restorations scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Gold foil restorations extract_gold_foil_restorations_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in gold foil restorations code extraction: {str(e)}")
            return ""
    
    def activate_gold_foil_restorations(self, scenario: str) -> str:
        """Activate the gold foil restorations analysis process and return results."""
        try:
            result = self.extract_gold_foil_restorations_code(scenario)
            if not result:
                print("No gold foil restorations code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating gold foil restorations analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_gold_foil_restorations(scenario)
        print(f"\n=== GOLD FOIL RESTORATIONS ANALYSIS RESULT ===")
        print(f"GOLD FOIL RESTORATIONS CODE: {result if result else 'None'}")

# Example usage
if __name__ == "__main__":
    gold_foil_restorations_service = GoldFoilRestorationsServices()
    scenario = input("Enter a gold foil restorations dental scenario: ")
    gold_foil_restorations_service.run_analysis(scenario) 