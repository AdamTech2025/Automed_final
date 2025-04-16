"""
Module for extracting amalgam restorations codes.
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

class AmalgamRestorationsServices:
    """Class to analyze and extract amalgam restorations codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing amalgam restorations services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert

### Before picking a code, ask:
- What was the primary reason the patient came in? Was it for a routine restoration, or to address a specific issue like decay or a broken tooth?
- How many surfaces of the tooth are involved in the amalgam restoration?
- Is the tooth primary or permanent, and does this affect the treatment approach?
- Are there any complicating factors (e.g., extensive decay, patient sensitivity) that might require a different code or narrative?
- Does the procedure include polishing, and is it the final restoration?

---

### Restorative Dental Codes: Amalgam Restorations (Including Polishing)

#### Code: D2140 - Amalgam — One Surface, Primary or Permanent
- **When to use:**
  - Placement of an amalgam restoration on one surface of a primary or permanent tooth.
  - Typically for small caries or minor defects limited to a single surface (e.g., occlusal).
- **What to check:**
  - Confirm the restoration involves only one surface (e.g., occlusal, buccal, lingual).
  - Verify the tooth type (primary or permanent) and its condition (e.g., caries extent).
  - Ensure the procedure includes preparation, amalgam placement, and polishing.
  - Check for adjacent restorations that might affect surface count.
- **Notes:**
  - Per-tooth code—specify tooth number and surface in documentation.
  - Used for both primary (deciduous) and permanent teeth; no distinction in coding.
  - If decay extends beyond one surface, use a higher code (e.g., D2150).
  - Polishing is included—do not bill separately.

#### Code: D2150 - Amalgam — Two Surfaces, Primary or Permanent
- **When to use:**
  - Placement of an amalgam restoration on two surfaces of a primary or permanent tooth.
  - For moderate caries or damage involving two distinct surfaces (e.g., occlusal and mesial).
- **What to check:**
  - Confirm two surfaces are restored (e.g., occlusal and proximal, or buccal and lingual).
  - Verify tooth type and ensure caries or defect spans both surfaces.
  - Assess preparation and amalgam placement across both surfaces, including polishing.
  - Check radiographs or clinical notes to validate surface involvement.
- **Notes:**
  - Per-tooth code—document tooth number and specific surfaces (e.g., MO, DO).
  - Applies to primary or permanent teeth—specify in records.
  - If a third surface is involved, use D2160 instead.
  - Includes polishing as part of the restoration process.

#### Code: D2160 - Amalgam — Three Surfaces, Primary or Permanent
- **When to use:**
  - Placement of an amalgam restoration on three surfaces of a primary or permanent tooth.
  - For larger caries or damage affecting three surfaces (e.g., mesial, occlusal, distal).
- **What to check:**
  - Confirm three surfaces are restored (e.g., MOD, or occlusal, buccal, lingual).
  - Verify tooth type and extent of decay or damage across all three surfaces.
  - Ensure the procedure includes caries removal, amalgam placement, and polishing.
  - Review clinical findings to ensure no additional surfaces are involved.
- **Notes:**
  - Per-tooth code—list tooth number and surfaces (e.g., MOD) in documentation.
  - Common for posterior teeth with extensive proximal and occlusal decay.
  - If four or more surfaces are restored, use D2161.
  - Polishing is integral to the code—do not separate.

#### Code: D2161 - Amalgam — Four or More Surfaces, Primary or Permanent
- **When to use:**
  - Placement of an amalgam restoration on four or more surfaces of a primary or permanent tooth.
  - For extensive caries or damage involving most or all of the tooth's surfaces (e.g., MODB).
- **What to check:**
  - Confirm four or more surfaces are restored (e.g., mesial, occlusal, distal, buccal, lingual).
  - Verify tooth type and that decay or defect justifies such extensive restoration.
  - Ensure full procedure (preparation, amalgam placement, polishing) is completed.
  - Assess if the restoration approaches a buildup or crown threshold (different codes).
- **Notes:**
  - Per-tooth code—document tooth number and all surfaces involved.
  - Rare in primary teeth; more common in permanent molars with severe decay.
  - If restoration resembles a core buildup or crown prep, consider D2950 or crown codes with narrative.
  - Includes polishing—ensure final contour and occlusion are noted.

---

### Key Takeaways:
- *Surface Count is Key:* Codes escalate from D2140 to D2161 based on the number of surfaces restored—count accurately.
- *Primary or Permanent:* Both tooth types use the same codes, but document tooth number and type for clarity.
- *Polishing Included:* Polishing is part of each code—don't bill separately or assume it justifies a higher code.
- *Patient Education:* Explain amalgam durability and care, though this isn't billable under these codes.
- *Documentation Precision:* Specify tooth number, surfaces restored, and clinical justification (e.g., caries extent) to support claims and audits.

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_amalgam_restorations_code(self, scenario: str) -> str:
        """Extract amalgam restorations code(s) for a given scenario."""
        try:
            print(f"Analyzing amalgam restorations scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Amalgam restorations extract_amalgam_restorations_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in amalgam restorations code extraction: {str(e)}")
            return ""
    
    def activate_amalgam_restorations(self, scenario: str) -> str:
        """Activate the amalgam restorations analysis process and return results."""
        try:
            result = self.extract_amalgam_restorations_code(scenario)
            if not result:
                print("No amalgam restorations code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating amalgam restorations analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_amalgam_restorations(scenario)
        print(f"\n=== AMALGAM RESTORATIONS ANALYSIS RESULT ===")
        print(f"AMALGAM RESTORATIONS CODE: {result if result else 'None'}")

# Example usage
if __name__ == "__main__":
    amalgam_restorations_service = AmalgamRestorationsServices()
    scenario = input("Enter an amalgam restorations dental scenario: ")
    amalgam_restorations_service.run_analysis(scenario) 