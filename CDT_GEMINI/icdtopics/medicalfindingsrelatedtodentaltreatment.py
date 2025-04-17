"""
Module for extracting medical findings related to dental treatment ICD-10 codes.
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

class MedicalFindingsServices:
    """Class to analyze and extract medical findings related to dental treatment ICD-10 codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing medical findings related to dental treatment."""
        return PromptTemplate(
            template=f"""
You are a highly experienced medical coding expert specializing in medical findings related to dental treatment. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

12.1 Medical Findings:
- Z01.20: Encounter for dental examination and cleaning without abnormal findings
- Z01.21: Encounter for dental examination and cleaning with abnormal findings
- Z13.84: Encounter for screening for dental disorders
- Z29.3: Encounter for prophylactic fluoride administration
- Z41.8: Encounter for other procedures for purposes other than remedying health state
- Z46.3: Encounter for fitting and adjustment of dental prosthetic device
- Z46.4: Encounter for fitting and adjustment of orthodontic device

12.2 Dental Treatment Complications:
- T88.52XA: Failed moderate sedation during procedure, initial encounter
- T88.52XD: Failed moderate sedation during procedure, subsequent encounter
- T88.52XS: Failed moderate sedation during procedure, sequela
- Y65.53: Performance of wrong procedure (operation) on correct patient
- Y69: Unspecified misadventure during surgical and medical care
- Y84.8: Other medical procedures as the cause of abnormal reaction

12.3 Dental Treatment History:
- Z87.828: Personal history of other (healed) physical injury and trauma
- Z91.89: Other specified personal risk factors, not elsewhere classified
- Z92.89: Personal history of other medical treatment
- Z98.818: Personal history of other surgery
- Z98.89: Other specified postprocedural states

12.4 Dental Treatment Observations:
- R68.89: Other general symptoms and signs
- R69: Illness, unspecified
- Z71.89: Other specified counseling
- Z72.89: Other problems related to lifestyle
- Z91.849: Other risk factors, not elsewhere classified

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_medical_findings_code(self, scenario: str) -> str:
        """Extract medical findings related to dental treatment code(s) for a given scenario."""
        try:
            print(f"Analyzing medical findings scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Medical findings extract_medical_findings_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in medical findings code extraction: {str(e)}")
            return ""
    
    def activate_medical_findings(self, scenario: str) -> str:
        """Activate the medical findings analysis process and return results."""
        try:
            result = self.extract_medical_findings_code(scenario)
            if not result:
                print("No medical findings code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating medical findings analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_medical_findings(scenario)
        print(f"\n=== MEDICAL FINDINGS ANALYSIS RESULT ===")
        print(f"MEDICAL FINDINGS CODE: {result if result else 'None'}")


medical_findings_service = MedicalFindingsServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a medical findings dental scenario: ")
    medical_findings_service.run_analysis(scenario)
