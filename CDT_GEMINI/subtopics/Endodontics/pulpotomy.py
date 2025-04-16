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

class PulpotomyServices:
    """Class to analyze and extract pulpotomy codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing pulpotomy procedures."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert

### Before Picking a Code, Ask:
- What was the primary reason the patient came in? Was it a routine visit, pain, or trauma?
- Is the procedure being performed on a primary or permanent tooth?
- Is this a therapeutic procedure to maintain pulp vitality or a temporary measure for pain relief?
- Does the tooth have incomplete root development (relevant for permanent teeth)?
- Is the procedure an emergency intervention or part of a planned treatment?

---

### Pulpotomy Codes

#### Code: D3220
**Heading:** Therapeutic pulpotomy (excluding final restoration) — removal of pulp coronal to the dentinocemental junction and application of medicament  
**When to Use:**  
- The patient has a primary or permanent tooth with a deep carious lesion or trauma requiring removal of the coronal pulp to preserve the vitality of the remaining radicular pulp.  
- A medicament (e.g., formocresol, MTA) is applied to maintain pulp health.  
- Use for therapeutic treatment, not as a precursor to root canal therapy.  
**What to Check:**  
- Confirm the tooth type (primary or permanent) via clinical exam or radiograph.  
- Assess pulp vitality (e.g., partial vitality with no necrosis in radicular pulp).  
- Verify the procedure is standalone and not the first stage of root canal therapy.  
- Check for contraindications (e.g., extensive pulp necrosis requiring root canal).  
**Notes:**  
- Excludes final restoration—use separate codes (e.g., D2940, D2930) for fillings or crowns.  
- Not for permanent teeth with incomplete root development (see D3222).  
- Not for apexogenesis or root canal preparation—document intent to maintain vitality.  

#### Code: D3221
**Heading:** Pulpal debridement, primary and permanent teeth  
**When to Use:**  
- The patient presents with acute pain in a primary or permanent tooth, and coronal pulp is removed to provide temporary relief prior to planned root canal therapy.  
- Use as an emergency or interim procedure when root canal therapy is not completed on the same day.  
**What to Check:**  
- Confirm acute pain or infection necessitating immediate intervention via exam or history.  
- Assess whether root canal therapy is planned but not initiated/completed same-day.  
- Verify the tooth’s condition (e.g., irreversible pulpitis, partial necrosis) supports debridement.  
- Check patient symptoms and consent for follow-up treatment.  
**Notes:**  
- Not for cases where root canal therapy (e.g., D3310-D3330) is completed same-day.  
- Often followed by endodontic codes—document as a temporary measure.  
- Requires clear documentation of pain and interim intent for insurance.  

#### Code: D3222
**Heading:** Partial pulpotomy for apexogenesis — permanent tooth with incomplete root development  
**When to Use:**  
- The patient has a permanent tooth with an immature apex (open root) and a vital pulp, where the coronal pulp is partially removed to promote continued root development (apexogenesis).  
- A medicament is applied to preserve pulp vitality and encourage dentin formation.  
- Use for young patients with incomplete root development, not as a root canal step.  
**What to Check:**  
- Confirm the tooth is permanent with an open apex via radiograph (e.g., wide canal, thin walls).  
- Assess pulp vitality and minimal coronal involvement (e.g., caries, trauma).  
- Verify patient age (typically 6-18) and tooth suitability for apexogenesis.  
- Check that the procedure aims to maintain vitality, not prepare for root canal.  
**Notes:**  
- Excludes final restoration—code separately (e.g., D2940, D2950).  
- Not for primary teeth or mature permanent teeth (use D3220 for primary).  
- Requires X-rays and a narrative to document immature apex and treatment goal.  

---

### Key Takeaways:
- **Tooth Type:** D3220 applies to primary or permanent teeth; D3222 is only for permanent teeth with immature roots.  
- **Therapeutic vs. Temporary:** D3220 and D3222 aim to preserve pulp vitality; D3221 is for temporary pain relief before root canal.  
- **Restoration Exclusion:** All codes exclude final restorations—use separate restorative codes.  
- **Apexogenesis Specificity:** D3222 is distinct for promoting root development, not routine pulpotomy.  
- **Documentation:** Clearly note tooth type, pulp status, and procedure intent (therapeutic, temporary, or apexogenesis) for insurance.

Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_pulpotomy_code(self, scenario: str) -> str:
        """Extract pulpotomy code(s) for a given scenario."""
        try:
            print(f"Analyzing pulpotomy scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Pulpotomy extract_pulpotomy_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in pulpotomy code extraction: {str(e)}")
            return ""
    
    def activate_pulpotomy(self, scenario: str) -> str:
        """Activate the pulpotomy analysis process and return results."""
        try:
            result = self.extract_pulpotomy_code(scenario)
            if not result:
                print("No pulpotomy code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating pulpotomy analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_pulpotomy(scenario)
        print(f"\n=== PULPOTOMY ANALYSIS RESULT ===")
        print(f"PULPOTOMY CODE: {result if result else 'None'}")

pulpotomy_service = PulpotomyServices()
# Example usage
if __name__ == "__main__":
    pulpotomy_service = PulpotomyServices()
    scenario = input("Enter a pulpotomy dental scenario: ")
    pulpotomy_service.run_analysis(scenario)