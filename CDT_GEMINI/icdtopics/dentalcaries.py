"""
Module for extracting dental caries ICD-10 codes.
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

class DentalCariesServices:
    """Class to analyze and extract dental caries ICD-10 codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing dental caries."""
        return PromptTemplate(
            template=f"""
You are a highly experienced medical coding expert specializing in dental caries. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

Dental Caries ICD-10 codes include:
2.1 Risk Factors
- Z91.841: Risk for dental caries, low
- Z91.842: Risk for dental caries, moderate
- Z91.843: Risk for dental caries, high

2.2 Caries
- K02.3: Arrested dental caries (decay and cavities) (includes coronal and root caries)
- K02.51: Dental caries on pit and fissure surface limited to enamel
- K02.52: Dental caries on pit and fissure surface penetrating into dentin
- K02.53: Dental caries on pit and fissure surface penetrating into pulp
- K02.61: Dental caries on smooth surface limited to enamel
- K02.62: Dental caries on smooth surface penetrating into dentin
- K02.63: Dental caries on smooth surface penetrating into pulp

2.2 Permanent Dentition:
- K02.7: Dental root caries
- K02.3: Arrested dental caries
- K02.9: Dental caries, unspecified

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_dental_caries_code(self, scenario: str) -> str:
        """Extract dental caries code(s) for a given scenario."""
        try:
            print(f"Analyzing dental caries scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Dental caries extract_dental_caries_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in dental caries code extraction: {str(e)}")
            return ""
    
    def activate_dental_caries(self, scenario: str) -> str:
        """Activate the dental caries analysis process and return results."""
        try:
            result = self.extract_dental_caries_code(scenario)
            if not result:
                print("No dental caries code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating dental caries analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_dental_caries(scenario)
        print(f"\n=== DENTAL CARIES ANALYSIS RESULT ===")
        print(f"DENTAL CARIES CODE: {result if result else 'None'}")


dental_caries_service = DentalCariesServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a dental caries scenario: ")
    dental_caries_service.run_analysis(scenario)
