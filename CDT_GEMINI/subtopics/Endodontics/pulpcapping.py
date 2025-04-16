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

class PulpCappingServices:
    """Class to analyze and extract pulp capping codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing pulp capping."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert

Before picking a code, ask:
- What was the primary reason the patient came in? Was it for a general check-up, or to address a specific concern?
- Is the treatment intended to preserve the pulp or remove infected tissue?
- Is the pulp exposed, nearly exposed, or has deep decay?
- Is the procedure direct or indirect?

---

### Endodontic Procedure Codes

#### Code: D3110
**Heading:** Pulp Cap — Direct (excluding final restoration)  
**When to Use:**  
- The patient has a tooth with an exposed pulp (e.g., due to trauma or deep caries), and a protective dressing (e.g., calcium hydroxide, MTA) is applied directly over the exposed pulp to promote healing and dentin bridge formation.  
- Use when the pulp is visibly exposed during caries removal or preparation.  
**What to Check:**  
- Confirm pulp exposure via clinical exam or visualization during treatment.  
- Assess the health of the exposed pulp (e.g., minimal bleeding, no signs of necrosis).  
- Verify the use of biocompatible material suitable for direct pulp capping.  
- Check the tooth's prognosis and restorability post-procedure.  
**Notes:**  
- Excludes final restoration—use separate codes (e.g., D2940, D2950) for fillings or crowns.  
- Not for indirect pulp capping (see D3120) or cases requiring pulpal therapy (e.g., D3220).  
- Documentation should include pulp status and material used for insurance justification.  

#### Code: D3120
**Heading:** Pulp Cap — Indirect (excluding final restoration)  
**When to Use:**  
- The patient has a tooth with deep caries close to the pulp but no exposure, and a protective dressing is applied over the remaining dentin to protect the pulp and encourage remineralization.  
- Use when all caries are removed, leaving a thin dentin layer over the pulp.  
**What to Check:**  
- Confirm no pulp exposure via clinical exam or radiograph (e.g., thin dentin layer visible).  
- Assess caries removal completion before placing the protective material.  
- Verify the material used (e.g., calcium hydroxide, glass ionomer) supports pulp vitality.  
- Check for symptoms (e.g., sensitivity) indicating pulp health.  
**Notes:**  
- Excludes final restoration—code separately for restorative work (e.g., D2940, D2950).  
- Not for direct pulp capping (see D3110) or when used as a base/liner under routine fillings.  
- Not applicable if caries remain—ensure complete caries removal is documented.  

---

### Key Takeaways:
- **Direct vs. Indirect:** D3110 is for exposed pulp; D3120 is for near-exposure with a protective dentin layer.  
- **Restoration Exclusion:** Both codes exclude final restorations—use separate restorative codes.  
- **Caries Management:** D3120 requires complete caries removal; incomplete removal may necessitate other codes (e.g., D2940).  
- **Documentation:** Record pulp status, caries depth, and materials used to support coding and insurance claims.  
- **Procedure Intent:** Focus is on pulp preservation, not pulpal removal or extensive endodontic therapy.

Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_pulp_capping_code(self, scenario: str) -> str:
        """Extract pulp capping code(s) for a given scenario."""
        try:
            print(f"Analyzing pulp capping scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Pulp capping extract_pulp_capping_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in pulp capping code extraction: {str(e)}")
            return ""
    
    def activate_pulp_capping(self, scenario: str) -> str:
        """Activate the pulp capping analysis process and return results."""
        try:
            result = self.extract_pulp_capping_code(scenario)
            if not result:
                print("No pulp capping code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating pulp capping analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_pulp_capping(scenario)
        print(f"\n=== PULP CAPPING ANALYSIS RESULT ===")
        print(f"PULP CAPPING CODE: {result if result else 'None'}")

pulpcapping_service = PulpCappingServices()
# # Example usage
# if __name__ == "__main__":
#     pulp_capping_service = PulpCappingServices()
#     scenario = input("Enter a pulp capping dental scenario: ")
#     pulp_capping_service.run_analysis(scenario)