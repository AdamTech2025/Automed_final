"""
Module for extracting complete dentures codes.
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

class CompleteDenturesServices:
    """Class to analyze and extract complete dentures codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing complete dentures services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert

## Prosthodontics, Removable - Complete Dentures & Routine Post-Delivery Care

### **Before picking a code, ask:**
- What was the primary reason the patient came in?
- Is this an initial placement or a follow-up?
- Does the code cover future procedures like rebasing or relining?
- Is the patient receiving the denture immediately after extractions or after healing?
- Are there any complicating factors such as residual ridge resorption or anatomical challenges?

---

### **Code: D5110 - Complete Denture (Maxillary)**
**Use when:** The patient is receiving a complete maxillary denture for the first time.
**Check:** Ensure the treatment includes a full upper denture covering the maxillary arch.
**Notes:** This code includes the fabrication and placement of the denture, but does not cover additional procedures like relining or rebasing later. Patient expectations regarding fit, comfort, and adjustment period should be managed.

---

### **Code: D5120 - Complete Denture (Mandibular)**
**Use when:** The patient is receiving a complete mandibular denture for the first time.
**Check:** Verify that the denture is a full prosthesis for the lower arch.
**Notes:** Covers the creation and fitting of the denture but does not include future modifications such as relining or rebasing. Mandibular dentures often require additional considerations due to lower ridge resorption and stability concerns.

---

### **Code: D5130 - Immediate Denture (Maxillary)**
**Use when:** The patient is receiving an immediate maxillary denture following extractions.
**Check:** Ensure the denture is placed immediately after extractions for proper healing support.
**Notes:** Includes limited follow-up care but **does not** cover future rebasing or relining procedures. Immediate dentures may require significant adjustments as healing progresses and should be relined or replaced within a few months.

---

### **Code: D5140 - Immediate Denture (Mandibular)**
**Use when:** The patient is receiving an immediate mandibular denture following extractions.
**Check:** Verify that the denture is placed right after the removal of teeth.
**Notes:** Includes limited follow-up care but **does not** include future rebasing or relining. Patients should be advised that healing may cause changes in fit and function, requiring additional procedures later.

---

### **Additional Considerations for Denture Patients:**
- **Adjustment Period:** Patients need time to adapt to new dentures, and multiple adjustments may be required.
- **Occlusion and Fit:** Proper occlusion must be assessed to avoid discomfort and TMJ issues.
- **Oral Hygiene:** Patients should be instructed on proper cleaning techniques to avoid infections like denture stomatitis.
- **Follow-Up Care:** Regular follow-ups are essential to monitor fit and function, particularly for immediate dentures.
- **Long-Term Maintenance:** Relining or rebasing is often necessary within a few years due to bone resorption.
- **Patient Expectations:** Clear communication about the limitations and adaptation process can improve satisfaction and compliance.

---

### **Key Takeaways:**
- **Complete dentures (D5110, D5120)** are for fully edentulous arches and do not include future adjustments.
- **Immediate dentures (D5130, D5140)** are placed right after extractions and include only **limited** follow-up care.
- **Future modifications like relining/rebasing** require additional codes and are **not** included under these codes.
- **Patient education and realistic expectations** play a crucial role in successful prosthodontic treatment.

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_complete_dentures_code(self, scenario: str) -> str:
        """Extract complete dentures code(s) for a given scenario."""
        try:
            print(f"Analyzing complete dentures scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Complete dentures extract_complete_dentures_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in complete dentures code extraction: {str(e)}")
            return ""
    
    def activate_complete_dentures(self, scenario: str) -> str:
        """Activate the complete dentures analysis process and return results."""
        try:
            result = self.extract_complete_dentures_code(scenario)
            if not result:
                print("No complete dentures code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating complete dentures analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_complete_dentures(scenario)
        print(f"\n=== COMPLETE DENTURES ANALYSIS RESULT ===")
        print(f"COMPLETE DENTURES CODE: {result if result else 'None'}")

# Example usage
if __name__ == "__main__":
    complete_dentures_service = CompleteDenturesServices()
    scenario = input("Enter a complete dentures dental scenario: ")
    complete_dentures_service.run_analysis(scenario) 