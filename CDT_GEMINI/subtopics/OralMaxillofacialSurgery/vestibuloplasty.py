"""
Module for extracting vestibuloplasty codes.
"""

import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from llm_services import LLMService, get_service, set_model, set_temperature

# Load environment variables
load_dotenv()

class VestibuloplastyServices:
    """Class to analyze and extract vestibuloplasty codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing vestibuloplasty scenarios."""
        from subtopics.prompt.prompt import PROMPT
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert specializing in oral and maxillofacial surgical procedures,

## **Vestibuloplasty Procedures**

### **Before picking a code, ask:**
- Is the procedure being performed for ridge extension via vestibuloplasty?
- Is the procedure limited to secondary epithelialization, or does it include soft tissue grafts and more extensive tissue management?
- What is the clinical indication for the vestibuloplasty (pre-prosthetic preparation, inadequate attached gingiva, etc.)?
- What specific arch and region are being treated (maxilla, mandible, anterior, posterior)?
- What is the extent of the vestibular deepening being performed?
- Does the procedure involve muscle repositioning, and if so, which specific muscles?
- Will the procedure include soft tissue grafting, and if so, what type of graft (free gingival, connective tissue, etc.)?
- Is management of hypertrophied or hyperplastic tissue required as part of the procedure?
- What is the planned method of surgical site coverage (surgical dressing, stent, etc.)?
- Is this being performed in preparation for a specific prosthetic plan?

---

#### **Code: D7340** – *Vestibuloplasty - ridge extension (secondary epithelialization)*
**Use when:** Performing a surgical procedure to increase relative alveolar ridge height by deepening the vestibular fornix and allowing the area to heal by secondary intention (epithelialization), without the use of soft tissue grafts.
**Check:** Documentation should specify the arch and region being treated, confirm that healing will be by secondary epithelialization without grafts, and detail the technique for vestibular extension.
**Note:** This procedure increases the relative height of the residual alveolar ridge by surgically lowering muscles and the floor of the vestibule. The detailed operative report should document the preoperative assessment of vestibular depth and attached gingiva, the clinical indication for vestibuloplasty, the specific surgical technique (often involving supraperiosteal dissection), management of muscle attachments, method of securing the depth of the newly created vestibule (suturing to periosteum, surgical stent), wound care instructions, and expected healing timeline. This technique relies on secondary epithelialization (granulation and epithelial migration) rather than primary closure or grafting, which affects post-operative management and healing time. Documentation should address plans for prosthetic treatment following adequate healing.

#### **Code: D7350** – *Vestibuloplasty - ridge extension (including soft tissue grafts, muscle reattachment, revision of soft tissue attachment and management of hypertrophied and hyperplastic tissue)*
**Use when:** Performing a more complex vestibuloplasty procedure that includes not only deepening of the vestibular fornix but also involves soft tissue grafting, muscle reattachment, revision of soft tissue attachments, and/or management of hypertrophied or hyperplastic tissues.
**Check:** Documentation must substantiate the complex nature of the procedure by detailing soft tissue grafting, muscle reattachment techniques, and/or management of hypertrophied tissue beyond simple vestibular extension.
**Note:** This more comprehensive procedure addresses multiple aspects of vestibular and ridge architecture. The extensive operative report should document the specific clinical indications requiring this level of intervention, the preoperative assessment of tissue condition (including muscle attachments and any hypertrophied/hyperplastic tissues), the surgical approach for vestibular extension, specific techniques for muscle repositioning and reattachment, the type and source of any soft tissue grafts utilized (free gingival, connective tissue, etc.), harvest technique if autogenous, preparation of the recipient site, graft stabilization method, management of any hypertrophied/hyperplastic tissues, use of surgical stents or dressings, and the comprehensive post-operative management protocol. Documentation should also address the anticipated timeline for prosthetic treatment following healing, as this procedure is often performed in preparation for removable or implant-supported prosthetics.

---

### **Key Takeaways:**
- **Procedural Complexity** - The key distinction between the two vestibuloplasty codes is the complexity of the procedure; D7340 involves secondary healing only, while D7350 includes grafting and more extensive tissue management.
- **Anatomical Documentation** - Precise documentation of the arch (maxilla or mandible) and regions treated (anterior, posterior, bilateral) is essential for complete procedural records.
- **Muscle Management** - For procedures involving muscle repositioning (particularly D7350), the specific muscles addressed and the technique for reattachment should be documented.
- **Graft Documentation** - When soft tissue grafts are utilized (D7350), the documentation should specify the type of graft material, source (autogenous or allogenic), dimensions, and stabilization technique.
- **Pre-Prosthetic Planning** - The relationship between the vestibuloplasty procedure and planned prosthetic rehabilitation should be documented, including the prosthetic benefit expected from increased ridge height.
- **Outcome Expectations** - Documentation should address the expected post-surgical ridge dimensions and how this relates to the prosthetic goals.
- **Post-Operative Protocols** - The method of maintaining the created vestibular depth during healing (stents, dressings, etc.) should be specified in the documentation.
- **Healing Timeline** - The anticipated healing timeline and follow-up schedule should be documented, acknowledging that secondary epithelialization (D7340) typically requires a longer healing period than grafting.
- **Tissue Management** - For code D7350, specific documentation of how hypertrophied or hyperplastic tissues were managed is important for justifying the more complex procedure code.
- **Clinical Illustrations** - Diagrams or photographs documenting pre- and post-operative conditions significantly strengthen the procedural record, particularly for demonstrating the extent of vestibular extension achieved.

Scenario:
"{{scenario}}"

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_vestibuloplasty_code(self, scenario: str) -> str:
        """Extract vestibuloplasty code for a given scenario."""
        try:
            print(f"Analyzing vestibuloplasty scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Vestibuloplasty extract code result: {code}")
            
            # Return empty string if no code found
            if code == "None" or not code or "not applicable" in code.lower():
                return ""
                
            return code
        except Exception as e:
            print(f"Error in extract_vestibuloplasty_code: {str(e)}")
            return ""
    
    def activate_vestibuloplasty(self, scenario: str) -> str:
        """Activate the vestibuloplasty analysis process and return results."""
        try:
            return self.extract_vestibuloplasty_code(scenario)
        except Exception as e:
            print(f"Error in activate_vestibuloplasty: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_vestibuloplasty(scenario)
        print(f"\n=== VESTIBULOPLASTY ANALYSIS RESULT ===")
        print(f"VESTIBULOPLASTY CODE: {result if result else 'None'}")


vestibuloplasty_service = VestibuloplastyServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a vestibuloplasty scenario: ")
    vestibuloplasty_service.run_analysis(scenario) 