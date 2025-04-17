"""
Module for extracting dental encounters ICD-10 codes.
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
from icdtopics.prompt import PROMPT

class DentalEncountersServices:
    """Class to analyze and extract dental encounters ICD-10 codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing dental encounters."""
        return PromptTemplate(
            template=f"""
You are a highly experienced medical coding expert specializing in dental encounters and examinations. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

1.1 Routine Dental Examinations:
- Z01.20: Encounter for dental examination and cleaning without abnormal findings
- Z01.21: Encounter for dental examination and cleaning with abnormal findings

1.2 Special Screening Examinations:
- Z13.84: Encounter for screening for dental disorders

1.3 Orthodontic-Related Encounters:
- Z46.4: Encounter for fitting and adjustment of orthodontic device

1.4 Dental Prosthesis-Related Encounters:
- Z45.81: Encounter for adjustment or removal of breast implant
- Z45.82: Encounter for adjustment or removal of myringotomy device (stent) (tube)
- Z45.89: Encounter for adjustment and management of other implanted devices
- Z46.3: Encounter for fitting and adjustment of dental prosthetic device

1.5 Dental Procedure Follow-ups:
- Z09: Encounter for follow-up examination after completed treatment for conditions other than malignant neoplasm

1.6 Encounters for Other Specified Aftercare:
- Z51.89: Encounter for other specified aftercare

1.7 Counseling:
- Z71.89: Other specified counseling

1.8 Fear of Dental Treatment:
- Z64.4: Discord with counselors

1.9 Problems Related to Care:
- Z74.0: Reduced mobility
- Z74.1: Need for assistance with personal care
- Z74.3: Need for continuous supervision
- Z76.5: Malingerer [conscious simulation]
- Z91.89: Other specified personal risk factors, not elsewhere classified

1.10 Problems Related to Medical Facilities and Other Health Care:
- Z75.3: Unavailability and inaccessibility of health care facilities
- Z75.4: Unavailability and inaccessibility of other helping agencies

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_dental_encounters_code(self, scenario: str) -> str:
        """Extract dental encounters code(s) for a given scenario."""
        try:
            print(f"Analyzing dental encounters scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Dental encounters extract_dental_encounters_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in dental encounters code extraction: {str(e)}")
            return ""
    
    def activate_dental_encounters(self, scenario: str) -> str:
        """Activate the dental encounters analysis process and return results."""
        try:
            result = self.extract_dental_encounters_code(scenario)
            if not result:
                print("No dental encounters code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating dental encounters analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_dental_encounters(scenario)
        print(f"\n=== DENTAL ENCOUNTERS ANALYSIS RESULT ===")
        print(f"DENTAL ENCOUNTERS CODE: {result if result else 'None'}")


dental_encounters_service = DentalEncountersServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a dental encounters scenario: ")
    dental_encounters_service.run_analysis(scenario)
