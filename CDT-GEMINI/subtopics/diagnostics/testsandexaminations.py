import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from subtopics.prompt.prompt import PROMPT


# Get model name from environment variable, default to gpt-4o if not set
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o")

def create_tests_and_examinations_extractor(temperature=0.0):
    """
    Create a LangChain-based Tests and Examinations extractor.
    """
    # Use ChatOpenAI for newer models like gpt-4o
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash-thinking-exp-01-21", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert

### **General Guidelines for Selecting Codes:**
1. **Determine the Test Purpose:** Identify whether the test is for microbial, genetic, caries risk, or systemic health assessment.
2. **Check Testing Methodology:** Ensure proper sample collection and analysis.
3. **Document Findings:** Properly record test results and their implications for treatment.
4. **Ensure Compliance:** Follow lab regulations and public health guidelines.


## Tests and Examinations - Detailed Guidelines

### **D0411 - HbA1c In-Office Point of Service Testing**
**When to Use:**
- To assess a patient’s HbA1c levels for diabetes monitoring.

**What to Check:**
- Ensure the test is necessary for patient evaluation and treatment planning.

**Notes:**
- Provides real-time data for immediate clinical decision-making.

---

### **D0412 - Blood Glucose Level Test (In-Office Using a Glucose Meter)**
**When to Use:**
- When an immediate reading of a patient’s blood glucose level is required.

**What to Check:**
- Must be performed at the point of service.

**Notes:**
- Helps in diabetes monitoring and emergency assessments.

---

### **D0414 - Laboratory Processing of Microbial Specimen**
**When to Use:**
- When microbial specimens need culture and sensitivity analysis.

**What to Check:**
- Requires laboratory processing and documentation.

**Notes:**
- A written report must be prepared and transmitted.

---

### **D0415 - Collection of Microorganisms for Culture and Sensitivity**
**When to Use:**
- When a microbial sample needs to be collected for diagnostic purposes.

**What to Check:**
- Ensure proper collection techniques are used.

**Notes:**
- Should be followed by laboratory processing.

---

### **D0416 - Viral Culture**
**When to Use:**
- For diagnosing viral infections, such as herpes.

**What to Check:**
- Appropriate clinical indications for viral testing.

**Notes:**
- Helps confirm the presence of viral pathogens.

---

### **D0417 - Collection and Preparation of Saliva Sample for Laboratory Testing**
**When to Use:**
- When a saliva sample is needed for diagnostic evaluation.

**What to Check:**
- Proper collection techniques must be followed.

**Notes:**
- Should be accompanied by analysis (D0418).

---

### **D0418 - Analysis of Saliva Sample**
**When to Use:**
- For chemical or biological saliva analysis.

**What to Check:**
- Ensure it is used for diagnostic purposes.

**Notes:**
- Often used for assessing bacterial load or enzyme activity.

---

### **D0419 - Assessment of Salivary Flow by Measurement**
**When to Use:**
- To identify low salivary flow and conditions like xerostomia.

**What to Check:**
- Patient risk factors for hyposalivation.

**Notes:**
- Can be used to assess effectiveness of saliva-stimulating medications.

---

### **D0422 - Collection and Preparation of Genetic Sample Material for Laboratory Analysis**
**When to Use:**
- When genetic testing is necessary for disease susceptibility.

**What to Check:**
- Ensure proper sample collection and patient consent.

**Notes:**
- Used for further laboratory analysis.

---

### **D0423 - Genetic Test for Susceptibility to Diseases (Specimen Analysis)**
**When to Use:**
- To detect genetic markers for disease risk.

**What to Check:**
- Certified lab must perform analysis.

**Notes:**
- Useful in identifying predisposition to systemic or oral diseases.

---

### **D0425 - Caries Susceptibility Tests**
**When to Use:**
- To determine a patient’s risk for developing cavities.

**What to Check:**
- Should not be used for carious dentin staining.

**Notes:**
- Helps guide preventive care and treatment planning.

---

### **D0431 - Adjunctive Pre-Diagnostic Test for Mucosal Abnormalities**
**When to Use:**
- To detect premalignant or malignant mucosal lesions.

**What to Check:**
- Not a replacement for cytology or biopsy.

**Notes:**
- Helps in early detection of oral cancers.

---

### **D0460 - Pulp Vitality Tests**
**When to Use:**
- To assess the vitality of the dental pulp.

**What to Check:**
- Must include multiple teeth and contralateral comparisons.

**Notes:**
- Helps determine the need for endodontic treatment.

---

### **D0470 - Diagnostic Casts**
**When to Use:**
- For study models in treatment planning.

**What to Check:**
- Proper impressions and cast preparation.

**Notes:**
- Essential for orthodontic and prosthodontic evaluations.

---

### **D0600 - Non-Ionizing Diagnostic Procedure**
**When to Use:**
- When monitoring changes in enamel, dentin, or cementum.

**What to Check:**
- Ensure appropriate use for quantification and tracking.

**Notes:**
- Provides a radiation-free alternative to detect structural changes.

---

### **D0601 - Caries Risk Assessment (Low Risk)**
**When to Use:**
- To document caries risk level using recognized assessment tools.

**What to Check:**
- Findings must indicate low risk.

**Notes:**
- Helps tailor preventive strategies.

---

### **D0602 - Caries Risk Assessment (Moderate Risk)**
**When to Use:**
- When a patient is assessed as moderate risk for caries.

**What to Check:**
- Must use recognized assessment tools.

**Notes:**
- Guides appropriate fluoride and remineralization strategies.

---

### **D0603 - Caries Risk Assessment (High Risk)**
**When to Use:**
- When a patient is at high risk for caries.

**What to Check:**
- Use standardized risk assessment tools.

**Notes:**
- Helps develop intensive preventive care plans.

---

### **D0604 - Antigen Testing for a Public Health Related Pathogen**
**When to Use:**
- When testing for active infections, including coronavirus.

**What to Check:**
- Ensure test is performed in an appropriate setting.

Notes:
- Provides rapid results for disease detection.

---

### **D0605 - Antibody Testing for a Public Health Related Pathogen**
When to Use:
- To detect antibodies indicating past infection.

What to Check:
- Ensure testing aligns with public health protocols.

Notes:
- Helps determine prior exposure and immunity status.

---

 **D0606 - Molecular Testing for a Public Health Related Pathogen**
When to Use:**
-For genetic detection of pathogens like coronavirus.

What to Check:
 Requires laboratory processing.

notes:
- High sensitivity for detecting viral infections.

---





### *Scenario:*
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_tests_and_examinations_code(scenario, temperature=0.0):
    """
    Extract Tests and Examinations code(s) for a given scenario.
    """
    chain = create_tests_and_examinations_extractor(temperature)
    return chain.run(question=scenario).strip()

def activate_tests_and_examinations(scenario):
    """
    Activate Tests and Examinations analysis and return results.
    """
    return extract_tests_and_examinations_code(scenario)