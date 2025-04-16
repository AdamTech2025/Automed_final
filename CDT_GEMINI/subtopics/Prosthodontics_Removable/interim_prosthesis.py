"""
Module for extracting interim prosthesis codes.
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

class InterimProsthesisServices:
    """Class to analyze and extract interim prosthesis codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing interim prosthesis services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert
### **Before picking a code, ask:**
- What was the primary reason the patient came in?
- Is the interim prosthesis needed for healing, aesthetics, or function?
- Is this a complete or partial denture?
- Is the denture maxillary or mandibular?
- Will the patient require a definitive prosthesis later?

#### Code: D5810  
**Heading:** Interim complete denture (maxillary)  
**When to Use:**  
- The patient requires a **temporary full upper denture** during the healing phase after extractions or surgery.  
- Planned use is **prior to delivery of a final maxillary complete denture**.  
- Useful when immediate esthetics, function, or tissue conditioning is needed before definitive treatment.  
**What to Check:**  
- Ensure the denture is truly **interim**, not final.  
- Verify extractions or surgeries have recently occurred or are planned.  
- Check the patient's healing progress and estimated timeline for final prosthesis.  
- Document the treatment plan including final prosthesis intent.  
**Notes:**  
- This is typically **not covered** as a "final prosthesis" by insurance — emphasize it is **transitional**.  
- May require a narrative stating the **reason for interim use** (e.g., surgical healing, bone remodeling).  
- Final denture fabrication should be coded separately (e.g., D5110).

---

#### Code: D5811  
**Heading:** Interim complete denture (mandibular)  
**When to Use:**  
- The patient needs a **temporary full lower denture** for use during the healing phase before receiving a definitive mandibular prosthesis.  
- Often used after full arch extractions or for tissue conditioning.  
**What to Check:**  
- Confirm the denture is **not the final prosthesis**.  
- Ensure a treatment plan exists for a final denture (e.g., D5120).  
- Evaluate healing needs or surgical conditions (e.g., bone grafting, implant planning).  
**Notes:**  
- This interim code helps with function and esthetics **during soft tissue or bony healing**.  
- A clear **transition plan to a permanent solution** should be documented.  
- Like D5810, insurance may request a narrative or deny duplicate prosthesis codes.

---

#### Code: D5820  
**Heading:** Interim partial denture (maxillary)  
**When to Use:**  
- Use when the patient needs a **temporary upper partial denture** to replace missing teeth during the healing phase.  
- Often used post-extraction, post-trauma, or during implant healing to maintain function/esthetics.  
**What to Check:**  
- Confirm it is **interim** and not definitive (D5213 is the definitive counterpart).  
- Verify extractions, implants, or ridge healing is part of the overall treatment plan.  
- Evaluate the need for immediate replacement of anterior teeth for appearance/social function.  
**Notes:**  
- Insurance plans often **limit coverage** to one prosthesis every 5+ years—narrative needed for interim approval.  
- Useful for temporary occlusal support, esthetics, or space maintenance during complex treatment.

---

#### Code: D5821  
**Heading:** Interim partial denture (mandibular)  
**When to Use:**  
- Applied when the patient requires a **temporary lower partial denture** during a healing or transition phase.  
- Common in cases of recent extractions, trauma, or implant preparation.  
**What to Check:**  
- Ensure the patient is **not receiving a final prosthesis** yet.  
- Confirm that tooth/arch condition is in transition (e.g., bone graft healing, socket healing, etc.).  
- Identify and document which teeth are being temporarily replaced.  
**Notes:**  
- This is **not a definitive partial denture**—plan and document for final prosthetic restoration.  
- Reimbursement may require documentation showing why the patient can't receive final treatment immediately.
### **Key Takeaways:**
- **Temporary Solution:** Interim prostheses are not meant for long-term use but aid in function, aesthetics, and healing.  
- **Patient Education:** Clearly explain that adjustments may be required as the tissues heal.  
- **Retention & Stability:** Check for proper retention and occlusion to minimize patient discomfort.  
- **Transition to Definitive Prosthesis:** Ensure a plan is in place for the final prosthetic solution once healing is complete.  


Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_interim_prosthesis_code(self, scenario: str) -> str:
        """Extract interim prosthesis code(s) for a given scenario."""
        try:
            print(f"Analyzing interim prosthesis scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Interim prosthesis extract_interim_prosthesis_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in interim prosthesis code extraction: {str(e)}")
            return ""
    
    def activate_interim_prosthesis(self, scenario: str) -> str:
        """Activate the interim prosthesis analysis process and return results."""
        try:
            result = self.extract_interim_prosthesis_code(scenario)
            if not result:
                print("No interim prosthesis code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating interim prosthesis analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_interim_prosthesis(scenario)
        print(f"\n=== INTERIM PROSTHESIS ANALYSIS RESULT ===")
        print(f"INTERIM PROSTHESIS CODE: {result if result else 'None'}")

# Example usage
if __name__ == "__main__":
    interim_prosthesis_service = InterimProsthesisServices()
    scenario = input("Enter an interim prosthesis dental scenario: ")
    interim_prosthesis_service.run_analysis(scenario) 