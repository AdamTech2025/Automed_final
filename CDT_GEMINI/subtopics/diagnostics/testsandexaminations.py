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

class TestsAndExaminationsServices:
    """Class to analyze and extract tests and examinations codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing tests and examinations."""
        return PromptTemplate(
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
- To assess a patient's HbA1c levels for diabetes monitoring.

**What to Check:**
- Ensure the test is necessary for patient evaluation and treatment planning.

**Notes:**
- Provides real-time data for immediate clinical decision-making.

---

### **D0412 - Blood Glucose Level Test (In-Office Using a Glucose Meter)**
**When to Use:**
- When an immediate reading of a patient's blood glucose level is required.

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
- To determine a patient's risk for developing cavities.

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
- Must use approved testing methods.

**Notes:**
- Helpful in infection control protocols.

---

### **D0605 - Antibody Testing for a Public Health Related Pathogen**
**When to Use:**
- To detect antibodies indicating previous infection or immunization.

**What to Check:**
- Must follow public health guidelines.

**Notes:**
- Assists in determining immune status.

---

### **D0606 - Molecular Testing for a Public Health Related Pathogen**
**When to Use:**
- For detailed molecular analysis of pathogens.

**What to Check:**
- Must use validated laboratory methods.

**Notes:**
- Offers higher sensitivity for pathogen detection.

Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_tests_and_examinations_code(self, scenario: str) -> str:
        """Extract tests and examinations code(s) for a given scenario."""
        try:
            print(f"Analyzing tests and examinations scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Tests and examinations extract_tests_and_examinations_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in tests and examinations code extraction: {str(e)}")
            return ""
    
    def activate_tests_and_examinations(self, scenario: str) -> str:
        """Activate the tests and examinations analysis process and return results."""
        try:
            result = self.extract_tests_and_examinations_code(scenario)
            if not result:
                print("No tests and examinations code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating tests and examinations analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_tests_and_examinations(scenario)
        print(f"\n=== TESTS AND EXAMINATIONS ANALYSIS RESULT ===")
        print(f"TESTS AND EXAMINATIONS CODE: {result if result else 'None'}")

tests_service = TestsAndExaminationsServices()
# Example usage
if __name__ == "__main__":
    tests_service = TestsAndExaminationsServices()
    scenario = input("Enter a tests and examinations dental scenario: ")
    tests_service.run_analysis(scenario)