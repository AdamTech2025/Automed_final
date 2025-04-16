"""
Module for extracting repairs to complete dentures codes.
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

class RepairsToCompleteDenturesServices:
    """Class to analyze and extract repairs to complete dentures codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing repairs to complete dentures services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert

## Prosthodontics, Removable - Repairs to Complete Dentures

### **Before picking a code, ask:**
- What was the primary reason the patient came in?
- Is this a repair to an existing denture or a replacement of a broken/missing component?
- Does the patient need an immediate fix, or will further adjustments be required?
- Has the patient experienced frequent breakage, indicating a need for a stronger material or alternative approach?

---

### **D5511 - Repair Broken Complete Denture Base, Mandibular**
**Use when:** The mandibular (lower) complete denture base is fractured and requires repair.
**Check:** Assess the extent of the damage and determine if repair is feasible. Ensure proper bonding of repair material.
**Notes:** Not to be used for a full denture replacement. Structural reinforcement may be needed for recurrent fractures.

---

### **D5512 - Repair Broken Complete Denture Base, Maxillary**
**Use when:** The maxillary (upper) complete denture base is fractured and requires repair.
**Check:** Evaluate the fit post-repair to ensure proper occlusion and comfort.
**Notes:** Similar to D5511, but specific to the upper arch. Ensure patient follows appropriate care to prevent future fractures.

---

### **D5520 - Replace Missing or Broken Teeth — Complete Denture (Each Tooth)**
**Use when:** One or more teeth on a complete denture have broken or fallen off and need replacement.
**Check:** Verify the correct shade and size for replacement teeth. Ensure proper alignment and occlusion.
**Notes:** This code applies per missing or broken tooth. If multiple teeth need replacement, consider alternative treatment options.

---

### **Key Takeaways:**
- **Assess Damage Extent:** Minor cracks can often be repaired, but extensive fractures may require new dentures.
- **Material Considerations:** Some repairs may require stronger materials or reinforcement to prevent recurrent damage.
- **Patient Compliance:** Educate patients on proper denture care to minimize future breakage.
- **Check Fit Post-Repair:** Always verify that repaired dentures fit properly to avoid irritation or occlusal issues.

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_repairs_to_complete_dentures_code(self, scenario: str) -> str:
        """Extract repairs to complete dentures code(s) for a given scenario."""
        try:
            print(f"Analyzing repairs to complete dentures scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Repairs to complete dentures extract_repairs_to_complete_dentures_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in repairs to complete dentures code extraction: {str(e)}")
            return ""
    
    def activate_repairs_to_complete_dentures(self, scenario: str) -> str:
        """Activate the repairs to complete dentures analysis process and return results."""
        try:
            result = self.extract_repairs_to_complete_dentures_code(scenario)
            if not result:
                print("No repairs to complete dentures code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating repairs to complete dentures analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_repairs_to_complete_dentures(scenario)
        print(f"\n=== REPAIRS TO COMPLETE DENTURES ANALYSIS RESULT ===")
        print(f"REPAIRS TO COMPLETE DENTURES CODE: {result if result else 'None'}")

# Example usage
if __name__ == "__main__":
    repairs_to_complete_dentures_service = RepairsToCompleteDenturesServices()
    scenario = input("Enter a repairs to complete dentures dental scenario: ")
    repairs_to_complete_dentures_service.run_analysis(scenario) 