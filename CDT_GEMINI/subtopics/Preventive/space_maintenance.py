"""
Module for extracting space maintenance codes.
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

class SpaceMaintenanceServices:
    """Class to analyze and extract space maintenance codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        # Use a single, comprehensive prompt template
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the single prompt template for analyzing all space maintenance services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert

### Before picking a code, ask:
- What was the primary reason the patient came in? Was it to maintain space due to premature tooth loss, for distal shoe guidance, or for another issue?
- Is the space maintainer fixed or removable? Is it a distal shoe design?
- Is it unilateral (one side) or bilateral (both sides), and which arch is involved (maxillary or mandibular)?
- Is this a new placement, a repair (re-cement/re-bond), or a removal procedure?
- Does the patient's dental history or current condition (e.g., crowding, eruption patterns, unerupted molar) support the need for space maintenance or a distal shoe?

---

### Preventive Dental Codes: Space Maintenance (Passive Appliances & Distal Shoe)

#### Code: D1510 - Space Maintainer — Fixed, Unilateral — Per Quadrant
- **When to use:**
  - Fixed unilateral space maintainer placed in one quadrant to preserve space after premature tooth loss.
  - Excludes distal shoe space maintainers (D1575).
- **What to check:**
  - Confirm premature loss of a primary tooth in the quadrant and need to maintain space.
  - Verify the appliance is fixed (e.g., band and loop) and unilateral (one side only).
  - Ensure it's not a distal shoe design.
- **Notes:**
  - Per-quadrant code—specify quadrant.
  - Used primarily in mixed dentition.

#### Code: D1516 - Space Maintainer — Fixed — Bilateral, Maxillary
- **When to use:**
  - Fixed bilateral space maintainer placed on the maxillary arch.
- **What to check:**
  - Confirm bilateral tooth loss in the maxillary arch and need for space preservation.
  - Verify the appliance is fixed (e.g., transpalatal arch).
- **Notes:**
  - Specific to maxillary arch.

#### Code: D1517 - Space Maintainer — Fixed — Bilateral, Mandibular
- **When to use:**
  - Fixed bilateral space maintainer placed on the mandibular arch.
- **What to check:**
  - Confirm bilateral tooth loss in the mandibular arch and space maintenance need.
  - Verify the appliance is fixed (e.g., lingual holding arch).
- **Notes:**
  - Specific to mandibular arch.

#### Code: D1520 - Space Maintainer — Removable, Unilateral — Per Quadrant
- **When to use:**
  - Removable unilateral space maintainer placed in one quadrant.
- **What to check:**
  - Confirm premature tooth loss and suitability for a removable device.
  - Verify the appliance is unilateral and removable.
- **Notes:**
  - Per-quadrant code.

#### Code: D1526 - Space Maintainer — Removable — Bilateral, Maxillary
- **When to use:**
  - Removable bilateral space maintainer placed on the maxillary arch.
- **What to check:**
  - Confirm bilateral maxillary tooth loss.
  - Verify the appliance is removable and bilateral.
- **Notes:**
  - Specific to maxillary arch.

#### Code: D1527 - Space Maintainer — Removable — Bilateral, Mandibular
- **When to use:**
  - Removable bilateral space maintainer placed on the mandibular arch.
- **What to check:**
  - Confirm bilateral mandibular tooth loss.
  - Verify the appliance is removable and bilateral.
- **Notes:**
  - Specific to mandibular arch.

#### Code: D1551 - Re-cement or Re-bond Bilateral Space Maintainer — Maxillary
- **When to use:**
  - Re-cementing or re-bonding a previously placed fixed bilateral maxillary space maintainer (originally D1516).
- **What to check:**
  - Confirm the original appliance is bilateral and maxillary.
  - Assess reason for failure and appliance integrity.
- **Notes:**
  - Specific to maxillary bilateral fixed maintainers.

#### Code: D1552 - Re-cement or Re-bond Bilateral Space Maintainer — Mandibular
- **When to use:**
  - Re-cementing or re-bonding a previously placed fixed bilateral mandibular space maintainer (originally D1517).
- **What to check:**
  - Confirm the original appliance is bilateral and mandibular.
  - Evaluate cause of detachment.
- **Notes:**
  - Specific to mandibular bilateral fixed maintainers.

#### Code: D1553 - Re-cement or Re-bond Unilateral Space Maintainer — Per Quadrant
- **When to use:**
  - Re-cementing or re-bonding a previously placed fixed unilateral space maintainer (originally D1510).
- **What to check:**
  - Confirm the original appliance is unilateral and fixed.
  - Identify quadrant.
- **Notes:**
  - Per-quadrant code.

