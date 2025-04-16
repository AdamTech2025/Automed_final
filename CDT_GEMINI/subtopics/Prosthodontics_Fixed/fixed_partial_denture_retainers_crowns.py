"""
Module for extracting fixed partial denture retainers - crowns codes.
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

class FixedPartialDentureRetainersCrownsServices:
    """Class to analyze and extract fixed partial denture retainers crowns codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing fixed partial denture retainers crowns services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert

### **Before picking a code, ask:**
- What was the primary reason the patient came in?
- What is the material of the crown retainer (e.g., porcelain, metal, zirconia)?
- Is this a new crown retainer or a repair/replacement?
- Which tooth or teeth are involved?
- What is the condition of the abutment tooth (e.g., heavily restored, minimal preparation)?

---

### **Code: D6710**  
**Heading:** Retainer Crown - Indirect Resin-Based Composite  
**Use when:** The patient needs a crown made of indirect resin-based composite to serve as a retainer in a fixed partial denture.  
**Check:** Verify that the crown is fabricated from laboratory-processed composite resin, not direct composite.  
**Note:** This offers a more economical option than porcelain or metal, but with less durability for long-term use.

---

### **Code: D6720**  
**Heading:** Retainer Crown - Resin with High Noble Metal  
**Use when:** The patient needs a crown with a high noble metal substructure and resin facing to serve as a retainer.  
**Check:** Confirm the use of high noble metal (significant gold content) with resin overlay.  
**Note:** Provides good strength from the metal with esthetic resin facing. More economical than PFM but less esthetic than all-ceramic.

---

### **Code: D6721**  
**Heading:** Retainer Crown - Resin with Predominantly Base Metal  
**Use when:** The patient needs a crown with a predominantly base metal substructure and resin facing as a retainer.  
**Check:** Verify the use of base metal (e.g., nickel-chromium) with resin overlay.  
**Note:** More economical option than noble metal crowns, but may present biocompatibility issues for patients with metal sensitivities.

---

### **Code: D6722**  
**Heading:** Retainer Crown - Resin with Noble Metal  
**Use when:** The patient needs a crown with a noble metal substructure and resin facing to serve as a retainer.  
**Check:** Confirm the use of noble metal (contains precious metals but less than high noble) with resin overlay.  
**Note:** A middle-ground option between high noble and base metal in terms of cost and properties.

---

### **Code: D6740**  
**Heading:** Retainer Crown - Porcelain/Ceramic  
**Use when:** The patient needs an all-ceramic crown to serve as a retainer in a fixed partial denture.  
**Check:** Verify the crown is entirely made of ceramic or porcelain with no metal substructure.  
**Note:** Provides excellent esthetics, especially for anterior bridges. Consider occlusal forces and span length when using all-ceramic retainers.

---

### **Code: D6750**  
**Heading:** Retainer Crown - Porcelain Fused to High Noble Metal  
**Use when:** The patient needs a porcelain-fused-to-high-noble-metal crown as a retainer.  
**Check:** Confirm the use of high noble metal with porcelain overlay for esthetics.  
**Note:** Combines strength of gold alloy with the esthetics of porcelain. Good for posterior and anterior regions.

---

### **Code: D6751**  
**Heading:** Retainer Crown - Porcelain Fused to Predominantly Base Metal  
**Use when:** The patient needs a porcelain-fused-to-base-metal crown as a retainer.  
**Check:** Verify the use of predominantly base metal with porcelain overlay.  
**Note:** More affordable than high noble metal. Monitor for potential metal allergies or gingival discoloration over time.

---

### **Code: D6752**  
**Heading:** Retainer Crown - Porcelain Fused to Noble Metal  
**Use when:** The patient needs a porcelain-fused-to-noble-metal crown as a retainer.  
**Check:** Confirm the use of noble metal with porcelain overlay.  
**Note:** Provides a balance between cost and biocompatibility compared to high noble and base metal options.

---

### **Code: D6753**  
**Heading:** Retainer Crown - Porcelain Fused to Titanium and Titanium Alloys  
**Use when:** The patient needs a porcelain-fused-to-titanium crown as a retainer.  
**Check:** Verify the use of titanium substructure with porcelain overlay.  
**Note:** Excellent biocompatibility option for patients with allergies to conventional dental alloys.

---

### **Code: D6780**  
**Heading:** Retainer Crown - 3/4 Cast High Noble Metal  
**Use when:** The patient needs a three-quarter cast crown made of high noble metal as a retainer.  
**Check:** Confirm this is a partial coverage restoration (covering three of the four axial surfaces) in high noble metal.  
**Note:** More conservative option that preserves tooth structure while providing retention for the bridge.

---

### **Code: D6781**  
**Heading:** Retainer Crown - 3/4 Cast Predominantly Base Metal  
**Use when:** The patient needs a three-quarter cast crown made of predominantly base metal as a retainer.  
**Check:** Verify this is a partial coverage restoration in predominantly base metal.  
**Note:** Economical option for cases where full coverage is not required and some tooth structure can be preserved.

