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

class ImplantSupportedProstheticsServices:
    """Class to analyze and extract implant-supported prosthetics component codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing implant-supported prosthetics components."""
        return PromptTemplate(
            template=f"""
You are a dental coding expert specializing in implant services.

### Before Picking a Code, Ask:
- What specific component of an implant-supported prosthesis is being placed?
- Is this a connecting bar, abutment, or attachment?
- If it's an abutment, is it prefabricated or custom-fabricated?
- Is this an interim component or a definitive component?
- Is this a semi-precision component?
- What is the purpose of the component in the overall prosthetic plan?

---

### Implant Supported Prosthetics Components

#### Code: D6055
**Heading:** Connecting bar — implant supported or abutment supported  
**When to Use:**  
- A bar is placed to connect multiple implants or abutments to stabilize a prosthesis (e.g., overdenture).  
- Use for bars linking multiple implants or abutments to distribute forces.  
**What to Check:**  
- Confirm multiple implants or abutments are present via clinical exam or radiograph.  
- Verify the bar is designed to support a removable prosthesis and enhance retention.  
- Assess material (e.g., metal) and design (e.g., Hader, Dolder) for stability.  
- Check the prosthetic plan for overdenture compatibility.  
**Notes:**  
- Enhances stability for removable prostheses by distributing occlusal forces.  
- Not for single implant restorations or fixed prostheses (e.g., crowns, bridges).  
- Documentation should specify implant/abutment count and bar purpose.  

#### Code: D6056
**Heading:** Prefabricated abutment — includes modification and placement  
**When to Use:**  
- A manufactured, ready-made abutment is placed on an implant, with possible chair-side modifications.  
- Use for cost-effective abutments requiring minimal customization.  
**What to Check:**  
- Confirm the abutment is prefabricated, not custom-made, via supplier details.  
- Document any modifications (e.g., contouring, angulation adjustments).  
- Verify compatibility with the implant system and prosthesis (e.g., crown, overdenture).  
- Check soft tissue contours and emergence profile needs.  
**Notes:**  
- More economical than custom abutments but may need adjustments for fit.  
- Not for complex cases requiring lab fabrication (see D6057) or temporary use (see D6051).  
- Include modification details in records for insurance.  

#### Code: D6057
**Heading:** Custom fabricated abutment — includes placement  
**When to Use:**  
- A laboratory-made abutment is placed, designed specifically for the patient’s implant and prosthesis.  
- Use for tailored abutments addressing unique anatomical or prosthetic needs.  
**What to Check:**  
- Confirm the abutment is custom-made by a lab, not prefabricated, via lab report.  
- Verify it addresses specific needs (e.g., angulation, tissue contours, esthetics).  
- Assess integration with the planned prosthesis (e.g., crown, bridge, overdenture).  
- Check implant stability and soft tissue health prior to placement.  
**Notes:**  
- Offers optimal emergence profiles and angulation correction but is costlier.  
- Not for prefabricated (see D6056) or interim abutments (see D6051).  
- Documentation should detail customization rationale and lab involvement.  

#### Code: D6051
**Heading:** Interim implant abutment placement  
**When to Use:**  
- A temporary abutment is placed during a healing or transitional period before the final prosthesis.  
- Use to shape soft tissue or support temporary restorations.  
**What to Check:**  
- Confirm the abutment is interim, not a healing cap, via clinical intent.  
- Document the transitional purpose and expected timeline to definitive abutment/prosthesis.  
- Verify implant stability and soft tissue healing status.  
- Check compatibility with temporary restorations (e.g., provisional crown).  
**Notes:**  
- Supports tissue shaping and temporary function; not for long-term use.  
- Distinct from healing caps, which are not coded as D6051.  
- Include interim purpose and timeline in records for clarity.  

#### Code: D6191
**Heading:** Semi-precision abutment — placement  
**When to Use:**  
- A semi-precision abutment is placed on an implant to align with a removable prosthesis attachment.  
- Use for initial or replacement semi-precision abutments.  
**What to Check:**  
- Confirm the abutment has milled surfaces for precise attachment alignment.  
- Verify it is part of a removable prosthesis plan (e.g., overdenture).  
- Assess implant position and compatibility with the prosthesis attachment.  
- Check if it’s initial placement or replacement of a worn component.  
**Notes:**  
- Enhances retention for removable prostheses via precise alignment.  
- Not for fixed prostheses or non-precision components (see D6056, D6057).  
- Document abutment type and prosthesis plan for insurance.  

#### Code: D6192
**Heading:** Semi-precision attachment — placement  
**When to Use:**  
- A semi-precision attachment is luted to a removable prosthesis to connect with a semi-precision abutment.  
- Use for initial or replacement attachments on the prosthesis side.  
**What to Check:**  
- Confirm the attachment is luted to the prosthesis, not the abutment (see D6191).  
- Verify it matches a semi-precision abutment for retention.  
- Assess the prosthesis condition and attachment integration (e.g., acrylic base).  
- Check if it’s initial placement or replacement due to wear.  
**Notes:**  
- Provides enhanced retention and stability for removable prostheses.  
- Requires a corresponding semi-precision abutment (D6191).  
- Documentation should specify attachment placement and prosthesis details.  

---

### Key Takeaways:
- **Component Focus:** Codes apply to supporting components (bars, abutments, attachments), not final prostheses like crowns or dentures.  
- **Type Specificity:** Distinguish between prefabricated (D6056), custom (D6057), interim (D6051), and semi-precision (D6191, D6192) components.  
- **Functional Role:** Components stabilize, retain, or shape for prostheses (e.g., overdentures, crowns).  
- **Documentation Essential:** Specify component type, materials, purpose, and prosthetic plan for insurance and clarity.  
- **Healing Caps Excluded:** Healing caps are not coded as interim abutments (D6051).  

Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_implant_supported_prosthetics_code(self, scenario: str) -> str:
        """Extract implant-supported prosthetics component code(s) for a given scenario."""
        try:
            print(f"Analyzing implant prosthetics scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Implant prosthetics extract_implant_supported_prosthetics_code result: {code}")
            if code.lower() in ["none", "", "not applicable"]:
                return ""
            return code
        except Exception as e:
            print(f"Error in implant prosthetics code extraction: {str(e)}")
            return ""
    
    def activate_implant_supported_prosthetics(self, scenario: str) -> str:
        """Activate the implant-supported prosthetics analysis process and return results."""
        try:
            result = self.extract_implant_supported_prosthetics_code(scenario)
            if not result:
                print("No implant prosthetics code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating implant prosthetics analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_implant_supported_prosthetics(scenario)
        print(f"\n=== IMPLANT SUPPORTED PROSTHETICS ANALYSIS RESULT ===")
        print(f"IMPLANT PROSTHETICS CODE: {result if result else 'None'}")

implant_supported_prosthetics_service = ImplantSupportedProstheticsServices()
# Example usage
if __name__ == "__main__":
    prosthetics_service = ImplantSupportedProstheticsServices()
    scenario = input("Enter an implant-supported prosthetics dental scenario: ")
    prosthetics_service.run_analysis(scenario)