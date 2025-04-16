"""
Module for extracting fixed partial denture retainers inlays onlays codes.
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

class FixedPartialDentureRetainersInlaysOnlaysServices:
    """Class to analyze and extract fixed partial denture retainers inlays onlays codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing fixed partial denture retainers inlays onlays services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert

Before picking a code, ask:
- What was the primary reason the patient came in? Was it for routine maintenance or a specific issue with the prosthesis?
- What material is being used for the retainer (e.g., cast metal, porcelain/ceramic, resin, titanium)?
- How many surfaces are involved in the inlay or onlay (two, three, or more)?
- Is this a resin-bonded fixed prosthesis or a traditional fixed partial denture retainer?
- Does the patient's dental history indicate specific material preferences or allergies (e.g., metal sensitivity)?

### Code: D6545  
**Heading:** retainer - cast metal for resin bonded fixed prosthesis  
- **When to use:** When a cast metal retainer is fabricated for a resin-bonded fixed prosthesis (e.g., Maryland bridge) to replace missing teeth.  
- **What to check:** Confirm the prosthesis is resin-bonded, not cemented traditionally, and verify the use of cast metal. Check the integrity of the bonding surfaces and adjacent teeth.  
- **Notes:** This is typically used for anterior or posterior single-tooth replacements. Ensure proper etching and bonding protocols are followed for resin adhesion. Not applicable for traditional cementation.

### Code: D6548  
**Heading:** retainer - porcelain/ceramic for resin bonded fixed prosthesis  
- **When to use:** When a porcelain or ceramic retainer is used in a resin-bonded fixed prosthesis.  
- **What to check:** Verify the material is porcelain/ceramic and the prosthesis is resin-bonded. Assess the esthetic requirements and strength of the bonding site.  
- **Notes:** Often chosen for anterior teeth due to esthetics. Requires careful handling to avoid chipping during bonding.

### Code: D6549  
**Heading:** resin retainer - for resin bonded fixed prosthesis  
- **When to use:** When a resin-based retainer is used in a resin-bonded fixed prosthesis.  
- **What to check:** Confirm the retainer is entirely resin-based and bonded, not cemented. Evaluate the durability needs of the site.  
- **Notes:** Less durable than metal or ceramic options; typically used for temporary or less stress-bearing areas.

### Code: D6600  
**Heading:** retainer inlay - porcelain/ceramic, two surfaces  
- **When to use:** For a porcelain/ceramic inlay retainer covering two surfaces in a fixed partial denture.  
- **What to check:** Ensure only two surfaces are involved and the material is porcelain/ceramic. Check for proper fit and occlusion.  
- **Notes:** Ideal for esthetic zones; verify no excessive occlusal forces that could fracture the ceramic.

### Code: D6601  
**Heading:** retainer inlay - porcelain/ceramic, three or more surfaces  
- **When to use:** When a porcelain/ceramic inlay retainer involves three or more surfaces.  
- **What to check:** Count the surfaces involved (three or more) and confirm porcelain/ceramic material. Assess marginal integrity.  
- **Notes:** More extensive than D6600; ensure patient understands esthetic and strength trade-offs.

### Code: D6602  
**Heading:** retainer inlay - cast high noble metal, two surfaces  
- **When to use:** For a cast high noble metal inlay retainer covering two surfaces.  
- **What to check:** Verify high noble metal (e.g., gold) and two-surface involvement. Check for patient metal tolerance.  
- **Notes:** High noble metals offer durability; suitable for posterior areas with higher chewing forces.

### Code: D6603  
**Heading:** retainer inlay - cast high noble metal, three or more surfaces  
- **When to use:** When a cast high noble metal inlay retainer spans three or more surfaces.  
- **What to check:** Confirm high noble metal and three or more surfaces. Evaluate occlusal load distribution.  
- **Notes:** More extensive restoration; excellent for longevity in high-stress areas.

### Code: D6604  
**Heading:** retainer inlay - cast predominantly base metal, two surfaces  
- **When to use:** For a base metal inlay retainer covering two surfaces.  
- **What to check:** Ensure predominantly base metal (e.g., nickel-chromium) and two surfaces. Screen for metal allergies.  
- **Notes:** Cost-effective but less biocompatible than noble metals; check patient history.

### Code: D6605  
**Heading:** retainer inlay - cast predominantly base metal, three or more surfaces  
- **When to use:** When a base metal inlay retainer involves three or more surfaces.  
- **What to check:** Verify base metal and three or more surfaces. Confirm fit and patient comfort.  
- **Notes:** Larger restoration; monitor for potential corrosion or sensitivity over time.

### Code: D6606  
**Heading:** retainer inlay - cast noble metal, two surfaces  
- **When to use:** For a noble metal inlay retainer covering two surfaces.  
- **What to check:** Confirm noble metal (e.g., palladium) and two surfaces. Assess occlusal stability.  
- **Notes:** Balances cost and durability; less gold content than high noble metals.

### Code: D6607  
**Heading:** retainer inlay - cast noble metal, three or more surfaces  
- **When to use:** When a noble metal inlay retainer spans three or more surfaces.  
- **What to check:** Verify noble metal and three or more surfaces. Check for proper seating.  
- **Notes:** Suitable for larger restorations with moderate stress; good longevity.

