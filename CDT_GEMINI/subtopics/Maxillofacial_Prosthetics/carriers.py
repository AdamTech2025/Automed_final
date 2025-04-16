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

class MaxillofacialProstheticsCarriersServices:
    """Class to analyze and extract maxillofacial prosthetics carriers codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing maxillofacial prosthetics carriers."""
        return PromptTemplate(
            template=f"""
You are a dental coding expert specializing in maxillofacial prosthetics.

### Before Picking a Code, Ask:
- What was the primary reason the patient came in?
- Is the prosthesis designed for fluoride application, medicament delivery, or radiation therapy?
- Is the device custom-fabricated and laboratory-processed?
- What is the specific function and duration of the prosthesis?
- Does the patient have a condition that requires sustained medicament contact or radiation therapy?

---

### Maxillofacial Prosthetics Carriers

#### Code: D5986
**Heading:** Fluoride Gel Carrier  
**When to Use:**  
- A prosthesis is created to apply fluoride gel for caries prevention or treatment.  
- Use for high-risk caries patients requiring daily fluoride.  
**What to Check:**  
- Confirm arch coverage and fit via clinical exam.  
- Verify caries risk (e.g., xerostomia, rampant decay).  
- Assess patient compliance with home use.  
- Check fabrication (lab-processed, custom tray).  
**Notes:**  
- Enhances fluoride delivery vs. topical methods.  
- Not for periodontal or vesiculobullous treatments (see D5995–D5996, D5991).  
- Document caries history, tray design, and usage instructions.  

#### Code: D5995
**Heading:** Periodontal Medicament Carrier with Peripheral Seal – Maxillary  
**When to Use:**  
- A custom carrier delivers periodontal medication to the maxillary arch.  
- Use for advanced periodontal disease requiring sustained drug contact.  
**What to Check:**  
- Confirm periodontal diagnosis (e.g., pocket depths, bone loss) via chart.  
- Verify peripheral seal and gingival adaptation.  
- Assess medication type (e.g., antibiotics, antimicrobials).  
- Check fit over teeth/mucosa.  
**Notes:**  
- Improves drug delivery for periodontitis vs. irrigation.  
- Not for mandibular arch (see D5996) or fluoride (see D5986).  
- Document periodontal status, seal integrity, and drug specifics.  

#### Code: D5996
**Heading:** Periodontal Medicament Carrier with Peripheral Seal – Mandibular  
**When to Use:**  
- A custom carrier delivers periodontal medication to the mandibular arch.  
- Use for mandibular periodontal therapy with sustained delivery.  
**What to Check:**  
- Confirm periodontal condition via exam/radiograph.  
- Verify retention and coverage of teeth/mucosa.  
- Assess seal effectiveness and drug compatibility.  
- Check patient ability to insert/remove.  
**Notes:**  
- Targets mandibular periodontitis with prolonged exposure.  
- Not for maxillary arch (see D5995) or radiation (see D5983).  
- Document disease severity, carrier fit, and medication plan.  

#### Code: D5983
**Heading:** Radiation Carrier  
**When to Use:**  
- A prosthesis holds radiation sources (e.g., radium, cesium) for localized therapy.  
- Use in coordination with oncology for precise radiation delivery.  
**What to Check:**  
- Confirm oncology referral and radiation plan via records.  
- Verify prosthesis stability for source placement.  
- Assess oral tissue tolerance and fit.  
- Check collaboration with radiation oncologist.  
**Notes:**  
- Critical for head/neck cancer treatment accuracy.  
- Not for medicament delivery (see D5991, D5995–D5996).  
- Document radiation type, prosthesis design, and oncologist input.  

#### Code: D5991
**Heading:** Vesiculobullous Disease Medicament Carrier  
**When to Use:**  
- A prosthesis delivers medications for vesiculobullous diseases (e.g., pemphigus, pemphigoid).  
- Use for mucosal conditions needing targeted therapy.  
**What to Check:**  
- Confirm diagnosis (e.g., biopsy, clinical exam) via notes.  
- Verify mucosal adaptation and drug retention.  
- Assess medication type (e.g., steroids, immunosuppressants).  
- Check patient comfort and compliance.  
**Notes:**  
- Enhances treatment for autoimmune mucosal disorders.  
- Not for periodontal or fluoride use (see D5995–D5996, D5986).  
- Document disease type, drug specifics, and carrier fit.  

#### Code: D5999
**Heading:** Unspecified Maxillofacial Prosthesis, By Report  
**When to Use:**  
- A maxillofacial prosthesis doesn’t match specific codes (D5983, D5986, D5991, D5995–D5996).  
- Use for unique or experimental carriers with narrative.  
**What to Check:**  
- Confirm no other code applies via scenario review.  
- Verify custom fabrication and medical necessity.  
- Assess detailed report (function, materials, purpose).  
- Check insurance requirements for approval.  
**Notes:**  
- Requires comprehensive documentation for reimbursement.  
- Not a default; use only for truly unique cases.  
- Document prosthesis type, clinical need, and fabrication details.  

---

### Key Takeaways:
- **Specialized Devices:** Codes target fluoride (D5986), periodontal (D5995–D5996), radiation (D5983), vesiculobullous (D5991), or unique (D5999) carriers.  
- **Custom Fit:** Devices are lab-processed for precise adaptation to teeth/mucosa.  
- **Therapeutic Focus:** Each serves a distinct purpose (caries, periodontitis, cancer, mucosal disease).  
- **Documentation Critical:** Specify condition, fit, materials, and necessity, especially for D5999.  
- **Team Approach:** Often involves periodontists, oncologists, or prosthodontists.  
- **Patient Education:** Ensure understanding of device use and maintenance.  
- **Code Precision:** Avoid D5999 unless no other code fits, with robust narrative.

Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_carriers_code(self, scenario: str) -> str:
        """Extract maxillofacial prosthetics carriers code(s) for a given scenario."""
        try:
            print(f"Analyzing maxillofacial carriers scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Carriers extract_carriers_code result: {code}")
            if code.lower() in ["none", "", "not applicable"]:
                return ""
            return code
        except Exception as e:
            print(f"Error in carriers code extraction: {str(e)}")
            return ""
    
    def activate_carriers(self, scenario: str) -> str:
        """Activate the maxillofacial carriers analysis process and return results."""
        try:
            result = self.extract_carriers_code(scenario)
            if not result:
                print("No maxillofacial carriers code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating maxillofacial carriers analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_carriers(scenario)
        print(f"\n=== MAXILLOFACIAL PROSTHETICS CARRIERS ANALYSIS RESULT ===")
        print(f"MAXILLOFACIAL CARRIERS CODE: {result if result else 'None'}")

carriers_service = MaxillofacialProstheticsCarriersServices()   
# Example usage
if __name__ == "__main__":
    carriers_service = MaxillofacialProstheticsCarriersServices()
    scenario = input("Enter a maxillofacial prosthetics carriers dental scenario: ")
    carriers_service.run_analysis(scenario)