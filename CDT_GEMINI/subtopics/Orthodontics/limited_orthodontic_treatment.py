"""
Module for extracting limited orthodontic treatment codes.
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

class LimitedOrthodonticTreatment:
    """Class to analyze and extract limited orthodontic treatment codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing limited orthodontic treatment."""
        return PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert

Before picking a code, ask:
What stage of dentition is the patient in—primary, transitional, adolescent, or adult?
Is the treatment focused on a specific issue or limited to a particular segment of the dentition?
What is the expected treatment duration—short-term or long-term?
Is the goal to address a specific problem rather than comprehensive alignment?
Will additional or comprehensive orthodontics be needed later?

Detailed Coding Guidelines for Limited Orthodontic Treatment
Code: D8010
Use when: Providing limited orthodontic treatment for the primary dentition.
Check: Ensure that the patient has primary teeth only and requires specific, focused orthodontic intervention rather than comprehensive treatment.
Note: Rarely used, but appropriate for specific issues like crossbites or space maintenance in very young children.
Code: D8020
Use when: Providing limited orthodontic treatment for the transitional dentition.
Check: Confirm that the patient has a mix of primary and permanent teeth and requires specific, targeted orthodontic care.
Note: Commonly used for early interceptive orthodontics to address specific issues before comprehensive treatment.
Code: D8030
Use when: Providing limited orthodontic treatment for adolescent dentition.
Check: Verify that the treatment addresses specific issues in adolescent patients and is not comprehensive in scope.
Note: Used for focused corrections in teenage patients, such as alignment of specific teeth or space management.
Code: D8040
Use when: Providing limited orthodontic treatment for adult dentition.
Check: Ensure that the treatment is focused on specific areas or problems in an adult patient's dentition.
Note: Often used for pre-prosthetic tooth movement or correction of specific alignment issues in adults.

Key Takeaways:
Limited orthodontic treatment addresses specific dental issues rather than comprehensive alignment.
The appropriate code depends on the patient's dentition stage (primary, transitional, adolescent, adult).
Documentation should specify the limited nature and goals of treatment to distinguish from comprehensive care.
Limited treatment may be a precursor to comprehensive orthodontics or a standalone intervention for specific issues.

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
    )

    def extract_limited_orthodontic_treatment_code(self, scenario: str) -> str:
        """Extract limited orthodontic treatment code for a given scenario."""
        try:
            print(f"Analyzing limited orthodontic treatment scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Limited orthodontic treatment extract_limited_orthodontic_treatment_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in limited orthodontic treatment code extraction: {str(e)}")
            return ""

    def activate_limited_orthodontic_treatment(self, scenario: str) -> str:
        """Activate the limited orthodontic treatment analysis process and return results."""
        try:
            result = self.extract_limited_orthodontic_treatment_code(scenario)
            if not result:
                print("No limited orthodontic treatment code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating limited orthodontic treatment analysis: {str(e)}")
            return "" 
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_limited_orthodontic_treatment(scenario)
        print(f"\n=== LIMITED ORTHODONTIC TREATMENT ANALYSIS RESULT ===")
        print(f"LIMITED ORTHODONTIC TREATMENT CODE: {result if result else 'None'}")


limited_orthodontic_treatment = LimitedOrthodonticTreatment()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a limited orthodontic treatment scenario: ")
    limited_orthodontic_treatment.run_analysis(scenario) 