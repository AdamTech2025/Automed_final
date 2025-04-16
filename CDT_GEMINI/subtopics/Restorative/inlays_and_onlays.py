"""
Module for extracting inlays and onlays codes.
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

class InlaysAndOnlaysServices:
    """Class to analyze and extract inlays and onlays codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing inlays and onlays services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert 

**Before picking a code, ask:**
- What was the primary reason the patient came in?
- Is this an inlay or an onlay restoration?
- What material is being used—metallic, porcelain/ceramic, or resin-based composite?
- How many surfaces of the tooth are involved?
- Is the restoration necessary due to decay, fracture, or cosmetic concerns?

---

### **Inlay/Onlay Restorations Codes**

#### **D2510 – Inlay, metallic, one surface**
**Use when:** A single-surface metallic inlay is placed within the tooth's structure.  
**Check:** Confirm there is no cusp coverage and that the restoration fits within the occlusal surface.  
**Note:** Used primarily for small cavities where a full crown is unnecessary.

#### **D2520 – Inlay, metallic, two surfaces**
**Use when:** A two-surface metallic inlay is placed within the tooth.  
**Check:** Verify precise adaptation to both surfaces and proper occlusal contact.  
**Note:** Suitable for cases with slightly larger caries or fractures that do not require cuspal coverage.

#### **D2530 – Inlay, metallic, three or more surfaces**
**Use when:** A metallic inlay restoration involving three or more surfaces is required.  
**Check:** Ensure the restoration provides adequate function without compromising the remaining tooth structure.  
**Note:** This is for larger restorations that still preserve the cusps.

#### **D2542 – Onlay, metallic, two surfaces**
**Use when:** A two-surface metallic onlay is placed with cusp coverage.  
**Check:** Confirm occlusal contact and proper bonding to support the tooth structure.  
**Note:** Used when additional reinforcement of the cusps is required.

#### **D2543 – Onlay, metallic, three surfaces**
**Use when:** A three-surface metallic onlay provides additional strength to the tooth.  
**Check:** Ensure functional occlusion and proper adaptation to the underlying structure.  
**Note:** Often used in posterior teeth to prevent further structural damage.

#### **D2544 – Onlay, metallic, four or more surfaces**
**Use when:** A metallic onlay covers four or more surfaces, reinforcing extensive damage.  
**Check:** Ensure stability and balance in occlusion.  
**Note:** Ideal for cases where significant cuspal protection is needed.

#### **D2610 – Inlay, porcelain/ceramic, one surface**
**Use when:** A single-surface porcelain/ceramic inlay is used for aesthetic restorations.  
**Check:** Verify proper color match and fit.  
**Note:** Provides superior esthetics compared to metallic restorations.

#### **D2620 – Inlay, porcelain/ceramic, two surfaces**
**Use when:** A two-surface porcelain/ceramic inlay is required.  
**Check:** Ensure a seamless blend with the natural tooth structure.  
**Note:** Common in anterior and premolar restorations for aesthetic appeal.

#### **D2630 – Inlay, porcelain/ceramic, three or more surfaces**
**Use when:** A three-surface inlay is required to restore larger areas.  
**Check:** Confirm durability and marginal adaptation.  
**Note:** Used for larger defects where conservation of natural tooth structure is possible.

#### **D2642 – Onlay, porcelain/ceramic, two surfaces**
**Use when:** A two-surface porcelain/ceramic onlay restores and reinforces cusps.  
**Check:** Verify occlusion and shade matching.  
**Note:** Popular for aesthetic restoration of posterior teeth.

#### **D2643 – Onlay, porcelain/ceramic, three surfaces**
**Use when:** A three-surface porcelain/ceramic onlay is placed for additional coverage.  
**Check:** Ensure strong bonding and accurate occlusal function.  
**Note:** Designed for patients requiring both durability and cosmetic appeal.

#### **D2644 – Onlay, porcelain/ceramic, four or more surfaces**
**Use when:** A four-surface or more onlay is needed for extensive tooth restoration.  
**Check:** Evaluate fit and resistance to fracture.  
**Note:** Often chosen as an alternative to full crowns.

#### **D2650 – Inlay, resin-based composite, one surface**
**Use when:** A one-surface resin-based composite inlay is used for conservative restoration.  
**Check:** Confirm bond strength and adaptation to the tooth.  
**Note:** Preferred for patients seeking metal-free fillings.

#### **D2651 – Inlay, resin-based composite, two surfaces**
**Use when:** A two-surface resin-based composite inlay is placed.  
**Check:** Ensure marginal seal and shade compatibility.  
**Note:** Used in areas requiring moderate reconstruction.

#### **D2652 – Inlay, resin-based composite, three or more surfaces**
**Use when:** A three-surface or larger inlay is needed to restore extensive damage.  
**Check:** Confirm stability and resistance to occlusal forces.  
**Note:** Provides an alternative to porcelain restorations.

#### **D2662 – Onlay, resin-based composite, two surfaces**
**Use when:** A two-surface resin-based composite onlay restores cusps.  
**Check:** Assess occlusion and ensure proper adhesion.  
**Note:** Offers a conservative approach to cusp replacement.

#### **D2663 – Onlay, resin-based composite, three surfaces**
**Use when:** A three-surface resin-based composite onlay reinforces a weakened tooth.  
**Check:** Ensure even distribution of biting forces.  
**Note:** Good for patients preferring non-metallic restorations.

#### **D2664 – Onlay, resin-based composite, four or more surfaces**
**Use when:** A four-surface or more resin-based composite onlay is necessary.  
**Check:** Confirm proper adaptation and esthetic results.  
**Note:** Serves as an alternative to crowns when more tooth structure can be preserved.

---

### **Key Takeaways:**
- **Inlay vs. Onlay:** Inlays restore internal portions of the tooth, while onlays cover cusps.
- **Material Choice:** Metallic is durable, porcelain/ceramic offers esthetics, and resin-based composite provides flexibility.
- **Surface Coverage:** The number of surfaces restored determines the correct code selection.
- **Occlusion Considerations:** Ensure that occlusion is balanced to prevent post-treatment complications.
- **Patient Preferences:** Some patients may prefer non-metallic options for better aesthetics.

---

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_inlays_and_onlays_code(self, scenario: str) -> str:
        """Extract inlays and onlays code(s) for a given scenario."""
        try:
            print(f"Analyzing inlays and onlays scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Inlays and onlays extract_inlays_and_onlays_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in inlays and onlays code extraction: {str(e)}")
            return ""
    
    def activate_inlays_and_onlays(self, scenario: str) -> str:
        """Activate the inlays and onlays analysis process and return results."""
        try:
            result = self.extract_inlays_and_onlays_code(scenario)
            if not result:
                print("No inlays and onlays code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating inlays and onlays analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_inlays_and_onlays(scenario)
        print(f"\n=== INLAYS AND ONLAYS ANALYSIS RESULT ===")
        print(f"INLAYS AND ONLAYS CODE: {result if result else 'None'}")

# Example usage
if __name__ == "__main__":
    inlays_and_onlays_service = InlaysAndOnlaysServices()
    scenario = input("Enter an inlays and onlays dental scenario: ")
    inlays_and_onlays_service.run_analysis(scenario) 