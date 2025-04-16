"""
Module for extracting denture rebase procedures codes.
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

class DentureRebaseProceduresServices:
    """Class to analyze and extract denture rebase procedures codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing denture rebase procedures services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert

## Prosthodontics, Removable - Denture Rebase Procedures

### **Before picking a code, ask:**
- What was the primary reason the patient came in?
- Is the existing denture causing discomfort, poor fit, or instability?
- Is this a routine maintenance procedure or due to significant wear or damage?
- Does the patient require a full denture or partial denture rebase?
- Is the denture hybrid, requiring special base material replacement?

---

### **D5710 - Rebase Complete Maxillary Denture**
**Use when:** The base of a complete maxillary denture requires replacement while retaining the existing denture teeth.
**Check:** Ensure that the teeth are in good condition and can be retained.
**Notes:** This procedure is done when the base material has deteriorated, causing poor fit or irritation.

---

### **D5711 - Rebase Complete Mandibular Denture**
**Use when:** The patient needs a new base for their complete mandibular denture.
**Check:** Confirm stability and occlusion; evaluate the condition of remaining alveolar ridges.
**Notes:** Necessary when the base material is compromised due to resorption or wear, leading to instability.

---

### **D5720 - Rebase Maxillary Partial Denture**
**Use when:** The acrylic base of a maxillary partial denture requires full replacement.
**Check:** Assess framework and teeth to ensure they can be retained.
**Notes:** Often needed due to long-term wear or significant adaptation changes in the oral tissues.

---

### **D5721 - Rebase Mandibular Partial Denture**
**Use when:** The patient needs a new base for their mandibular partial denture while keeping existing teeth and framework.
**Check:** Ensure proper adaptation of the new base to the remaining structures.
**Notes:** Essential when the existing base has lost integrity, affecting retention and stability.

---

### **D5725 - Rebase Hybrid Prosthesis**
**Use when:** The base material of a hybrid prosthesis (implant-supported denture) needs replacement.
**Check:** Evaluate implant stability and ensure framework compatibility with new base material.
**Notes:** This procedure is used when the original base material deteriorates, leading to fit issues or patient discomfort.

---

### **Key Takeaways:**
- **Rebasing replaces the entire denture base while retaining existing teeth.**
- **Use when denture fit is compromised due to material degradation, tissue changes, or resorption.**
- **Ensure the teeth and framework are stable and functional before rebasing.**
- **Rebasing differs from relining, which only adds material to the existing base rather than replacing it.**
- **Hybrid prosthesis rebasing involves implant-supported restorations, requiring careful assessment.**

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_denture_rebase_procedures_code(self, scenario: str) -> str:
        """Extract denture rebase procedures code(s) for a given scenario."""
        try:
            print(f"Analyzing denture rebase procedures scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Denture rebase procedures extract_denture_rebase_procedures_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in denture rebase procedures code extraction: {str(e)}")
            return ""
    
    def activate_denture_rebase_procedures(self, scenario: str) -> str:
        """Activate the denture rebase procedures analysis process and return results."""
        try:
            result = self.extract_denture_rebase_procedures_code(scenario)
            if not result:
                print("No denture rebase procedures code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating denture rebase procedures analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_denture_rebase_procedures(scenario)
        print(f"\n=== DENTURE REBASE PROCEDURES ANALYSIS RESULT ===")
        print(f"DENTURE REBASE PROCEDURES CODE: {result if result else 'None'}")

# Example usage
if __name__ == "__main__":
    denture_rebase_procedures_service = DentureRebaseProceduresServices()
    scenario = input("Enter a denture rebase procedures dental scenario: ")
    denture_rebase_procedures_service.run_analysis(scenario) 