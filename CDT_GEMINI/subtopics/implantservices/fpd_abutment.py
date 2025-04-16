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

class FixedPartialDentureAbutmentSupportedServices:
    """Class to analyze and extract abutment-supported fixed partial denture retainer codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing abutment-supported fixed partial denture retainers."""
        return PromptTemplate(
            template=f"""
You are a dental coding expert specializing in implant services.

### Before Picking a Code, Ask:
- What material is the FPD retainer made of? (porcelain/ceramic, metal, porcelain-fused-to-metal, etc.)
- If it's porcelain-fused-to-metal, what type of metal is used? (high noble, predominantly base, noble, titanium)
- Is the retainer being attached to an abutment on an implant?
- Is this retainer part of a fixed partial denture spanning multiple teeth?
- What is the location of the implant in the mouth?
- Are there special considerations for material selection based on esthetics or functional requirements?

---

### Fixed Partial Denture (FPD) Retainer, Abutment Supported

#### Code: D6068
**Heading:** Abutment supported retainer for porcelain/ceramic FPD  
**When to Use:**  
- A ceramic retainer for a fixed partial denture (bridge) is placed on an implant abutment.  
- Use for retainers fully made of porcelain/ceramic with no metal substructure.  
**What to Check:**  
- Confirm the retainer material is entirely porcelain or ceramic via lab specs.  
- Verify the retainer is part of an FPD and attached to an implant abutment, not a single crown.  
- Assess the tooth position (often anterior) for esthetic priority.  
- Check for patient allergies or esthetic demands favoring ceramics.  
**Notes:**  
- Ideal for anterior regions due to natural appearance and tissue compatibility.  
- Not for porcelain-fused-to-metal retainers (see D6069, D6070, D6071, D6195) or single crowns (see D6058).  
- Documentation should specify material, FPD involvement, and abutment use.  

#### Code: D6069
**Heading:** Abutment supported retainer for porcelain fused to metal FPD (high noble metal)  
**When to Use:**  
- A porcelain-fused-to-metal retainer with a high noble metal substructure is placed on an implant abutment for an FPD.  
- Use when the metal contains ≥60% noble metal, with ≥40% gold.  
**What to Check:**  
- Confirm the metal meets high noble criteria (≥60% noble, ≥40% gold) via lab report.  
- Verify the retainer is part of an FPD and abutment-supported.  
- Assess biocompatibility needs and suitability for anterior or posterior use.  
- Check occlusion and esthetic integration with pontics.  
**Notes:**  
- Offers excellent biocompatibility and porcelain bond strength.  
- Not for base or noble metals (see D6070, D6071) or single crowns (see D6059).  
- Requires material documentation for insurance justification.  

#### Code: D6070
**Heading:** Abutment supported retainer for porcelain fused to metal FPD (predominantly base metal)  
**When to Use:**  
- A porcelain-fused-to-metal retainer with a predominantly base metal substructure is placed on an implant abutment for an FPD.  
- Use when the metal contains <25% noble metal.  
**What to Check:**  
- Confirm the metal is predominantly base (<25% noble) via lab specs.  
- Verify the retainer is part of an FPD and abutment-supported.  
- Assess cost considerations or patient allergies to base metals.  
- Check suitability for posterior regions where esthetics is less critical.  
**Notes:**  
- Economical option but may have reduced biocompatibility in some patients.  
- Not for high noble or noble metals (see D6069, D6071) or single crowns (see D6060).  
- Document material and FPD details clearly.  

#### Code: D6071
**Heading:** Abutment supported retainer for porcelain fused to metal FPD (noble metal)  
**When to Use:**  
- A porcelain-fused-to-metal retainer with a noble metal substructure is placed on an implant abutment for an FPD.  
- Use when the metal contains ≥25% noble metal but does not meet high noble criteria.  
**What to Check:**  
- Confirm the metal contains ≥25% noble metal via lab documentation.  
- Verify the retainer is part of an FPD and abutment-supported.  
- Assess the balance of cost, durability, and esthetics.  
- Check for patient-specific needs (e.g., metal sensitivity).  
**Notes:**  
- Balances cost and biocompatibility for anterior or posterior FPDs.  
- Not for high noble or base metals (see D6069, D6070) or single crowns (see D6061).  
- Include metal composition in records for insurance.  

#### Code: D6195
**Heading:** Abutment supported retainer — porcelain fused to titanium and titanium alloys  
**When to Use:**  
- A porcelain-fused-to-titanium retainer is placed on an implant abutment for an FPD.  
- Use when the substructure is specifically titanium or a titanium alloy.  
**What to Check:**  
- Confirm the substructure is titanium or titanium alloy via lab report.  
- Verify the retainer is part of an FPD and abutment-supported.  
- Assess patient needs for lightweight, biocompatible materials (e.g., metal allergies).  
- Check esthetic and functional requirements for the bridge.  
**Notes:**  
- Ideal for patients with metal sensitivities due to titanium’s biocompatibility.  
- Not for other metal types (see D6069, D6070, D6071) or single crowns (see D6097).  
- Documentation should note titanium use and FPD involvement.  

#### Code: D6072
**Heading:** Abutment supported retainer for cast metal FPD (high noble metal)  
**When to Use:**  
- A full cast metal retainer made of high noble metal is placed on an implant abutment for an FPD.  
- Use when the metal contains ≥60% noble metal, with ≥40% gold.  
**What to Check:**  
- Confirm the metal meets high noble criteria (≥60% noble, ≥40% gold) via lab specs.  
- Verify the retainer is full metal, part of an FPD, and abutment-supported.  
- Assess suitability for posterior regions where strength is prioritized.  
- Check patient tolerance for metal visibility.  
**Notes:**  
- Excellent for posterior FPDs due to durability.  
- Not for porcelain-fused or base metal retainers (see D6069, D6073) or single crowns (see D6062).  
- Requires material documentation for insurance.  

#### Code: D6073
**Heading:** Abutment supported retainer for cast metal FPD (predominantly base metal)  
**When to Use:**  
- A full cast metal retainer made of predominantly base metal is placed on an implant abutment for an FPD.  
- Use when the metal contains <25% noble metal.  
**What to Check:**  
- Confirm the metal is predominantly base (<25% noble) via lab report.  
- Verify the retainer is full metal, part of an FPD, and abutment-supported.  
- Assess cost-effectiveness and patient acceptance of metal esthetics.  
- Check for posterior placement where strength is key.  
**Notes:**  
- Economical option with good strength for posterior FPDs.  
- Not for noble or high noble metals (see D6072, D6074) or single crowns (see D6063).  
- Document material and FPD details clearly.  

#### Code: D6074
**Heading:** Abutment supported retainer for cast metal FPD (noble metal)  
**When to Use:**  
- A full cast metal retainer made of noble metal is placed on an implant abutment for an FPD.  
- Use when the metal contains ≥25% noble metal but is not high noble.  
**What to Check:**  
- Confirm the metal contains ≥25% noble metal via lab specs.  
- Verify the retainer is full metal, part of an FPD, and abutment-supported.  
- Assess durability vs. esthetic trade-offs for posterior use.  
- Check patient-specific needs (e.g., biocompatibility).  
**Notes:**  
- Balances cost and durability for posterior FPDs.  
- Not for base or high noble metals (see D6072, D6073) or single crowns (see D6064).  
- Include metal composition in documentation.  

#### Code: D6194
**Heading:** Abutment supported retainer crown for FPD — titanium and titanium alloys  
**When to Use:**  
- A full titanium retainer is placed on an implant abutment for an FPD.  
- Use when the retainer is made entirely of titanium or titanium alloy.  
**What to Check:**  
- Confirm the retainer is entirely titanium or titanium alloy via lab report.  
- Verify it is part of an FPD and abutment-supported, not a single crown.  
- Assess patient needs for biocompatibility or lightweight materials.  
- Check functional requirements (often posterior) for the bridge.  
**Notes:**  
- Excellent for patients with metal allergies due to titanium’s properties.  
- Not for porcelain-fused titanium retainers (see D6195) or single crowns (see D6094).  
- Documentation should specify titanium use and FPD involvement.  

---

### Key Takeaways:
- **Retainer Focus:** Codes are for retainers in fixed partial dentures (bridges) supported by implant abutments, not single crowns.  
- **Material Drives Coding:** Codes differ by retainer material (porcelain/ceramic, metal, porcelain-fused-to-metal) and metal type (high noble, noble, base, titanium).  
- **Abutment Specific:** Ensure the retainer is abutment-supported, not directly implant-supported.  
- **Esthetics vs. Function:** Porcelain/ceramic (D6068) suits anterior regions; metal retainers (D6072–D6074, D6194) are better for posterior strength.  
- **Documentation Critical:** Specify material, metal composition, FPD structure, and abutment use for insurance and clarity.

Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_fpd_abutment_code(self, scenario: str) -> str:
        """Extract abutment-supported fixed partial denture retainer code(s) for a given scenario."""
        try:
            print(f"Analyzing FPD abutment scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"FPD abutment extract_fpd_abutment_code result: {code}")
            if code.lower() in ["none", "", "not applicable"]:
                return ""
            return code
        except Exception as e:
            print(f"Error in FPD abutment code extraction: {str(e)}")
            return ""
    
    def activate_fpd_abutment(self, scenario: str) -> str:
        """Activate the abutment-supported fixed partial denture retainer analysis process and return results."""
        try:
            result = self.extract_fpd_abutment_code(scenario)
            if not result:
                print("No FPD abutment code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating FPD abutment analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_fpd_abutment(scenario)
        print(f"\n=== FIXED PARTIAL DENTURE ABUTMENT SUPPORTED ANALYSIS RESULT ===")
        print(f"FPD RETAINER CODE: {result if result else 'None'}")

fpd_abutment_service = FixedPartialDentureAbutmentSupportedServices()
# Example usage
if __name__ == "__main__":
    fpd_service = FixedPartialDentureAbutmentSupportedServices()
    scenario = input("Enter an abutment-supported fixed partial denture retainer dental scenario: ")
    fpd_service.run_analysis(scenario)