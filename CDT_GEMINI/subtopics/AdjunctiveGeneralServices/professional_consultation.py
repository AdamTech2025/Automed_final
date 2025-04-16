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

class ProfessionalConsultationServices:
    """Class to analyze and extract professional consultation codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing professional consultations."""
        return PromptTemplate(
            template=f"""
You are a dental coding expert

Before picking a code, ask:
- Is the consultation being provided by a dentist or a medical health care professional?
- Is the consultation for diagnostic purposes, or is it related to a broader medical concern affecting dental treatment?
- Is this a one-time consultation, or will it require ongoing collaboration with another provider?
- Will the consulted practitioner be initiating additional diagnostic or therapeutic services?
- Does the consultation include a full oral evaluation, or is it limited to discussion and advice?

---

### **Detailed Coding Guidelines for Professional Consultation**

#### **Code: D9310** – *Consultation - Diagnostic Service Provided by a Dentist or Physician Other Than the Requesting Dentist or Physician*
**Use when:** A patient is referred to another dentist or physician for their professional opinion or advice regarding a specific dental problem.
**Check:** Ensure that the consultation is formally requested by another provider and that the consulting practitioner provides a documented evaluation.
**Note:** This code includes an oral evaluation but does not cover additional treatment or procedures initiated by the consultant. If further diagnostic or therapeutic services are required, they must be billed separately.

#### **Code: D9311** – *Consultation with a Medical Health Care Professional*
**Use when:** A dentist consults with a medical professional (e.g., physician, specialist) regarding a patient's medical condition that may impact dental treatment.
**Check:** Ensure the consultation is medically necessary and directly related to the patient's dental care plan.
**Note:** Common cases include discussions about patients with cardiovascular conditions, diabetes, bleeding disorders, or immunosuppressive conditions that may require adjustments in dental treatment. Documentation of the consultation, including any recommendations made by the medical provider, is essential.

---

### **Key Takeaways:**
- **D9310** is used when a dentist or physician provides a second opinion or diagnosis at the request of another provider. This includes an oral evaluation.
- **D9311** is used when a treating dentist consults with a medical provider to assess how a patient's medical condition may affect planned dental procedures.
- **Ensure proper documentation** of the consultation request, findings, and recommendations to justify the billing of these codes.
- **Additional procedures or treatments** initiated as a result of the consultation must be coded separately.

By using these codes appropriately, dental providers can ensure accurate billing and seamless interdisciplinary coordination for comprehensive patient care.

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_professional_consultation_code(self, scenario: str) -> str:
        """Extract professional consultation code(s) for a given scenario."""
        try:
            print(f"Analyzing professional consultation scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Professional consultation extract_professional_consultation_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in professional consultation code extraction: {str(e)}")
            return ""
    
    def activate_professional_consultation(self, scenario: str) -> str:
        """Activate the professional consultation analysis process and return results."""
        try:
            result = self.extract_professional_consultation_code(scenario)
            if not result:
                print("No professional consultation code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating professional consultation analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_professional_consultation(scenario)
        print(f"\n=== PROFESSIONAL CONSULTATION ANALYSIS RESULT ===")
        print(f"PROFESSIONAL CONSULTATION CODE: {result if result else 'None'}")


professional_consultation_service = ProfessionalConsultationServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a professional consultation dental scenario: ")
    professional_consultation_service.run_analysis(scenario)