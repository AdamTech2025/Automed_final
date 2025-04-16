"""
Module for extracting other fixed partial denture services codes.
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

class OtherFixedPartialDentureServicesServices:
    """Class to analyze and extract other fixed partial denture services codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing other fixed partial denture services services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert

Before picking a code, ask:
- What was the primary reason the patient came in? Was it for a repair, adjustment, or a specific prosthetic need?
- Is the procedure related to stabilizing, repairing, or enhancing a fixed partial denture?
- Does the patient have a removable overdenture or a fully fixed prosthesis?
- Is the service for an adult or pediatric patient?
- Are there specific material failures or unique circumstances requiring a narrative report?

### Code: D6920  
**Heading:** connector bar  
- **When to use:** When a connector bar is attached to a fixed partial denture retainer or coping to stabilize and anchor a removable overdenture prosthesis.  
- **What to check:** Confirm the presence of a removable overdenture and ensure the connector bar is securely attached to the fixed retainer or coping. Verify the stability of the overdenture post-placement.  
- **Notes:** Enhances retention for overdentures; typically used in cases with significant tooth loss. Ensure proper alignment to avoid undue stress on abutments.

### Code: D6930  
**Heading:** re-cement or re-bond fixed partial denture  
- **When to use:** When a fixed partial denture needs to be re-cemented or re-bonded due to loosening or detachment.  
- **What to check:** Assess why the prosthesis became loose (e.g., cement failure, occlusal issues). Check the integrity of the prosthesis and abutment teeth before re-cementing.  
- **Notes:** Not for new placements; only for existing prostheses. Clean and prepare surfaces thoroughly to ensure a strong bond. Document the reason for detachment.

### Code: D6940  
**Heading:** stress breaker  
- **When to use:** When a non-rigid connector (stress breaker) is incorporated into a fixed partial denture to reduce stress on abutment teeth.  
- **What to check:** Verify the need for stress distribution (e.g., mobile abutments or uneven occlusal forces). Ensure the stress breaker functions without compromising prosthesis stability.  
- **Notes:** Common in cases with periodontally compromised teeth. Requires precise design to balance flexibility and support; monitor abutment health over time.

### Code: D6950  
**Heading:** precision attachment  
- **When to use:** When a precision attachment (a pair of components) is used to connect a fixed partial denture to a removable prosthesis, separate from the main prosthesis.  
- **What to check:** Confirm the attachment consists of two interlocking parts (e.g., male and female components). Check fit, retention, and patient comfort during function.  
- **Notes:** Enhances stability and esthetics for hybrid prostheses. Requires meticulous maintenance instructions for patients; verify compatibility with existing restorations.

### Code: D6980  
**Heading:** fixed partial denture repair necessitated by restorative material failure  
- **When to use:** When a fixed partial denture requires repair due to a failure in the restorative material (e.g., porcelain fracture, metal crack).  
- **What to check:** Identify the specific material failure and assess the extent of damage. Ensure the repair restores function and esthetics without replacing the entire prosthesis.  
- **Notes:** Not for wear-and-tear or patient misuse; strictly material-related issues. Document the failure type for insurance; may require lab involvement.

### Code: D6985  
**Heading:** pediatric partial denture, fixed  
- **When to use:** When a fixed partial denture is provided for a pediatric patient, primarily for esthetic purposes.  
- **What to check:** Confirm the patient is a child and the primary goal is esthetics (e.g., anterior tooth loss). Assess growth considerations and parental consent.  
- **Notes:** Temporary solution until permanent teeth erupt; focus on esthetics over function. Monitor jaw development to avoid interference with growth.

### Code: D6999  
**Heading:** unspecified fixed prosthodontic procedure, by report  
- **When to use:** When a fixed prosthodontic procedure doesn't fit any specific code and requires a detailed narrative description.  
- **What to check:** Ensure no other code applies and provide a thorough report detailing the procedure, materials, and purpose. Verify clinical necessity and uniqueness.  
- **Notes:** Use sparingly; narrative must justify the procedure for insurance approval. Common for experimental or highly customized work; include photos if possible.

### Key Takeaways:
- **Purpose-Driven Coding:** Match the code to the primary intent (e.g., stabilization, repair, esthetics) rather than the complexity of the work.  
- **Material and Design Focus:** Identify material failures or specific components (e.g., stress breakers, precision attachments) to select the correct code.  
- **Patient Age Matters:** Differentiate pediatric (D6985) from adult procedures; pediatric codes prioritize esthetics over long-term function.  
- **Narrative Precision:** For D6999, a detailed report is critical—vague descriptions risk denial.  
- **Post-Procedure Evaluation:** Always check stability, occlusion, and patient comfort after services to ensure success and avoid rework.



Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_other_fixed_partial_denture_services_code(self, scenario: str) -> str:
        """Extract other fixed partial denture services code(s) for a given scenario."""
        try:
            print(f"Analyzing other fixed partial denture services scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Other fixed partial denture services extract_other_fixed_partial_denture_services_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in other fixed partial denture services code extraction: {str(e)}")
            return ""
    
    def activate_other_fixed_partial_denture_services(self, scenario: str) -> str:
        """Activate the other fixed partial denture services analysis process and return results."""
        try:
            result = self.extract_other_fixed_partial_denture_services_code(scenario)
            if not result:
                print("No other fixed partial denture services code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating other fixed partial denture services analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_other_fixed_partial_denture_services(scenario)
        print(f"\n=== OTHER FIXED PARTIAL DENTURE SERVICES ANALYSIS RESULT ===")
        print(f"OTHER FIXED PARTIAL DENTURE SERVICES CODE: {result if result else 'None'}")

# Create and export service instance
other_fixed_partial_denture_services_service = OtherFixedPartialDentureServicesServices()

# Example usage
if __name__ == "__main__":
    scenario = input("Enter an other fixed partial denture services dental scenario: ")
    other_fixed_partial_denture_services_service.run_analysis(scenario) 