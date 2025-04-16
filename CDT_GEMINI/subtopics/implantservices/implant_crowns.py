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

class SingleCrownsImplantSupportedServices:
    """Class to analyze and extract implant-supported single crown codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing implant-supported single crowns."""
        return PromptTemplate(
            template=f"""
You are a dental coding expert specializing in implant services.

### Before Picking a Code, Ask:
- What material is the crown made of? (porcelain/ceramic, metal, porcelain-fused-to-metal, etc.)
- If it's porcelain-fused-to-metal, what type of metal alloy is used? (high noble, predominantly base, noble, titanium)
- Is the crown being attached directly to the implant (not using an abutment)?
- Is this a single crown restoration or part of a multi-unit prosthesis?
- What is the location of the implant in the mouth?
- Are there special considerations for material selection based on esthetics or functional requirements?

---

### Single Crowns, Implant Supported

#### Code: D6065
**Heading:** Implant supported porcelain/ceramic crown  
**When to Use:**  
- A single all-ceramic or all-porcelain crown is placed directly on an implant without an intermediate abutment.  
- Use for restorations fully made of porcelain/ceramic with no metal substructure.  
**What to Check:**  
- Confirm the crown material is entirely porcelain or ceramic via lab specs.  
- Verify the crown is attached directly to the implant, not via an abutment or part of a multi-unit prosthesis.  
- Assess the tooth position (often anterior) for esthetic priority.  
- Check for patient allergies or esthetic requirements favoring ceramics.  
**Notes:**  
- Ideal for anterior teeth due to excellent translucency and natural appearance.  
- Not for porcelain-fused-to-metal crowns (see D6066, D6082, D6083, D6084) or abutment-supported crowns (see D6058).  
- Documentation should specify material and direct implant support for insurance.  

#### Code: D6066
**Heading:** Implant supported crown — porcelain fused to high noble alloys  
**When to Use:**  
- A porcelain-fused-to-metal crown with a high noble metal substructure is placed directly on an implant.  
- Use when the metal contains ≥60% noble metal, with ≥40% gold.  
**What to Check:**  
- Confirm the metal meets high noble criteria (≥60% noble, ≥40% gold) via lab report.  
- Verify the crown is single-unit and attached directly to the implant.  
- Assess biocompatibility needs (e.g., minimal corrosion risk).  
- Check esthetic and functional balance (suitable for anterior or posterior).  
**Notes:**  
- Offers excellent biocompatibility and bond strength to porcelain.  
- Not for base or noble metals (see D6082, D6083) or abutment-supported crowns (see D6059).  
- Requires material documentation for insurance justification.  

#### Code: D6082
**Heading:** Implant supported crown — porcelain fused to predominantly base alloys  
**When to Use:**  
- A porcelain-fused-to-metal crown with a predominantly base metal substructure is placed directly on an implant.  
- Use when the metal contains <25% noble metal.  
**What to Check:**  
- Confirm the metal is predominantly base (<25% noble) via lab specs.  
- Verify the crown is a single-unit restoration attached directly to the implant.  
- Assess cost considerations or patient allergies to base metals.  
- Check suitability for posterior teeth where esthetics is less critical.  
**Notes:**  
- More affordable but may have reduced biocompatibility in sensitive patients.  
- Not for high noble or noble metals (see D6066, D6083) or abutment-supported crowns (see D6060).  
- Document material and direct implant support for clarity.  

#### Code: D6083
**Heading:** Implant supported crown — porcelain fused to noble alloys  
**When to Use:**  
- A porcelain-fused-to-metal crown with a noble metal substructure is placed directly on an implant.  
- Use when the metal contains ≥25% noble metal but does not meet high noble criteria.  
**What to Check:**  
- Confirm the metal contains ≥25% noble metal via lab documentation.  
- Verify the crown is single-unit and attached directly to the implant.  
- Assess the balance of cost, durability, and esthetics.  
- Check for patient-specific needs (e.g., metal sensitivity).  
**Notes:**  
- Balances cost and biocompatibility for anterior or posterior use.  
- Not for high noble or base metals (see D6066, D6082) or abutment-supported crowns (see D6061).  
- Include metal composition in records for insurance.  

#### Code: D6084
**Heading:** Implant supported crown — porcelain fused to titanium or titanium alloys  
**When to Use:**  
- A porcelain-fused-to-titanium crown is placed directly on an implant.  
- Use when the substructure is specifically titanium or a titanium alloy.  
**What to Check:**  
- Confirm the substructure is titanium or titanium alloy via lab report.  
- Verify the crown is a single-unit restoration attached directly to the implant.  
- Assess patient needs for lightweight, biocompatible materials (e.g., metal allergies).  
- Check esthetic and functional requirements.  
**Notes:**  
- Ideal for patients with metal sensitivities due to titanium’s biocompatibility.  
- Not for other metal types (see D6066, D6082, D6083) or abutment-supported crowns (see D6097).  
- Documentation should note titanium use for insurance approval.  

#### Code: D6067
**Heading:** Implant supported crown — high noble alloys  
**When to Use:**  
- A full metal crown made of high noble alloys is placed directly on an implant.  
- Use when the metal contains ≥60% noble metal, with ≥40% gold.  
**What to Check:**  
- Confirm the metal meets high noble criteria (≥60% noble, ≥40% gold) via lab specs.  
- Verify the crown is full metal and attached directly to the implant.  
- Assess suitability for posterior teeth where strength is prioritized.  
- Check patient tolerance for metal visibility.  
**Notes:**  
- Excellent for posterior restorations due to durability.  
- Not for porcelain-fused or base metal crowns (see D6066, D6086) or abutment-supported crowns (see D6062).  
- Requires material documentation for insurance.  

#### Code: D6086
**Heading:** Implant supported crown — predominantly base alloys  
**When to Use:**  
- A full metal crown made of predominantly base alloys is placed directly on an implant.  
- Use when the metal contains <25% noble metal.  
**What to Check:**  
- Confirm the metal is predominantly base (<25% noble) via lab report.  
- Verify the crown is full metal and single-unit attached directly to the implant.  
- Assess cost-effectiveness and patient acceptance of metal esthetics.  
- Check for posterior placement where strength is key.  
**Notes:**  
- Economical option with good strength for posterior teeth.  
- Not for noble or high noble metals (see D6067, D6087) or abutment-supported crowns (see D6063).  
- Document material details clearly.  

#### Code: D6087
**Heading:** Implant supported crown — noble alloys  
**When to Use:**  
- A full metal crown made of noble alloys is placed directly on an implant.  
- Use when the metal contains ≥25% noble metal but is not high noble.  
**What to Check:**  
- Confirm the metal contains ≥25% noble metal via lab specs.  
- Verify the crown is full metal and attached directly to the implant.  
- Assess durability vs. esthetic trade-offs for posterior use.  
- Check patient-specific needs (e.g., biocompatibility).  
**Notes:**  
- Balances cost and durability for posterior restorations.  
- Not for base or high noble metals (see D6067, D6086) or abutment-supported crowns (see D6064).  
- Include metal composition in documentation.  

#### Code: D6088
**Heading:** Implant supported crown — titanium and titanium alloys  
**When to Use:**  
- A full titanium crown is placed directly on an implant.  
- Use when the crown is made entirely of titanium or titanium alloy.  
**What to Check:**  
- Confirm the crown is entirely titanium or titanium alloy via lab report.  
- Verify it is a single-unit restoration attached directly to the implant.  
- Assess patient needs for biocompatibility or lightweight materials.  
- Check functional requirements (often posterior).  
**Notes:**  
- Excellent for patients with metal allergies due to titanium’s properties.  
- Not for porcelain-fused titanium crowns (see D6084) or abutment-supported crowns (see D6094).  
- Documentation should specify titanium use for insurance clarity.  

---

### Key Takeaways:
- **Single-Unit Focus:** All codes are for single crowns placed directly on implants, not via abutments or as part of multi-unit prostheses.  
- **Material Drives Coding:** Codes differ by crown material (porcelain/ceramic, metal, porcelain-fused-to-metal) and metal type (high noble, noble, base, titanium).  
- **Implant Direct Support:** Ensure the crown is attached directly to the implant, not an abutment-supported restoration.  
- **Esthetics vs. Function:** Porcelain/ceramic (D6065) suits anterior teeth; metal crowns (D6067, D6086–D6088) are better for posterior strength.  
- **Documentation Critical:** Specify material, metal composition, and direct implant support in records for insurance and clarity.

Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_implant_crowns_code(self, scenario: str) -> str:
        """Extract implant-supported single crown code(s) for a given scenario."""
        try:
            print(f"Analyzing implant crowns scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Implant crowns extract_implant_crowns_code result: {code}")
            if code.lower() in ["none", "", "not applicable"]:
                return ""
            return code
        except Exception as e:
            print(f"Error in implant crowns code extraction: {str(e)}")
            return ""
    
    def activate_single_crowns_implant(self, scenario: str) -> str:
        """Activate the implant-supported single crowns analysis process and return results."""
        try:
            result = self.extract_implant_crowns_code(scenario)
            if not result:
                print("No implant crowns code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating implant crowns analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_single_crowns_implant(scenario)
        print(f"\n=== IMPLANT SUPPORTED CROWNS ANALYSIS RESULT ===")
        print(f"IMPLANT SUPPORTED CROWN CODE: {result if result else 'None'}")

implant_crowns_service = SingleCrownsImplantSupportedServices()
# Example usage
if __name__ == "__main__":
    crowns_service = SingleCrownsImplantSupportedServices()
    scenario = input("Enter an implant-supported single crown dental scenario: ")
    crowns_service.run_analysis(scenario)