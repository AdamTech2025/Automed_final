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

class ImplantAbutmentSupportedRemovableDenturesServices:
    """Class to analyze and extract implant/abutment supported removable dentures codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing implant/abutment supported removable dentures."""
        return PromptTemplate(
            template=f"""
You are a dental coding expert specializing in implant services.

### Before Picking a Code, Ask:
- Is the arch fully edentulous (completely without teeth) or partially edentulous?
- Is the prosthesis for the maxillary (upper) or mandibular (lower) arch?
- Is the removable denture supported by implants, abutments, or both?
- What type of attachments or retention systems are being utilized?
- How many implants are supporting the removable prosthesis?
- What are the patient's functional and esthetic requirements for the prosthesis?

---

### Implant/Abutment Supported Removable Dentures

#### Code: D6110
**Heading:** Implant/abutment supported removable denture for edentulous arch – maxillary  
**When to Use:**  
- A removable prosthesis is created for a completely edentulous maxillary arch, supported by implants or abutments.  
- Use for patient-removable overdentures enhancing stability over conventional dentures.  
**What to Check:**  
- Confirm full maxillary edentulism via clinical exam or radiograph.  
- Verify implant/abutment count and positions (e.g., 4-6 for maxilla).  
- Assess attachment system (e.g., locators, ball, bar-clip).  
- Check denture base material (e.g., acrylic) and design rationale.  
**Notes:**  
- Improves retention, function, and comfort for resorbed ridges.  
- Not for partial edentulism (see D6112) or fixed prostheses.  
- Document attachments, implant count, and patient needs (e.g., hygiene, cost).  

#### Code: D6111
**Heading:** Implant/abutment supported removable denture for edentulous arch – mandibular  
**When to Use:**  
- A removable prosthesis is created for a completely edentulous mandibular arch, supported by implants or abutments.  
- Use for overdentures, often with minimal implants (e.g., 2-4).  
**What to Check:**  
- Confirm full mandibular edentulism via exam.  
- Verify implant/abutment support (e.g., two-implant standard).  
- Assess attachment type (e.g., locators for cost-effectiveness).  
- Check patient dexterity for maintenance.  
**Notes:**  
- Standard of care for mandibular edentulism due to stability gains.  
- Not for partial arches (see D6113) or fixed options.  
- Document implant positions, retention system, and bone preservation benefits.  

#### Code: D6112
**Heading:** Implant/abutment supported removable denture for partially edentulous arch – maxillary  
**When to Use:**  
- A removable prosthesis is created for a partially edentulous maxillary arch, supported by implants/abutments and natural teeth.  
- Use for hybrid stability combining implant and tooth support.  
**What to Check:**  
- Confirm remaining teeth and implant/abutment positions via exam.  
- Verify force distribution design (implants vs. teeth).  
- Assess attachment/clasp integration for retention.  
- Check biomechanical balance to avoid overload.  
**Notes:**  
- Enhances stability over conventional partials with proprioception.  
- Not for full edentulism (see D6110).  
- Document teeth, implants, and design specifics (e.g., stress-breaking attachments).  

#### Code: D6113
**Heading:** Implant/abutment supported removable denture for partially edentulous arch – mandibular  
**When to Use:**  
- A removable prosthesis is created for a partially edentulous mandibular arch, supported by implants/abutments and natural teeth.  
- Use for posterior support in distal extensions.  
**What to Check:**  
- Confirm remaining teeth and implant roles via radiograph.  
- Verify design for posterior stability (e.g., implant placement).  
- Assess integration of attachments with tooth clasps.  
- Check reduction in movement/food entrapment.  
**Notes:**  
- Improves function vs. conventional partials, especially distally.  
- Not for full edentulism (see D6111).  
- Document implant/tooth support, attachment type, and stability gains.  

---

### Key Takeaways:
- **Removable Focus:** Codes apply to patient-removable overdentures, not fixed prostheses or conventional dentures.  
- **Arch Specificity:** Differentiate fully edentulous (D6110–D6111) vs. partially edentulous (D6112–D6113) and maxillary vs. mandibular.  
- **Support Type:** Involves implants, abutments, or both, with attachments critical for retention (e.g., locators, bars).  
- **Stability Gains:** Offers superior function, bone preservation, and comfort over traditional dentures.  
- **Biomechanics Matter:** Partial cases require balancing implant rigidity and tooth mobility.  
- **Documentation Essential:** Specify attachments, implant count, materials, and patient factors (e.g., hygiene, esthetics).  
- **Patient Education:** Emphasize maintenance of prosthesis and supporting elements.

Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_removable_dentures_code(self, scenario: str) -> str:
        """Extract implant/abutment supported removable dentures code(s) for a given scenario."""
        try:
            print(f"Analyzing removable dentures scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Removable dentures extract_removable_dentures_code result: {code}")
            if code.lower() in ["none", "", "not applicable"]:
                return ""
            return code
        except Exception as e:
            print(f"Error in removable dentures code extraction: {str(e)}")
            return ""
    
    def activate_removable_dentures(self, scenario: str) -> str:
        """Activate the removable dentures analysis process and return results."""
        try:
            result = self.extract_removable_dentures_code(scenario)
            if not result:
                print("No removable dentures code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating removable dentures analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_removable_dentures(scenario)
        print(f"\n=== IMPLANT/ABUTMENT SUPPORTED REMOVABLE DENTURES ANALYSIS RESULT ===")
        print(f"REMOVABLE DENTURES CODE: {result if result else 'None'}")

removable_dentures_service = ImplantAbutmentSupportedRemovableDenturesServices()
# Example usage
if __name__ == "__main__":
    dentures_service = ImplantAbutmentSupportedRemovableDenturesServices()
    scenario = input("Enter an implant/abutment supported removable dentures dental scenario: ")
    dentures_service.run_analysis(scenario)