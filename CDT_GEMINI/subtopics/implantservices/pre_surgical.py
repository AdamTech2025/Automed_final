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

class PreSurgicalImplantServices:
    """Class to analyze and extract pre-surgical implant services codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing pre-surgical implant services."""
        return PromptTemplate(
            template=f"""
You are a dental coding expert specializing in implant services.

### Before Picking a Code, Ask:
- Is a radiographic/surgical implant index being created for treatment planning or implant placement?
- What is the purpose of the index in the overall treatment plan?
- Will the index be used during radiographic exposure, treatment planning, or during the surgical procedure?
- Does the index relate osteotomy or fixture position to existing anatomic structures?
- Is this creating a guide for a single implant or multiple implants?
- Will this index be used for both diagnosis and surgical guidance?

---

### Pre-Surgical Implant Services

#### Code: D6190
**Heading:** Radiographic/surgical implant index, by report  
**When to Use:**  
- A specialized appliance is created to relate osteotomy or fixture position to existing anatomic structures during pre-surgical planning and/or implant placement.  
- Use for radiographic assessment, treatment planning, or surgical guidance.  
**What to Check:**  
- Confirm the index's purpose (radiographic, surgical, or both) via treatment plan.  
- Verify fabrication details (e.g., CBCT-based, 3D-printed) and materials.  
- Assess anatomic references (e.g., nerve, sinus, teeth) and implant count.  
- Ensure narrative details creation process and clinical use.  
**Notes:**  
- Enhances precision for complex cases (e.g., multiple implants, limited bone).  
- Requires detailed narrative specifying purpose, fabrication, and anatomy.  
- Not for routine planning or standard radiographs.  
- Document index type, materials, and prosthetic integration.  

---

### Key Takeaways:
- **Precision Tool:** D6190 is for radiographic/surgical indices guiding implant placement relative to critical anatomy (e.g., nerve, sinus).  
- **Narrative Critical:** Requires a detailed report on fabrication, materials, and clinical use.  
- **Complex Cases:** Used for multiple implants, compromised bone, or high-risk anatomy.  
- **Diagnostic and Surgical:** May serve planning (CBCT integration) and/or surgery (guided placement).  
- **Distinct Service:** Separate from routine diagnostics or surgical procedures.  
- **Prosthetic Alignment:** Considers final prosthesis design for functional/esthetic outcomes.

Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_pre_surgical_code(self, scenario: str) -> str:
        """Extract pre-surgical implant services code(s) for a given scenario."""
        try:
            print(f"Analyzing pre-surgical implant scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Pre-surgical extract_pre_surgical_code result: {code}")
            if code.lower() in ["none", "", "not applicable"]:
                return ""
            return code
        except Exception as e:
            print(f"Error in pre-surgical code extraction: {str(e)}")
            return ""
    
    def activate_pre_surgical(self, scenario: str) -> str:
        """Activate the pre-surgical implant services analysis process and return results."""
        try:
            result = self.extract_pre_surgical_code(scenario)
            if not result:
                print("No pre-surgical implant code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating pre-surgical implant analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_pre_surgical(scenario)
        print(f"\n=== PRE-SURGICAL IMPLANT SERVICES ANALYSIS RESULT ===")
        print(f"PRE-SURGICAL IMPLANT CODE: {result if result else 'None'}")

# Create the pre_surgical_service instance at module level
pre_surgical_service = PreSurgicalImplantServices()

# Example usage
if __name__ == "__main__":
    scenario = input("Enter a pre-surgical implant services dental scenario: ")
    pre_surgical_service.run_analysis(scenario)