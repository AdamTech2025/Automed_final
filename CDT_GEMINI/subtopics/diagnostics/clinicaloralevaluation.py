import os
import sys
from langchain.prompts import PromptTemplate
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file
from subtopics.prompt.prompt import PROMPT



def create_clinical_oral_evaluations_extractor():
    """
    Create a LangChain-based Clinical Oral Evaluations extractor.
    """
    template = f"""
You are a highly experienced dental coding expert, 

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

- patient must have to come to the docter beacause of signs of periodontal disease or have a history of periodontal disease(the reason for visit)
eg:
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
    """
    
    prompt = PromptTemplate(template=template, input_variables=["scenario"])
    return create_chain(prompt)

def extract_clinical_oral_evaluations_code(scenario):
    """
    Extract Clinical Oral Evaluations code(s) for a given scenario.
    """
    try:
        extractor = create_clinical_oral_evaluations_extractor()
        result = invoke_chain(extractor, {"scenario": scenario})
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Error in clinical oral evaluations code extraction: {str(e)}")
        return None

def activate_clinical_oral_evaluations(scenario):
    """
    Activate Clinical Oral Evaluations analysis and return results.
    """
    try:
        result = extract_clinical_oral_evaluations_code(scenario)
        return result
    except Exception as e:
        print(f"Error activating clinical oral evaluations analysis: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = "A new patient comes in for their first dental visit in 5 years. The dentist performs a comprehensive examination including medical history, dental history, oral cancer screening, and full periodontal charting."
    result = activate_clinical_oral_evaluations(scenario)
    print(result)
