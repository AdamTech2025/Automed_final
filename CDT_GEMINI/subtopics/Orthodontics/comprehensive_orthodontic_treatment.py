"""
Module for extracting comprehensive orthodontic treatment codes.
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

class ComprehensiveOrthodonticTreatment:
    """Class to analyze and extract comprehensive orthodontic treatment codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing comprehensive orthodontic treatment."""
        return PromptTemplate(
            template=f"""
    You are a highly experienced dental coding expert

Before picking a code, ask:
What stage of dentition is the patient in—transitional, adolescent, or adult?
Is this a full-course orthodontic treatment rather than a limited or interceptive treatment?
Does the patient require alignment of all or most teeth, including bite correction and occlusal adjustments?
Will the treatment involve multiple phases, including appliances, brackets, or other orthodontic interventions?
Are there specific skeletal or dental malocclusions being corrected over an extended period?
Will retention and post-treatment stabilization be necessary?

Detailed Coding Guidelines for Comprehensive Orthodontic Treatment
Code: D8070
Use when: Providing comprehensive orthodontic treatment for the transitional dentition.
Check: Ensure that the patient has a mix of primary and permanent teeth and requires full orthodontic correction.
Note: Typically used when significant alignment or bite issues are addressed before full permanent dentition erupts.
Code: D8080
Use when: Providing comprehensive orthodontic treatment for adolescent patients.
Check: Confirm that the patient has fully erupted permanent teeth and requires full orthodontic treatment.
Note: This is the most commonly used comprehensive orthodontic code for teenagers undergoing complete alignment correction.
Code: D8090
Use when: Providing comprehensive orthodontic treatment for adult dentition.
Check: Ensure that the patient requires full orthodontic correction, including bite realignment, over an extended treatment period.
Note: Often used for adult patients undergoing complex orthodontic treatment, including pre-prosthetic adjustments.

Key Takeaways:
Comprehensive orthodontic treatment addresses full dental alignment, bite correction, and occlusal adjustments.
Treatment is categorized based on dentition stage: transitional, adolescent, or adult.
Ensure documentation supports the necessity of full orthodontic intervention over an extended period.
Treatment often includes multiple phases, appliances, and retention strategies.

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
    )

    def extract_comprehensive_orthodontic_treatment_code(self, scenario: str) -> str:
        """Extract comprehensive orthodontic treatment code for a given scenario."""
        try:
            print(f"Analyzing comprehensive orthodontic treatment scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Comprehensive orthodontic treatment extract_comprehensive_orthodontic_treatment_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in comprehensive orthodontic treatment code extraction: {str(e)}")
            return ""

    def activate_comprehensive_orthodontic_treatment(self, scenario: str) -> str:
        """Activate the comprehensive orthodontic treatment analysis process and return results."""
        try:
            result = self.extract_comprehensive_orthodontic_treatment_code(scenario)
            if not result:
                print("No comprehensive orthodontic treatment code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating comprehensive orthodontic treatment analysis: {str(e)}")
            return "" 
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_comprehensive_orthodontic_treatment(scenario)
        print(f"\n=== COMPREHENSIVE ORTHODONTIC TREATMENT ANALYSIS RESULT ===")
        print(f"COMPREHENSIVE ORTHODONTIC TREATMENT CODE: {result if result else 'None'}")


comprehensive_orthodontic_treatment = ComprehensiveOrthodonticTreatment()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a comprehensive orthodontic treatment scenario: ")
    comprehensive_orthodontic_treatment.run_analysis(scenario) 