---

### **Code: D6782**  
**Heading:** Retainer Crown - 3/4 Cast Noble Metal  
**Use when:** The patient needs a three-quarter cast crown made of noble metal as a retainer.  
**Check:** Confirm this is a partial coverage restoration in noble metal.  
**Note:** Mid-range option in terms of cost and properties for partial coverage bridge retainers.

---

### **Code: D6783**  
**Heading:** Retainer Crown - 3/4 Porcelain/Ceramic  
**Use when:** The patient needs a three-quarter crown made of porcelain/ceramic as a retainer.  
**Check:** Verify this is a partial coverage restoration entirely in ceramic material.  
**Note:** Provides good esthetics while preserving some tooth structure. Consider carefully for high-stress areas.

---

### **Code: D6784**  
**Heading:** Retainer Crown - 3/4 Titanium and Titanium Alloys  
**Use when:** The patient needs a three-quarter crown made of titanium as a retainer.  
**Check:** Confirm this is a partial coverage restoration in titanium.  
**Note:** Biocompatible option for patients with metal allergies who also benefit from partial coverage design.

---

### **Code: D6790**  
**Heading:** Retainer Crown - Full Cast High Noble Metal  
**Use when:** The patient needs a full cast crown made entirely of high noble metal as a retainer.  
**Check:** Verify the crown is fabricated completely from high noble metal with no porcelain or resin facing.  
**Note:** Extremely durable option, ideal for posterior bridges with significant occlusal forces.

---

### **Code: D6791**  
**Heading:** Retainer Crown - Full Cast Predominantly Base Metal  
**Use when:** The patient needs a full cast crown made entirely of predominantly base metal as a retainer.  
**Check:** Confirm the crown is fabricated completely from base metal.  
**Note:** Economical and strong option for posterior bridges. Screen for potential metal sensitivities.

---

### **Code: D6792**  
**Heading:** Retainer Crown - Full Cast Noble Metal  
**Use when:** The patient needs a full cast crown made entirely of noble metal as a retainer.  
**Check:** Verify the crown is fabricated completely from noble metal.  
**Note:** Good middle-ground option for full cast retainers in terms of cost and properties.

---

### **Code: D6793**  
**Heading:** Interim Retainer Crown - Further Treatment or Completion of Diagnosis Necessary Prior to Final Impression  
**Use when:** The patient needs a temporary crown to serve as a bridge retainer while awaiting final treatment decisions.  
**Check:** Confirm this is truly an interim restoration, not a permanent retainer crown.  
**Note:** Used when diagnosis is incomplete or when healing must occur before final impressions.

---

### **Code: D6794**  
**Heading:** Retainer Crown - Titanium and Titanium Alloys  
**Use when:** The patient needs a full cast crown made entirely of titanium as a retainer.  
**Check:** Verify the crown is fabricated completely from titanium.  
**Note:** Highly biocompatible option for patients with metal sensitivities. Lightweight yet strong.

---

### **Key Takeaways:**
- **Material Selection:** Material choice impacts code selection, durability, esthetics, and cost.
- **Full vs. Partial Coverage:** Three-quarter crowns (D6780-D6784) preserve more tooth structure but may not be suitable for all abutment teeth.
- **Metal Type Matters:** Distinguish between high noble, noble, and base metals based on precious metal content.
- **Biocompatibility:** Consider titanium options (D6753, D6784, D6794) for patients with metal allergies.
- **Interim vs. Definitive:** Interim retainer crowns (D6793) should only be used temporarily while awaiting final treatment.

Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_fixed_partial_denture_retainers_crowns_code(self, scenario: str) -> str:
        """Extract fixed partial denture retainers crowns code(s) for a given scenario."""
        try:
            print(f"Analyzing fixed partial denture retainers crowns scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Fixed partial denture retainers crowns extract_fixed_partial_denture_retainers_crowns_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in fixed partial denture retainers crowns code extraction: {str(e)}")
            return ""
    
    def activate_fixed_partial_denture_retainers_crowns(self, scenario: str) -> str:
        """Activate the fixed partial denture retainers crowns analysis process and return results."""
        try:
            result = self.extract_fixed_partial_denture_retainers_crowns_code(scenario)
            if not result:
                print("No fixed partial denture retainers crowns code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating fixed partial denture retainers crowns analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_fixed_partial_denture_retainers_crowns(scenario)
        print(f"\n=== FIXED PARTIAL DENTURE RETAINERS CROWNS ANALYSIS RESULT ===")
        print(f"FIXED PARTIAL DENTURE RETAINERS CROWNS CODE: {result if result else 'None'}")

# Create and export service instance
fixed_partial_denture_retainers_crowns_service = FixedPartialDentureRetainersCrownsServices()

# Example usage
if __name__ == "__main__":
    scenario = input("Enter a fixed partial denture retainers crowns dental scenario: ")
    fixed_partial_denture_retainers_crowns_service.run_analysis(scenario) 