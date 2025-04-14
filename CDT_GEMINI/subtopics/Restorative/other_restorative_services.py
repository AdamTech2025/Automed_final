"""
Module for extracting other restorative services codes.
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
 
def create_other_restorative_services_extractor(temperature=0.0):
    """
    Create a LangChain-based other restorative services code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert

### Before picking a code, ask:
- What was the primary reason the patient came in? Is it a repair, a new restoration, or a protective measure?
- Is the procedure direct (in-office) or indirect (lab-fabricated)?
- Does it involve a primary or permanent tooth?
- Is the restoration addressing a failure, caries, or structural need?
- Are there additional factors like existing prosthetics or patient symptoms influencing the procedure?

### D2990 - Resin Infiltration of Incipient Smooth Surface Lesions
**When to use:**
- When placing an infiltrating resin to strengthen, stabilize, or limit the progression of early, non-cavitated smooth surface lesions.
- Typically used for incipient caries not requiring traditional restoration.

**What to check:**
- Confirm the lesion is non-cavitated and limited to enamel (e.g., white spot lesions).
- Assess the tooth’s smooth surface (buccal or lingual) and absence of structural damage.
- Verify patient’s caries risk and oral hygiene habits.

**Notes:**
- Not for cavitated lesions requiring drilling/filling (e.g., D2391).
- Requires documentation of lesion location and rationale (e.g., “#8 buccal incipient lesion”).
- Often considered preventive; insurance coverage may vary.

### D2910 - Re-cement or Re-bond Inlay, Onlay, Veneer, or Partial Coverage Restoration
**When to use:**
- When re-cementing or re-bonding an existing inlay, onlay, veneer, or partial coverage restoration that has become dislodged.

**What to check:**
- Ensure the restoration is intact and reusable (no fractures or material failure).
- Check the tooth for decay or damage that might require a new restoration instead.
- Verify occlusion after re-cementation to avoid bite issues.

**Notes:**
- Does not apply to crowns (use D2920) or repairs (use D2981/D2982).
- Documentation should note the restoration type and reason for dislodgement (e.g., “#19 onlay debonded due to adhesive failure”).
- May require surface preparation or new cement.

### D2915 - Re-cement or Re-bond Indirectly Fabricated or Prefabricated Post and Core
**When to use:**
- When re-cementing or re-bonding an indirectly fabricated or prefabricated post and core that has loosened.

**What to check:**
- Confirm the post and core is intact and the tooth structure supports reattachment.
- Assess for underlying issues (e.g., recurrent decay, fracture) that may contraindicate re-cementation.
- Check crown fit (if present) post-procedure.

**Notes:**
- Specific to post and core; not for crowns alone (use D2920).
- Requires documentation of post type and reason for failure.
- May need radiographic confirmation of fit.

### D2920 - Re-cement or Re-bond Crown
**When to use:**
- When re-cementing or re-bonding a dislodged crown (primary or permanent).

**What to check:**
- Verify the crown’s integrity (no cracks or wear) and the tooth’s condition (no new decay).
- Ensure proper fit and occlusion after re-cementation.
- Check for patient symptoms (e.g., sensitivity) that might indicate a bigger issue.

**Notes:**
- Not for post and core issues (use D2915) or repairs (use D2980).
- Documentation should specify tooth number and crown type (e.g., “#27 PFM crown re-cemented”).
- Temporary cement may be used if prognosis is uncertain.

### D2921 - Reattachment of Tooth Fragment, Incisal Edge, or Cusp
**When to use:**
- When reattaching a broken tooth fragment (e.g., incisal edge or cusp) using adhesive techniques.

**What to check:**
- Confirm the fragment is available, intact, and fits the tooth precisely.
- Assess the tooth for pulp exposure or cracks requiring additional treatment.
- Check occlusion and esthetics post-reattachment.

**Notes:**
- Typically for trauma cases; not for caries-related loss.
- Requires documentation of fragment source and bonding method.
- May need follow-up for vitality testing.

### D2929 - Prefabricated Porcelain/Ceramic Crown — Primary Tooth
**When to use:**
- When placing a prefabricated porcelain or ceramic crown on a primary tooth for restorative or esthetic purposes.

**What to check:**
- Verify the primary tooth’s condition (e.g., extensive caries, fracture) warrants a crown.
- Ensure proper size and fit of the prefabricated crown.
- Check occlusion and parental consent for esthetic focus.

**Notes:**
- Often used in pediatric dentistry for anterior teeth.
- Documentation should note tooth number and clinical need.
- Not for permanent teeth (use D2928).

### D2928 - Prefabricated Porcelain/Ceramic Crown — Permanent Tooth
**When to use:**
- When placing a prefabricated porcelain or ceramic crown on a permanent tooth.

**What to check:**
- Confirm the permanent tooth requires a crown due to decay, fracture, or esthetic need.
- Assess fit and shade match of the prefabricated crown.
- Check occlusion and patient expectations.

**Notes:**
- Less common than custom crowns (e.g., D2740); used for expediency.
- Requires documentation of tooth number and rationale.
- Not for primary teeth (use D2929).

### D2930 - Prefabricated Stainless Steel Crown — Primary Tooth
**When to use:**
- When placing a prefabricated stainless steel crown on a primary tooth, typically for extensive caries or structural loss.

**What to check:**
- Verify the primary tooth’s condition justifies a crown (e.g., multi-surface decay).
- Ensure proper size and fit; check occlusion post-placement.
- Assess pulp health (may need pulpotomy first).

**Notes:**
- Standard in pediatric dentistry; durable and cost-effective.
- Documentation should include tooth letter and clinical findings.
- Not for permanent teeth (use D2931).

### D2931 - Prefabricated Stainless Steel Crown — Permanent Tooth
**When to use:**
- When placing a prefabricated stainless steel crown on a permanent tooth, often as a temporary or cost-effective solution.

**What to check:**
- Confirm the permanent tooth’s condition (e.g., decay, fracture) and patient’s financial/esthetic preferences.
- Check fit and occlusion; ensure no pulp involvement.
- Assess long-term plan (e.g., eventual custom crown).

**Notes:**
- Less common than D2930; used in specific cases (e.g., molars).
- Requires documentation of tooth number and purpose.
- Not for primary teeth (use D2930).

### D2932 - Prefabricated Resin Crown
**When to use:**
- When placing a prefabricated resin crown on a primary or permanent tooth for restorative or esthetic needs.

**What to check:**
- Verify the tooth’s condition and suitability for a resin crown (e.g., anterior esthetics).
- Ensure proper fit, shade, and occlusion.
- Check patient’s caries risk and oral hygiene.

**Notes:**
- Less durable than stainless steel or porcelain; often temporary.
- Documentation should specify tooth and material.
- May apply to either dentition; clarify in notes.

### D2933 - Prefabricated Stainless Steel Crown with Resin Window
**When to use:**
- When placing an open-face stainless steel crown with an esthetic resin facing or veneer, typically on primary teeth.

**What to check:**
- Confirm the tooth (usually anterior) needs both durability and esthetics.
- Assess fit of the stainless steel base and resin window placement.
- Check occlusion and esthetic outcome.

**Notes:**
- Combines D2930 durability with esthetic appeal.
- Documentation should note tooth letter and resin application.
- Primarily for primary teeth; rare in permanent dentition.

### D2934 - Prefabricated Esthetic Coated Stainless Steel Crown — Primary Tooth
**When to use:**
- When placing a stainless steel primary crown with an exterior esthetic coating for improved appearance.

**What to check:**
- Verify the primary tooth’s condition (e.g., caries, fracture) and esthetic need.
- Ensure the coated crown fits and matches adjacent teeth.
- Check occlusion and coating integrity.

**Notes:**
- Differs from D2933 by full coating vs. window.
- Documentation should include tooth letter and clinical justification.
- Not for permanent teeth.

### D2940 - Protective Restoration
**When to use:**
- When placing a direct restorative material to protect a tooth or tissue, relieving pain, promoting healing, or preventing deterioration.

**What to check:**
- Assess the tooth for sensitivity, exposure, or risk (e.g., after trauma or caries removal).
- Confirm it’s not for endodontic access closure or as a base/liner.
- Check patient symptoms and urgency.

**Notes:**
- Temporary measure; not a definitive restoration.
- Documentation should specify tooth and purpose (e.g., “#9 sedative filling for sensitivity”).
- Often used in emergency visits.

### D2941 - Interim Therapeutic Restoration — Primary Dentition
**When to use:**
- When placing an adhesive restorative material on a primary tooth after caries debridement (e.g., by hand) for early childhood caries management.

**What to check:**
- Verify the primary tooth has early caries and no pulp involvement.
- Confirm debridement method (e.g., spoon excavation) and material used.
- Check parental understanding of its interim nature.

**Notes:**
- Not a final restoration; often part of caries arrest strategy.
- Documentation should note tooth letter and caries extent.
- Common in pediatric settings (e.g., SDF follow-up).

### D2949 - Restorative Foundation for an Indirect Restoration
**When to use:**
- When placing restorative material to create an ideal form for a future indirect restoration, eliminating undercuts.

**What to check:**
- Assess the tooth’s preparation for an indirect restoration (e.g., crown, onlay).
- Confirm material placement enhances retention/shape.
- Check compatibility with planned indirect restoration.

**Notes:**
- Differs from D2950 (core buildup); focuses on form, not retention.
- Documentation should specify tooth and planned restoration.
- Often a lab prep step.

### D2950 - Core Buildup, Including Any Pins When Required
**When to use:**
- When building up coronal structure for retention of a separate extracoronal restoration (e.g., crown).

**What to check:**
- Verify insufficient natural tooth structure for crown retention.
- Assess need for pins and their placement feasibility.
- Check post-buildup occlusion and crown prep readiness.

**Notes:**
- Not a filler for undercuts (use D2949); focuses on structural support.
- Documentation should note tooth, materials, and pins (if used).
- Often paired with D2952/D2954.

### D2951 - Pin Retention — Per Tooth, in Addition to Restoration
**When to use:**
- When adding pins to a restoration (e.g., amalgam, composite) for extra retention, per tooth.

**What to check:**
- Confirm the tooth requires additional retention beyond adhesive means.
- Assess pin placement and tooth integrity (no fractures).
- Check final restoration stability.

**Notes:**
- Used with direct restorations, not crowns.
- Documentation should specify tooth and number of pins.
- Less common with modern adhesives.

### D2952 - Post and Core in Addition to Crown, Indirectly Fabricated
**When to use:**
- When a custom-fabricated post and core is placed as a single unit before a crown.

**What to check:**
- Verify the tooth’s root canal status and coronal loss.
- Assess lab-fabricated post/core fit and crown prep.
- Check radiographic alignment and occlusion.

**Notes:**
- Indirect process; differs from D2954 (prefabricated).
- Documentation should note tooth and lab involvement.
- Use D2953 for additional posts.

### D2953 - Each Additional Indirectly Fabricated Post — Same Tooth
**When to use:**
- When an additional indirectly fabricated post is placed in the same tooth as D2952.

**What to check:**
- Confirm the need for multiple posts (e.g., multi-rooted tooth).
- Assess fit and stability with primary post/core.
- Check radiographic positioning.

**Notes:**
- Always paired with D2952; not standalone.
- Documentation should specify tooth and post count.
- Rare; typically one post suffices.

### D2954 - Prefabricated Post and Core in Addition to Crown
**When to use:**
- When a prefabricated post is used with a core buildup before a crown.

**What to check:**
- Verify root canal completion and coronal loss.
- Ensure prefabricated post fits and core material bonds well.
- Check crown prep readiness and occlusion.

**Notes:**
- In-office procedure; differs from D2952 (indirect).
- Documentation should note tooth and materials.
- Use D2957 for additional posts.

### D2957 - Each Additional Prefabricated Post — Same Tooth
**When to use:**
- When an additional prefabricated post is placed in the same tooth as D2954.

**What to check:**
- Confirm multiple posts are needed (e.g., molar with multiple canals).
- Assess fit with primary post and core stability.
- Check radiographic alignment.

**Notes:**
- Always paired with D2954; not standalone.
- Documentation should specify tooth and post count.
- Uncommon due to single-post efficacy.

### D2955 - Post Removal
**When to use:**
- When removing an existing post (prefabricated or custom) from a tooth.

**What to check:**
- Assess the post’s condition (e.g., fractured, loose) and removal feasibility.
- Confirm tooth integrity post-removal (no root fracture).
- Check need for subsequent treatment (e.g., new post).

**Notes:**
- Often preparatory for retreatment or extraction.
- Documentation should note tooth, post type, and method (e.g., ultrasonic).
- May require radiographs pre/post.

### D2960 - Labial Veneer (Resin Laminate) — Direct
**When to use:**
- When placing a direct resin-bonded labial/facial veneer in-office.

**What to check:**
- Verify the tooth’s esthetic need (e.g., discoloration, shape).
- Assess enamel availability for bonding and shade match.
- Check occlusion and patient satisfaction.

**Notes:**
- Less durable than indirect veneers (D2961/D2962).
- Documentation should note tooth and resin type.
- Common for minor esthetic fixes.

### D2961 - Labial Veneer (Resin Laminate) — Indirect
**When to use:**
- When placing an indirect, lab-fabricated resin-bonded labial/facial veneer.

**What to check:**
- Confirm the tooth’s condition supports indirect veneer (e.g., minimal prep).
- Assess lab fit, shade, and occlusion.
- Check patient expectations for durability/esthetics.

**Notes:**
- More durable than D2960; lab-processed.
- Documentation should note tooth and lab details.
- Less common than porcelain (D2962).

### D2962 - Labial Veneer (Porcelain Laminate) — Indirect
**When to use:**
- When placing an indirect, lab-fabricated porcelain/ceramic veneer, often extending interproximally or over the incisal edge.

**What to check:**
- Verify the tooth’s prep and esthetic goals (e.g., alignment, color).
- Assess veneer fit, shade, and occlusion from lab.
- Check bonding integrity and patient approval.

**Notes:**
- Gold standard for esthetic veneers.
- Documentation should note tooth and porcelain type.
- Requires precise prep and lab communication.

### D2971 - Additional Procedures to Customize a Crown to Fit Under an Existing Partial Denture Framework
**When to use:**
- When extra steps are needed to adapt a crown to fit under an existing partial denture framework.

**What to check:**
- Confirm the partial denture’s clasp/rest design and crown compatibility.
- Assess crown contouring needs and occlusion.
- Check partial denture fit post-procedure.

**Notes:**
- Used with a separate crown code (e.g., D2740).
- Documentation should note tooth, partial, and modifications.
- Ensures prosthetic harmony.



### D2980 - Crown Repair Necessitated by Restorative Material Failure
**When to use:**
- When repairing a crown due to failure of the restorative material (e.g., porcelain fracture, metal exposure) rather than tooth structure or cement failure.

**What to check:**
- Confirm the crown’s material failure (e.g., chipped porcelain, cracked zirconia) via visual or radiographic exam.
- Assess the underlying tooth for decay or fracture that might require a new crown instead.
- Check occlusion and patient symptoms (e.g., sensitivity) post-repair.

**Notes:**
- Not for re-cementation (use D2920) or tooth-related issues; focuses on material breakdown.
- Documentation must specify tooth number, failure type (e.g., “#19 PFM porcelain chipped”), and repair method (e.g., composite bonding).
- May be temporary; monitor for recurrence.

### D2981 - Inlay Repair Necessitated by Restorative Material Failure
**When to use:**
- When repairing an inlay due to failure of the restorative material (e.g., cracked ceramic, worn composite) rather than tooth or adhesive failure.

**What to check:**
- Verify the inlay’s material failure (e.g., fracture, degradation) and distinguish it from tooth damage.
- Assess the inlay’s fit and surrounding tooth structure for integrity.
- Check occlusion and esthetics after repair.

**Notes:**
- Not for re-cementation (use D2910); specific to material issues.
- Documentation should note tooth number, failure details (e.g., “#14 ceramic inlay cracked”), and repair technique.
- Insurance may question necessity; narrative is key.

### D2982 - Onlay Repair Necessitated by Restorative Material Failure
**When to use:**
- When repairing an onlay due to failure of the restorative material (e.g., porcelain chip, resin wear) rather than tooth or bonding failure.

**What to check:**
- Confirm the onlay’s material failure (e.g., cusp fracture, surface wear) via clinical exam.
- Evaluate the tooth for secondary issues (e.g., caries) that might necessitate replacement.
- Check occlusion and functionality post-repair.

**Notes:**
- Distinct from re-cementation (D2910); targets material defects.
- Documentation must include tooth number, failure specifics (e.g., “#3 gold onlay cusp fractured”), and repair approach.
- May extend onlay lifespan; assess longevity.

### D2999 - Unspecified Restorative Procedure, By Report
**When to use:**
- When performing a restorative procedure not adequately described by an existing CDT code, requiring a detailed narrative.

**What to check:**
- Ensure no specific code (e.g., D2980, D2940) applies to the procedure.
- Assess the clinical necessity and complexity (e.g., unique materials, techniques).
- Verify patient consent, especially if experimental or costly.

**Notes:**
- Examples: laser-assisted restoration, custom repairs beyond standard codes.
- Requires a thorough report with tooth number, procedure details, and justification (e.g., “#8 novel resin technique for atypical defect”).
- Pre-authorization recommended due to variable reimbursement.


### D2975= Key Takeaways:
- Direct vs. Indirect: Direct procedures (e.g., D2940, D2960) are immediate, while indirect (e.g., D2952, D2962) involve lab work for precision.
- Primary vs. Permanent: Codes like D2929/D2930 distinguish dentition; choose accurately.
- Purpose Drives Coding: Match the code to the procedure’s intent (e.g., protective D2940 vs. core D2950).
- Documentation is Critical: Repairs, customizations, and unspecified codes (D2980-D2999) need detailed narratives.
- Adjunct Codes: D2951, D2953, D2957 enhance primary procedures—don’t use alone.

Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_other_restorative_services_code(scenario, temperature=0.0):
    """
    Extract other restorative services code(s) for a given scenario.
    """
    try:
        chain = create_other_restorative_services_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Other restorative services code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_other_restorative_services_code: {str(e)}")
        return ""

def activate_other_restorative_services(scenario):
    """
    Activate other restorative services analysis and return results.
    """
    try:
        return extract_other_restorative_services_code(scenario)
    except Exception as e:
        print(f"Error in activate_other_restorative_services: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "5-year-old patient needs a stainless steel crown on primary molar tooth letter 'K'."
    result = activate_other_restorative_services(scenario)
    print(result) 