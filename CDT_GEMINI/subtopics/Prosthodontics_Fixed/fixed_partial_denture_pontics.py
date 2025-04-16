"""
Module for extracting fixed partial denture pontics codes.
"""

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

class FixedPartialDenturePonticsServices:
    """Class to analyze and extract fixed partial denture pontics codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing fixed partial denture pontics services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert

### **Before picking a code, ask:**
- What was the primary reason the patient came in?
- Is the reline being done directly in the mouth or indirectly in a lab?
- Is this a complete or partial denture?
- Is the denture maxillary or mandibular?
- Does the patient have any history of discomfort, instability, or changes in fit?

---

## **Prosthodontics, Fixed**

### **Code: D6205**  
**Heading:** Pontic - Indirect Resin-Based Composite  
**Use when:** A permanent pontic is being placed using an indirect resin-based composite.  
**Check:** Ensure this is not used as a temporary or provisional prosthesis.  
**Note:** This is a definitive restoration, not for short-term use.

### **Code: D6210**  
**Heading:** Pontic - Cast High Noble Metal  
**Use when:** A pontic is being placed in a fixed prosthesis using high noble metal.  
**Check:** Confirm the material choice aligns with patient needs and insurance coverage.  

### **Code: D6211**  
**Heading:** Pontic - Cast Predominantly Base Metal  
**Use when:** A pontic is being placed in a fixed prosthesis using base metal.  
**Check:** Verify patient's metal allergies and compatibility with existing restorations.  

### **Code: D6212**  
**Heading:** Pontic - Cast Noble Metal  
**Use when:** A pontic is being placed in a fixed prosthesis using noble metal.  
**Check:** Ensure the use of noble metal meets functional and esthetic requirements.  

### **Code: D6214**  
**Heading:** Pontic - Titanium and Titanium Alloys  
**Use when:** A pontic is being placed in a fixed prosthesis using titanium or titanium alloys.  
**Check:** Confirm the biocompatibility and suitability for the patient's needs.  

### **Code: D6240**  
**Heading:** Pontic - Porcelain Fused to High Noble Metal  
**Use when:** A pontic is needed with porcelain esthetics and high noble metal strength.  
**Check:** Verify the metal type and ensure proper occlusion.  

### **Code: D6241**  
**Heading:** Pontic - Porcelain Fused to Predominantly Base Metal  
**Use when:** A pontic is needed with porcelain esthetics and base metal strength.  
**Check:** Ensure proper bonding and patient tolerance for base metal.  

### **Code: D6242**  
**Heading:** Pontic - Porcelain Fused to Noble Metal  
**Use when:** A pontic is needed with porcelain esthetics and noble metal strength.  
**Check:** Confirm noble metal usage based on patient and insurance preferences.  

### **Code: D6243**  
**Heading:** Pontic - Porcelain Fused to Titanium and Titanium Alloys  
**Use when:** A pontic is being placed in a fixed prosthesis using titanium with porcelain esthetics.  
**Check:** Ensure proper compatibility with adjacent restorations.  

### **Code: D6245**  
**Heading:** Pontic - Porcelain/Ceramic  
**Use when:** A pontic is needed with high esthetic demands using full porcelain/ceramic material.  
**Check:** Confirm occlusal compatibility and fracture resistance.  

### **Code: D6250**  
**Heading:** Pontic - Resin with High Noble Metal  
**Use when:** A pontic is being placed with resin and high noble metal.  
**Check:** Ensure the resin layer is properly bonded and functional.  

### **Code: D6251**  
**Heading:** Pontic - Resin with Predominantly Base Metal  
**Use when:** A pontic is being placed with resin and predominantly base metal.  
**Check:** Verify patient tolerance and durability expectations.  

### **Code: D6252**  
**Heading:** Pontic - Resin with Noble Metal  
**Use when:** A pontic is being placed with resin and noble metal.  
**Check:** Confirm material compatibility and esthetic expectations.  

### **Code: D6253**  
**Heading:** Interim Pontic - Further Treatment or Completion of Diagnosis Necessary Prior to Final Impression  
**Use when:** A temporary pontic is required before a final prosthesis can be fabricated.  
**Check:** Ensure this is not used as a routine temporary pontic.  
**Note:** Intended for cases requiring extended diagnostic workup.  

---

### **Key Takeaways:**
- **Direct vs. Indirect:** Direct relines are immediate, while indirect relines require lab processing but last longer.
- **Complete vs. Partial:** Ensure the correct code is selected based on whether the patient has a complete or partial denture.
- **Patient Education:** Explain the difference between direct and indirect relines to manage patient expectations.
- **Occlusion & Fit:** Always verify post-treatment occlusion to prevent bite imbalances.
- **Long-Term Adjustments:** Some relines may require further modifications as soft tissues continue to adapt.


Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_fixed_partial_denture_pontics_code(self, scenario: str) -> str:
        """Extract fixed partial denture pontics code(s) for a given scenario."""
        try:
            print(f"Analyzing fixed partial denture pontics scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Fixed partial denture pontics extract_fixed_partial_denture_pontics_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in fixed partial denture pontics code extraction: {str(e)}")
            return ""
    
    def activate_fixed_partial_denture_pontics(self, scenario: str) -> str:
        """Activate the fixed partial denture pontics analysis process and return results."""
        try:
            result = self.extract_fixed_partial_denture_pontics_code(scenario)
            if not result:
                print("No fixed partial denture pontics code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating fixed partial denture pontics analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_fixed_partial_denture_pontics(scenario)
        print(f"\n=== FIXED PARTIAL DENTURE PONTICS ANALYSIS RESULT ===")
        print(f"FIXED PARTIAL DENTURE PONTICS CODE: {result if result else 'None'}")

# Create and export service instance
fixed_partial_denture_pontics_service = FixedPartialDenturePonticsServices()

# Example usage
if __name__ == "__main__":
    scenario = input("Enter a fixed partial denture pontics dental scenario: ")
    fixed_partial_denture_pontics_service.run_analysis(scenario) 