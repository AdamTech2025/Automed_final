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

class ApexificationServices:
    """Class to analyze and extract apexification/recalcification codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing apexification/recalcification."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert

Before Picking a Code, Ask:
- What was the primary reason the patient came in? Did they present with symptoms (e.g., pain, swelling) tied to a previously treated root canal, or was it discovered during a routine visit?
- Which tooth is being retreated? Is it an anterior, premolar, or molar tooth?
- Has the prior root canal failed due to issues like persistent infection, poor sealing, or new pathology?
- Are there diagnostic tools (e.g., radiographs, clinical exams) confirming the need for retreatment?
- Is the tooth still restorable, or does its condition suggest a different approach (e.g., extraction)?

---

### Apexification/Recalcification (Endodontic Retreatment with Provided Codes)
#### **Code:** D3351  
**Heading:** Apexification/Recalcification – Initial Visit  
**When to Use:**  
- The patient has an immature permanent tooth or an open apex that requires apical closure.  
- Used in cases involving root resorption, perforations, or other anomalies requiring calcific barrier formation.  
- Typically indicated when performing endodontic treatment on a non-vital tooth with an incompletely formed apex.  
- May also apply when repairing perforations or managing resorptive defects with medicament therapy.  

**What to Check:**  
- Confirm the presence of an open apex or apical pathology via radiographic evidence.  
- Assess the tooth's vitality and pulpal status (usually necrotic pulp in young permanent teeth).  
- Evaluate whether the root is restorable and the prognosis is favorable with apexification.  
- Document clinical signs (e.g., sinus tract, swelling) and diagnostic testing (cold test, percussion).  

**Notes:**  
- Includes opening the tooth, canal debridement, placement of the first medicament (e.g., calcium hydroxide, MTA), and necessary radiographs.  
- Often represents the **first stage of root canal therapy** for immature teeth.  
- Follow-up visits for additional medicament replacement may require **D3352**, and the final visit for closure is coded with **D3353**.  
- Document material used and rationale clearly for insurance—especially in trauma or developmental cases.  

### Key Takeaways:
- **Tooth Location Drives Coding:** D3346 (anterior), D3347 (premolar), and D3348 (molar) are specific to tooth type—precision is critical.  
- **Evidence of Failure:** Retreatment codes require proof of prior root canal issues (e.g., imaging, symptoms).  
- **Non-Surgical Only:** These codes apply to non-surgical retreatments; surgical options have separate codes.  
- **Restoration Separate:** Final restorations aren't included—code them independently.  
- **Insurance Prep:** Expect to provide narratives and X-rays to support retreatment claims.

Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_apexification_code(self, scenario: str) -> str:
        """Extract apexification/recalcification code(s) for a given scenario."""
        try:
            print(f"Analyzing apexification scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Apexification extract_apexification_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in apexification code extraction: {str(e)}")
            return ""
    
    def activate_apexification(self, scenario: str) -> str:
        """Activate the apexification analysis process and return results."""
        try:
            result = self.extract_apexification_code(scenario)
            if not result:
                print("No apexification code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating apexification analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_apexification(scenario)
        print(f"\n=== APEXIFICATION ANALYSIS RESULT ===")
        print(f"APEXIFICATION CODE: {result if result else 'None'}")

apexification_service = ApexificationServices()
# Example usage
if __name__ == "__main__":
    apexification_service = ApexificationServices()
    scenario = input("Enter an apexification dental scenario: ")
    apexification_service.run_analysis(scenario)