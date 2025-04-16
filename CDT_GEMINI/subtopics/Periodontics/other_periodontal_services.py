"""
Module for extracting other periodontal services codes.
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

class OtherPeriodontalServices:
    """Class to analyze and extract other periodontal services codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing other periodontal services."""
        return PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert

 Before picking a code, ask:
- What was the primary reason the patient came in? Is it ongoing periodontal maintenance, an unscheduled issue, or a specific periodontal concern?
- Has the patient undergone prior periodontal therapy (e.g., scaling/root planing or surgery) that influences the procedure?
- Is the procedure routine, therapeutic, or an adjunct to another treatment?
- Who is performing the service (treating dentist, staff, or another provider)?
- Are there clinical findings (e.g., inflammation, pocket depths) that justify the procedure?

### D4910 - Periodontal Maintenance
**When to use:**
- For patients with a history of periodontal therapy (e.g., scaling/root planing, surgery) who require ongoing maintenance to prevent disease recurrence.
- Performed at intervals determined by the dentist's clinical evaluation, typically every 3-6 months, for the life of the dentition or implants.

**What to check:**
- Verify prior periodontal treatment in the patient's chart (e.g., D4341, D4342, or surgical codes).
- Assess current periodontal status (pocket depths, bleeding on probing, plaque/calculus levels).
- Confirm the need for site-specific scaling/root planing or polishing based on clinical findings.

**Notes:**
- Includes supragingival and subgingival plaque/calculus removal, plus polishing; not a prophylaxis (D1110).
- If new periodontal disease is detected, additional codes (e.g., D4341, D4342) may apply instead.
- Documentation must specify prior therapy, interval justification, and areas treated to support insurance claims.

### D4920 - Unscheduled Dressing Change (By Someone Other Than Treating Dentist or Their Staff)
**When to use:**
- When a patient requires an unscheduled change of periodontal dressings (e.g., post-surgical packing) by a provider other than the original treating dentist or their staff.
- Typically applies in emergency or follow-up scenarios outside the treating office.

**What to check:**
- Confirm the patient had recent periodontal surgery requiring dressings (e.g., gingivectomy, flap surgery).
- Verify the provider performing the change isn't affiliated with the original treating dentist's practice.
- Assess the condition of the surgical site (e.g., healing, infection, dressing integrity).

**Notes:**
- Rare code; most dressing changes are handled by the treating dentist and bundled into surgical fees.
- Requires documentation of the surgical procedure date, reason for the unscheduled change (e.g., loose dressing, discomfort), and provider details.
- Not for routine dressing adjustments during planned follow-ups.

### D4921 - Gingival Irrigation with a Medicinal Agent — Per Quadrant
**When to use:**
- When a quadrant-specific irrigation with a medicinal agent (e.g., chlorhexidine) is performed to reduce inflammation or bacterial load in gingival tissues.
- Used as an adjunct to other periodontal treatments, not as a standalone procedure.

**What to check:**
- Identify the quadrant(s) with clinical signs of inflammation or infection (e.g., swelling, redness, suppuration).
- Confirm the medicinal agent used and its therapeutic purpose (e.g., antimicrobial, anti-inflammatory).
- Check if this follows or complements another procedure (e.g., scaling, surgery).

**Notes:**
- Not widely reimbursed by insurance unless paired with a primary procedure; narrative may be required.
- Documentation must specify quadrant(s), agent used, and clinical justification (e.g., "Q1 irrigated with 0.12% chlorhexidine due to localized gingivitis").
- Not for full-mouth irrigation; use D4999 if no quadrant-specific code applies.

### D4999 - Unspecified Periodontal Procedure, By Report
**When to use:**
- For periodontal procedures not covered by specific CDT codes, requiring a detailed narrative to describe the service.
- Examples include experimental treatments, unique adjunctive therapies, or complex case-specific interventions.

**What to check:**
- Ensure no other periodontal code (e.g., D4910, D4341) accurately describes the procedure.
- Assess the clinical necessity and complexity of the service (e.g., unusual tools, techniques, or time required).
- Verify patient consent and understanding of the procedure's purpose and potential out-of-pocket cost.

**Notes:**
- Requires a comprehensive report with procedure details, clinical findings, and justification for insurance submission.
- Common uses: laser therapy (if not coded elsewhere), custom splinting beyond D4322/D4323, or full-mouth irrigation not covered by D4921.
- Approval and reimbursement vary widely; pre-authorization is recommended.

### Key Takeaways:
- History Matters: D4910 hinges on prior periodontal therapy; always confirm the patient's treatment background.
- Provider Specificity: D4920 is unique to external providers, making it situational and rare.
- Adjunct vs. Primary: D4921 and D4999 often support other treatments—clarify their role in the care plan.
- Narrative Precision: Unspecified (D4999) and less common codes (D4920, D4921) demand detailed documentation for approval.
- Maintenance vs. Treatment: Distinguish ongoing care (D4910) from acute interventions to avoid coding overlap.

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
    )

    def extract_other_periodontal_services_code(self, scenario: str) -> str:
        """Extract other periodontal services code for a given scenario."""
        try:
            print(f"Analyzing other periodontal services scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Other periodontal services extract_other_periodontal_services_code result: {code}")
            return code
        except Exception as e:
                print(f"Error in other periodontal services code extraction: {str(e)}")
                return ""

    def activate_other_periodontal_services(self, scenario: str) -> str:
        """Activate the other periodontal services analysis process and return results."""
        try:
            result = self.extract_other_periodontal_services_code(scenario)
            if not result:
                print("No other periodontal services code returned")
                return ""
            return result
        except Exception as e:
                print(f"Error activating other periodontal services analysis: {str(e)}")
                return "" 
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_other_periodontal_services(scenario)
        print(f"\n=== OTHER PERIODONTAL SERVICES ANALYSIS RESULT ===")
        print(f"OTHER PERIODONTAL SERVICES CODE: {result if result else 'None'}")


other_periodontal_services = OtherPeriodontalServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter an other periodontal services scenario: ")
    other_periodontal_services.run_analysis(scenario) 