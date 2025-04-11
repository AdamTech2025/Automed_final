"""
Module for extracting non-surgical periodontal services codes.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from subtopics.prompt.prompt import PROMPT


# Load environment variables
load_dotenv()

# Get model name from environment variable, default to gpt-4o if not set
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o")

def create_non_surgical_services_extractor(temperature=0.0):
    """
    Create a LangChain-based non-surgical periodontal services code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert

Before picking a code, ask:
- What was the primary reason the patient came in? Was it routine maintenance, a specific periodontal complaint, or inflammation without periodontitis?
- Is there evidence of periodontal disease (e.g., bone loss, deep pockets) or just gingival inflammation?
- How many teeth or quadrants are affected by the condition?
- Is this a therapeutic procedure or a preparatory step for further evaluation/treatment?
- Are there any systemic health factors (e.g., diabetes) or medications affecting periodontal health?

### D4322 - Splint — Intra-Coronal; Natural Teeth or Prosthetic Crowns
**When to use:**
- When an additional procedure is performed to physically link individual teeth or prosthetic crowns intra-coronally (within the tooth structure) for stabilization and added strength.
- Typically used in cases of mobile teeth due to periodontal disease or trauma needing support.

**What to check:**
- Confirm the teeth or crowns involved are structurally sound enough for intra-coronal splinting.
- Assess the degree of mobility and periodontal status (e.g., pocket depths, bone loss).
- Verify patient’s bite and occlusion to ensure splinting won’t disrupt function.

**Notes:**
- This is not a standalone treatment; it’s an adjunct to periodontal therapy or restorative work.
- Requires precise documentation of the teeth involved and the method of splinting (e.g., composite, wire).
- Not appropriate if teeth are too compromised to support the splint.

### D4323 - Splint — Extra-Coronal; Natural Teeth or Prosthetic Crowns
**When to use:**
- When an additional procedure links teeth or prosthetic crowns extra-coronally (outside the tooth structure) to provide stabilization and strength.
- Used for periodontal support in cases of mobility or to reinforce prosthetic restorations.

**What to check:**
- Evaluate the periodontal health and mobility of the teeth to be splinted.
- Check for adequate crown height and surface area for extra-coronal attachment (e.g., bonding or clasps).
- Ensure no interference with occlusion or hygiene access post-splinting.

**Notes:**
- Differs from D4322 by being external rather than within the tooth structure.
- May involve temporary or permanent materials; specify in documentation.
- Patient must be educated on oral hygiene challenges with extra-coronal splints.

### D4341 - Periodontal Scaling and Root Planing — Four or More Teeth per Quadrant
**When to use:**
- For patients with diagnosed periodontal disease requiring therapeutic scaling and root planing on four or more teeth per quadrant.
- Indicated when there’s plaque, calculus, and rough root surfaces due to disease progression.

**What to check:**
- Confirm periodontal disease via charting (pocket depths ≥4mm, bleeding on probing, bone loss).
- Count the number of affected teeth per quadrant (must be 4+).
- Assess for systemic factors (e.g., diabetes) that may influence healing.

**Notes:**
- This is not a preventive procedure; it’s therapeutic and requires a periodontal diagnosis.
- May involve local anesthesia and multiple visits depending on severity.
- Documentation must include quadrant(s) treated and clinical findings (e.g., pocket depths pre- and post-treatment).

### D4342 - Periodontal Scaling and Root Planing — One to Three Teeth per Quadrant
**When to use:**
- For patients with periodontal disease affecting only 1-3 teeth per quadrant, requiring therapeutic scaling and root planing.
- Used when disease is localized rather than widespread in a quadrant.

**What to check:**
- Verify periodontal disease with clinical evidence (e.g., pocket depths, calculus, bone loss) on 1-3 teeth per quadrant.
- Ensure the rest of the quadrant doesn’t qualify for D4341 (4+ teeth).
- Check for adjacent tissue health to rule out broader inflammation.

