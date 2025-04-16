"""
Module for extracting other preventive services codes.
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

class OtherPreventiveServices:
    """Class to analyze and extract other preventive services codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing other preventive services."""
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert

 Before picking a code, ask:
- What was the primary reason the patient came in? Was it for routine prevention, or to address a specific risk factor like caries, periodontal disease, or substance use?
- What is the patient's risk profile? Are they at high risk for caries, oral disease, or behavioral health issues?
- Is the service educational (counseling/instructions) or a physical intervention (sealant/medicament)?
- Does the patient's dental or medical history support the need for this preventive measure?
- Are there specific teeth or conditions targeted, or is this a general preventive service?

---

### Preventive Dental Codes: Other Preventive Services

#### Code: D1310 - Nutritional Counseling for Control of Dental Disease
- **When to use:**
  - Patient receives counseling on diet and food choices to manage caries or periodontal disease.
  - Part of a preventive or treatment plan for patients with dietary-related oral health risks.
- **What to check:**
  - Assess patient's dietary habits (e.g., sugar intake, acidic foods) linked to caries or gum issues.
  - Confirm counseling is specific to dental disease control, not general nutrition advice.
  - Review dental history for active caries or periodontal conditions justifying the service.
- **Notes:**
  - Requires documentation of specific dietary recommendations and their oral health impact.
  - Not for casual diet chats—must tie directly to caries/periodontal management.
  - Often paired with other preventive or therapeutic codes but billed separately.

#### Code: D1320 - Tobacco Counseling for the Control and Prevention of Oral Disease
- **When to use:**
  - Patient receives tobacco cessation or prevention counseling to reduce oral disease risk.
  - Aimed at improving outcomes for dental therapies affected by tobacco use.
- **What to check:**
  - Verify patient's tobacco use history (e.g., smoking, chewing) and related oral findings.
  - Ensure counseling addresses specific oral risks (e.g., cancer, periodontal disease).
  - Check if cessation aids or referrals were provided as part of the session.
- **Notes:**
  - Documentation must link tobacco use to oral health risks and detail counseling content.
  - Not for general health advice—focus is on oral disease prevention/control.
  - May apply to current users or those at risk of starting tobacco use.

#### Code: D1321 - Counseling for High-Risk Substance Use
- **When to use:**
  - Patient receives education on oral, behavioral, and systemic effects of high-risk substance use (e.g., alcohol, opioids, cannabis, vaping).
  - Targets prevention or management of substance-related oral health issues.
- **What to check:**
  - Identify patient's substance use patterns and administration methods (e.g., inhaling, ingesting).
  - Assess oral signs like enamel erosion, xerostomia, or soft tissue damage tied to substance use.
  - Confirm counseling addresses specific health effects, not just general warnings.
- **Notes:**
  - Broader than D1320—includes various substances beyond tobacco.
  - Requires detailed notes on substances discussed and their oral/systemic impact.
  - Useful for patients with addiction history or emerging high-risk behaviors.

#### Code: D1330 - Oral Hygiene Instructions
- **When to use:**
  - Patient receives personalized home care instructions (e.g., brushing, flossing techniques).
  - Part of preventive education to improve oral hygiene practices.
- **What to check:**
  - Evaluate patient's current oral hygiene skills and areas needing improvement.
  - Confirm instructions are tailored (e.g., use of interdental brushes, specific techniques).
  - Check if aids like floss or mouthwash were demonstrated or recommended.
- **Notes:**
  - Not for casual advice—must involve structured, patient-specific guidance.
  - Documentation should list techniques taught and any tools suggested.
  - Often provided during prophylaxis or recall visits but coded separately.

#### Code: D1351 - Sealant — Per Tooth
- **When to use:**
  - Sealant applied to a mechanically/chemically prepared enamel surface to prevent decay.
  - Typically for permanent molars in caries-prone patients (often children/teens).
- **What to check:**
  - Confirm tooth is caries-free and sealant-eligible (e.g., deep pits/fissures).
  - Verify preparation method (e.g., etching) and sealant material used.
  - Assess patient's caries risk to justify the procedure.
- **Notes:**
  - Per-tooth code—bill separately for each tooth treated.
  - Not for teeth with existing restorations or decay extending into dentin.
  - Documentation must specify tooth number and sealant application details.

#### Code: D1352 - Preventive Resin Restoration (Moderate to High Caries Risk) — Permanent Tooth
- **When to use:**
  - Conservative restoration of an active cavitated lesion in a pit/fissure, not into dentin.
  - Includes sealant placement in non-carious radiating fissures/pits.
- **What to check:**
  - Confirm lesion is active but shallow (enamel-only, no dentin involvement).
  - Verify patient's moderate-to-high caries risk status.
  - Ensure procedure includes both restoration and sealant components.
- **Notes:**
  - For permanent teeth only; bridges preventive and restorative care.
  - Requires documentation of caries risk, lesion location, and materials used.
  - Distinct from D1351—addresses early decay, not just prevention.

#### Code: D1353 - Sealant Repair — Per Tooth
- **When to use:**
  - Repair or replacement of a previously placed sealant that's damaged or lost.
  - Applied to maintain decay prevention on a specific tooth.
- **What to check:**
  - Confirm prior sealant placement and current condition (e.g., chipped, worn).
  - Assess tooth for caries or new risk factors since original sealant.
  - Verify repair method (e.g., re-etching, new sealant application).
- **Notes:**
  - Per-tooth code—document tooth number and repair specifics.
  - Not for initial sealant placement (use D1351) or extensive decay.
  - Insurance may require proof of prior sealant and time since application.

#### Code: D1354 - Application of Caries Arresting Medicament — Per Tooth
- **When to use:**
  - Topical application of a caries-arresting agent (e.g., silver diamine fluoride) to an active, non-symptomatic lesion.
  - No mechanical removal of sound tooth structure involved.
- **What to check:**
  - Confirm lesion is active but asymptomatic (no pain or sensitivity).
  - Verify medicament used (e.g., SDF) and application method.
  - Assess tooth condition—must be unrestored or minimally restored.
- **Notes:**
  - Per-tooth code—document tooth number and medicament type.
  - Conservative approach; not for symptomatic teeth needing restoration.
  - Patient consent advised due to potential staining (e.g., with SDF).

#### Code: D1355 - Caries Preventive Medicament Application — Per Tooth
- **When to use:**
  - Application of a medicament for primary prevention or remineralization (e.g., non-fluoride agents).
  - Not for caries arrest (D1354) or topical fluoride (D1206/D1208).
- **What to check:**
  - Confirm purpose is prevention/remineralization, not treatment of active caries.
  - Verify medicament is non-fluoride (e.g., calcium phosphate products).
  - Assess enamel condition for early demineralization signs.
- **Notes:**
  - Per-tooth code—specify tooth and agent used in documentation.
  - Distinct from fluoride codes (D1206/D1208) and caries arrest (D1354).
  - Often used in high-risk patients before visible caries develop.

---

### Key Takeaways:
- *Counseling vs. Application:* D1310-D1330 focus on education; D1351-D1355 involve physical interventions—match intent to code.
- *Risk-Based Coding:* Patient's caries or disease risk drives code selection (e.g., D1352 for high-risk patients).
- *Per-Tooth Specificity:* Codes like D1351-D1355 require tooth numbers and detailed notes for billing accuracy.
- *Patient Education:* Counseling codes (D1310-D1321) enhance outcomes but need specific oral health ties to justify use.
- *Documentation Precision:* Link services to patient history, risk factors, and procedure details to support claims.

Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_other_preventive_services_code(self, scenario: str) -> str:
        """Extract other preventive services code(s) for a given scenario."""
        try:
            print(f"Analyzing other preventive services scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Other preventive services extract_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in other preventive services code extraction: {str(e)}")
            return ""
    
    def activate_other_preventive_services(self, scenario: str) -> str:
        """Activate the other preventive services analysis process and return results."""
        try:
            result = self.extract_other_preventive_services_code(scenario)
            if not result:
                print("No other preventive services code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating other preventive services analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_other_preventive_services(scenario)
        print(f"\n=== OTHER PREVENTIVE SERVICES ANALYSIS RESULT ===")
        print(f"OTHER PREVENTIVE SERVICES CODE: {result if result else 'None'}")

other_preventive_service = OtherPreventiveServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter an other preventive services dental scenario: ")
    other_preventive_service.run_analysis(scenario) 