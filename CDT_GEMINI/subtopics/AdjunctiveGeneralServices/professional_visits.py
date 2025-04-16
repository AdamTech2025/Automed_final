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

class ProfessionalVisitsServices:
    """Class to analyze and extract professional visits codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing professional visits."""
        return PromptTemplate(
            template=f"""
You are a dental coding expert

### **Before picking a code, ask:**
- Is the visit occurring outside of the dentist's office, such as in a hospital, nursing home, or extended care facility?
- Is the visit for consultation, observation, or active treatment?
- Did the visit occur during or outside of regular office hours?
- Was the visit part of a scheduled case presentation for extensive treatment planning?
- Are there additional services provided during the visit that need separate coding?

---

### **Detailed Coding Guidelines for Professional Visits**

#### **Code: D9410** – *House/Extended Care Facility Call*
**Use when:** A dentist provides care at a non-office location, such as a nursing home, long-term care facility, hospice, or institution.
**Check:** Ensure that the visit is necessary due to patient limitations preventing travel to a dental office.
**Note:** This code is reported in addition to specific procedures performed during the visit.

#### **Code: D9420** – *Hospital or Ambulatory Surgical Center Call*
**Use when:** A dentist treats a patient in a hospital or surgical center rather than the dental office.
**Check:** Confirm that the patient is admitted or receiving care in a hospital or ambulatory setting.
**Note:** Any services provided during the visit should be coded separately in addition to this call code.

#### **Code: D9430** – *Office Visit for Observation (During Regularly Scheduled Hours) - No Other Services Performed*
**Use when:** A patient visits the office for observation, but no active treatment or procedures are performed.
**Check:** Ensure that the visit is strictly for monitoring or follow-up without any additional dental procedures.
**Note:** If treatment is rendered, use the appropriate procedural code instead.

#### **Code: D9440** – *Office Visit - After Regularly Scheduled Hours*
**Use when:** A dentist sees a patient outside of normal business hours.
**Check:** Confirm that the visit is necessary and conducted outside of standard office hours, such as evenings, weekends, or emergencies.
**Note:** This code is used in addition to any treatment provided during the after-hours visit.

#### **Code: D9450** – *Case Presentation, Subsequent to Detailed and Extensive Treatment Planning*
**Use when:** A dentist presents a detailed treatment plan to the patient, involving complex or multiple procedures.
**Check:** Ensure that the treatment plan is comprehensive, requiring an in-depth consultation beyond routine discussions.
**Note:** Typically applies to extensive restorative, prosthodontic, or surgical treatment plans.

---

### **Key Takeaways:**
- **D9410 & D9420** cover professional visits outside of the dental office and must be used in addition to any services provided.
- **D9430 & D9440** are for office visits without treatment, differentiating between regular and after-hours visits.
- **D9450** is specifically for case presentations related to detailed and extensive treatment plans.
- **Ensure proper documentation** of the visit's necessity, setting, and whether additional procedures were performed.

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_professional_visits_code(self, scenario: str) -> str:
        """Extract professional visits code(s) for a given scenario."""
        try:
            print(f"Analyzing professional visits scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Professional visits extract_professional_visits_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in professional visits code extraction: {str(e)}")
            return ""
    
    def activate_professional_visits(self, scenario: str) -> str:
        """Activate the professional visits analysis process and return results."""
        try:
            result = self.extract_professional_visits_code(scenario)
            if not result:
                print("No professional visits code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating professional visits analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_professional_visits(scenario)
        print(f"\n=== PROFESSIONAL VISITS ANALYSIS RESULT ===")
        print(f"PROFESSIONAL VISITS CODE: {result if result else 'None'}")

professional_visits_service = ProfessionalVisitsServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a professional visits dental scenario: ")
    professional_visits_service.run_analysis(scenario)