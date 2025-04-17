"""
Module for extracting disorders of pulp and periapical tissues ICD-10 codes.
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

class PulpPeriapicalServices:
    """Class to analyze and extract disorders of pulp and periapical tissues ICD-10 codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing disorders of pulp and periapical tissues."""
        return PromptTemplate(
            template=f"""
You are a highly experienced medical coding expert specializing in disorders of pulp and periapical tissues. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

7.1 Pulp and Periapical Conditions:
- K04.0: Pulpitis
- K04.01: Reversible pulpitis
- K04.02: Irreversible pulpitis
- K04.1: Necrosis of pulp
- K04.2: Pulp degeneration
- K04.3: Abnormal hard tissue formation in pulp
- K04.4: Acute apical periodontitis of pulpal origin
- K04.5: Chronic apical periodontitis
- K04.6: Periapical abscess with sinus
- K04.7: Periapical abscess without sinus
- K04.8: Radicular cyst
- K04.9: Other and unspecified diseases of pulp and periapical tissues

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_pulp_periapical_code(self, scenario: str) -> str:
        """Extract disorders of pulp and periapical tissues code(s) for a given scenario."""
        try:
            print(f"Analyzing pulp and periapical disorders scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Pulp and periapical disorders extract_pulp_periapical_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in pulp and periapical disorders code extraction: {str(e)}")
            return ""
    
    def activate_pulp_periapical_disorders(self, scenario: str) -> str:
        """Activate the pulp and periapical disorders analysis process and return results."""
        try:
            result = self.extract_pulp_periapical_code(scenario)
            if not result:
                print("No pulp and periapical disorders code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating pulp and periapical disorders analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_pulp_periapical_disorders(scenario)
        print(f"\n=== PULP AND PERIAPICAL DISORDERS ANALYSIS RESULT ===")
        print(f"PULP AND PERIAPICAL DISORDERS CODE: {result if result else 'None'}")


pulp_periapical_service = PulpPeriapicalServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a pulp and periapical disorders dental scenario: ")
    pulp_periapical_service.run_analysis(scenario)
