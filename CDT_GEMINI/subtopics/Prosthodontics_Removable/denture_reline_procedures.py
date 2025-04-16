"""
Module for extracting denture reline procedures codes.
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

class DentureRelineProceduresServices:
    """Class to analyze and extract denture reline procedures codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing denture reline procedures services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert

## Prosthodontics, Removable - Denture Reline Procedures

### **Before picking a code, ask:**
- What was the primary reason the patient came in?
- Is the reline being done directly in the mouth or indirectly in a lab?
- Is this a complete or partial denture?
- Is the denture maxillary or mandibular?
- Does the patient have any history of discomfort, instability, or changes in fit?

---

### **D5730 - Reline Complete Maxillary Denture (Direct)**
**Use when:** The patient requires a same-day reline of a complete maxillary denture using a chairside procedure.
**Check:** Ensure proper adaptation of the reline material intraorally. Evaluate occlusion and stability after reline.
**Notes:** Direct relines are performed in the dental office and typically provide immediate improvement in fit. Suitable for patients with minor adjustments needed.

---

### **D5731 - Reline Complete Mandibular Denture (Direct)**
**Use when:** A chairside reline is necessary for a mandibular complete denture.
**Check:** Confirm even distribution of reline material and ensure no excessive pressure points.
**Notes:** Direct relines allow quick results but may not last as long as lab-processed (indirect) relines. Ideal for patients needing a faster solution.

---

### **D5740 - Reline Maxillary Partial Denture (Direct)**
**Use when:** A maxillary partial denture needs an immediate in-office reline.
**Check:** Assess fit and occlusion after application of new liner.
**Notes:** Suitable for minor modifications where the patient experiences minor tissue changes affecting fit.

---

### **D5741 - Reline Mandibular Partial Denture (Direct)**
**Use when:** The patient's mandibular partial denture requires a same-day reline.
**Check:** Ensure adaptation of the material to soft tissue without causing pressure spots.
**Notes:** Provides a short-term solution for patients experiencing discomfort or looseness.

---

### **D5750 - Reline Complete Maxillary Denture (Indirect)**
**Use when:** A complete maxillary denture needs a lab-processed reline for better long-term stability.
**Check:** Take accurate impressions for the lab and verify occlusion before sending.
**Notes:** Indirect relines are more durable and precise compared to direct relines. Requires the patient to be without the denture while it is processed in the lab.

---

### **D5751 - Reline Complete Mandibular Denture (Indirect)**
**Use when:** A lab-processed reline is required for a mandibular complete denture.
**Check:** Ensure the impression captures accurate soft tissue adaptation before sending to the lab.
**Notes:** Indirect relines provide a better long-term fit and function compared to direct relines.

---

### **D5760 - Reline Maxillary Partial Denture (Indirect)**
**Use when:** A maxillary partial denture requires a laboratory-processed reline.
**Check:** Ensure a detailed impression is taken to create a precise adaptation to the patient's tissues.
**Notes:** Indirect relines improve longevity and are preferable for significant tissue or bone changes.

---

### **D5761 - Reline Mandibular Partial Denture (Indirect)**
**Use when:** A lab-based reline is required for a mandibular partial denture.
**Check:** Verify tissue adaptation and occlusion before final delivery.
**Notes:** Indirect relines require more time but result in better fit, durability, and comfort for the patient.

---

### **Key Takeaways:**
- **Direct vs. Indirect:** Direct relines are immediate, while indirect relines require lab processing but last longer.
- **Complete vs. Partial:** Ensure the correct code is selected based on whether the patient has a complete or partial denture.
- **Patient Education:** Explain the difference between direct and indirect relines to manage patient expectations.
- **Occlusion & Fit:** Always verify post-treatment occlusion to prevent bite imbalances.
- **Long-Term Adjustments:** Some relines may require further modifications as soft tissues continue to adapt.


Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_denture_reline_procedures_code(self, scenario: str) -> str:
        """Extract denture reline procedures code(s) for a given scenario."""
        try:
            print(f"Analyzing denture reline procedures scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Denture reline procedures extract_denture_reline_procedures_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in denture reline procedures code extraction: {str(e)}")
            return ""
    
    def activate_denture_reline_procedures(self, scenario: str) -> str:
        """Activate the denture reline procedures analysis process and return results."""
        try:
            result = self.extract_denture_reline_procedures_code(scenario)
            if not result:
                print("No denture reline procedures code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating denture reline procedures analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_denture_reline_procedures(scenario)
        print(f"\n=== DENTURE RELINE PROCEDURES ANALYSIS RESULT ===")
        print(f"DENTURE RELINE PROCEDURES CODE: {result if result else 'None'}")

# Example usage
if __name__ == "__main__":
    denture_reline_procedures_service = DentureRelineProceduresServices()
    scenario = input("Enter a denture reline procedures dental scenario: ")
    denture_reline_procedures_service.run_analysis(scenario) 