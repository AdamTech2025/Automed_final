"""
Module for extracting other orthodontic services codes.
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

class OtherOrthodonticServices:
    """Class to analyze and extract other orthodontic services codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing other orthodontic services."""
        return PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert

Before picking a code, ask:
Is this a pre-treatment evaluation or a periodic visit during treatment?
Is the service related to monitoring, retention, appliance repair, or re-bonding?
Does the patient require adjustments, repairs, or removal of orthodontic devices?
Is this a case where a standard code does not apply, requiring a report-based procedure?

Code: D8660
Use when: Monitoring a patient's growth and dental development before starting orthodontic treatment.
 Check: Ensure periodic evaluations are documented separately from diagnostic procedures.
 Note: This code applies to observation appointments to determine the right time for treatment.
Code: D8670
Use when: Conducting a periodic orthodontic treatment visit, typically for adjustments.
 Check: Confirm that the visit is part of an ongoing orthodontic treatment plan.
 Note: This is used for routine checkups and appliance adjustments during treatment.
Code: D8680
Use when: Completing orthodontic treatment and transitioning to retention.
 Check: Ensure documentation includes removal of appliances and placement of retainers.
 Note: This is a post-treatment phase to maintain alignment after braces are removed.
Code: D8681
Use when: Adjusting a removable orthodontic retainer after initial placement.
 Check: Verify that this is an adjustment visit, not a retainer replacement.
 Note: Routine minor modifications to retainers fall under this code.
Code: D8695
Use when: Removing fixed orthodontic appliances before treatment completion.
 Check: Ensure removal is due to reasons other than successful treatment completion.
 Note: Typically used for early removal due to patient preference or medical necessity.
Code: D8696
Use when: Repairing a maxillary orthodontic appliance, excluding brackets and standard braces.
 Check: Ensure the repair involves functional appliances, expanders, or specialized devices.
 Note: Standard bracket repairs are not included under this code.
Code: D8697
Use when: Repairing a mandibular orthodontic appliance, excluding standard braces.
 Check: Confirm the repair is necessary for non-standard orthodontic appliances.
 Note: Functional appliances and expanders fall under this category.
Code: D8698
Use when: Re-cementing or re-bonding a fixed maxillary retainer.
 Check: Ensure it is a reattachment, not a new retainer placement.
 Note: This applies to retainers that become loose but are still intact.
Code: D8699
Use when: Re-cementing or re-bonding a fixed mandibular retainer.
 Check: Confirm the original retainer is being reattached, not replaced.
 Note: This helps maintain retention without creating a new appliance.
Code: D8701
Use when: Repairing and reattaching a fixed retainer in the maxillary arch.
 Check: Ensure documentation includes the cause of damage and the method of repair.
 Note: Covers repairs beyond simple re-bonding, such as fractured retainers.
Code: D8702
Use when: Repairing and reattaching a fixed retainer in the mandibular arch.
 Check: Confirm the retainer is intact and requires only repair, not replacement.
 Note: Similar to D8701 but for the lower arch.
Code: D8703
Use when: Replacing a lost or broken maxillary retainer.
 Check: Ensure that the retainer is no longer usable and requires full replacement.
 Note: This code is for completely new retainers, not simple repairs.
Code: D8704
Use when: Replacing a lost or broken mandibular retainer.
 Check: Verify the need for a new retainer due to loss or irreparable damage.
 Note: Used similarly to D8703 but for the lower arch.
Code: D8999
Use when: A procedure is not adequately described by any existing orthodontic code.
 Check: Ensure proper documentation of the procedure details in a report.
 Note: This is a catch-all code for unlisted orthodontic services, requiring justification.

Key Takeaways:
Differentiate between pre-treatment evaluations, periodic visits, retention, and repairs.
Ensure documentation clearly supports the need for the service provided.
Use D8999 for unique orthodontic procedures that don't fit standard codes.
Be specific about whether the service is for maxillary or mandibular appliances.



SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
    )

    def extract_other_orthodontic_services_code(self, scenario: str) -> str:
        """Extract other orthodontic services code for a given scenario."""
        try:
            print(f"Analyzing other orthodontic services scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Other orthodontic services extract_other_orthodontic_services_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in other orthodontic services code extraction: {str(e)}")
            return ""

    def activate_other_orthodontic_services(self, scenario: str) -> str:
        """Activate the other orthodontic services analysis process and return results."""
        try:
            result = self.extract_other_orthodontic_services_code(scenario)
            if not result:
                print("No other orthodontic services code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating other orthodontic services analysis: {str(e)}")
            return "" 
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_other_orthodontic_services(scenario)
        print(f"\n=== OTHER ORTHODONTIC SERVICES ANALYSIS RESULT ===")
        print(f"OTHER ORTHODONTIC SERVICES CODE: {result if result else 'None'}")


other_orthodontic_services = OtherOrthodonticServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter an other orthodontic services scenario: ")
    other_orthodontic_services.run_analysis(scenario) 