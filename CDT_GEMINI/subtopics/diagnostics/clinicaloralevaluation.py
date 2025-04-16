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

class ClinicalOralEvaluationsServices:
    """Class to analyze and extract clinical oral evaluation codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing clinical oral evaluations."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert

# Dental Evaluation CDT Code Cheat Sheet

---

## 📘 CDT Code Reference

### **D0120 – Periodic Oral Evaluation (Established Patient)**
**When to Use:**
- Routine recall exams for established patients
- Typically every 6 months

**What to Check:**
- Patient must have had a prior D0120 or D0150
- Includes:
  - Medical/Dental history update
  - Oral cancer screening
  - Periodontal screening
  - Caries risk assessment

**Notes:**
- No treatment included under this code
- Additional diagnostics must be billed separately
- Findings must be discussed with the patient

---

### **D0140 – Limited Oral Evaluation (Problem Focused)**
**When to Use:**
- For emergency visits or specific dental issues:
  - Pain
  - Swelling
  - Broken teeth
  - Trauma

**What to Check:**
- Radiographs, testing, or treatment may be needed
- Separate CDT codes for each

**Notes:**
- Appropriate for new or established patients with urgent needs
- May lead to same-day treatment

---

### **D0145 – Oral Evaluation for Patient Under 3 Years + Caregiver Counseling**
**When to Use:**
- Children under 3 years
- Preferably within 6 months of first tooth eruption

**What to Check:**
- Includes:
  - Review of oral/physical health history
  - Cavity risk assessment
  - Prevention planning
  - Counseling parent/caregiver

**Notes:**
- Education is the primary purpose, not treatment

---

### **D0150 – Comprehensive Oral Evaluation (New or Established Patient)**
**When to Use:**
- New patients
- Established patients with major changes or returning after 3+ years

**What to Check:**
- Must include:
  - Complete dental/medical history
  - Oral cancer screening
  - Full perio charting
  - Occlusion/TMJ review

**Notes:**
- More in-depth than D0120
- No treatment included under this code

---

### **D0160 – Detailed and Extensive Oral Evaluation (Problem-Focused, By Report)**
**When to Use:**
- Complex cases needing:
  - Multidisciplinary input
  - Advanced diagnostics
  - TMJ or dentofacial anomaly management

**What to Check:**
- Full documentation required:
  - Condition description
  - Special diagnostics used

**Notes:**
- Requires a written report

---

### **D0170 – Re-Evaluation (Limited, Problem-Focused – Not Post-Op)**
**When to Use:**
- Follow-up for:
  - Soft tissue lesion
  - Pain recheck
  - Traumatic injury monitoring

**What to Check:**
- Patient must have had an earlier documented evaluation

**Notes:**
- Not for post-op check-ups
- Used to monitor specific known problems

---

### **D0171 – Re-Evaluation (Post-Operative Visit)**
**When to Use:**
- After surgeries like:
  - Extraction
  - Periodontal therapy
  - Implant placement

**What to Check:**
- Evaluation is for healing/complication review

**Notes:**
- Should reference the procedure performed

---

### **D0180 – Comprehensive Periodontal Evaluation (New or Established Patient)**
**When to Use:**
- Patient must come to the doctor because of signs of periodontal disease or have a history of periodontal disease (reason for visit), e.g.:
  - Bleeding gums
  - Diabetes
  - Smoking
  - Bone loss

**What to Check:**
- Must include:
  - 6-point periodontal probing
  - Full periodontal charting
  - Occlusion and tooth restoration check

**Notes:**
- More extensive than D0150
- Should not be used casually—only when periodontal concern is valid

---

Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_clinical_oral_evaluations_code(self, scenario: str) -> str:
        """Extract clinical oral evaluation code(s) for a given scenario."""
        try:
            print(f"Analyzing clinical oral evaluations scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Clinical oral evaluations extract_clinical_oral_evaluations_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in clinical oral evaluations code extraction: {str(e)}")
            return ""
    
    def activate_clinical_oral_evaluations(self, scenario: str) -> str:
        """Activate the clinical oral evaluations analysis process and return results."""
        try:
            result = self.extract_clinical_oral_evaluations_code(scenario)
            if not result:
                print("No clinical oral evaluations code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating clinical oral evaluations analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_clinical_oral_evaluations(scenario)
        print(f"\n=== CLINICAL ORAL EVALUATIONS ANALYSIS RESULT ===")
        print(f"CLINICAL ORAL EVALUATIONS CODE: {result if result else 'None'}")


clinical_oral_evaluations_service = ClinicalOralEvaluationsServices()
# Example usage
if __name__ == "__main__":
    evaluations_service = ClinicalOralEvaluationsServices()
    scenario = input("Enter a clinical oral evaluations dental scenario: ")
    evaluations_service.run_analysis(scenario)