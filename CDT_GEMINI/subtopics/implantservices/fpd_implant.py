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

class FixedPartialDentureImplantSupportedServices:
    """Class to analyze and extract implant-supported fixed partial denture retainer codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing implant-supported fixed partial denture retainers."""
        return PromptTemplate(
            template=f"""
You are a dental coding expert specializing in implant services.

### Before Picking a Code, Ask:
- What material is the FPD retainer made of? (porcelain/ceramic, metal, porcelain-fused-to-metal, etc.)
- If it's porcelain-fused-to-metal, what type of metal is used? (high noble, predominantly base, noble, titanium)
- Is the retainer being attached directly to the implant without an abutment?
- Is this retainer part of a fixed partial denture spanning multiple teeth?
- What is the location of the implant in the mouth?
- Are there special considerations for material selection based on esthetics or functional requirements?

---

### Fixed Partial Denture (FPD) Supported by Implant Retainers

#### Code: D6075
**Heading:** Implant supported retainer for ceramic FPD  
**When to Use:**  
- A ceramic retainer for a fixed partial denture (bridge) is placed directly on an implant without an intermediate abutment.  
- Use for retainers fully made of porcelain/ceramic with no metal substructure.  
**What to Check:**  
- Confirm the retainer material is entirely porcelain or ceramic via lab specs.  
- Verify the retainer is part of an FPD and attached directly to the implant, not via an abutment.  
- Assess the tooth position (often anterior) for esthetic priority.  
- Check durability for high-stress areas and patient esthetic demands.  
**Notes:**  
- Ideal for anterior regions due to excellent esthetics but may be less durable than metal options.  
- Not for porcelain-fused-to-metal retainers (see D6076, D6098, D6099, D6120) or abutment-supported retainers (see D6068).  
- Documentation should specify material, FPD involvement, and direct implant support.  

#### Code: D6076
**Heading:** Implant supported retainer for FPD — porcelain fused to high noble alloys  
**When to Use:**  
- A porcelain-fused-to-metal retainer with a high noble metal substructure is placed directly on an implant for an FPD.  
- Use when the metal contains ≥60% noble metal, with ≥40% gold.  
**What to Check:**  
- Confirm the metal meets high noble criteria (≥60% noble, ≥40% gold) via lab report.  
- Verify the retainer is part of an FPD and attached directly to the implant.  
- Assess biocompatibility and suitability for anterior or posterior use.  
- Check occlusion and esthetic integration with pontics.  
**Notes:**  
- Offers excellent biocompatibility and porcelain bond strength.  
- Not for base or noble metals (see D6098, D6099) or abutment-supported retainers (see D6069).  
- Requires material documentation for insurance justification.  

#### Code: D6098
**Heading:** Implant supported retainer — porcelain fused to predominantly base alloys  
**When to Use:**  
- A porcelain-fused-to-metal retainer with a predominantly base metal substructure is placed directly on an implant for an FPD.  
- Use when the metal contains <25% noble metal.  
**What to Check:**  
- Confirm the metal is predominantly base (<25% noble) via lab specs.  
- Verify the retainer is part of an FPD and attached directly to the implant.  
- Assess cost considerations or patient allergies to base metals.  
- Check suitability for posterior regions where esthetics is less critical.  
**Notes:**  
- Economical option but may have reduced biocompatibility in some patients.  
- Not for high noble or noble metals (see D6076, D6099) or abutment-supported retainers (see D6070).  
- Document material and FPD details clearly.  

#### Code: D6099
**Heading:** Implant supported retainer for FPD — porcelain fused to noble alloys  
**When to Use:**  
- A porcelain-fused-to-metal retainer with a noble metal substructure is placed directly on an implant for an FPD.  
- Use when the metal contains ≥25% noble metal but does not meet high noble criteria.  
**What to Check:**  
- Confirm the metal contains ≥25% noble metal via lab documentation.  
- Verify the retainer is part of an FPD and attached directly to the implant.  
- Assess the balance of cost, durability, and esthetics.  
- Check for patient-specific needs (e.g., metal sensitivity).  
**Notes:**  
- Balances cost and biocompatibility for anterior or posterior FPDs.  
- Not for high noble or base metals (see D6076, D6098) or abutment-supported retainers (see D6071).  
- Include metal composition in records for insurance.  

#### Code: D6120
**Heading:** Implant supported retainer — porcelain fused to titanium and titanium alloys  
**When to Use:**  
- A porcelain-fused-to-titanium retainer is placed directly on an implant for an FPD.  
- Use when the substructure is specifically titanium or a titanium alloy.  
**What to Check:**  
- Confirm the substructure is titanium or titanium alloy via lab report.  
- Verify the retainer is part of an FPD and attached directly to the implant.  
- Assess patient needs for lightweight, biocompatible materials (e.g., metal allergies).  
- Check esthetic and functional requirements for the bridge.  
**Notes:**  
- Ideal for patients with metal sensitivities due to titanium’s biocompatibility.  
- Not for other metal types (see D6076, D6098, D6099) or abutment-supported retainers (see D6195).  
- Documentation should note titanium use and FPD involvement.  

#### Code: D6077
**Heading:** Implant supported retainer for metal FPD — high noble alloys  
**When to Use:**  
- A full metal retainer made of high noble alloys is placed directly on an implant for an FPD.  
- Use when the metal contains ≥60% noble metal, with ≥40% gold.  
**What to Check:**  
- Confirm the metal meets high noble criteria (≥60% noble, ≥40% gold) via lab specs.  
- Verify the retainer is full metal, part of an FPD, and attached directly to the implant.  
- Assess suitability for posterior regions where strength is prioritized.  
- Check patient tolerance for metal visibility.  
**Notes:**  
- Excellent for posterior FPDs due to durability.  
- Not for porcelain-fused or base metal retainers (see D6076, D6121) or abutment-supported retainers (see D6072).  
- Requires material documentation for insurance.  

#### Code: D6121
**Heading:** Implant supported retainer for metal FPD — predominantly base alloys  
**When to Use:**  
- A full metal retainer made of predominantly base alloys is placed directly on an implant for an FPD.  
- Use when the metal contains <25% noble metal.  
**What to Check:**  
- Confirm the metal is predominantly base (<25% noble) via lab report.  
- Verify the retainer is full metal, part of an FPD, and attached directly to the implant.  
- Assess cost-effectiveness and patient acceptance of metal esthetics.  
- Check for posterior placement where strength is key.  
**Notes:**  
- Economical option with good strength for posterior FPDs.  
- Not for noble or high noble metals (see D6077, D6122) or abutment-supported retainers (see D6073).  
- Document material and FPD details clearly.  

#### Code: D6122
**Heading:** Implant supported retainer for metal FPD — noble alloys  
**When to Use:**  
- A full metal retainer made of noble alloys is placed directly on an implant for an FPD.  
- Use when the metal contains ≥25% noble metal but is not high noble.  
**What to Check:**  
- Confirm the metal contains ≥25% noble metal via lab specs.  
- Verify the retainer is full metal, part of an FPD, and attached directly to the implant.  
- Assess durability vs. esthetic trade-offs for posterior use.  
- Check patient-specific needs (e.g., biocompatibility).  
**Notes:**  
- Balances cost and durability for posterior FPDs.  
- Not for base or high noble metals (see D6077, D6121) or abutment-supported retainers (see D6074).  
- Include metal composition in documentation.  

#### Code: D6123
**Heading:** Implant supported retainer for metal FPD — titanium and titanium alloys  
**When to Use:**  
- A full titanium retainer is placed directly on an implant for an FPD.  
- Use when the retainer is made entirely of titanium or titanium alloy.  
**What to Check:**  
- Confirm the retainer is entirely titanium or titanium alloy via lab report.  
- Verify it is part of an FPD and attached directly to the implant, not via an abutment.  
- Assess patient needs for biocompatibility or lightweight materials.  
- Check functional requirements (often posterior) for the bridge.  
**Notes:**  
- Excellent for patients with metal allergies due to titanium’s properties.  
- Not for porcelain-fused titanium retainers (see D6120) or abutment-supported retainers (see D6194).  
- Documentation should specify titanium use and FPD involvement.  

---

### Key Takeaways:
- **Implant Direct Support:** Codes are for retainers in fixed partial dentures (bridges) attached directly to implants, not via abutments.  
- **Material Drives Coding:** Codes differ by retainer material (porcelain/ceramic, metal, porcelain-fused-to-metal) and metal type (high noble, noble, base, titanium).  
- **FPD Specific:** Ensure the retainer is part of a bridge, not a single crown or abutment-supported restoration.  
- **Esthetics vs. Function:** Porcelain/ceramic (D6075) suits anterior regions; metal retainers (D6077, D6121–D6123) are better for posterior strength.  
- **Documentation Critical:** Specify material, metal composition, FPD structure, and direct implant support for insurance and clarity.

Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_fpd_implant_code(self, scenario: str) -> str:
        """Extract implant-supported fixed partial denture retainer code(s) for a given scenario."""
        try:
            print(f"Analyzing FPD implant scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"FPD implant extract_fpd_implant_code result: {code}")
            if code.lower() in ["none", "", "not applicable"]:
                return ""
            return code
        except Exception as e:
            print(f"Error in FPD implant code extraction: {str(e)}")
            return ""
    
    def activate_fpd_implant(self, scenario: str) -> str:
        """Activate the implant-supported fixed partial denture retainer analysis process and return results."""
        try:
            result = self.extract_fpd_implant_code(scenario)
            if not result:
                print("No FPD implant code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating FPD implant analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_fpd_implant(scenario)
        print(f"\n=== FIXED PARTIAL DENTURE IMPLANT SUPPORTED ANALYSIS RESULT ===")
        print(f"FPD IMPLANT RETAINER CODE: {result if result else 'None'}")

fpd_implant_service = FixedPartialDentureImplantSupportedServices()
# Example usage
if __name__ == "__main__":
    fpd_implant_service = FixedPartialDentureImplantSupportedServices()
    scenario = input("Enter an implant-supported fixed partial denture retainer dental scenario: ")
    fpd_implant_service.run_analysis(scenario)