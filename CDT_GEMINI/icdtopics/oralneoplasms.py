"""
Module for extracting oral neoplasms ICD-10 codes.
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

class OralNeoplasmsServices:
    """Class to analyze and extract oral neoplasms ICD-10 codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing oral neoplasms."""
        return PromptTemplate(
            template=f"""
You are a highly experienced medical coding expert specializing in oral neoplasms. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

13.1 Malignant Neoplasms:
- C00.0: Malignant neoplasm of external upper lip
- C00.1: Malignant neoplasm of external lower lip
- C00.2: Malignant neoplasm of external lip, unspecified
- C00.3: Malignant neoplasm of upper lip, inner aspect
- C00.4: Malignant neoplasm of lower lip, inner aspect
- C00.5: Malignant neoplasm of lip, unspecified, inner aspect
- C00.6: Malignant neoplasm of commissure of lip, unspecified
- C00.8: Malignant neoplasm of overlapping sites of lip
- C00.9: Malignant neoplasm of lip, unspecified

13.2 Benign Neoplasms:
- D10.0: Benign neoplasm of lip
- D10.1: Benign neoplasm of tongue
- D10.2: Benign neoplasm of floor of mouth
- D10.30: Benign neoplasm of unspecified part of mouth
- D10.39: Benign neoplasm of other parts of mouth
- D10.4: Benign neoplasm of tonsil
- D10.5: Benign neoplasm of other parts of oropharynx
- D10.6: Benign neoplasm of nasopharynx
- D10.7: Benign neoplasm of hypopharynx
- D10.9: Benign neoplasm of pharynx, unspecified

13.3 Neoplasms of Uncertain Behavior:
- D37.01: Neoplasm of uncertain behavior of lip
- D37.02: Neoplasm of uncertain behavior of tongue
- D37.04: Neoplasm of uncertain behavior of minor salivary glands
- D37.05: Neoplasm of uncertain behavior of pharynx
- D37.09: Neoplasm of uncertain behavior of other specified sites of the oral cavity

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_oral_neoplasms_code(self, scenario: str) -> str:
        """Extract oral neoplasms code(s) for a given scenario."""
        try:
            print(f"Analyzing oral neoplasms scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Oral neoplasms extract_oral_neoplasms_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in oral neoplasms code extraction: {str(e)}")
            return ""
    
    def activate_oral_neoplasms(self, scenario: str) -> str:
        """Activate the oral neoplasms analysis process and return results."""
        try:
            result = self.extract_oral_neoplasms_code(scenario)
            if not result:
                print("No oral neoplasms code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating oral neoplasms analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_oral_neoplasms(scenario)
        print(f"\n=== ORAL NEOPLASMS ANALYSIS RESULT ===")
        print(f"ORAL NEOPLASMS CODE: {result if result else 'None'}")


oral_neoplasms_service = OralNeoplasmsServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter an oral neoplasms dental scenario: ")
    oral_neoplasms_service.run_analysis(scenario)