#### Code: D1556 - Removal of Fixed Unilateral Space Maintainer — Per Quadrant
- **When to use:**
  - Removal of a fixed unilateral space maintainer (originally D1510).
  - Typically when the permanent tooth erupts or space maintenance is no longer needed.
  - Removal is necessary due to impingement on erupting teeth, tissue irritation, or other clinical complications caused by the appliance.
- **What to check:**
  - Confirm the appliance is unilateral and fixed in the specified quadrant.
  - Verify eruption status or treatment plan change OR reason for complication requiring removal.
- **Notes:**
  - Per-quadrant code.

#### Code: D1557 - Removal of Fixed Bilateral Space Maintainer — Maxillary
- **When to use:**
  - Removal of a fixed bilateral maxillary space maintainer (originally D1516).
  - Used when space maintenance is complete or no longer required (e.g., permanent teeth erupted).
  - Removal is necessary due to impingement on erupting teeth, tissue irritation, or other clinical complications caused by the appliance.
- **What to check:**
  - Confirm the appliance is bilateral and maxillary.
  - Check for permanent tooth eruption or orthodontic plan updates OR reason for complication requiring removal.
- **Notes:**
  - Specific to maxillary bilateral fixed maintainers.

#### Code: D1558 - Removal of Fixed Bilateral Space Maintainer — Mandibular
- **When to use:**
  - Removal of a fixed bilateral mandibular space maintainer (originally D1517).
  - Applied when space preservation is no longer necessary (e.g., permanent teeth erupted).
  - Removal is necessary due to impingement on erupting teeth, tissue irritation, or other clinical complications caused by the appliance.
- **What to check:**
  - Confirm the appliance is bilateral and mandibular.
  - Assess eruption of permanent teeth or changes in treatment needs OR reason for complication requiring removal.
- **Notes:**
  - Specific to mandibular bilateral fixed maintainers.

#### Code: D1575 - Distal Shoe Space Maintainer — Fixed, Unilateral — Per Quadrant
- **When to use:**
  - Fabrication and delivery of a fixed, unilateral distal shoe space maintainer in one quadrant.
  - Designed to extend subgingivally and distally to guide the eruption of the first permanent molar after premature loss of a primary molar (typically the second primary molar).
- **What to check:**
  - Confirm premature loss of a primary molar and the first permanent molar is unerupted, requiring guidance.
  - Verify the appliance is fixed, unilateral, and uses a distal shoe design (e.g., a metal extension into the tissue).
  - Assess the quadrant involved and ensure proper space for the erupting molar.
  - Check radiographs to confirm the position of the unerupted molar and surrounding bone structure.
  - Ensure this is for initial placement only, not follow-up or replacement.
- **Notes:**
  - Per-quadrant code—specify quadrant.
  - Distinct from other space maintainers (e.g., D1510) due to its subgingival extension and specific purpose.
  - Does not include ongoing adjustments, follow-up visits, or replacement appliances after eruption.
  - Typically used in pediatric patients with mixed dentition; requires careful monitoring due to tissue interaction.

---

### Key Takeaways:
- *Appliance Type:* Match fixed/removable, unilateral/bilateral, maxillary/mandibular, and distal shoe features to the correct code.
- *Service Type:* Distinguish between initial placement, repair (re-cement/re-bond), and removal.
- *Distal Shoe:* D1575 is specific for guiding unerupted first permanent molars with a subgingival extension.
- *Specificity:* Use the most precise code available for the service rendered.
- *Documentation Precision:* Note quadrant, appliance design, arch, and purpose clearly.

Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    # Renamed to extract_code to match other subtopic files' structure
    def extract_code(self, scenario: str) -> str:
        """Extract space maintenance code(s) for a given scenario using the comprehensive prompt."""
        try:
            print(f"Analyzing space maintenance scenario: {scenario[:100]}...")
            # Use the single, combined prompt template
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Space maintenance extract_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in space maintenance code extraction: {str(e)}")
            return ""
    
    # Simplified activation method, matching the structure of other_preventive_services.py
    def activate_space_maintenance(self, scenario: str) -> str:
        """Activate the space maintenance analysis process and return results."""
        try:
            # Directly call the primary extraction method
            result = self.extract_code(scenario)
            if not result:
                print("No space maintenance code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating space maintenance analysis: {str(e)}")
            return ""
    
    # run_analysis method kept for potential standalone testing
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_space_maintenance(scenario)
        print(f"\n=== SPACE MAINTENANCE ANALYSIS RESULT ===")
        print(f"SPACE MAINTENANCE CODE: {result if result else 'None'}")

space_maintenance_service = SpaceMaintenanceServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a space maintenance dental scenario: ")
    space_maintenance_service.run_analysis(scenario) 