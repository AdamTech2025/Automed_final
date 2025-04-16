"""
Module for extracting topical fluoride codes.
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

class TopicalFluorideServices:
    """Class to analyze and extract topical fluoride codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing topical fluoride services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert

### Before picking a code, ask:
- What was the primary reason the patient came in? Was it for a routine preventive visit, or to address a specific caries risk or sensitivity concern?
- What type of fluoride treatment is being applied? Is it varnish or another form (e.g., gel, foam)?
- What is the patient's age and caries risk level? Does their dental history justify fluoride application?
- Is this a standalone procedure, or is it part of a broader preventive or treatment plan?
- Are there any contraindications, such as allergies or recent fluoride exposure, that might affect the choice?

---

### Preventive Dental Codes: Topical Fluoride Treatment (Office Procedure)

#### Code: D1206 - Topical Application of Fluoride Varnish
- **When to use:**
  - For patients of any age receiving fluoride varnish as a preventive measure.
  - Typically applied during routine prophylaxis or recall visits to reduce caries risk.
  - Ideal for patients with moderate to high caries risk or enamel sensitivity.
- **What to check:**
  - Confirm the patient's caries risk assessment (e.g., history of decay, diet, oral hygiene habits).
  - Verify that varnish (not gel or foam) is the delivery method—usually a painted-on, sticky coating.
  - Review dental history for recent fluoride treatments to avoid over-application.
  - Ensure no allergies to varnish components (e.g., colophony resin) are present.
- **Notes:**
  - This code is specific to varnish; do not use for other fluoride forms like gel or foam (see D1208).
  - Often paired with prophylaxis (D1110/D1120) but billed separately.
  - Patient instructions post-application (e.g., no eating/drinking for 30 minutes) should be documented but aren't part of the code.
  - Can be used for both children and adults; age isn't a limiting factor, but caries risk is key.

#### Code: D1208 - Topical Application of Fluoride — Excluding Varnish
- **When to use:**
  - For patients of any age receiving fluoride treatment via gel, foam, or rinse (not varnish).
  - Applied during routine preventive visits to strengthen enamel and prevent decay.
  - Suitable for low to moderate caries risk patients or as part of a pediatric fluoride protocol.
- **What to check:**
  - Confirm the delivery method is gel, foam, or rinse—not varnish (varnish uses D1206).
  - Assess the patient's caries risk and whether this method suits their needs (e.g., gel in trays for kids).
  - Check for recent fluoride exposure (e.g., at-home treatments) to avoid excess fluoride intake.
  - Evaluate oral health status to ensure no active untreated decay requires priority treatment.
- **Notes:**
  - Excludes varnish; use this code for tray-applied gels, foams, or swish-and-spit rinses in-office.
  - Commonly used in pediatric dentistry with custom trays, but applicable to adults too.
  - Does not include at-home fluoride products (e.g., prescription toothpaste)—those aren't billable.
  - Documentation should specify the fluoride type (e.g., 1.23% APF gel) and application method.

---

### Key Takeaways:
- *Varnish vs. Non-Varnish:* D1206 is exclusively for varnish; D1208 covers all other in-office topical fluoride forms (gel, foam, rinse).
- *Caries Risk Drives Use:* Both codes aim to prevent decay, but the patient's risk level and treatment preference guide the choice.
- *Method Matters:* Verify the application method before coding—varnish is distinct from other forms in both technique and billing.
- *Patient Education:* Inform patients about post-treatment care (e.g., avoiding food/drink) to maximize fluoride benefits.
- *Documentation Precision:* Note the fluoride type, patient risk factors, and application details to support the code if questioned.

Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_topical_fluoride_code(self, scenario: str) -> str:
        """Extract topical fluoride code(s) for a given scenario."""
        try:
            print(f"Analyzing topical fluoride scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Topical fluoride extract_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in topical fluoride code extraction: {str(e)}")
            return ""
    
    def activate_topical_fluoride(self, scenario: str) -> str:
        """Activate the topical fluoride analysis process and return results."""
        try:
            result = self.extract_topical_fluoride_code(scenario)
            if not result:
                print("No topical fluoride code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating topical fluoride analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_topical_fluoride(scenario)
        print(f"\n=== TOPICAL FLUORIDE ANALYSIS RESULT ===")
        print(f"TOPICAL FLUORIDE CODE: {result if result else 'None'}")

topical_fluoride_service = TopicalFluorideServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a topical fluoride dental scenario: ")
    topical_fluoride_service.run_analysis(scenario)