**Notes:**
- Requires precise documentation of which teeth are treated and why (e.g., “Tooth #3, 5mm pocket with calculus”).
- Not for prophylaxis; must be tied to a periodontal diagnosis.
- May be a precursor to more extensive treatment if disease progresses.

### D4346 - Scaling in Presence of Generalized Moderate or Severe Gingival Inflammation — Full Mouth, After Oral Evaluation
**When to use:**
- For patients with generalized moderate to severe gingival inflammation (no periodontitis) needing full-mouth scaling after an oral evaluation.
- Indicated for swollen, inflamed gingiva, suprabony pockets, and moderate to severe bleeding on probing.

**What to check:**
- Confirm absence of periodontitis (no bone loss or attachment loss beyond gingivitis).
- Assess inflammation level (generalized, not localized) and bleeding on probing.
- Ensure an oral evaluation (e.g., D0120, D0140) precedes this procedure.

**Notes:**
- Cannot be reported with prophylaxis (D1110), scaling/root planing (D4341/D4342), or debridement (D4355).
- Focus is on removing plaque, calculus, and stains causing inflammation.
- Patient education on home care is critical post-treatment to prevent recurrence.

### D4355 - Full Mouth Debridement to Enable a Comprehensive Periodontal Evaluation and Diagnosis on a Subsequent Visit
**When to use:**
- When heavy plaque and calculus prevent a thorough periodontal evaluation, requiring full-mouth debridement as a preliminary step.
- Used to clear the way for a detailed exam/diagnosis on a later visit.

**What to check:**
- Assess the extent of plaque/calculus buildup obscuring periodontal assessment.
- Confirm that a comprehensive evaluation (e.g., D0150, D0160) isn’t possible without debridement.
- Check patient’s ability to tolerate the procedure (may need anesthesia).

**Notes:**
- Not a definitive treatment; it’s preparatory for a future periodontal diagnosis.
- Documentation must justify why a full exam couldn’t be completed initially.
- Typically followed by a recall visit for detailed charting and treatment planning.

### D4381 - Localized Delivery of Antimicrobial Agents via a Controlled Release Vehicle into Diseased Crevicular Tissue, Per Tooth
**When to use:**
- When FDA-approved antimicrobial agents are delivered subgingivally via controlled-release devices into periodontal pockets to suppress pathogens.
- Used as an adjunct to scaling/root planing in specific, persistent pockets.

**What to check:**
- Confirm periodontal disease with pockets ≥4mm post-scaling/root planing that remain unresponsive.
- Identify specific teeth and pocket depths for treatment.
- Verify patient isn’t allergic to the antimicrobial agent used.

**Notes:**
- Requires prior scaling/root planing; not a standalone treatment.
- Documentation must list teeth treated, pocket depths, and agent used (e.g., Arestin).
- Patient must be monitored for response and potential reapplication.

### Key Takeaways:
- Diagnosis Drives Coding: Always tie the code to a specific periodontal diagnosis or clinical need, not just the amount of work done.
- Quadrant vs. Localized: D4341/D4342 depend on the number of teeth affected per quadrant; count carefully.
- Inflammation vs. Disease: D4346 is for gingivitis only, while D4341/D4342/D4381 require periodontitis.
- Adjunct Procedures: Splinting (D4322/D4323) and antimicrobials (D4381) enhance stability or therapy, not replace it.
- Documentation is King: Insurers require detailed narratives (e.g., pocket depths, tooth numbers, clinical justification) for approval.



{{question}}
{PROMPT}
""",
        input_variables=["question"]    
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_non_surgical_services_code(scenario, temperature=0.0):
    """
    Extract non-surgical periodontal services code(s) for a given scenario.
    """
    try:
        chain = create_non_surgical_services_extractor(temperature)
        result = chain.run(question=scenario)
        print(f"Non-surgical periodontal services code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_non_surgical_services_code: {str(e)}")
        return ""

def activate_non_surgical_services(scenario):
    """
    Activate non-surgical periodontal services analysis and return results.
    """
    try:
        return extract_non_surgical_services_code(scenario)
    except Exception as e:
        print(f"Error in activate_non_surgical_services: {str(e)}")
        return "" 