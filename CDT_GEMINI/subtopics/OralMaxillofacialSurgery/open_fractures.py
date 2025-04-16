"""
Module for extracting open fractures codes.
"""

import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from llm_services import LLMService, get_service, set_model, set_temperature

# Load environment variables
load_dotenv()

class OpenFracturesServices:
    """Class to analyze and extract open fractures codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing open fractures scenarios."""
        from subtopics.prompt.prompt import PROMPT
        return PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert specializing in oral and maxillofacial trauma management,

## **Open Fractures Treatment**

### **Before picking a code, ask:**
- Which specific anatomical structure is involved in the fracture (maxilla, mandible, malar, zygomatic arch, alveolus)?
- Is an open or closed reduction technique being used for treatment?
- Are teeth present in the fracture line that require immobilization?
- What type of fixation is being used (internal or external)?
- Is the fracture simple, comminuted, or complex?
- Are multiple surgical approaches required for adequate reduction and fixation?
- Does the fracture involve facial bones requiring special consideration?
- What imaging was used to characterize the fracture before treatment?
- Are there any neurovascular considerations in the fracture management?
- What is the plan for post-operative stabilization and monitoring?

---

#### D7710 - Maxilla - Open Reduction  
**When to Use:** Apply this code for open reduction of a maxillary open fracture, where an incision is required to access and reduce the fracture.  
**What to Check:** Confirm the fracture is open (exposed to the mouth or externally) and verify the use of an incision for reduction.  
**Notes:** This code is specific to surgical intervention; if no incision is made, use D7720. Documentation should specify the fracture's exposure and surgical approach.  

#### D7720 - Maxilla - Closed Reduction  
**When to Use:** Use for closed reduction of a maxillary open fracture, where no incision is needed to reduce the fracture.  
**What to Check:** Ensure the fracture is open but treated non-surgically, without an incision.  
**Notes:** If an incision is required, switch to D7710. This code reflects a less invasive approach despite the open fracture classification.  

#### D7730 - Mandible - Open Reduction  
**When to Use:** Select this code for open reduction of a mandibular open fracture, requiring an incision to reduce the fracture.  
**What to Check:** Verify the fracture's exposure (to the mouth or externally) and confirm the use of an incision for reduction.  
**Notes:** Distinct from D7740 (closed reduction). Documentation must detail the surgical method and fracture characteristics.  

#### D7740 - Mandible - Closed Reduction  
**When to Use:** Apply when treating a mandibular open fracture with closed reduction, without an incision.  
**What to Check:** Confirm the fracture is open but managed non-surgically, with no incision involved.  
**Notes:** Use D7730 if an incision is made. This code focuses on a simpler reduction method for an open fracture.  

#### D7750 - Malar and/or Zygomatic Arch - Open Reduction  
**When to Use:** Use this code for open reduction of an open fracture in the malar (cheekbone) or zygomatic arch, requiring an incision.  
**What to Check:** Ensure the fracture is open and verify that an incision was made to reduce it in the malar or zygomatic region.  
**Notes:** Teeth are not typically involved. Documentation should highlight the surgical approach and fracture exposure.  

#### D7760 - Malar and/or Zygomatic Arch - Closed Reduction  
**When to Use:** Select for closed reduction of an open fracture in the malar or zygomatic arch, where no incision is required.  
**What to Check:** Confirm the fracture is open but treated non-surgically, without an incision.  
**Notes:** If an incision is used, switch to D7750. This code emphasizes a non-invasive reduction for an open fracture.  

#### D7770 - Alveolus - Open Reduction Stabilization of Teeth  
**When to Use:** Apply this code for open reduction of an alveolar open fracture, requiring an incision, with stabilization of teeth.  
**What to Check:** Verify the fracture is exposed (to the mouth or externally), an incision is made, and teeth are stabilized (e.g., wiring, banding, splinting).  
**Notes:** This differs from D7771 due to the surgical approach. Documentation must support tooth stabilization and the open fracture's nature.  

#### D7771 - Alveolus - Closed Reduction Stabilization of Teeth  
**When to Use:** Use for closed reduction of an alveolar open fracture, with stabilization of teeth, without an incision.  
**What to Check:** Confirm the fracture is open (exposed to the mouth or externally) and teeth are stabilized, with no incision required.  
**Notes:** If an incision is involved, use D7770. Focus is on non-surgical reduction with tooth stabilization as needed.  

#### D7780 - Facial Bones - Complicated Reduction with Fixation and Multiple Approaches  
**When to Use:** Select this code for complex open fractures of facial bones (e.g., jaws, cheeks, orbital bones) requiring complicated reduction, fixation, and multiple surgical approaches.  
**What to Check:** Verify involvement of multiple facial bones, the need for extensive fixation, and the use of multiple incisions or approaches for an open fracture.  
**Notes:** This code is for highly complex cases. Detailed narrative documentation is essential to justify the procedure's scope and complexity.  


---

### **Key Takeaways:**
- **Open vs. Closed Technique** - The primary distinction between code pairs is whether direct surgical exposure of the fracture site was performed (open) or whether treatment was accomplished without visualizing the fracture line (closed).
- **Anatomical Specificity** - Proper code selection requires identifying the exact anatomical structure(s) involved (maxilla, mandible, malar, zygomatic arch, alveolus).
- **Tooth Involvement** - When teeth are present in the fracture line, documentation should address their management and role in stabilization.
- **Fixation Method** - The type of fixation used (plates, screws, wires, arch bars, intermaxillary fixation) should be specifically documented.
- **Occlusal Verification** - For fractures affecting tooth-bearing areas, documentation should confirm restoration of proper occlusal relationships.
- **Multiple Approaches** - For code D7680, documentation must support the need for multiple surgical approaches to address the complex fracture pattern.
- **Radiographic Correlation** - References to pre- and post-operative imaging that guided treatment and confirmed reduction strengthen documentation.
- **Functional Assessment** - Post-reduction evaluation of function (occlusion, mandibular movement, sensation) should be included in documentation.
- **Healing Plan** - Documentation should address the stabilization period, follow-up protocol, and plan for hardware or fixation removal.
- **Complication Management** - For complex cases, documentation should address potential complications and monitoring strategy.

Scenario:
"{{scenario}}"

{PROMPT}
""",
            input_variables=["scenario"]
    )

    def extract_open_fractures_code(self, scenario: str) -> str:
        """Extract open fractures code for a given scenario."""
        try:
            print(f"Analyzing open fractures scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Open fractures extract code result: {code}")
            
            # Return empty string if no code found
            if code == "None" or not code or "not applicable" in code.lower():
                return ""
                
            return code
        except Exception as e:
            print(f"Error in extract_open_fractures_code: {str(e)}")
            return ""

    def activate_open_fractures(self, scenario: str) -> str:
        """Activate the open fractures analysis process and return results."""
        try:
            return self.extract_open_fractures_code(scenario)
        except Exception as e:
            print(f"Error in activate_open_fractures: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_open_fractures(scenario)
        print(f"\n=== OPEN FRACTURES ANALYSIS RESULT ===")
        print(f"OPEN FRACTURES CODE: {result if result else 'None'}")


open_fractures_service = OpenFracturesServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter an open fractures scenario: ")
    open_fractures_service.run_analysis(scenario) 