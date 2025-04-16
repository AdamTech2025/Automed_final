"""
Module for extracting traumatic wounds codes.
"""

import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from llm_services import LLMService, get_service, set_model, set_temperature

# Load environment variables
load_dotenv()

class TraumaticWoundsServices:
    """Class to analyze and extract traumatic wounds codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing traumatic wounds scenarios."""
        from subtopics.prompt.prompt import PROMPT
        return PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert specializing in treatment of traumatic wounds in the oral cavity,

## **Traumatic Wound Procedures**

### **Before picking a code, ask:**
- What is the length of the wound requiring closure?
- Is this a simple or complicated suturing case?
- Are there multiple tissue layers involved in the wound?
- Are there neurovascular structures involved that require special attention?
- Is the wound recent (acute) or older (delayed closure)?
- What anatomical location is the traumatic wound (intraoral, facial, etc.)?
- Does the wound extend beyond the oral cavity into facial structures?
- Was the wound a result of trauma or is it an iatrogenic (surgical) wound?
- Are there complicating factors such as infection or foreign bodies?
- Will specialized closure techniques be required beyond simple interrupted sutures?

---

#### **Code: D7910** – *Suture of recent small wounds up to 5 cm*
**Use when:** Performing simple closure of recent traumatic wounds in or around the oral cavity that measure up to 5 cm in length.
**Check:** Verify that the injury was traumatic in nature (not a surgical incision) and required suturing as an emergency or unplanned procedure.
**Note:** This code is intended for relatively straightforward closures of recent traumatic wounds using standard suturing techniques. It typically involves single-layer closure with simple interrupted or continuous sutures. Documentation should include wound length, location, suture material used, and closure technique. Photographs are highly recommended for trauma cases to document the extent of the original injury.

#### **Code: D7911** – *Complicated suture - up to 5 cm*
**Use when:** Closing traumatic wounds up to 5 cm that involve complex tissue structures requiring layered closure, careful dissection, or specialized techniques.
**Check:** Documentation must clearly substantiate the complexity factors that distinguish this from simple suturing, such as involvement of deeper tissue layers, proximity to nerves or vessels, wounds with irregular edges, or those requiring tension-reduction techniques.
**Note:** The complexity that justifies this code over D7910 must be clearly documented. This may include debridement of necrotic tissue, management of specialized structures (salivary ducts, nerve branches), or requiring layered closure techniques. The procedure typically takes significantly longer than simple suturing due to the careful attention needed for optimal functional and aesthetic results. The operative notes should explicitly detail why standard closure techniques were insufficient for this particular wound.

#### **Code: D7912** – *Complicated suture - greater than 5 cm*
**Use when:** Performing complex wound closure for traumatic injuries exceeding 5 cm in length that involve multiple tissue layers, delicate anatomical structures, or challenging wound geography.
**Check:** The documentation must include precise wound measurements exceeding 5 cm, detailed description of the wound complexity, and specific techniques employed for closure that reflect the complicated nature of the repair.
**Note:** This code represents the highest level of traumatic wound management in the dental setting. These cases often involve extensive facial or intraoral lacerations with multiple components. The procedure typically requires significant time, specialized suture materials, and advanced closure techniques. Detailed documentation should include the total wound length (cumulative if multiple wounds), anatomical structures involved, layer-by-layer closure description, and any additional stabilization required. Post-operative care instructions and follow-up plans are particularly important for these complex cases.

---

### **Key Takeaways:**
- **Emergency Nature** - These codes are specifically for traumatic wounds requiring immediate or urgent attention, not planned surgical incisions.
- **Measurement Matters** - Accurate documentation of wound length (in centimeters) is critical for proper code selection, with 5 cm being the key threshold.
- **Complexity Factors** - Justification for "complicated" suture codes must include specific factors beyond wound length, such as depth, tissue types involved, or proximity to critical structures.
- **Photographic Documentation** - Pre-suturing photos significantly strengthen documentation and can help justify code selection, especially for complicated repairs.
- **Anatomical Considerations** - Different areas of the oral cavity and face present unique suturing challenges that may influence complexity determination.
- **Layer-by-Layer Description** - For complicated sutures, document each tissue layer closed and the specific suturing technique used for each.
- **Materials Matter** - Documentation should specify suture materials and sizes used, as these often reflect the complexity of the repair.
- **Timing Context** - Note when the injury occurred relative to the repair, as delayed closure may increase complexity.
- **Follow-up Planning** - Document the planned suture removal timing and any intermediate evaluations needed for complicated wounds.
- **Surgical vs. Traumatic** - These codes are not used for closing planned surgical incisions; they are exclusively for traumatic wounds.

Scenario:
"{{scenario}}"

{PROMPT}
""",
            input_variables=["scenario"]
    )

    def extract_traumatic_wounds_code(self, scenario: str) -> str:
        """Extract traumatic wounds code for a given scenario."""
        try:
            print(f"Analyzing traumatic wounds scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Traumatic wounds extract code result: {code}")
            
            # Return empty string if no code found
            if code == "None" or not code or "not applicable" in code.lower():
                return ""
                
            return code
        except Exception as e:
            print(f"Error in extract_traumatic_wounds_code: {str(e)}")
            return ""

    def activate_traumatic_wounds(self, scenario: str) -> str:
        """Activate the traumatic wounds analysis process and return results."""
        try:
            return self.extract_traumatic_wounds_code(scenario)
        except Exception as e:
            print(f"Error in activate_traumatic_wounds: {str(e)}")
            return ""

    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_traumatic_wounds(scenario)
        print(f"\n=== TRAUMATIC WOUNDS ANALYSIS RESULT ===")
        print(f"TRAUMATIC WOUNDS CODE: {result if result else 'None'}")


traumatic_wounds_service = TraumaticWoundsServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a traumatic wounds scenario: ")
    traumatic_wounds_service.run_analysis(scenario) 