"""
Module for extracting findings of bost teeth ICD-10 codes.
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

class LostTeethServices:
    """Class to analyze and extract findings of lost teeth ICD-10 codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing findings of lost teeth."""
        return PromptTemplate(
            template=f"""
You are a highly experienced medical coding expert specializing in findings of lost teeth. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

10.1 Findings of Lost Teeth:
- K08.121: Complete loss of teeth due to trauma, class I
- K08.122: Complete loss of teeth due to trauma, class II
- K08.123: Complete loss of teeth due to trauma, class III
- K08.124: Complete loss of teeth due to trauma, class IV
- K08.129: Complete loss of teeth due to trauma, unspecified class
- K08.131: Complete loss of teeth due to periodontal diseases, class I
- K08.132: Complete loss of teeth due to periodontal diseases, class II
- K08.133: Complete loss of teeth due to periodontal diseases, class III
- K08.134: Complete loss of teeth due to periodontal diseases, class IV
- K08.139: Complete loss of teeth due to periodontal diseases, unspecified class
- K08.191: Complete loss of teeth due to other specified cause, class I
- K08.192: Complete loss of teeth due to other specified cause, class II
- K08.193: Complete loss of teeth due to other specified cause, class III
- K08.194: Complete loss of teeth due to other specified cause, class IV
- K08.199: Complete loss of teeth due to other specified cause, unspecified class

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_lost_teeth_code(self, scenario: str) -> str:
        """Extract findings of lost teeth code(s) for a given scenario."""
        try:
            print(f"Analyzing lost teeth scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Lost teeth extract_lost_teeth_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in lost teeth code extraction: {str(e)}")
            return ""
    
    def activate_lost_teeth(self, scenario: str) -> str:
        """Activate the lost teeth analysis process and return results."""
        try:
            result = self.extract_lost_teeth_code(scenario)
            if not result:
                print("No lost teeth code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating lost teeth analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_lost_teeth(scenario)
        print(f"\n=== LOST TEETH ANALYSIS RESULT ===")
        print(f"LOST TEETH CODE: {result if result else 'None'}")


lost_teeth_service = LostTeethServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a findings of lost teeth dental scenario: ")
    lost_teeth_service.run_analysis(scenario) 