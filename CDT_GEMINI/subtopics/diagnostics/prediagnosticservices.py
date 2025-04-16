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

class PrediagnosticServices:
    """Class to analyze and extract prediagnostic services codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing prediagnostic services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced medical coding expert

## Pre-Diagnostic Services - Detailed Guidelines

### **D0190 - Screening of a Patient**
**When to Use:**
- When conducting a general screening to determine if a patient needs further dental evaluation.
- Includes state or federally mandated screenings.

**What to Check:**
- Ensure it is a preliminary evaluation and does not include a full diagnosis.
- Used to determine the necessity of a comprehensive dental exam.

**Notes:**
- Not a substitute for a complete dental examination.
- Typically used in community health screenings or school programs.

---

### **D0191 - Assessment of a Patient**
**When to Use:**
- When performing a limited clinical inspection to identify signs of oral or systemic disease, malformation, or injury.
- Used to determine the need for a referral for diagnosis and treatment.

**What to Check:**
- Ensure findings are documented.
- Should be used for preliminary assessments and not as a full diagnostic evaluation.

**Notes:**
- Helps identify patients who may require specialized care or further testing.
- Can be used in triage situations.

---

### **General Guidelines for Selecting Codes:**
1. **Determine Purpose:** Screening (D0190) is for general identification of patients needing further care, while assessment (D0191) is a more focused inspection for specific concerns.
2. **Check Documentation Requirements:** Record findings properly to justify further diagnostic procedures or referrals.
3. **Understand Limitations:** These codes do not include full diagnostic evaluations or treatment planning.

Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_prediagnostic_services_code(self, scenario: str) -> str:
        """Extract prediagnostic services code(s) for a given scenario."""
        try:
            print(f"Analyzing prediagnostic services scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Prediagnostic services extract_prediagnostic_services_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in prediagnostic services code extraction: {str(e)}")
            return ""
    
    def activate_prediagnostic_services(self, scenario: str) -> str:
        """Activate the prediagnostic services analysis process and return results."""
        try:
            result = self.extract_prediagnostic_services_code(scenario)
            if not result:
                print("No prediagnostic services code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating prediagnostic services analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_prediagnostic_services(scenario)
        print(f"\n=== PREDIAGNOSTIC SERVICES ANALYSIS RESULT ===")
        print(f"PREDIAGNOSTIC SERVICES CODE: {result if result else 'None'}")

prediagnostic_service = PrediagnosticServices()
# Example usage
if __name__ == "__main__":
    prediagnostic_service = PrediagnosticServices()
    scenario = input("Enter a prediagnostic services dental scenario: ")
    prediagnostic_service.run_analysis(scenario)