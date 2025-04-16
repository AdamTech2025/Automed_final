"""
Module for extracting complicated suturing codes.
"""

import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from llm_services import LLMService, get_service, set_model, set_temperature

# Load environment variables
load_dotenv()

class ComplicatedSuturingServices:
    """Class to analyze and extract complicated suturing codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing complicated suturing scenarios."""
        from subtopics.prompt.prompt import PROMPT
        return PromptTemplate(
        template=f"""
You are a dental coding expert specializing in oral and maxillofacial surgery,

## **Complicated Suturing (Wounds, Lacerations)**

### **Before picking a code, ask:**
- What is the total length of the wound(s) being sutured (up to 5 cm or greater than 5 cm)?
- Is this a recent small wound or a complicated wound requiring advanced closure techniques?
- Does the wound involve multiple tissue layers requiring separate closure techniques?
- Was extensive tissue mobilization required to achieve primary closure?
- Is this a traumatic wound or a surgical incision?
- Are there anatomical factors that increase the complexity of wound closure?
- Does the location of the wound present accessibility challenges for suturing?
- Are there patient factors (age, medical conditions) that complicate the closure?
- Was specialized suture material or technique required due to wound characteristics?
- Does the documentation specifically describe the extensive soft tissue work required?

---

#### **Code: D7910** – *Suture of recent small wounds up to 5 cm*
**Use when:** Closing recent traumatic wounds measuring up to 5 cm in total length where more than simple interrupted sutures are required, but the closure doesn't meet the criteria for "complicated" suturing.
**Check:** Documentation should specify that this is a traumatic wound (not a surgical incision), the measured length in centimeters, and that the closure required more elaborate suturing than basic interrupted sutures.
**Note:** This code applies to wounds resulting from trauma that require prompt closure but don't involve the extensive tissue manipulation characteristic of complicated sutures. The procedural documentation should include the wound's etiology, dimensions (length, width, depth), location, suturing technique employed, suture material used, and whether any debridement was necessary prior to closure. This code is not appropriate for routine closure of surgical incisions, which is included in the surgical procedure code itself.

#### **Code: D7911** – *Complicated suture - up to 5 cm*
**Use when:** Performing closure of traumatic wounds up to 5 cm in total length that require extensive soft tissue mobilization and isolation to achieve primary closure due to wound characteristics, location, or tissue loss.
**Check:** Documentation must specifically detail the complicated nature of the closure, including the extensive tissue manipulation required, and clearly state that the total wound length does not exceed 5 cm.
**Note:** The "complicated" designation requires explicit documentation of factors that elevate the procedure beyond routine suturing. These might include irregular wound edges requiring debridement, undermining or advancement of adjacent tissues, layered closure of multiple tissue planes, proximity to vital structures requiring special consideration, or anatomically challenging locations. The operative note should provide a detailed description of the specific mobilization techniques employed, any regional anatomical challenges, and why standard closure methods were insufficient. This code is not to be used for closure of planned surgical incisions.

#### **Code: D7912** – *Complicated suture - greater than 5 cm*
**Use when:** Closing traumatic wounds that exceed 5 cm in total length where extensive soft tissue mobilization and isolation techniques are required to achieve primary closure due to wound characteristics, loss of tissue, or difficult location.
**Check:** Documentation must specifically measure and record the wound length as greater than 5 cm and detail the extensive tissue manipulation and advanced techniques required for closure.
**Note:** This code represents the highest level of traumatic wound closure in dental practice. The procedure documentation should comprehensively describe the complexity factors, including the specific mobilization techniques employed, layered closure methodology if used, management of anatomical structures in proximity to the wound, and justification for the extensive approach. For wounds with multiple components, the total cumulative length should be calculated and documented. As with other suturing codes, this applies only to traumatic wounds, not to planned surgical incisions. Photographic documentation is particularly valuable for these complex cases.

---

### **Key Takeaways:**
- **Traumatic Origin Requirement** - These codes apply exclusively to traumatic wounds, not to planned surgical incisions whose closure is included in the surgical procedure code.
- **Length Measurement** - Precise documentation of wound length in centimeters is critical, with 5 cm being the key threshold between codes D7911 and D7912.
- **Complexity Documentation** - For "complicated" suture codes (D7911, D7912), documentation must explicitly detail the extensive tissue mobilization and manipulation required.
- **Wound Characteristics** - Factors that may justify "complicated" designation include irregular edges, multiple tissue layers, tissue loss requiring advancement techniques, or anatomically challenging locations.
- **Multiple Wounds** - When multiple wounds are present, the cumulative length of all wounds should be documented and considered in code selection.
- **Technique Description** - Documentation should specifically describe the suturing techniques used, including any layered closure, tissue undermining, or advancement procedures.
- **Anatomical Considerations** - Special attention to anatomical structures (nerves, vessels, ducts) should be documented when they influence the closure approach.
- **Material Specification** - The type and size of suture materials used should be documented, as specialized materials may support the complexity of the case.
- **Photographic Evidence** - Pre- and post-closure photographs significantly strengthen documentation for complex cases.
- **Clear Distinction** - Clear documentation should distinguish between "more than simple interrupted sutures" (D7910) and "extensive mobilization and isolation of soft tissues" (D7911/D7912).

Scenario:
"{{scenario}}"

{PROMPT}
""",
            input_variables=["scenario"]
    )

    def extract_complicated_suturing_code(self, scenario: str) -> str:
        """Extract complicated suturing code for a given scenario."""
        try:
            print(f"Analyzing complicated suturing scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Complicated suturing extract code result: {code}")
            
            # Return empty string if no code found
            if code == "None" or not code or "not applicable" in code.lower():
                return ""
                
            return code
        except Exception as e:
            print(f"Error in extract_complicated_suturing_code: {str(e)}")
            return ""

    def activate_complicated_suturing(self, scenario: str) -> str:
        """Activate the complicated suturing analysis process and return results."""
        try:
            return self.extract_complicated_suturing_code(scenario)
        except Exception as e:
            print(f"Error in activate_complicated_suturing: {str(e)}")
            return "" 
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_complicated_suturing(scenario)
        print(f"\n=== COMPLICATED SUTURING ANALYSIS RESULT ===")
        print(f"COMPLICATED SUTURING CODE: {result if result else 'None'}")


complicated_suturing_service = ComplicatedSuturingServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a complicated suturing scenario: ")
    complicated_suturing_service.run_analysis(scenario) 