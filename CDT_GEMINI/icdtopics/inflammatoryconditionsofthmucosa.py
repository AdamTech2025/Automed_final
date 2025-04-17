"""
Module for extracting inflammatory conditions of the oral mucosa ICD-10 codes.
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

class InflammatoryMucosaServices:
    """Class to analyze and extract inflammatory conditions of the oral mucosa ICD-10 codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing inflammatory conditions of the oral mucosa."""
        return PromptTemplate(
            template=f"""
You are a highly experienced medical coding expert specializing in inflammatory conditions of the oral mucosa. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

8.1 Inflammatory Conditions of the Oral Mucosa:
- K12.0: Recurrent oral aphthae
- K12.1: Other forms of stomatitis
- K12.2: Cellulitis and abscess of mouth
- K12.30: Oral mucositis (ulcerative), unspecified
- K12.31: Oral mucositis (ulcerative) due to antineoplastic therapy
- K12.32: Oral mucositis (ulcerative) due to other drugs
- K12.33: Oral mucositis (ulcerative) due to radiation
- K12.39: Other oral mucositis (ulcerative)

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_inflammatory_mucosa_code(self, scenario: str) -> str:
        """Extract inflammatory conditions of the oral mucosa code(s) for a given scenario."""
        try:
            print(f"Analyzing inflammatory mucosa scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Inflammatory mucosa extract_inflammatory_mucosa_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in inflammatory mucosa code extraction: {str(e)}")
            return ""
    
    def activate_inflammatory_mucosa(self, scenario: str) -> str:
        """Activate the inflammatory mucosa analysis process and return results."""
        try:
            result = self.extract_inflammatory_mucosa_code(scenario)
            if not result:
                print("No inflammatory mucosa code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating inflammatory mucosa analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_inflammatory_mucosa(scenario)
        print(f"\n=== INFLAMMATORY MUCOSA ANALYSIS RESULT ===")
        print(f"INFLAMMATORY MUCOSA CODE: {result if result else 'None'}")


inflammatory_mucosa_service = InflammatoryMucosaServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter an inflammatory mucosa dental scenario: ")
    inflammatory_mucosa_service.run_analysis(scenario)
