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

class UnclassifiedTreatmentServices:
    """Class to analyze and extract unclassified treatment codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing unclassified treatments."""
        return PromptTemplate(
            template=f"""
You are a dental coding expert

## **Unclassified Treatment**

### **Before picking a code, ask:**
- Does the procedure or service fit any existing CDT code?
- Has the procedure been performed using a new or emerging technology?
- Is the procedure or service experimental or investigational?
- Is there documentation explaining why a standard code doesn't apply?
- Is there a clinical narrative that describes the specific treatment in detail?

---

### **Detailed Coding Guidelines for Unclassified Treatment**

#### **Code: D9999** – *Unspecified Adjunctive Procedure, By Report*
**Use when:** A dental procedure is performed that cannot be adequately described by any other existing CDT code.
**Check:** Ensure that no standard code exists that could adequately describe the procedure.
**Note:** This code requires a detailed narrative report that explains the nature, extent, and necessity of the procedure and the time, effort, and equipment required.

---

### **Common Uses for D9999:**
- New or evolving dental procedures not yet assigned a specific code
- Experimental or innovative treatments
- Use of technology or approaches that significantly modify standard procedures
- Services that combine elements of multiple procedures in a way not described by existing codes

---

### **Key Takeaways:**
- **D9999 should be a last resort** when no other code accurately describes the procedure.
- **Always include a detailed report** with clinical documentation and justification.
- **Check for updates to CDT codes** before using D9999, as new codes are added regularly.
- **The narrative should explain why** standard codes are insufficient.

This code is subject to greater scrutiny by payers and may require additional documentation for reimbursement.

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_unclassified_treatment_code(self, scenario: str) -> str:
        """Extract unclassified treatment code(s) for a given scenario."""
        try:
            print(f"Analyzing unclassified treatment scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Unclassified treatment extract_unclassified_treatment_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in unclassified treatment code extraction: {str(e)}")
            return ""
    
    def activate_unclassified_treatment(self, scenario: str) -> str:
        """Activate the unclassified treatment analysis process and return results."""
        try:
            result = self.extract_unclassified_treatment_code(scenario)
            if not result:
                print("No unclassified treatment code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating unclassified treatment analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_unclassified_treatment(scenario)
        print(f"\n=== UNCLASSIFIED TREATMENT ANALYSIS RESULT ===")
        print(f"UNCLASSIFIED TREATMENT CODE: {result if result else 'None'}")

unclassified_service = UnclassifiedTreatmentServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter an unclassified treatment dental scenario: ")
    unclassified_service.run_analysis(scenario)