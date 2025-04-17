"""
Module for extracting social determinants of health ICD-10 codes.
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

class SocialDeterminantsServices:
    """Class to analyze and extract social determinants of health ICD-10 codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing social determinants of health."""
        return PromptTemplate(
            template=f"""
You are a highly experienced medical coding expert specializing in social determinants of health. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

17.1 Social Determinants of Health:
- Z55.0: Illiteracy and low-level literacy
- Z55.3: Underachievement in school
- Z55.4: Educational maladjustment and discord with teachers and classmates
- Z55.8: Other problems related to education and literacy
- Z56.0: Unemployment, unspecified
- Z56.82: Military deployment status
- Z59.0: Homelessness
- Z59.1: Inadequate housing
- Z59.4: Lack of adequate food and safe drinking water
- Z59.8: Other problems related to housing and economic circumstances
- Z60.2: Problems related to living alone
- Z60.3: Acculturation difficulty
- Z62.810: Personal history of physical and sexual abuse in childhood
- Z62.811: Personal history of psychological abuse in childhood
- Z62.820: Parent-child conflict
- Z62.891: Sibling rivalry
- Z63.72: Alcoholism and drug addiction in family
- Z75.3: Unavailability and inaccessibility of health care facilities
- Z75.4: Unavailability and inaccessibility of other helping agencies

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_social_determinants_code(self, scenario: str) -> str:
        """Extract social determinants of health code(s) for a given scenario."""
        try:
            print(f"Analyzing social determinants scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Social determinants extract_social_determinants_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in social determinants code extraction: {str(e)}")
            return ""
    
    def activate_social_determinants(self, scenario: str) -> str:
        """Activate the social determinants analysis process and return results."""
        try:
            result = self.extract_social_determinants_code(scenario)
            if not result:
                print("No social determinants code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating social determinants analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_social_determinants(scenario)
        print(f"\n=== SOCIAL DETERMINANTS ANALYSIS RESULT ===")
        print(f"SOCIAL DETERMINANTS CODE: {result if result else 'None'}")


social_determinants_service = SocialDeterminantsServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a social determinants dental scenario: ")
    social_determinants_service.run_analysis(scenario)
