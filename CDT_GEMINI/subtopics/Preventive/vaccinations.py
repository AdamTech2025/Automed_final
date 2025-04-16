"""
Module for extracting vaccination codes.
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

class VaccinationsServices:
    """
    Class for extracting vaccination codes.
    """
    
    def __init__(self, llm_service: LLMService = None):
        """
        Initialize the VaccinationsServices class.
        
        Args:
            llm_service (LLMService, optional): LLM service instance. Defaults to None.
        """
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
        
    def _create_prompt_template(self) -> PromptTemplate:
        """
        Create a LangChain-based prompt template for vaccination code extraction.
        
        Returns:
            PromptTemplate: A configured prompt template for vaccination code extraction.
        """
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert

 Before picking a code, ask:
- What was the primary reason the patient came in? Was it for a preventive vaccination, or to address a specific health concern?
- Which vaccine is being administered (e.g., Pfizer, Moderna, AstraZeneca, Janssen, HPV), and what dose in the series (first, second, third, booster)?
- Is the patient pediatric or adult, and does the dosage align with their age group or formulation (e.g., tris-sucrose pediatric)?
- Are there any contraindications, allergies, or prior vaccine reactions in the patient's medical history?
- Is this a standard vaccination procedure, or does it require a narrative report (e.g., D1999 for unspecified cases)?

---

### Preventive Dental Codes: Vaccinations

#### Code: D1701 - Pfizer-BioNTech Covid-19 Vaccine Administration — First Dose
- **When to use:**
  - Administration of the first dose of Pfizer-BioNTech Covid-19 vaccine (mRNA, 30mcg/0.3mL, intramuscular).
  - Part of the initial two-dose series for Covid-19 prevention.
- **What to check:**
  - Confirm patient eligibility (age 12+ for standard formulation) and no prior Covid-19 vaccination.
  - Verify vaccine type, dosage (30mcg/0.3mL), and intramuscular administration.
  - Review medical history for allergies (e.g., polyethylene glycol) or contraindications.
- **Notes:**
  - Specific to first dose—document lot number, injection site, and patient consent.
  - Typically administered in a dental office as part of public health efforts.
  - Schedule second dose (D1702) approximately 21 days later.

#### Code: D1702 - Pfizer-BioNTech Covid-19 Vaccine Administration — Second Dose
- **When to use:**
  - Administration of the second dose of Pfizer-BioNTech Covid-19 vaccine (mRNA, 30mcg/0.3mL, intramuscular).
  - Completes the initial two-dose series.
- **What to check:**
  - Confirm first dose (D1701) was given 21 days prior (±4 days per CDC guidelines).
  - Verify same vaccine type and dosage as first dose.
  - Assess for adverse reactions from the first dose.
- **Notes:**
  - Document completion of primary series and any side effects observed.
  - Not for boosters or third doses—use D1708/D1709 for those.
  - Patient education on post-vaccination care is key.

#### Code: D1703 - Moderna Covid-19 Vaccine Administration — First Dose
- **When to use:**
  - Administration of the first dose of Moderna Covid-19 vaccine (mRNA, 100mcg/0.5mL, intramuscular).
  - Initiates the two-dose series for Covid-19 prevention.
- **What to check:**
  - Confirm patient eligibility (age 18+) and no prior Covid-19 vaccination.
  - Verify vaccine type, dosage (100mcg/0.5mL), and intramuscular delivery.
  - Check for allergies (e.g., polysorbate) or medical contraindications.
- **Notes:**
  - Specific to first dose—record administration details and patient response.
  - Schedule second dose (D1704) approximately 28 days later.
  - Distinct from Pfizer due to higher dosage and different mRNA platform.

#### Code: D1704 - Moderna Covid-19 Vaccine Administration — Second Dose
- **When to use:**
  - Administration of the second dose of Moderna Covid-19 vaccine (mRNA, 100mcg/0.5mL, intramuscular).
  - Completes the initial two-dose series.
- **What to check:**
  - Confirm first dose (D1703) was given 28 days prior (±4 days).
  - Verify consistent vaccine type and dosage with first dose.
  - Assess for prior dose reactions or new health changes.
- **Notes:**
  - Marks full vaccination status—document thoroughly.
  - Not for boosters or third doses—use D1710/D1711 instead.
  - Monitor for side effects, which may be stronger than first dose.

#### Code: D1705 - AstraZeneca Covid-19 Vaccine Administration — First Dose
- **When to use:**
  - Administration of the first dose of AstraZeneca Covid-19 vaccine (rS-ChAdOx1, 5x10¹⁰ VP/0.5mL, intramuscular).
  - Starts the two-dose series for Covid-19 prevention.
- **What to check:**
  - Confirm patient eligibility and no prior Covid-19 vaccination.
  - Verify vaccine type (viral vector), dosage, and intramuscular administration.
  - Review for contraindications (e.g., history of thrombosis).
- **Notes:**
  - Specific to first dose—note viral vector platform vs. mRNA vaccines.
  - Schedule second dose (D1706) 4-12 weeks later per protocol.
  - Less common in some regions; verify availability and approval.

#### Code: D1706 - AstraZeneca Covid-19 Vaccine Administration — Second Dose
- **When to use:**
  - Administration of the second dose of AstraZeneca Covid-19 vaccine (rS-ChAdOx1, 5x10¹⁰ VP/0.5mL, intramuscular).
  - Completes the two-dose series.
- **What to check:**
  - Confirm first dose (D1705) was given 4-12 weeks prior.
  - Verify same vaccine type and dosage as first dose.
  - Assess for adverse events from the first dose (e.g., clotting risks).
- **Notes:**
  - Document completion of series and patient tolerance.
  - Not for boosters—use narrative or other codes if applicable.
  - Educate on potential delayed side effects.

#### Code: D1707 - Janssen Covid-19 Vaccine Administration — Single Dose
- **When to use:**
  - Administration of the single-dose Janssen Covid-19 vaccine (Ad26, 5x10¹⁰ VP/0.5mL, intramuscular).
  - Provides full vaccination in one visit.
- **What to check:**
  - Confirm patient eligibility (age 18+) and no prior Covid-19 vaccination.
  - Verify vaccine type (viral vector), dosage, and single-dose protocol.
  - Check for contraindications (e.g., clotting disorders).
- **Notes:**
  - Single-dose code—document as complete vaccination.
  - No second dose required; boosters use D1712.
  - Ideal for patients needing rapid immunization.

#### Code: D1708 - Pfizer-BioNTech Covid-19 Vaccine Administration — Third Dose
- **When to use:**
  - Administration of a third dose of Pfizer-BioNTech Covid-19 vaccine (mRNA, 30mcg/0.3mL, intramuscular).
  - For immunocompromised patients needing additional primary dosing.
- **What to check:**
  - Confirm completion of two-dose series (D1701, D1702) and immunocompromised status.
  - Verify timing (at least 28 days after second dose) and same dosage.
  - Assess medical justification (e.g., cancer, organ transplant).
- **Notes:**
  - Not a booster—specific to third primary dose; document condition.
  - Distinct from D1709 (booster for general population).
  - Requires prior authorization in some cases.

#### Code: D1709 - Pfizer-BioNTech Covid-19 Vaccine Administration — Booster Dose
- **When to use:**
  - Administration of a booster dose of Pfizer-BioNTech Covid-19 vaccine (mRNA, 30mcg/0.3mL, intramuscular).
  - Enhances immunity post-primary series.
- **What to check:**
  - Confirm two-dose series completed at least 6 months prior.
  - Verify patient eligibility (e.g., age 12+, risk factors) per guidelines.
  - Ensure same vaccine type and dosage as primary series.
- **Notes:**
  - Booster-specific—document prior vaccination dates.
  - Not for immunocompromised third doses (use D1708).
  - Monitor for booster-specific side effects.

#### Code: D1710 - Moderna Covid-19 Vaccine Administration — Third Dose
- **When to use:**
  - Administration of a third dose of Moderna Covid-19 vaccine (mRNA, 100mcg/0.5mL, intramuscular).
  - For immunocompromised patients as part of the primary series.
- **What to check:**
  - Confirm two-dose series (D1703, D1704) and immunocompromised condition.
  - Verify timing (at least 28 days after second dose) and dosage.
  - Assess medical need (e.g., HIV, immunosuppression).
- **Notes:**
  - Third primary dose—document clinical rationale.
  - Not a booster—use D1711 for boosters.
  - May require insurance pre-approval.

#### Code: D1711 - Moderna Covid-19 Vaccine Administration — Booster Dose
- **When to use:**
  - Administration of a booster dose of Moderna Covid-19 vaccine (mRNA, 50mcg/0.25mL, intramuscular).
  - Boosts immunity after primary series.
- **What to check:**
  - Confirm two-dose series completed at least 6 months prior.
  - Verify reduced dosage (50mcg/0.25mL) vs. primary doses.
  - Check eligibility (e.g., age 18+, risk factors).
- **Notes:**
  - Booster-specific—note lower dose than primary series.
  - Document prior vaccination and timing.
  - Distinct from third dose (D1710) for immunocompromised.

#### Code: D1712 - Janssen Covid-19 Vaccine Administration — Booster Dose
- **When to use:**
  - Administration of a booster dose of Janssen Covid-19 vaccine (Ad26, 5x10¹⁰ VP/0.5mL, intramuscular).
  - Enhances immunity post-single dose.
- **What to check:**
  - Confirm single dose (D1707) given at least 2 months prior.
  - Verify same vaccine type and dosage for booster.
  - Assess eligibility per current guidelines.
- **Notes:**
  - Booster-specific—document initial dose date.
  - May be used with heterologous boosting (check payer rules).
  - Monitor for rare side effects (e.g., thrombosis).

#### Code: D1713 - Pfizer-BioNTech Covid-19 Vaccine Administration Tris-Sucrose Pediatric — First Dose
- **When to use:**
  - Administration of the first dose of Pfizer-BioNTech pediatric Covid-19 vaccine (mRNA, 10mcg/0.2mL, tris-sucrose, intramuscular).
  - For children aged 5-11 in a two-dose series.
- **What to check:**
  - Confirm patient age (5-11) and no prior vaccination.
  - Verify pediatric formulation (10mcg/0.2mL) with tris-sucrose buffer.
  - Review for allergies or contraindications specific to children.
- **Notes:**
  - Age-specific—document lot number and injection site.
  - Use orange cap vials (distinct from adult/adolescent purple cap).
  - Schedule second dose (D1714) 21 days later.

#### Code: D1714 - Pfizer-BioNTech Covid-19 Vaccine Administration Tris-Sucrose Pediatric — Second Dose
- **When to use:**
  - Administration of the second dose of Pfizer-BioNTech pediatric Covid-19 vaccine (mRNA, 10mcg/0.2mL, tris-sucrose, intramuscular).
  - Completes the primary series for children aged 5-11.
- **What to check:**
  - Confirm first dose (D1713) given 21 days prior (±4 days).
  - Verify correct pediatric formulation and dosage.
  - Assess for reactions to the first dose.
- **Notes:**
  - Marks completion of pediatric primary series.
  - Document using same color cap vial as first dose (orange).
  - Parent education on side effects and post-vaccination care is essential.

#### Code: D9997 - Dental Case Management — Patients With Special Health Care Needs
- **When to use:**
  - Additional coordination of oral health care services for patients with special needs.
  - May include integration with vaccine administration for high-risk patients.
- **What to check:**
  - Confirm patient has documented special health care needs affecting dental care.
  - Verify additional time/resources were required (e.g., coordination with PCP).
  - Assess if case management was directly related to vaccination.
- **Notes:**
  - Not specific to vaccines; documents complex care coordination.
  - May be used alongside vaccine codes if applicable.
  - Requires documentation of special needs and coordination efforts.

---

### Key Takeaways:
- COVID-19 vaccine codes are specific to the manufacturer, dose number, and formulation.
- Proper documentation of vaccine details (lot, site, patient consent) is crucial.
- Pediatric formulations have dedicated codes distinct from adult versions.
- Boosters and third doses have separate codes based on clinical indication.
- Case management codes may apply for patients with special needs requiring vaccination.
- Always verify the latest CDC and regulatory guidance before administering vaccines in dental settings.

SCENARIO: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_vaccinations_code(self, scenario: str) -> str:
        """
        Extract the appropriate vaccination code based on a clinical scenario.
        
        Args:
            scenario (str): The clinical scenario to analyze.
            
        Returns:
            str: The extracted vaccination code or empty string if none found.
        """
        try:
            print(f"Analyzing vaccination scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Vaccination extract_vaccinations_code result: {code}")
            return code
        except Exception as e:
            print(f"Error in vaccination code extraction: {str(e)}")
            return ""
    
    def activate_vaccinations(self, scenario: str) -> str:
        """
        Activate the vaccination code extraction process and return results.
        
        Args:
            scenario (str): The clinical scenario to analyze.
            
        Returns:
            str: The extracted vaccination code or empty string if none found.
        """
        try:
            result = self.extract_vaccinations_code(scenario)
            if not result:
                print("No vaccination code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating vaccination analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """
        Run the analysis and print results.
        
        Args:
            scenario (str): The clinical scenario to analyze.
        """
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_vaccinations(scenario)
        print(f"\n=== VACCINATION ANALYSIS RESULT ===")
        print(f"VACCINATION CODE: {result if result else 'None'}")


vaccinations_service = VaccinationsServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a vaccination dental scenario: ")
    vaccinations_service.run_analysis(scenario) 