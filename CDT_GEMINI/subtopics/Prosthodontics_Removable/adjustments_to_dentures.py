"""
Module for extracting adjustments to dentures codes.
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

class AdjustmentsToDenturesServices:
    """Class to analyze and extract adjustments to dentures codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing adjustments to dentures services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert

## Prosthodontics, Removable - Adjustments to Dentures

### **Before picking a code, ask:**
- What was the primary reason the patient came in?
- Is this a new denture or an existing one needing adjustments?
- What specific issue is the patient experiencing (fit, function, breakage)?
- Is the adjustment related to occlusion, pressure sores, or retention issues?
- Does the denture require repair, replacement of components, or a complete remake?

---

### **D5410 - Adjust Complete Denture (Maxillary)**
**Use when:** A maxillary complete denture requires adjustment for fit, occlusion, or patient comfort.
**Check:** Look for pressure points, overextensions, and occlusal discrepancies.
**Notes:** Often needed after initial denture placement or due to tissue changes. Minor adjustments can greatly improve comfort and function.

---

### **D5411 - Adjust Complete Denture (Mandibular)**
**Use when:** A mandibular complete denture requires adjustment.
**Check:** Evaluate for areas of irritation, overextensions, or improper occlusion.
**Notes:** Mandibular dentures often require more frequent adjustments due to lower stability compared to maxillary dentures.

---

### **D5421 - Adjust Partial Denture (Maxillary)**
**Use when:** A maxillary partial denture needs minor adjustments for comfort or function.
**Check:** Inspect clasps, rests, and base extensions for proper fit.
**Notes:** Adjustments may involve relieving pressure points, improving retention, or modifying occlusion.

---

### **D5422 - Adjust Partial Denture (Mandibular)**
**Use when:** A mandibular partial denture requires fit or occlusal adjustments.
**Check:** Ensure clasps are not causing irritation, and check occlusion.
**Notes:** Adjustments may be necessary if the patient experiences discomfort due to shifting or pressure points.

---

### **D5511 - Repair Broken Complete Denture Base (Mandibular)**
**Use when:** A mandibular complete denture has a fractured base that needs repair.
**Check:** Confirm the extent of the damage and whether repair is feasible.
**Notes:** Repairs should restore function without compromising denture integrity. Consider relining if structural support is weakened.

---

### **D5512 - Repair Broken Complete Denture Base (Maxillary)**
**Use when:** A maxillary complete denture has a broken base that needs repair.
**Check:** Assess whether the breakage is due to poor fit, stress points, or patient mishandling.
**Notes:** If repeated breakages occur, a new denture may be needed rather than continued repairs.

---

### **D5520 - Replace Missing or Broken Teeth (Complete Denture, Each Tooth)**
**Use when:** One or more teeth on a complete denture are missing or fractured and need replacement.
**Check:** Ensure proper occlusion and fit after replacement.
**Notes:** If multiple teeth are missing or recurrent fractures occur, a new denture or reinforcement may be required.

---

### **Key Takeaways:**
- **Adjustments vs. Repairs:** Adjustments focus on fit and comfort, while repairs restore function after damage.
- **Denture Base vs. Teeth:** Repairing the base (D5511, D5512) differs from replacing teeth (D5520), which should be coded separately.
- **Assessment is Crucial:** Always determine the underlying cause of discomfort or breakage to provide long-term solutions.
- **Patient Education:** Educate patients on proper care and handling to minimize future issues.

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_adjustments_to_dentures_code(self, scenario: str) -> str:
        """Extract adjustments to dentures code(s) for a given scenario."""
        try:
            print(f"Analyzing adjustments to dentures scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Adjustments to dentures extract_adjustments_to_dentures_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in adjustments to dentures code extraction: {str(e)}")
            return ""
    
    def activate_adjustments_to_dentures(self, scenario: str) -> str:
        """Activate the adjustments to dentures analysis process and return results."""
        try:
            result = self.extract_adjustments_to_dentures_code(scenario)
            if not result:
                print("No adjustments to dentures code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating adjustments to dentures analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_adjustments_to_dentures(scenario)
        print(f"\n=== ADJUSTMENTS TO DENTURES ANALYSIS RESULT ===")
        print(f"ADJUSTMENTS TO DENTURES CODE: {result if result else 'None'}")

# Example usage
if __name__ == "__main__":
    adjustments_to_dentures_service = AdjustmentsToDenturesServices()
    scenario = input("Enter an adjustments to dentures dental scenario: ")
    adjustments_to_dentures_service.run_analysis(scenario) 