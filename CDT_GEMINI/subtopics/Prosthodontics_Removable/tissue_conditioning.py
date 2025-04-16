"""
Module for extracting tissue conditioning codes.
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
from subtopics.prompt.prompt import PROMPT

class TissueConditioningServices:
    """Class to analyze and extract tissue conditioning codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing tissue conditioning services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert
Before Picking a Code, Ask:
Is the patient experiencing irritation, inflammation, or hyperplasia under an existing prosthesis?

Is this part of a preparatory phase before fabricating a new denture or reline?

Are you planning to make a final impression once the tissues are healthy?

Is this a soft liner applied chairside (not lab-processed)?

Is the tissue response being monitored over a 2–4 week period?

Code: D5850
Heading: Tissue conditioning, maxillary
When to Use:

Apply when the upper arch tissues are inflamed or distorted due to a poor-fitting prosthesis.

Used as a temporary treatment to promote tissue healing before taking a final impression for a new maxillary denture or reline.
What to Check:

Ensure it's a therapeutic soft liner, not a reline or rebase.

Confirm treatment is followed by future prosthetic work (e.g., D5110 or D5750).

Note progress in clinical records — usually adjusted or replaced within 2–4 weeks.
Notes:

Cannot be billed as a definitive procedure; it is preparatory.

Requires chairside application and intraoral evaluation of soft tissue healing.

Code: D5851
Heading: Tissue conditioning, mandibular
When to Use:

Use for lower arch tissue that needs healing before denture procedures.

Common with inflamed, flabby, or traumatized tissue from long-term denture wear.
What to Check:

Confirm the intent is pre-impression therapy before final prosthesis.

Ensure documentation of soft tissue response and reason for conditioning.

Used in conjunction with full or partial mandibular prosthetic plans.
Notes:

Typically replaced or evaluated within weeks.

Include a narrative if billing alongside other prosthodontic codes.

Key Takeaways:
Tissue Conditioning ≠ Reline: It's a temporary therapeutic step, not a fit adjustment.

Requires Follow-Up: Conditioning should be monitored and replaced within 2–4 weeks.

Document Clearly: Record reason for tissue conditioning, material used, and future prosthetic plan.

Chairside Procedure: Applied directly in the office — lab-processed liners are coded differently.


Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_tissue_conditioning_code(self, scenario: str) -> str:
        """Extract tissue conditioning code(s) for a given scenario."""
        try:
            print(f"Analyzing tissue conditioning scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Tissue conditioning extract_tissue_conditioning_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in tissue conditioning code extraction: {str(e)}")
            return ""
    
    def activate_tissue_conditioning(self, scenario: str) -> str:
        """Activate the tissue conditioning analysis process and return results."""
        try:
            result = self.extract_tissue_conditioning_code(scenario)
            if not result:
                print("No tissue conditioning code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating tissue conditioning analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_tissue_conditioning(scenario)
        print(f"\n=== TISSUE CONDITIONING ANALYSIS RESULT ===")
        print(f"TISSUE CONDITIONING CODE: {result if result else 'None'}")

# Example usage
if __name__ == "__main__":
    tissue_conditioning_service = TissueConditioningServices()
    scenario = input("Enter a tissue conditioning dental scenario: ")
    tissue_conditioning_service.run_analysis(scenario) 