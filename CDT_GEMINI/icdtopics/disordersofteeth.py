"""
Module for extracting disorders of teeth ICD-10 codes.
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

class TeethDisordersServices:
    """Class to analyze and extract disorders of teeth ICD-10 codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing disorders of teeth."""
        return PromptTemplate(
            template=f"""
You are a highly experienced medical coding expert specializing in disorders of teeth. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

Disorders of Teeth ICD-10 codes include:
3.1 Occlusal Trauma
- K08.81: Primary occlusal trauma
- K08.82: Secondary occlusal trauma
- K08.89: Other specified disorders of teeth and supporting structures
  (Includes: Enlargement of alveolar ridge NOS, Insufficient anatomic crown height, 
   Insufficient clinical crown length, Irregular alveolar process, Toothache NOS)

3.2 Tooth Wear
- K03.0: Excessive attrition of teeth
- K03.1: Abrasion of teeth
- K03.2: Erosion of teeth
- K03.3: Pathological resorption of teeth

3.3 Other Disorders
- K03.4: Hypercementosis
- K03.5: Ankylosis of teeth
- K03.6: Deposits [accretions] on teeth
- K03.7: Posteruptive color changes of dental hard tissues
- K03.81: Cracked tooth
- K03.89: Other specified diseases of hard tissues of teeth
- K03.9: Disease of hard tissues of teeth, unspecified

9.2 Tooth Loss:
- K08.109: Complete loss of teeth, unspecified cause, unspecified class
- K08.419: Partial loss of teeth, unspecified cause, unspecified class
- K08.3: Retained dental root
- K08.401: Partial loss of teeth, unspecified cause, class I
- K08.402: Partial loss of teeth, unspecified cause, class II
- K08.403: Partial loss of teeth, unspecified cause, class III
- K08.404: Partial loss of teeth, unspecified cause, class IV

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_teeth_disorders_code(self, scenario: str) -> str:
        """Extract disorders of teeth code(s) for a given scenario."""
        try:
            print(f"Analyzing teeth disorders scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Teeth disorders extract_teeth_disorders_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in teeth disorders code extraction: {str(e)}")
            return ""
    
    def activate_disorders_of_teeth(self, scenario: str) -> str:
        """Activate the teeth disorders analysis process and return results."""
        try:
            result = self.extract_teeth_disorders_code(scenario)
            if not result:
                print("No teeth disorders code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating teeth disorders analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_disorders_of_teeth(scenario)
        print(f"\n=== TEETH DISORDERS ANALYSIS RESULT ===")
        print(f"TEETH DISORDERS CODE: {result if result else 'None'}")


teeth_disorders_service = TeethDisordersServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a disorders of teeth dental scenario: ")
    teeth_disorders_service.run_analysis(scenario)
