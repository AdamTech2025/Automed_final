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

class GeneralMaxillofacialProstheticsServices:
    """Class to analyze and extract general maxillofacial prosthetics codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing general maxillofacial prosthetics."""
        return PromptTemplate(
            template=f"""
You are a dental coding expert specializing in maxillofacial prosthetics.

### Before Picking a Code, Ask:
- What was the primary reason the patient came in?
- Is the prosthesis initial, a replacement, or a modification?
- Is the prosthesis intraoral or extraoral?
- What anatomical structure is being restored (e.g., ear, nose, palate, eye)?
- Are there changes to the tissue bed that may affect prosthesis retention or fit?

---

### General Maxillofacial Prosthetics

#### Code: D5992
**Heading:** Adjustment of maxillofacial prosthetic appliance  
**When to Use:**  
- A maxillofacial prosthesis requires adjustment beyond routine maintenance.  
- Use for adaptations due to tissue or functional changes.  
**What to Check:**  
- Confirm adjustment addresses fit/function, not cleaning (see D5993).  
- Verify narrative for tissue change or patient complaint.  
- Assess prosthesis type (intraoral/extraoral).  
**Notes:**  
- Requires detailed report for reimbursement.  
- Not for routine maintenance or remake.  
- Document adjustment reason, extent, and outcome.  

#### Code: D5993
**Heading:** Maintenance and cleaning of maxillofacial prosthesis  
**When to Use:**  
- A prosthesis is cleaned/maintained without design/fit alteration.  
- Use for intraoral/extraoral prostheses.  
**What to Check:**  
- Confirm service is cleaning only, no adjustments (see D5992).  
- Verify prosthesis condition and patient hygiene.  
- Assess frequency of maintenance.  
**Notes:**  
- Routine care to extend prosthesis life.  
- Not for structural changes or remakes.  
- Document cleaning method and prosthesis status.  

#### Code: D5914
**Heading:** Auricular prosthesis, initial  
**When to Use:**  
- A new ear prosthesis is fabricated with a new mold.  
- Use for first-time auricular restoration.  
**What to Check:**  
- Confirm tissue loss (e.g., trauma, surgery) via records.  
- Verify new mold creation.  
- Assess tissue bed stability.  
**Notes:**  
- Mold may be reused later (see D5927).  
- Not for replacements or adjustments.  
- Document mold process, materials, and indication.  

#### Code: D5927
**Heading:** Auricular prosthesis, replacement  
**When to Use:**  
- An ear prosthesis is replaced using an existing mold.  
- Use when tissue bed is unchanged.  
**What to Check:**  
- Confirm mold usability via exam.  
- Verify no tissue changes since original.  
- Assess replacement need (e.g., wear, damage).  
**Notes:**  
- Cost-effective vs. new mold (see D5914).  
- Not for initial prostheses or tissue changes.  
- Document mold reuse and prosthesis condition.  

#### Code: D5987
**Heading:** Commissure splint  
**When to Use:**  
- A splint aids lip movement/separation post-surgery/trauma.  
- Use for contractures or restricted motion.  
**What to Check:**  
- Confirm surgical/traumatic indication via history.  
- Verify splint design for lip function.  
- Assess patient tolerance and compliance.  
**Notes:**  
- Common post-oncologic/reconstructive surgery.  
- Not for dental occlusion or stents (see D5982).  
- Document indication, fit, and functional goal.  

#### Code: D5924
**Heading:** Cranial prosthesis  
**When to Use:**  
- A permanent skull implant prosthesis is placed.  
- Use post-cranioplasty for defects.  
**What to Check:**  
- Confirm surgical defect via imaging/records.  
- Verify biocompatibility and permanent placement.  
- Assess custom fabrication.  
**Notes:**  
- Non-removable, surgically fixed.  
- Not for facial or intraoral prostheses.  
- Document defect size, materials, and surgical plan.  

#### Code: D5925
**Heading:** Facial augmentation implant prosthesis  
**When to Use:**  
- Surgical implants augment facial structures.  
- Use for custom restorations (e.g., cheek, chin).  
**What to Check:**  
- Confirm surgical plan via notes/imaging.  
- Verify custom vs. prefabricated implant.  
- Assess anatomical need (e.g., asymmetry).  
**Notes:**  
- Rarely prefabricated due to variation.  
- Not for removable prostheses.  
- Document implant type, site, and surgical details.  

#### Code: D5912
**Heading:** Facial moulage (complete)  
**When to Use:**  
- A full-face impression captures all facial structures.  
- Use for total facial prosthesis planning.  
**What to Check:**  
- Confirm need for complete moulage via case.  
- Verify non-reusable impression.  
- Assess defect extent (e.g., trauma, cancer).  
**Notes:**  
- Single-use for comprehensive molds.  
- Not for sectional impressions (see D5911).  
- Document impression process and purpose.  

#### Code: D5911
**Heading:** Facial moulage (sectional)  
**When to Use:**  
- Partial facial impressions capture specific regions.  
- Use for segmented prosthesis planning.  
**What to Check:**  
- Confirm regions included (e.g., nose, cheek).  
- Verify if sections combine for larger mold.  
- Assess defect specificity.  
**Notes:**  
- Allows targeted restoration vs. full moulage.  
- Not for complete faces (see D5912).  
- Document section details and mold use.  

#### Code: D5919
**Heading:** Facial prosthesis, new  
**When to Use:**  
- A new removable facial prosthesis is fabricated.  
- Use for tissue loss (trauma, surgery, congenital).  
**What to Check:**  
- Confirm defect type and extent via exam.  
- Verify new mold creation.  
- Assess retention/leakage risks.  
**Notes:**  
- May need future adjustments (see D5992).  
- Not for replacements (see D5929).  
- Document defect, mold, and prosthetic design.  

#### Code: D5929
**Heading:** Facial prosthesis, replacement  
**When to Use:**  
- A facial prosthesis is replaced using an existing mold.  
- Use when tissue bed is stable.  
**What to Check:**  
- Confirm mold usability and tissue stability.  
- Verify replacement need (e.g., wear).  
- Assess fit vs. original.  
**Notes:**  
- Faster/cheaper than new mold (see D5919).  
- Not for tissue changes or initial prostheses.  
- Document mold reuse and prosthesis status.  

#### Code: D5951
**Heading:** Feeding aid  
**When to Use:**  
- A temporary prosthesis aids feeding in cleft palate infants.  
- Use pre-surgical repair for sucking/swallowing.  
**What to Check:**  
- Confirm cleft palate via exam/records.  
- Verify temporary use until surgery.  
- Assess fit for feeding function.  
**Notes:**  
- Critical for infant nutrition.  
- Not for adults or permanent use.  
- Document cleft severity, fit, and feeding outcome.  

#### Code: D5934
**Heading:** Mandibular resection prosthesis with guide flange  
**When to Use:**  
- A prosthesis guides a resected mandible with flange.  
- Use post-resection for occlusal/masticatory function.  
**What to Check:**  
- Confirm resection anatomy via imaging.  
- Verify flange design for guidance.  
- Assess patient tolerance.  
**Notes:**  
- Enhances chewing vs. non-flanged (see D5935).  
- Not for non-resected mandibles.  
- Document resection extent, flange role, and function.  

#### Code: D5935
**Heading:** Mandibular resection prosthesis without guide flange  
**When to Use:**  
- A prosthesis aids resected mandible without flange.  
- Use when flanges are intolerable or unneeded.  
**What to Check:**  
- Confirm resection and flange absence via notes.  
- Verify functional need (e.g., mastication).  
- Assess simpler design rationale.  
**Notes:**  
- Less control than D5934 but easier to tolerate.  
- Not for flanged prostheses.  
- Document resection, design, and patient feedback.  

#### Code: D5913
**Heading:** Nasal prosthesis, initial  
**When to Use:**  
- A new nasal prosthesis is fabricated with a new mold.  
- Use for first-time nasal restoration.  
**What to Check:**  
- Confirm nasal defect (e.g., cancer, trauma) via records.  
- Verify new mold creation.  
- Assess tissue bed stability.  
**Notes:**  
- Mold reusable for replacements (see D5926).  
- Not for replacements or adjustments.  
- Document defect, mold, and prosthetic details.  

#### Code: D5926
**Heading:** Nasal prosthesis, replacement  
**When to Use:**  
- A nasal prosthesis is replaced using an existing mold.  
- Use with stable tissue bed.  
**What to Check:**  
- Confirm mold usability and no tissue changes.  
- Verify replacement need (e.g., degradation).  
- Assess fit vs. original.  
**Notes:**  
- Cost-effective vs. new mold (see D5913).  
- Not for initial prostheses or tissue changes.  
- Document mold reuse and prosthesis condition.  

#### Code: D5922
**Heading:** Nasal septal prosthesis  
**When to Use:**  
- A prosthesis closes a nasal septal defect.  
- Use for perforations or surgical defects.  
**What to Check:**  
- Confirm septal defect via exam/imaging.  
- Verify material durability (e.g., acrylic).  
- Assess replacement frequency.  
**Notes:**  
- May degrade, needing frequent remakes.  
- Not for external nasal prostheses.  
- Document defect size, material, and fit.  

#### Code: D5932
**Heading:** Obturator prosthesis, definitive  
**When to Use:**  
- A long-term obturator replaces maxilla/tissue post-resection.  
- Use with stable tissues.  
**What to Check:**  
- Confirm healed resection site via exam.  
- Verify no further surgery planned.  
- Assess seal and function (e.g., speech, eating).  
**Notes:**  
- Final stage after interim/surgical obturators.  
- Not for temporary use (see D5931, D5936).  
- Document tissue stability, fit, and function.  

#### Code: D5936
**Heading:** Obturator prosthesis, interim  
**When to Use:**  
- A temporary obturator is used post-maxillary resection.  
- Use during healing before definitive prosthesis.  
**What to Check:**  
- Confirm recent resection and healing phase.  
- Verify no surgical revisions planned.  
- Assess adjustments needed.  
**Notes:**  
- Bridges to D5932; may need frequent tweaks.  
- Not for surgical (see D5931) or definitive use.  
- Document healing stage, fit, and interim role.  

#### Code: D5933
**Heading:** Obturator prosthesis, modification  
**When to Use:**  
- An existing obturator (surgical/interim/definitive) is adjusted.  
- Use for fit, seal, or tissue changes.  
**What to Check:**  
- Confirm adjustment need (e.g., leakage, discomfort).  
- Verify obturator type and condition.  
- Assess tissue change rationale.  
**Notes:**  
- Avoids full remake vs. new prosthesis.  
- Not for initial fabrication.  
- Document adjustment details and outcome.  

#### Code: D5931
**Heading:** Obturator prosthesis, surgical  
**When to Use:**  
- A temporary obturator is placed during/after maxillary surgery.  
- Use for immediate post-resection defects.  
**What to Check:**  
- Confirm surgical timing via operative notes.  
- Verify temporary role and adjustment needs.  
- Assess defect size and tissue state.  
**Notes:**  
- Often adjusted frequently post-surgery.  
- Not for interim (see D5936) or definitive (see D5932).  
- Document surgical context, fit, and adjustments.  

#### Code: D5916
**Heading:** Ocular prosthesis, permanent  
**When to Use:**  
- A permanent eye prosthesis is fabricated.  
- Use post-trauma/surgery for eye loss.  
**What to Check:**  
- Confirm enucleation/anophthalmia via records.  
- Verify fit and aesthetic match.  
- Assess cleaning/maintenance plan.  
**Notes:**  
- Long-term use with periodic care.  
- Not for temporary eyes (see D5923).  
- Document defect, fit, and patient education.  

#### Code: D5923
**Heading:** Ocular prosthesis, interim  
**When to Use:**  
- A temporary eye prosthesis is used during healing.  
- Use post-trauma/surgery before permanent eye.  
**What to Check:**  
- Confirm healing phase via exam.  
- Verify clear acrylic use and non-aesthetic focus.  
- Assess transition to D5916.  
**Notes:**  
- Precedes permanent prosthesis.  
- Not for long-term use.  
- Document healing status and interim role.  

#### Code: D5915
**Heading:** Orbital prosthesis  
**When to Use:**  
- A full orbital prosthesis restores eye and surrounding tissues.  
- Use for complete orbital defects (skin, muscle, eyelid).  
**What to Check:**  
- Confirm defect extent via imaging/records.  
- Verify new mold creation.  
- Assess tissue stability.  
**Notes:**  
- Comprehensive vs. ocular only (see D5916).  
- Not for replacements (see D5928).  
- Document defect, mold, and prosthetic scope.  

#### Code: D5928
**Heading:** Orbital prosthesis, replacement  
**When to Use:**  
- An orbital prosthesis is replaced using an existing mold.  
- Use with stable tissue bed.  
**What to Check:**  
- Confirm mold usability and tissue stability.  
- Verify replacement need (e.g., wear).  
- Assess fit vs. original.  
**Notes:**  
- Faster/cheaper than new mold (see D5915).  
- Not for initial prostheses.  
- Document mold reuse and prosthesis status.  

#### Code: D5954
**Heading:** Palatal augmentation prosthesis  
**When to Use:**  
- A removable prosthesis augments palate for tongue function.  
- Use for speech/swallowing improvement.  
**What to Check:**  
- Confirm functional deficit (e.g., dysphagia) via exam.  
- Verify removable design and fit.  
- Assess speech/swallowing outcomes.  
**Notes:**  
- Often called speech prosthesis.  
- Not for permanent lifts (see D5955).  
- Document deficit, fit, and functional gain.  

#### Code: D5955
**Heading:** Palatal lift prosthesis, definitive  
**When to Use:**  
- A permanent prosthesis elevates soft palate.  
- Use after successful interim trial.  
**What to Check:**  
- Confirm interim success (e.g., D5958) via records.  
- Verify long-term fit and function.  
- Assess velopharyngeal competence.  
**Notes:**  
- Long-term solution for palate dysfunction.  
- Not for diagnostic use (see D5958).  
- Document trial outcome, fit, and function.  

#### Code: D5958
**Heading:** Palatal lift prosthesis, interim  
**When to Use:**  
- A temporary prosthesis evaluates palatal lift for speech/swallowing.  
- Use for diagnostic/therapeutic trial.  
**What to Check:**  
- Confirm functional need via speech/swallowing tests.  
- Verify short-term use and patient response.  
- Assess potential for D5955.  
**Notes:**  
- Tests feasibility before definitive prosthesis.  
- Not for permanent use.  
- Document trial purpose, fit, and outcomes.  

#### Code: D5959
**Heading:** Palatal lift prosthesis, modification  
**When to Use:**  
- An existing palatal lift is adjusted for fit/retention.  
- Use for comfort or function issues.  
**What to Check:**  
- Confirm adjustment need (e.g., soreness, instability).  
- Verify prosthesis condition and type.  
- Assess tissue or functional change.  
**Notes:**  
- Extends prosthesis life vs. remake.  
- Not for initial fabrication.  
- Document adjustment details and patient feedback.  

#### Code: D5985
**Heading:** Radiation cone locator prosthesis  
**When to Use:**  
- A prosthesis targets radiation in oral cancer treatment.  
- Use during split-course irradiation.  
**What to Check:**  
- Confirm oncology plan via referral/notes.  
- Verify precise radiation delivery design.  
- Assess fit and stability.  
**Notes:**  
- Enhances radiation accuracy.  
- Not for shielding (see D5984).  
- Document oncology collaboration and design.  

#### Code: D5984
**Heading:** Radiation shield prosthesis  
**When to Use:**  
- A prosthesis protects tissues during radiation therapy.  
- Use with lead or shielding materials.  
**What to Check:**  
- Confirm shielding need via radiation plan.  
- Verify material (e.g., lead) and positioning.  
- Assess tissue protection efficacy.  
**Notes:**  
- Shields healthy tissues, unlike D5985.  
- Not for radiation delivery.  
- Document shield design and radiation protocol.  

#### Code: D5953
**Heading:** Speech aid prosthesis, adult  
**When to Use:**  
- A prosthesis aids speech in adult cleft palate patients.  
- Use for velopharyngeal insufficiency.  
**What to Check:**  
- Confirm cleft/insufficiency via exam/records.  
- Verify crown attachments if used.  
- Assess speech improvement.  
**Notes:**  
- Often fixed or semi-permanent.  
- Not for pediatric use (see D5952).  
- Document cleft status, fit, and speech gain.  

#### Code: D5960
**Heading:** Speech aid prosthesis, modification  
**When to Use:**  
- A speech prosthesis section is revised.  
- Use for partial adjustments in adults/pediatrics.  
**What to Check:**  
- Confirm specific section needing change.  
- Verify functional issue (e.g., speech clarity).  
- Assess prosthesis condition.  
**Notes:**  
- Extends device life vs. full remake.  
- Not for initial fabrication.  
- Document revision details and outcome.  

#### Code: D5952
**Heading:** Speech aid prosthesis, pediatric  
**When to Use:**  
- A temporary prosthesis aids speech in cleft palate children.  
- Use with deciduous teeth for retention.  
**What to Check:**  
- Confirm cleft palate and deciduous teeth via exam.  
- Verify temporary use until growth/surgery.  
- Assess speech function.  
**Notes:**  
- Supports speech development pre-surgery.  
- Not for adults (see D5953).  
- Document cleft, fit, and speech progress.  

#### Code: D5988
**Heading:** Surgical splint  
**When to Use:**  
- A splint stabilizes jaws post-fracture/trauma.  
- Use for healing and occlusal support.  
**What to Check:**  
- Confirm trauma/fracture via imaging/history.  
- Verify splint design (e.g., arch bars, dentures).  
- Assess stabilization duration.  
**Notes:**  
- Temporary for healing phase.  
- Not for soft tissue stents (see D5982).  
- Document trauma, design, and healing plan.  

#### Code: D5982
**Heading:** Surgical stent  
**When to Use:**  
- A stent applies pressure for soft tissue healing.  
- Use post-surgery for tissue adaptation.  
**What to Check:**  
- Confirm surgical indication via operative notes.  
- Verify stent material (e.g., soft liner, compound).  
- Assess pressure application and fit.  
**Notes:**  
- Aids soft tissue, not jaws (see D5988).  
- Not for radiation or splints.  
- Document surgery, material, and healing goal.  

#### Code: D5937
**Heading:** Trismus appliance  
**When to Use:**  
- A prosthesis manages restricted jaw opening (trismus).  
- Use post-surgery/trauma, not TMJ issues.  
**What to Check:**  
- Confirm trismus diagnosis via exam/history.  
- Verify appliance design for aperture increase.  
- Assess non-TMJ etiology.  
**Notes:**  
- Focuses on jaw mobility, not occlusion.  
- Not for TMJ disorders.  
- Document trismus cause, design, and progress.  

---

### Key Takeaways:
- **Initial vs. Replacement:** Distinguish new prostheses (new molds) from replacements (existing molds).  
- **Intraoral/Extraoral:** Codes specify anatomical focus (e.g., facial, palatal, mandibular).  
- **Mold Reusability:** Verify tissue stability for mold reuse to avoid new fabrication.  
- **Indication Specificity:** Match codes to exact function (e.g., speech, feeding, radiation).  
- **Documentation Critical:** Provide narratives for adjustments, unique cases, or reimbursements.  
- **Follow-Up Care:** Plan for modifications, maintenance, or replacements based on tissue changes.  
- **Patient-Centered:** Consider tolerance, function, and healing phase in code selection.

Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_general_prosthetics_code(self, scenario: str) -> str:
        """Extract general maxillofacial prosthetics code(s) for a given scenario."""
        try:
            print(f"Analyzing general maxillofacial scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"General prosthetics extract_general_prosthetics_code result: {code}")
            if code.lower() in ["none", "", "not applicable"]:
                return ""
            return code
        except Exception as e:
            print(f"Error in general prosthetics code extraction: {str(e)}")
            return ""
    
    def activate_general_prosthetics(self, scenario: str) -> str:
        """Activate the general maxillofacial prosthetics analysis process and return results."""
        try:
            result = self.extract_general_prosthetics_code(scenario)
            if not result:
                print("No general maxillofacial prosthetics code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating general maxillofacial prosthetics analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_general_prosthetics(scenario)
        print(f"\n=== GENERAL MAXILLOFACIAL PROSTHETICS ANALYSIS RESULT ===")
        print(f"GENERAL MAXILLOFACIAL PROSTHETICS CODE: {result if result else 'None'}")

general_prosthetics_service = GeneralMaxillofacialProstheticsServices()
# Example usage
if __name__ == "__main__":
    prosthetics_service = GeneralMaxillofacialProstheticsServices()
    scenario = input("Enter a general maxillofacial prosthetics dental scenario: ")
    prosthetics_service.run_analysis(scenario)