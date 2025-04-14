"""
Module for extracting vaccination codes.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from subtopics.prompt.prompt import PROMPT
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file

# Load environment variables
load_dotenv()

# Get model name from environment variable, default to gpt-4o if not set
 
def create_vaccinations_extractor(temperature=0.0):
    """
    Create a LangChain-based vaccinations code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert

 Before picking a code, ask:
- What was the primary reason the patient came in? Was it for a preventive vaccination, or to address a specific health concern?
- Which vaccine is being administered (e.g., Pfizer, Moderna, AstraZeneca, Janssen, HPV), and what dose in the series (first, second, third, booster)?
- Is the patient pediatric or adult, and does the dosage align with their age group or formulation (e.g., tris-sucrose pediatric)?
- Are there any contraindications, allergies, or prior vaccine reactions in the patient’s medical history?
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
  - Verify pediatric formulation (10mcg/0.2mL, tris-sucrose buffer).
  - Check for allergies or contraindications specific to children.
- **Notes:**
  - Pediatric-specific—document age and dose details.
  - Schedule second dose (D1714) 21 days later.
  - Distinct from adult formulation (D1701).

#### Code: D1714 - Pfizer-BioNTech Covid-19 Vaccine Administration Tris-Sucrose Pediatric — Second Dose
- **When to use:**
  - Administration of the second dose of Pfizer-BioNTech pediatric Covid-19 vaccine (mRNA, 10mcg/0.2mL, tris-sucrose, intramuscular).
  - Completes the pediatric two-dose series.
- **What to check:**
  - Confirm first dose (D1713) given 21 days prior.
  - Verify same pediatric formulation and dosage.
  - Assess for reactions from the first dose.
- **Notes:**
  - Marks full vaccination for ages 5-11—document thoroughly.
  - Not for adult doses or boosters.
  - Educate parents on post-vaccination monitoring.

#### Code: D1781 - Vaccine Administration — Human Papillomavirus — Dose 1
- **When to use:**
  - Administration of the first dose of HPV vaccine (Gardasil 9, 0.5mL, intramuscular).
  - Prevents HPV-related diseases (e.g., oral cancers).
- **What to check:**
  - Confirm patient eligibility (typically ages 9-45) and no prior HPV vaccination.
  - Verify vaccine type (Gardasil 9) and dosage (0.5mL).
  - Check for allergies (e.g., yeast) or contraindications.
- **Notes:**
  - First of 2-3 dose series—document schedule (e.g., 0, 2, 6 months).
  - Relevant in dentistry due to oral cancer prevention.
  - Schedule second dose (D1782) accordingly.

#### Code: D1782 - Vaccine Administration — Human Papillomavirus — Dose 2
- **When to use:**
  - Administration of the second dose of HPV vaccine (Gardasil 9, 0.5mL, intramuscular).
  - Part of the HPV vaccination series.
- **What to check:**
  - Confirm first dose (D1781) given (e.g., 1-2 months prior).
  - Verify same vaccine type and dosage.
  - Assess for prior dose reactions.
- **Notes:**
  - Second dose timing varies (e.g., 2 months if <15, 6 months if older).
  - Document progress in series and patient tolerance.
  - May complete series for younger patients; third dose (D1783) for others.

#### Code: D1783 - Vaccine Administration — Human Papillomavirus — Dose 3
- **When to use:**
  - Administration of the third dose of HPV vaccine (Gardasil 9, 0.5mL, intramuscular).
  - Completes the three-dose series for full immunity.
- **What to check:**
  - Confirm two prior doses (D1781, D1782) and timing (e.g., 6 months after first).
  - Verify consistent vaccine type and dosage.
  - Check for adverse reactions from earlier doses.
- **Notes:**
  - Required for patients starting series at age 15+ or immunocompromised.
  - Document completion and educate on long-term benefits.
  - Not needed if two-dose schedule applies (ages 9-14).

#### Code: D1999 - Unspecified Preventive Procedure, By Report
- **When to use:**
  - For a preventive procedure not adequately described by existing codes.
  - Requires a narrative report to justify its use (e.g., unique vaccination scenario).
- **What to check:**
  - Confirm no specific code applies to the procedure performed.
  - Assess the preventive nature and patient need (e.g., experimental vaccine).
  - Prepare detailed documentation explaining the service.
- **Notes:**
  - Narrative required—include procedure details, rationale, and materials.
  - Payer approval may vary; pre-authorization recommended.
  - Use sparingly when standard codes (e.g., D1701-D1783) don’t fit.

---

### Key Takeaways:
- *Vaccine Specificity:* Codes are tied to manufacturer, dose number, and formulation (e.g., pediatric vs. adult, mRNA vs. viral vector)—match precisely.
- *Dose Sequence Matters:* Differentiate between primary series (first/second/third), boosters, and single-dose vaccines for accurate coding.
- *Age and Eligibility:* Pediatric (D1713, D1714) and adult doses vary—verify patient age and formulation.
- *Patient Education:* Inform patients of series timing, side effects, and follow-up needs, though not billable under these codes.
- *Documentation Precision:* Record vaccine type, lot number, dose number, injection site, and patient response to support claims and audits.


Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_vaccinations_code(scenario, temperature=0.0):
    """
    Extract vaccinations code(s) for a given scenario.
    """
    try:
        chain = create_vaccinations_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Vaccinations code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_vaccinations_code: {str(e)}")
        return ""

def activate_vaccinations(scenario):
    """
    Activate vaccinations analysis and return results.
    """
    try:
        return extract_vaccinations_code(scenario)
    except Exception as e:
        print(f"Error in activate_vaccinations: {str(e)}")
        return "" 