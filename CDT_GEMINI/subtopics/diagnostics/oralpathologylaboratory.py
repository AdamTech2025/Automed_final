import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from subtopics.prompt.prompt import PROMPT


# Get model name from environment variable, default to gpt-4o if not set
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o")

def create_oral_pathology_laboratory_extractor(temperature=0.0):
    """
    Create a LangChain-based Oral Pathology Laboratory test extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash-8b", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced medical coding expert. 

Canvas ## Oral Pathology Laboratory - Detailed Guidelines

### **General Guidelines for Choosing Codes:**
1. **Determine the Test Purpose:** Identify if the test is for microbial, genetic, or cytologic evaluation.
2. **Check Testing Methodology:** Ensure proper sample collection and processing.
3. **Document Findings:** Accurately record test results for compliance and treatment planning.
4. **Ensure Regulatory Compliance:** Follow laboratory and public health guidelines.



### **D0472 - Accession of Tissue, Gross Examination, Preparation and Transmission of Written Report**
**When to Use:**
- When reporting architecturally intact tissue obtained by invasive means.

**What to Check:**
- Ensure the tissue sample is architecturally intact and collected invasively.

**Notes:**
- Only includes gross examination without microscopic analysis.

---

### **D0473 - Accession of Tissue, Gross and Microscopic Examination, Preparation and Transmission of Written Report**
**When to Use:**
- When both gross and microscopic examination is required for tissue analysis.

**What to Check:**
- Confirm that microscopic evaluation is necessary beyond gross assessment.

**Notes:**
- Offers more detailed tissue evaluation compared to D0472.

---

### **D0474 - Accession of Tissue, Gross and Microscopic Examination, Including Assessment of Surgical Margins for Presence of Disease, Preparation and Transmission of Written Report**
**When to Use:**
- When tissue examination includes evaluation of surgical margins for disease presence.

**What to Check:**
- Verify the requirement for surgical margin analysis.

**Notes:**
- Helps determine completeness of surgical excisions.

---

### **D0480 - Accession of Exfoliative Cytologic Smears, Microscopic Examination, Preparation and Transmission of Written Report**
**When to Use:**
- For microscopic examination of exfoliative cytologic smears.

**What to Check:**
- Ensure the sample is from a cytologic smear, not a tissue biopsy.

**Notes:**
- Commonly used for non-invasive cellular assessments.

---

### **D0486 - Laboratory Accession of Transepithelial Cytologic Sample, Microscopic Examination, Preparation and Transmission of Written Report**
**When to Use:**
- When a transepithelial cytologic sample is analyzed for diagnostic evaluation.

**What to Check:**
- Ensure the sample consists of disaggregated transepithelial cells.

**Notes:**
- Useful for detecting mucosal abnormalities.

---

### **D0475 - Decalcification Procedure**
**When to Use:**
- When hard tissue requires processing for microscopic examination.

**What to Check:**
- Verify necessity of decalcification for tissue sectioning.

**Notes:**
- Essential for mineralized tissue analysis.

---

### **D0476 - Special Stains for Microorganisms**
**When to Use:**
- When additional stains are needed to identify microorganisms.

**What to Check:**
- Confirm that microorganism identification is required.

**Notes:**
- Frequently used for bacterial and fungal detection.

---

### **D0477 - Special Stains, Not for Microorganisms**
**When to Use:**
- When special stains are required for elements like melanin, mucin, iron, or glycogen.

**What to Check:**
- Verify the stain’s diagnostic purpose.

**Notes:**
- Helps identify tissue abnormalities.

---

### **D0478 - Immunohistochemical Stains**
**When to Use:**
- When antibody-based reagents are applied for diagnosis.

**What to Check:**
- Confirm necessity for immunohistochemical analysis.

**Notes:**
- Used for tumor markers and cell differentiation.

---

### **D0479 - Tissue In-Situ Hybridization, Including Interpretation**
**When to Use:**
- When DNA/RNA identification in tissue samples is needed for diagnosis.

**What to Check:**
- Ensure hybridization technique is necessary.

**Notes:**
- Used for genetic and infectious disease diagnostics.

---

### **D0481 - Electron Microscopy**
**When to Use:**
- When detailed ultrastructural examination of tissue is required.

**What to Check:**
- Confirm conventional microscopy is insufficient.

**Notes:**
- Provides high-resolution imaging.

---

### **D0482 - Direct Immunofluorescence**
**When to Use:**
- When detecting immune reactants in skin or mucosal samples.

**What to Check:**
- Confirm the necessity for immunofluorescence testing.

**Notes:**
- Used in autoimmune disease diagnosis.

---

### **D0483 - Indirect Immunofluorescence**
**When to Use:**
- When identifying circulating immune reactants.

**What to Check:**
- Ensure systemic immunological involvement.

**Notes:**
- Used for diagnosing systemic autoimmune conditions.



---

### **D0485 - Consultation, Including Preparation of Slides from Biopsy Material Supplied by Referring Source**
**When to Use:**
- When both slide preparation and consultation are necessary.

**What to Check:**
- Ensure the sample requires slide preparation before analysis.

**Notes:**
- More comprehensive than D0484.

---

### **D0502 - Other Oral Pathology Procedures, By Report**
**When to Use:**
- When reporting oral pathology procedures not covered by another code.

**What to Check:**
- Confirm that no existing code fits the procedure.

**Notes:**
- Requires detailed procedural documentation.

---

### **D0999 - Unspecified Diagnostic Procedure, By Report**
**When to Use:**
- When performing a diagnostic procedure that lacks a specific code.

**What to Check:**
- Ensure no other defined code describes the procedure.

**Notes:**
- Must include a full procedural description.  

### *Scenario:*
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_oral_pathology_laboratory_code(scenario, temperature=0.0):
    """
    Extract Oral Pathology Laboratory test code(s) for a given scenario.
    """
    chain = create_oral_pathology_laboratory_extractor(temperature)
    return chain.run(question=scenario).strip()

def activate_oral_pathology_laboratory(scenario):
    """
    Activate Oral Pathology Laboratory analysis and return results.
    """
    return extract_oral_pathology_laboratory_code(scenario)