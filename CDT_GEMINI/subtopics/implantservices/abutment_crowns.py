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

class SingleCrownsAbutmentSupportedServices:
    """Class to analyze and extract abutment-supported single crown codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing abutment-supported single crowns."""
        return PromptTemplate(
            template=f"""
You are a dental coding expert specializing in implant services.

### Before Picking a Code, Ask:
- What material is the crown made of? (porcelain/ceramic, metal, porcelain-fused-to-metal, etc.)
- If it's porcelain-fused-to-metal, what type of metal is used? (high noble, predominantly base, noble metal, titanium)
- Is the crown being attached to an abutment on an implant?
- Is this a single crown restoration or part of a multi-unit structure?
- What is the location of the implant in the mouth?
- Are there any special considerations for material selection based on esthetics or functional requirements?

---

### Single Crowns, Abutment Supported

#### Code: D6058
**Heading:** Abutment supported porcelain/ceramic crown  
**When to Use:**  
- A single all-ceramic or all-porcelain crown is placed on an implant abutment.  
- Use for restorations fully made of porcelain/ceramic with no metal substructure.  
**What to Check:**  
- Confirm the crown material is entirely porcelain or ceramic via documentation or lab specs.  
- Verify the crown is attached to an implant abutment, not cement- or screw-retained directly to the implant.  
- Assess the tooth position (often anterior) for esthetic priority.  
- Check for patient allergies or esthetic requirements favoring ceramics.  
**Notes:**  
- Ideal for anterior teeth due to excellent translucency and natural appearance.  
- Not for porcelain-fused-to-metal crowns (see D6059, D6060, D6061, D6097).  
- Documentation should specify material and abutment use for insurance.  

#### Code: D6059
**Heading:** Abutment supported porcelain fused to metal crown (high noble metal)  
**When to Use:**  
- A porcelain-fused-to-metal crown with a high noble metal substructure is placed on an implant abutment.  
- Use when the metal contains ≥60% noble metal, with ≥40% gold.  
**What to Check:**  
- Confirm the metal composition meets high noble criteria (≥60% noble, ≥40% gold) via lab report.  
- Verify the crown is abutment-supported and single-unit.  
- Assess biocompatibility needs (e.g., minimal corrosion risk).  
- Check esthetic and functional balance (suitable for anterior or posterior).  
**Notes:**  
- Offers excellent biocompatibility and bond strength to porcelain.  
- Not for base or noble metals (see D6060, D6061).  
- Requires material documentation for insurance justification.  

#### Code: D6060
**Heading:** Abutment supported porcelain fused to metal crown (predominantly base metal)  
**When to Use:**  
- A porcelain-fused-to-metal crown with a predominantly base metal substructure is placed on an implant abutment.  
- Use when the metal contains <25% noble metal.  
**What to Check:**  
- Confirm the metal is predominantly base (<25% noble) via lab specs.  
- Verify the crown is a single-unit restoration on an implant abutment.  
- Assess cost considerations or patient allergies to base metals.  
- Check suitability for posterior teeth where esthetics is less critical.  
**Notes:**  
- More affordable but may have reduced biocompatibility in sensitive patients.  
- Not for high noble or noble metals (see D6059, D6061).  
- Document material and abutment details for clarity.  

#### Code: D6061
**Heading:** Abutment supported porcelain fused to metal crown (noble metal)  
**When to Use:**  
- A porcelain-fused-to-metal crown with a noble metal substructure is placed on an implant abutment.  
- Use when the metal contains ≥25% noble metal but does not meet high noble criteria.  
**What to Check:**  
- Confirm the metal contains ≥25% noble metal via lab documentation.  
- Verify the crown is abutment-supported and single-unit.  
- Assess the balance of cost, durability, and esthetics.  
- Check for patient-specific needs (e.g., metal sensitivity).  
**Notes:**  
- Balances cost and biocompatibility for anterior or posterior use.  
- Not for high noble or base metals (see D6059, D6060).  
- Include metal composition in records for insurance.  

#### Code: D6097
**Heading:** Abutment supported crown — porcelain fused to titanium or titanium alloys  
**When to Use:**  
- A porcelain-fused-to-titanium crown is placed on an implant abutment.  
- Use when the substructure is specifically titanium or a titanium alloy.  
**What to Check:**  
- Confirm the substructure is titanium or titanium alloy via lab report.  
- Verify the crown is a single-unit restoration on an implant abutment.  
- Assess patient needs for lightweight, biocompatible materials (e.g., metal allergies).  
- Check esthetic and functional requirements.  
**Notes:**  
- Ideal for patients with metal sensitivities due to titanium’s biocompatibility.  
- Not for other metal types (see D6059, D6060, D6061).  
- Documentation should note titanium use for insurance approval.  

#### Code: D6062
**Heading:** Abutment supported cast metal crown (high noble metal)  
**When to Use:**  
- A full cast metal crown made of high noble metal is placed on an implant abutment.  
- Use when the metal contains ≥60% noble metal, with ≥40% gold.  
**What to Check:**  
- Confirm the metal meets high noble criteria (≥60% noble, ≥40% gold) via lab specs.  
- Verify the crown is full metal and abutment-supported.  
- Assess suitability for posterior teeth where strength is prioritized.  
- Check patient tolerance for metal visibility.  
**Notes:**  
- Excellent for posterior restorations due to durability.  
- Not for porcelain-fused or base metal crowns (see D6059, D6063).  
- Requires material documentation for insurance.  

#### Code: D6063
**Heading:** Abutment supported cast metal crown (predominantly base metal)  
**When to Use:**  
- A full cast metal crown made of predominantly base metal is placed on an implant abutment.  
- Use when the metal contains <25% noble metal.  
**What to Check:**  
- Confirm the metal is predominantly base (<25% noble) via lab report.  
- Verify the crown is full metal and single-unit on an abutment.  
- Assess cost-effectiveness and patient acceptance of metal esthetics.  
- Check for posterior placement where strength is key.  
**Notes:**  
- Economical option with good strength for posterior teeth.  
- Not for noble or high noble metals (see D6062, D6064).  
- Document material details clearly.  

#### Code: D6064
**Heading:** Abutment supported cast metal crown (noble metal)  
**When to Use:**  
- A full cast metal crown made of noble metal is placed on an implant abutment.  
- Use when the metal contains ≥25% noble metal but is not high noble.  
**What to Check:**  
- Confirm the metal contains ≥25% noble metal via lab specs.  
- Verify the crown is full metal and abutment-supported.  
- Assess durability vs. esthetic trade-offs for posterior use.  
- Check patient-specific needs (e.g., biocompatibility).  
**Notes:**  
- Balances cost and durability for posterior restorations.  
- Not for base or high noble metals (see D6062, D6063).  
- Include metal composition in documentation.  

#### Code: D6094
**Heading:** Abutment supported crown (titanium)  
**When to Use:**  
- A full titanium crown is placed on an implant abutment.  
- Use when the crown is made entirely of titanium or titanium alloy.  
**What to Check:**  
- Confirm the crown is entirely titanium or titanium alloy via lab report.  
- Verify it is a single-unit restoration on an implant abutment.  
- Assess patient needs for biocompatibility or lightweight materials.  
- Check functional requirements (often posterior).  
**Notes:**  
- Excellent for patients with metal allergies due to titanium’s properties.  
- Not for porcelain-fused titanium crowns (see D6097).  
- Documentation should specify titanium for insurance clarity.  

---

### Key Takeaways:
- **Single-Unit Focus:** All codes are for single crowns on implant abutments, not multi-unit restorations.  
- **Material Drives Coding:** Codes differ by crown material (porcelain/ceramic, metal, or porcelain-fused-to-metal) and metal type (high noble, noble, base, titanium).  
- **Abutment Specific:** Ensure the crown is abutment-supported, not cement- or screw-retained directly to the implant.  
- **Esthetics vs. Function:** Porcelain/ceramic (D6058) suits anterior teeth; metal crowns (D6062–D6064, D6094) are better for posterior strength.  
- **Documentation Critical:** Specify material, metal composition, and abutment use in records for insurance and clarity.

Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_abutment_crowns_code(self, scenario: str) -> str:
        """Extract abutment-supported single crown code(s) for a given scenario."""
        try:
            print(f"Analyzing abutment crowns scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Abutment crowns extract_abutment_crowns_code result: {code}")
            if code.lower() in ["none", "", "not applicable"]:
                return ""
            return code
        except Exception as e:
            print(f"Error in abutment crowns code extraction: {str(e)}")
            return ""
    
    def activate_single_crowns_abutment(self, scenario: str) -> str:
        """Activate the abutment-supported single crowns analysis process and return results."""
        try:
            result = self.extract_abutment_crowns_code(scenario)
            if not result:
                print("No abutment crowns code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating abutment crowns analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_single_crowns_abutment(scenario)
        print(f"\n=== ABUTMENT SUPPORTED CROWNS ANALYSIS RESULT ===")
        print(f"ABUTMENT SUPPORTED CROWN CODE: {result if result else 'None'}")

abutment_crowns_service = SingleCrownsAbutmentSupportedServices()
# Example usage
if __name__ == "__main__":
    crowns_service = SingleCrownsAbutmentSupportedServices()
    scenario = input("Enter an abutment-supported single crown dental scenario: ")
    crowns_service.run_analysis(scenario)