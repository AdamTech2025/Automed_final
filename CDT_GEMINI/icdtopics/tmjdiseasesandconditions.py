"""
Module for extracting TMJ diseases and conditions ICD-10 codes.
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

class TMJDisordersServices:
    """Class to analyze and extract TMJ diseases and conditions ICD-10 codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing TMJ diseases and conditions."""
        return PromptTemplate(
            template=f"""
You are a highly experienced medical coding expert specializing in TMJ diseases and conditions. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

11.1 TMJ Disorders:
- M26.601: Right temporomandibular joint disorder, unspecified
- M26.602: Left temporomandibular joint disorder, unspecified
- M26.603: Bilateral temporomandibular joint disorder, unspecified
- M26.609: Unspecified temporomandibular joint disorder, unspecified side
- M26.69: Other specified disorders of temporomandibular joint

11.2 Adhesions and Ankylosis:
- M26.611: Adhesions and ankylosis of right temporomandibular joint
- M26.612: Adhesions and ankylosis of left temporomandibular joint
- M26.613: Adhesions and ankylosis of bilateral temporomandibular joint

11.3 Arthralgia:
- M26.621: Arthralgia of right temporomandibular joint
- M26.622: Arthralgia of left temporomandibular joint
- M26.623: Arthralgia of bilateral temporomandibular joint

11.4 Articular Disc Disorders:
- M26.631: Articular disc disorder of right temporomandibular joint
- M26.632: Articular disc disorder of left temporomandibular joint
- M26.633: Articular disc disorder of bilateral temporomandibular joint

11.5 Arthritis of Temporomandibular Joint:
- M26.641: Arthritis of right temporomandibular joint
- M26.642: Arthritis of left temporomandibular joint
- M26.643: Arthritis of bilateral temporomandibular joint

11.6 Arthropathy of Temporomandibular Joint:
- M26.651: Arthropathy of right temporomandibular joint
- M26.652: Arthropathy of left temporomandibular joint
- M26.653: Arthropathy of bilateral temporomandibular joint

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_tmj_disorders_code(self, scenario: str) -> str:
        """Extract TMJ diseases and conditions code(s) for a given scenario."""
        try:
            print(f"Analyzing TMJ disorders scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"TMJ disorders extract_tmj_disorders_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in TMJ disorders code extraction: {str(e)}")
            return ""
    
    def activate_tmj_disorders(self, scenario: str) -> str:
        """Activate the TMJ disorders analysis process and return results."""
        try:
            result = self.extract_tmj_disorders_code(scenario)
            if not result:
                print("No TMJ disorders code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating TMJ disorders analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_tmj_disorders(scenario)
        print(f"\n=== TMJ DISORDERS ANALYSIS RESULT ===")
        print(f"TMJ DISORDERS CODE: {result if result else 'None'}")


tmj_disorders_service = TMJDisordersServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a TMJ disorders dental scenario: ")
    tmj_disorders_service.run_analysis(scenario)
