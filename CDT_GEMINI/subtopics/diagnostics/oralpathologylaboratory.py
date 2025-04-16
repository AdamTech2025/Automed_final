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

class OralPathologyLaboratoryServices:
    """Class to analyze and extract oral pathology laboratory codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing oral pathology laboratory tests."""
        return PromptTemplate(
            template=f"""
You are a highly experienced medical coding expert

## Oral Pathology Laboratory - Detailed Guidelines

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
- Verify the stain's diagnostic purpose.

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

Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_oral_pathology_laboratory_code(self, scenario: str) -> str:
        """Extract oral pathology laboratory code(s) for a given scenario."""
        try:
            print(f"Analyzing oral pathology laboratory scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Oral pathology laboratory extract_oral_pathology_laboratory_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in oral pathology laboratory code extraction: {str(e)}")
            return ""
    
    def activate_oral_pathology_laboratory(self, scenario: str) -> str:
        """Activate the oral pathology laboratory analysis process and return results."""
        try:
            result = self.extract_oral_pathology_laboratory_code(scenario)
            if not result:
                print("No oral pathology laboratory code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating oral pathology laboratory analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_oral_pathology_laboratory(scenario)
        print(f"\n=== ORAL PATHOLOGY LABORATORY ANALYSIS RESULT ===")
        print(f"ORAL PATHOLOGY LABORATORY CODE: {result if result else 'None'}")

oral_pathology_laboratory_service = OralPathologyLaboratoryServices()
# Example usage
if __name__ == "__main__":
    pathology_service = OralPathologyLaboratoryServices()
    scenario = input("Enter an oral pathology laboratory dental scenario: ")
    pathology_service.run_analysis(scenario)