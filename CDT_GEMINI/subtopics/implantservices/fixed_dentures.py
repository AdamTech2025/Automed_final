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

class ImplantAbutmentSupportedFixedDenturesServices:
    """Class to analyze and extract implant/abutment-supported fixed dentures codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing implant/abutment-supported fixed dentures."""
        return PromptTemplate(
            template=f"""
You are a dental coding expert specializing in implant services.

### Before Picking a Code, Ask:
- Is the arch fully edentulous (completely without teeth) or partially edentulous?
- Is the prosthesis for the maxillary (upper) or mandibular (lower) arch?
- Is this intended as a permanent prosthesis or an interim prosthesis?
- What is the timeframe for using this prosthesis (permanent vs. temporary during healing)?
- Are there any special considerations based on the patient's oral anatomy?
- What materials are being used for the prosthesis?

---

### Implant/Abutment Supported Fixed Dentures

#### Code: D6114
**Heading:** Implant/abutment supported fixed denture for edentulous arch – maxillary  
**When to Use:**  
- A permanent fixed prosthesis is created for a completely edentulous upper arch, supported by implants or abutments.  
- Use for full-arch restorations replacing all maxillary teeth.  
**What to Check:**  
- Confirm the maxillary arch has no natural teeth via clinical exam or radiograph.  
- Verify sufficient implants (typically 4–8) are placed to support the prosthesis.  
- Assess the prosthesis design (e.g., screw-retained, cement-retained) and material (e.g., zirconia, acrylic).  
- Check occlusion and esthetic requirements for the upper arch.  
**Notes:**  
- Provides significant functional and esthetic benefits for fully edentulous patients.  
- Not for partial edentulism (see D6116) or interim use (see D6119).  
- Documentation should include implant count, arch status, and material details.  

#### Code: D6115
**Heading:** Implant/abutment supported fixed denture for edentulous arch – mandibular  
**When to Use:**  
- A permanent fixed prosthesis is created for a completely edentulous lower arch, supported by implants or abutments.  
- Use for full-arch restorations replacing all mandibular teeth.  
**What to Check:**  
- Confirm the mandibular arch is fully edentulous via exam or imaging.  
- Verify adequate implant support (often 4–6 implants) for stability.  
- Assess anatomical constraints (e.g., bone density, nerve position) affecting implant placement.  
- Check functional demands (e.g., chewing forces) for the lower arch.  
**Notes:**  
- Requires different implant positioning than maxillary due to anatomical differences.  
- Not for partial edentulism (see D6117) or temporary prostheses (see D6118).  
- Document implant positions and prosthesis specs for insurance.  

#### Code: D6116
**Heading:** Implant/abutment supported fixed denture for partially edentulous arch – maxillary  
**When to Use:**  
- A permanent fixed prosthesis is created for a partially edentulous upper arch, supported by implants or abutments.  
- Use when some natural teeth remain in the maxillary arch.  
**What to Check:**  
- Identify remaining natural teeth via clinical exam or radiograph and document replaced teeth.  
- Confirm implant/abutment support for the prosthesis (typically 2–4 implants per segment).  
- Assess occlusion compatibility with natural teeth and esthetic integration.  
- Check prosthesis design for biomechanical stability.  
**Notes:**  
- Requires careful planning to align with existing dentition.  
- Not for fully edentulous arches (see D6114) or interim use (see D6119).  
- Include details of remaining teeth and implant positions in records.  

#### Code: D6117
**Heading:** Implant/abutment supported fixed denture for partially edentulous arch – mandibular  
**When to Use:**  
- A permanent fixed prosthesis is created for a partially edentulous lower arch, supported by implants or abutments.  
- Use when some natural teeth remain in the mandibular arch.  
**What to Check:**  
- Confirm which mandibular teeth remain and document replaced teeth via exam or imaging.  
- Verify implant/abutment support (often 2–4 implants) and stability.  
- Assess biomechanical forces, especially for posterior replacements.  
- Check occlusion and integration with natural teeth.  
**Notes:**  
- May face higher chewing forces than maxillary prostheses.  
- Not for fully edentulous arches (see D6115) or temporary use (see D6118).  
- Documentation should note remaining teeth and prosthesis design.  

#### Code: D6118
**Heading:** Implant/abutment supported interim fixed denture for edentulous arch – mandibular  
**When to Use:**  
- A temporary fixed prosthesis is placed for a fully edentulous lower arch during healing or prior to a permanent prosthesis.  
- Use for interim restorations to maintain function and esthetics.  
**What to Check:**  
- Confirm the mandibular arch is fully edentulous via exam or radiograph.  
- Verify the interim nature (e.g., during osseointegration) and expected timeline to permanent prosthesis.  
- Assess implant stability and temporary material (e.g., acrylic) suitability.  
- Check patient needs for function during healing (e.g., phonetics, chewing).  
**Notes:**  
- Protects healing implants while allowing limited function.  
- Not for permanent use (see D6115) or partial edentulism (see D6117).  
- Document interim purpose and timeline for insurance clarity.  

#### Code: D6119
**Heading:** Implant/abutment supported interim fixed denture for edentulous arch – maxillary  
**When to Use:**  
- A temporary fixed prosthesis is placed for a fully edentulous upper arch during healing or prior to a permanent prosthesis.  
- Use for interim restorations to support esthetics and function.  
**What to Check:**  
- Confirm the maxillary arch is fully edentulous via clinical exam or imaging.  
- Verify the temporary purpose and timeline to permanent prosthesis (e.g., D6114).  
- Assess implant stability and material choice (e.g., acrylic, composite) for interim use.  
- Check esthetic and phonetic requirements during healing.  
**Notes:**  
- Allows evaluation of function and esthetics before final design.  
- Not for permanent use (see D6114) or partial edentulism (see D6116).  
- Include clinical rationale for interim prosthesis in records.  

---

### Key Takeaways:
- **Fixed Prostheses:** Codes apply to non-removable dentures supported by implants or abutments.  
- **Arch Specificity:** Distinguish between maxillary (upper) and mandibular (lower) due to functional and anatomical differences.  
- **Edentulism Status:** Separate codes for fully edentulous (D6114, D6115, D6118, D6119) vs. partially edentulous (D6116, D6117) arches.  
- **Permanent vs. Interim:** D6114–D6117 are permanent; D6118–D6119 are temporary for healing or transition.  
- **Documentation:** Specify arch status, remaining teeth (if any), implant count, and prosthesis material (e.g., zirconia, acrylic).  
- **Hybrid Prostheses:** Often involve metal frameworks with acrylic/composite teeth—note design details.

Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_fixed_dentures_code(self, scenario: str) -> str:
        """Extract implant/abutment-supported fixed dentures code(s) for a given scenario."""
        try:
            print(f"Analyzing fixed dentures scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Fixed dentures extract_fixed_dentures_code result: {code}")
            if code.lower() in ["none", "", "not applicable"]:
                return ""
            return code
        except Exception as e:
            print(f"Error in fixed dentures code extraction: {str(e)}")
            return ""
    
    def activate_implant_supported_fixed_dentures(self, scenario: str) -> str:
        """Activate the implant/abutment-supported fixed dentures analysis process and return results."""
        try:
            result = self.extract_fixed_dentures_code(scenario)
            if not result:
                print("No fixed dentures code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating fixed dentures analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_implant_supported_fixed_dentures(scenario)
        print(f"\n=== IMPLANT/ABUTMENT SUPPORTED FIXED DENTURES ANALYSIS RESULT ===")
        print(f"FIXED DENTURES CODE: {result if result else 'None'}")

# Create service instance
fixed_dentures_service = ImplantAbutmentSupportedFixedDenturesServices()

# Example usage
if __name__ == "__main__":
    scenario = input("Enter an implant/abutment-supported fixed dentures dental scenario: ")
    fixed_dentures_service.run_analysis(scenario)