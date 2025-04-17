"""
Module for extracting alveolar ridge disorders ICD-10 codes.
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

class AlveolarRidgeDisordersServices:
    """Class to analyze and extract alveolar ridge disorders ICD-10 codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing alveolar ridge disorders."""
        return PromptTemplate(
            template=f"""
You are a highly experienced medical coding expert specializing in alveolar ridge disorders. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

6.1 Atrophy of Alveolar Ridge:
- K08.20: Unspecified atrophy of edentulous alveolar ridge
- K08.21: Minimal atrophy of the mandible
- K08.22: Moderate atrophy of the mandible
- K08.23: Severe atrophy of the mandible
- K08.24: Minimal atrophy of maxilla
- K08.25: Moderate atrophy of the maxilla
- K08.26: Severe atrophy of the maxilla

6.2 Alveolar Anomalies:
- M26.71: Alveolar maxillary hyperplasia
- M26.72: Alveolar mandibular hyperplasia
- M26.73: Alveolar maxillary hypoplasia
- M26.74: Alveolar mandibular hypoplasia
- M26.79: Other specified alveolar anomalies

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_alveolar_ridge_disorders_code(self, scenario: str) -> str:
        """Extract alveolar ridge disorders code(s) for a given scenario."""
        try:
            print(f"Analyzing alveolar ridge disorders scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Alveolar ridge disorders extract_alveolar_ridge_disorders_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in alveolar ridge disorders code extraction: {str(e)}")
            return ""
    
    def activate_alveolar_ridge_disorders(self, scenario: str) -> str:
        """Activate the alveolar ridge disorders analysis process and return results."""
        try:
            result = self.extract_alveolar_ridge_disorders_code(scenario)
            if not result:
                print("No alveolar ridge disorders code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating alveolar ridge disorders analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_alveolar_ridge_disorders(scenario)
        print(f"\n=== ALVEOLAR RIDGE DISORDERS ANALYSIS RESULT ===")
        print(f"ALVEOLAR RIDGE DISORDERS CODE: {result if result else 'None'}")


alveolar_ridge_disorders_service = AlveolarRidgeDisordersServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter an alveolar ridge disorders dental scenario: ")
    alveolar_ridge_disorders_service.run_analysis(scenario)
