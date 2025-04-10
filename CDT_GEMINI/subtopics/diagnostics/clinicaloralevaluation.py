import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from subtopics.prompt.prompt import PROMPT


# Get model name from environment variable, default to gpt-4o if not set
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o")

def create_clinical_oral_evaluations_extractor(temperature=0.0):
    """
    Create a LangChain-based Clinical Oral Evaluations extractor.
    """
    # Use ChatOpenAI for newer models like gpt-4o
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
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



 Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_clinical_oral_evaluations_code(scenario, temperature=0.0):
    """
    Extract Clinical Oral Evaluations code(s) for a given scenario.
    """
    try:
        chain = create_clinical_oral_evaluations_extractor(temperature)
        result = chain.run(question=scenario)
        print(f"Clinical oral evaluations code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_clinical_oral_evaluations_code: {str(e)}")
        return ""

def activate_clinical_oral_evaluations(scenario):
    """
    Activate Clinical Oral Evaluations analysis and return results.
    """
    return extract_clinical_oral_evaluations_code(scenario)
