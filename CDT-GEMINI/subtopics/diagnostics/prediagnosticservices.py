import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from subtopics.prompt.prompt import PROMPT


# Get model name from environment variable, default to gpt-4o if not set
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o")

def create_prediagnostic_services_extractor(temperature=0.0):
    """
    Create a LangChain-based Prediagnostic Services extractor.
    """
    # Use ChatOpenAI for newer models like gpt-4o
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash-thinking-exp-01-21", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced medical coding expert, 


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

### *Scenario:*
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_prediagnostic_services_code(scenario, temperature=0.0):
    """
    Extract Prediagnostic Services code(s) for a given scenario.
    """
    chain = create_prediagnostic_services_extractor(temperature)
    return chain.run(question=scenario).strip()

def activate_prediagnostic_services(scenario):
    """
    Activate Prediagnostic Services analysis and return results.
    """
    return extract_prediagnostic_services_code(scenario)