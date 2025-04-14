"""
Module for extracting other periodontal services codes.
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
 
def create_other_periodontal_services_extractor(temperature=0.0):
    """
    Create a LangChain-based other periodontal services code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
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
- Performed at intervals determined by the dentist’s clinical evaluation, typically every 3-6 months, for the life of the dentition or implants.

**What to check:**
- Verify prior periodontal treatment in the patient’s chart (e.g., D4341, D4342, or surgical codes).
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
- Verify the provider performing the change isn’t affiliated with the original treating dentist’s practice.
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
- Documentation must specify quadrant(s), agent used, and clinical justification (e.g., “Q1 irrigated with 0.12% chlorhexidine due to localized gingivitis”).
- Not for full-mouth irrigation; use D4999 if no quadrant-specific code applies.

### D4999 - Unspecified Periodontal Procedure, By Report
**When to use:**
- For periodontal procedures not covered by specific CDT codes, requiring a detailed narrative to describe the service.
- Examples include experimental treatments, unique adjunctive therapies, or complex case-specific interventions.

**What to check:**
- Ensure no other periodontal code (e.g., D4910, D4341) accurately describes the procedure.
- Assess the clinical necessity and complexity of the service (e.g., unusual tools, techniques, or time required).
- Verify patient consent and understanding of the procedure’s purpose and potential out-of-pocket cost.

**Notes:**
- Requires a comprehensive report with procedure details, clinical findings, and justification for insurance submission.
- Common uses: laser therapy (if not coded elsewhere), custom splinting beyond D4322/D4323, or full-mouth irrigation not covered by D4921.
- Approval and reimbursement vary widely; pre-authorization is recommended.

### Key Takeaways:
- History Matters: D4910 hinges on prior periodontal therapy; always confirm the patient’s treatment background.
- Provider Specificity: D4920 is unique to external providers, making it situational and rare.
- Adjunct vs. Primary: D4921 and D4999 often support other treatments—clarify their role in the care plan.
- Narrative Precision: Unspecified (D4999) and less common codes (D4920, D4921) demand detailed documentation for approval.
- Maintenance vs. Treatment: Distinguish ongoing care (D4910) from acute interventions to avoid coding overlap.



Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_other_periodontal_services_code(scenario, temperature=0.0):
    """
    Extract other periodontal services code(s) for a given scenario.
    """
    try:
        chain = create_other_periodontal_services_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Other periodontal services code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_other_periodontal_services_code: {str(e)}")
        return ""

def activate_other_periodontal_services(scenario):
    """
    Activate other periodontal services analysis and return results.
    """
    try:
        return extract_other_periodontal_services_code(scenario)
    except Exception as e:
        print(f"Error in activate_other_periodontal_services: {str(e)}")
        return "" 