### Code: D6624  
**Heading:** retainer inlay - titanium  
- **When to use:** For a titanium inlay retainer in a fixed partial denture.  
- **What to check:** Confirm titanium material and surface involvement (not surface-specific). Evaluate biocompatibility.  
- **Notes:** Excellent for patients with metal allergies; lightweight and strong.

### Code: D6608  
**Heading:** retainer onlay - porcelain/ceramic, two surfaces  
- **When to use:** For a porcelain/ceramic onlay retainer covering two surfaces.  
- **What to check:** Ensure two surfaces and porcelain/ceramic material. Verify occlusal clearance.  
- **Notes:** Onlays cover cusps; esthetic but fragile under heavy loads.

### Code: D6609  
**Heading:** retainer onlay - porcelain/ceramic, three or more surfaces  
- **When to use:** When a porcelain/ceramic onlay retainer involves three or more surfaces.  
- **What to check:** Confirm three or more surfaces and porcelain/ceramic. Assess fracture risk.  
- **Notes:** More extensive than D6608; prioritize esthetics with caution for posterior use.

### Code: D6610  
**Heading:** retainer onlay - cast high noble metal, two surfaces  
- **When to use:** For a high noble metal onlay retainer covering two surfaces.  
- **What to check:** Verify high noble metal and two surfaces. Check occlusal harmony.  
- **Notes:** Durable and reliable for posterior teeth; high noble metal resists wear.

### Code: D6611  
**Heading:** retainer onlay - cast high noble metal, three or more surfaces  
- **When to use:** When a high noble metal onlay retainer spans three or more surfaces.  
- **What to check:** Confirm high noble metal and three or more surfaces. Ensure proper contours.  
- **Notes:** Extensive restoration; excellent for heavy occlusal demands.

### Code: D6612  
**Heading:** retainer onlay - cast predominantly base metal, two surfaces  
- **When to use:** For a base metal onlay retainer covering two surfaces.  
- **What to check:** Verify base metal and two surfaces. Screen for sensitivity.  
- **Notes:** Economical option; monitor for potential irritation.

### Code: D6613  
**Heading:** retainer onlay - cast predominantly base metal, three or more surfaces  
- **When to use:** When a base metal onlay retainer involves three or more surfaces.  
- **What to check:** Confirm base metal and three or more surfaces. Check fit and occlusion.  
- **Notes:** Larger restoration; cost-effective but less noble.

### Code: D6614  
**Heading:** retainer onlay - cast noble metal, two surfaces  
- **When to use:** For a noble metal onlay retainer covering two surfaces.  
- **What to check:** Verify noble metal and two surfaces. Assess durability needs.  
- **Notes:** Good middle-ground option for strength and cost.

### Code: D6615  
**Heading:** retainer onlay - cast noble metal, three or more surfaces  
- **When to use:** When a noble metal onlay retainer spans three or more surfaces.  
- **What to check:** Confirm noble metal and three or more surfaces. Ensure occlusal fit.  
- **Notes:** Reliable for larger restorations; balances cost and performance.

### Code: D6634  
**Heading:** retainer onlay - titanium  
- **When to use:** For a titanium onlay retainer in a fixed partial denture.  
- **What to check:** Verify titanium material and surface involvement (not surface-specific). Check biocompatibility.  
- **Notes:** Ideal for allergy-prone patients; strong and corrosion-resistant.

### Key Takeaways:
- **Material Matters:** Choose codes based on the specific material (e.g., porcelain, high noble metal, titanium) and ensure compatibility with patient needs.  
- **Surface Count:** Accurately count involved surfaces (two vs. three or more) to avoid over- or under-coding.  
- **Resin-Bonded vs. Traditional:** Distinguish between resin-bonded prostheses (D6545-D6549) and traditional retainers (D6600-D6634).  
- **Patient History:** Consider allergies, esthetic preferences, and occlusal demands when selecting materials.  
- **Occlusal Integrity:** Post-placement, always verify occlusion to prevent future complications.




Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_fixed_partial_denture_retainers_inlays_onlays_code(self, scenario: str) -> str:
        """Extract fixed partial denture retainers inlays onlays code(s) for a given scenario."""
        try:
            print(f"Analyzing fixed partial denture retainers inlays onlays scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Fixed partial denture retainers inlays onlays extract_fixed_partial_denture_retainers_inlays_onlays_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in fixed partial denture retainers inlays onlays code extraction: {str(e)}")
            return ""
    
    def activate_fixed_partial_denture_retainers_inlays_onlays(self, scenario: str) -> str:
        """Activate the fixed partial denture retainers inlays onlays analysis process and return results."""
        try:
            result = self.extract_fixed_partial_denture_retainers_inlays_onlays_code(scenario)
            if not result:
                print("No fixed partial denture retainers inlays onlays code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating fixed partial denture retainers inlays onlays analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_fixed_partial_denture_retainers_inlays_onlays(scenario)
        print(f"\n=== FIXED PARTIAL DENTURE RETAINERS INLAYS ONLAYS ANALYSIS RESULT ===")
        print(f"FIXED PARTIAL DENTURE RETAINERS INLAYS ONLAYS CODE: {result if result else 'None'}")

# Create and export service instance
fixed_partial_denture_retainers_inlays_onlays_service = FixedPartialDentureRetainersInlaysOnlaysServices()

# Example usage
if __name__ == "__main__":
    scenario = input("Enter a fixed partial denture retainers inlays onlays dental scenario: ")
    fixed_partial_denture_retainers_inlays_onlays_service.run_analysis(scenario) 