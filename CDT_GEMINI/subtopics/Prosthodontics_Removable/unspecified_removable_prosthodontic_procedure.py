"""
Module for extracting unspecified removable prosthodontic procedure codes.
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

class UnspecifiedRemovableProsthodonticProcedureServices:
    """Class to analyze and extract unspecified removable prosthodontic procedure codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing unspecified removable prosthodontic procedure services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert

### **Before Picking a Code, Ask:**
- Is the procedure truly **not described** by any existing CDT code?
- Have you reviewed all related prosthodontic, implant, and adjunctive codes?
- Can you provide a **detailed narrative** describing the procedure, materials, and clinical rationale?
- Is there supporting documentation (e.g., radiographs, lab invoice, photos)?
- Is this a one-time or temporary solution, or part of a larger treatment plan?

---

#### **Code: D5899**  
**Heading:** Unspecified removable prosthodontic procedure, by report  
**When to Use:**  
- Used only when a **removable prosthodontic service** doesn't match any existing CDT code.  
- Common scenarios include **custom modifications**, **digital workflows**, or **novel techniques** not covered under standard codes.  
**What to Check:**  
- Confirm that no appropriate CDT code exists (D5110–D5876 range).  
- Prepare a detailed report: procedure description, materials used, treatment purpose, and patient benefit.  
- Include clinical photos, diagnostic evidence, and lab documentation if available.  
**Notes:**  
- **"By report" is mandatory** — claim submission must include a thorough narrative.  
- Use sparingly and only when no other code appropriately applies.  
- Often subject to **insurance review or denial** without sufficient justification.

---

### **Key Takeaways:**
- **Narrative is Essential**: Claims without detailed explanation are likely to be denied.
- **Use When No Other Code Fits**: This is a fallback for true exceptions, not a substitute for existing CDT codes.
- **Attach Documentation**: Support claims with photos, models, invoices, or clinical records.
- **Billing May Be Delayed**: Be prepared for payer follow-up or prior authorization requests.


Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_unspecified_removable_prosthodontic_procedure_code(self, scenario: str) -> str:
        """Extract unspecified removable prosthodontic procedure code(s) for a given scenario."""
        try:
            print(f"Analyzing unspecified removable prosthodontic procedure scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Unspecified removable prosthodontic procedure extract_unspecified_removable_prosthodontic_procedure_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in unspecified removable prosthodontic procedure code extraction: {str(e)}")
            return ""
    
    def activate_unspecified_removable_prosthodontic_procedure(self, scenario: str) -> str:
        """Activate the unspecified removable prosthodontic procedure analysis process and return results."""
        try:
            result = self.extract_unspecified_removable_prosthodontic_procedure_code(scenario)
            if not result:
                print("No unspecified removable prosthodontic procedure code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating unspecified removable prosthodontic procedure analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_unspecified_removable_prosthodontic_procedure(scenario)
        print(f"\n=== UNSPECIFIED REMOVABLE PROSTHODONTIC PROCEDURE ANALYSIS RESULT ===")
        print(f"UNSPECIFIED REMOVABLE PROSTHODONTIC PROCEDURE CODE: {result if result else 'None'}")

# Example usage
if __name__ == "__main__":
    unspecified_removable_prosthodontic_procedure_service = UnspecifiedRemovableProsthodonticProcedureServices()
    scenario = input("Enter an unspecified removable prosthodontic procedure dental scenario: ")
    unspecified_removable_prosthodontic_procedure_service.run_analysis(scenario) 