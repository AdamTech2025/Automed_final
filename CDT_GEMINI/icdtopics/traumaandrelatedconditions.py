"""
Module for extracting trauma and related conditions ICD-10 codes.
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

class TraumaConditionsServices:
    """Class to analyze and extract trauma and related conditions ICD-10 codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing trauma and related conditions."""
        return PromptTemplate(
            template=f"""
You are a highly experienced medical coding expert specializing in trauma and related conditions. 
Analyze the given scenario and determine the most applicable ICD-10 code(s).

16.1 Dislocation and Fracture of Jaw:
- S02.60XA: Fracture of mandible, unspecified, initial encounter
- S02.609A: Fracture of mandible, unspecified part, unspecified side, initial encounter
- S02.61XA: Fracture of condylar process of mandible, initial encounter
- S02.62XA: Fracture of subcondylar process of mandible, initial encounter
- S02.63XA: Fracture of coronoid process of mandible, initial encounter
- S02.64XA: Fracture of ramus of mandible, initial encounter
- S02.65XA: Fracture of angle of mandible, initial encounter
- S02.66XA: Fracture of symphysis of mandible, initial encounter
- S02.67XA: Fracture of alveolus of mandible, initial encounter
- S02.69XA: Fracture of mandible of other specified site, initial encounter
- S03.0XXA: Dislocation of jaw, initial encounter

16.2 Dental Trauma:
- S02.5XXA: Fracture of tooth (traumatic), initial encounter
- S03.2XXA: Dislocation of tooth, initial encounter

16.3 Trauma to Mouth, Oral Cavity, and Related Structures:
- S00.501A: Unspecified superficial injury of lip, initial encounter
- S00.511A: Abrasion of lip, initial encounter
- S00.521A: Blister (nonthermal) of lip, initial encounter
- S00.531A: Contusion of lip, initial encounter
- S00.541A: External constriction of part of lip, initial encounter
- S00.551A: Superficial foreign body of lip, initial encounter
- S00.561A: Insect bite (nonvenomous) of lip, initial encounter
- S00.571A: Other superficial bite of lip, initial encounter
- S00.511A: Abrasion of oral cavity, initial encounter
- S00.512A: Abrasion of oral cavity, initial encounter
- S01.501A: Unspecified open wound of lip, initial encounter
- S01.502A: Unspecified open wound of oral cavity, initial encounter
- S01.511A: Laceration without foreign body of lip, initial encounter
- S01.512A: Laceration without foreign body of oral cavity, initial encounter
- S01.521A: Laceration with foreign body of lip, initial encounter
- S01.522A: Laceration with foreign body of oral cavity, initial encounter
- S01.531A: Puncture wound without foreign body of lip, initial encounter
- S01.532A: Puncture wound without foreign body of oral cavity, initial encounter
- S01.541A: Puncture wound with foreign body of lip, initial encounter
- S01.542A: Puncture wound with foreign body of oral cavity, initial encounter
- S01.551A: Open bite of lip, initial encounter
- S01.552A: Open bite of oral cavity, initial encounter
- S01.90XA: Unspecified open wound of unspecified part of head, initial encounter

16.4 Burns and Corrosions:
- T28.0XXA: Burn of mouth and pharynx, initial encounter
- T28.5XXA: Corrosion of mouth and pharynx, initial encounter

16.5 Foreign Body in Mouth:
- T18.0XXA: Foreign body in mouth, initial encounter
- T18.1XXA: Foreign body in esophagus, initial encounter

16.6 Tongue Injuries:
- S00.532A: Contusion of oral cavity, initial encounter
- S01.512A: Laceration without foreign body of oral cavity, initial encounter
- S01.522A: Laceration with foreign body of oral cavity, initial encounter
- S01.532A: Puncture wound without foreign body of oral cavity, initial encounter
- S01.542A: Puncture wound with foreign body of oral cavity, initial encounter
- S01.552A: Open bite of oral cavity, initial encounter

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_trauma_conditions_code(self, scenario: str) -> str:
        """Extract trauma and related conditions code(s) for a given scenario."""
        try:
            print(f"Analyzing trauma conditions scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Trauma conditions extract_trauma_conditions_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in trauma conditions code extraction: {str(e)}")
            return ""
    
    def activate_trauma_conditions(self, scenario: str) -> str:
        """Activate the trauma conditions analysis process and return results."""
        try:
            result = self.extract_trauma_conditions_code(scenario)
            if not result:
                print("No trauma conditions code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating trauma conditions analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_trauma_conditions(scenario)
        print(f"\n=== TRAUMA CONDITIONS ANALYSIS RESULT ===")
        print(f"TRAUMA CONDITIONS CODE: {result if result else 'None'}")


trauma_conditions_service = TraumaConditionsServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a trauma conditions dental scenario: ")
    trauma_conditions_service.run_analysis(scenario)
