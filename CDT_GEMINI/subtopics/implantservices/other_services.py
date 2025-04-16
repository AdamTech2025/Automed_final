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

class OtherImplantServices:
    """Class to analyze and extract other implant services codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing other implant services."""
        return PromptTemplate(
            template=f"""
You are a dental coding expert specializing in implant services.

### Before Picking a Code, Ask:
- What type of service is being performed? (maintenance, repair, replacement, etc.)
- Is the procedure related to an existing implant, abutment, or implant-supported prosthesis?
- Is the procedure addressing a complication or part of routine maintenance?
- Is this a replacement of a component or repair of an existing component?
- Is the procedure for a removable or fixed prosthesis?
- Does the procedure involve specific components like retaining screws or semi-precision attachments?

---

### Other Implant Services

#### Code: D6080
**Heading:** Implant maintenance procedures when prostheses are removed and reinserted, including cleansing of prostheses and abutments  
**When to Use:**  
- Professional maintenance is performed on a fixed implant-supported prosthesis requiring removal, cleaning, and reinsertion.  
- Use for comprehensive cleaning of both prosthesis and abutments, not in-place cleaning.  
**What to Check:**  
- Confirm the prosthesis was removed and reinserted via clinical notes.  
- Verify it’s a fixed prosthesis (e.g., bridge, not overdenture).  
- Assess peri-implant tissue health and component wear.  
- Check frequency (e.g., 3-6 months for high-risk patients, annually for others).  
**Notes:**  
- Involves cleaning, inspecting components, and retightening screws if needed.  
- Not for removable prostheses or in-place cleaning.  
- Document prosthesis type, cleaning methods, and patient home care instructions.  

#### Code: D6081
**Heading:** Scaling and debridement in the presence of inflammation or mucositis of a single implant  
**When to Use:**  
- Non-surgical periodontal maintenance is performed on a single implant with peri-implant mucositis.  
- Use for biofilm/calculus removal with specialized instruments.  
**What to Check:**  
- Confirm inflammation/mucositis via clinical exam (e.g., bleeding on probing).  
- Verify use of implant-safe instruments (e.g., plastic, titanium).  
- Ensure no bone loss (else consider peri-implantitis codes).  
- Cannot be reported with D1110, D4910, or D4346 same visit.  
**Notes:**  
- Aims to prevent progression to peri-implantitis.  
- Includes irrigation and home care instructions.  
- Document inflammation signs and treatment specifics.  

#### Code: D6085
**Heading:** Provisional implant crown  
**When to Use:**  
- A temporary crown is placed on an implant during healing before the final prosthesis.  
- Use to shape soft tissue or assess esthetics/function.  
**What to Check:**  
- Confirm temporary purpose and duration via treatment plan.  
- Verify material (e.g., acrylic, composite) and retention (screw/cement).  
- Assess gingival shaping and occlusal function.  
- Check patient esthetic satisfaction.  
**Notes:**  
- Shapes emergence profile and evaluates phonetics/esthetics.  
- Not for permanent crowns or multi-unit provisionals.  
- Document material, retention, and provisional goals.  

#### Code: D6090
**Heading:** Repair implant supported prosthesis, by report  
**When to Use:**  
- Repairs are made to a fixed implant-supported prosthesis (non-removable).  
- Use for porcelain/acrylic fractures, tooth replacement, etc.  
**What to Check:**  
- Confirm prosthesis is fixed and non-patient-removable.  
- Verify damage type (e.g., fracture, wear) via clinical exam.  
- Ensure narrative details repair materials and techniques.  
- Assess repair durability.  
**Notes:**  
- Requires detailed narrative for insurance.  
- Not for removable prostheses or abutment repairs (see D6095).  
- Document damage extent and repair limitations.  

#### Code: D6091
**Heading:** Replacement of replaceable part of semi-precision or precision attachment of implant/abutment supported prosthesis, per attachment  
**When to Use:**  
- A worn semi-precision/precision attachment component is replaced (e.g., O-rings, clips).  
- Use per attachment for removable prostheses.  
**What to Check:**  
- Confirm attachment type (e.g., nylon insert, rubber O-ring).  
- Verify it’s a replaceable part, not the abutment (see D6191).  
- Assess wear cause (e.g., patient habits, design).  
- Check prosthesis condition.  
**Notes:**  
- Restores retention for removable prostheses.  
- Report per attachment replaced.  
- Document brand, position, and replacement rationale.  

#### Code: D6092
**Heading:** Re-cement or re-bond implant/abutment supported crown  
**When to Use:**  
- A loose implant/abutment-supported crown is re-cemented.  
- Use for intact crowns suitable for re-cementation.  
**What to Check:**  
- Confirm crown integrity via inspection.  
- Verify abutment stability and cement failure cause.  
- Assess cement choice (temporary/permanent) and margin depth.  
- Check occlusion post-cementation.  
**Notes:**  
- Involves cleaning, recementing, and verifying fit.  
- Not for prosthesis replacement or FPDs (see D6093).  
- Document cement type and failure analysis.  

#### Code: D6093
**Heading:** Re-cement or re-bond implant/abutment supported fixed partial denture  
**When to Use:**  
- A loose implant/abutment-supported fixed partial denture (FPD) is re-cemented.  
- Use for intact multi-unit prostheses.  
**What to Check:**  
- Confirm FPD integrity and abutment stability.  
- Verify complete seating at all abutments.  
- Assess cement selection and failure cause (e.g., occlusion).  
- Check contacts and occlusion post-cementation.  
**Notes:**  
- More complex than D6092 due to multi-unit seating.  
- Not for single crowns (see D6092) or replacement.  
- Document cement type, seating process, and preventive measures.  

#### Code: D6095
**Heading:** Repair implant abutment, by report  
**When to Use:**  
- A damaged implant abutment is repaired, not replaced.  
- Use for re-contouring, thread repair, etc.  
**What to Check:**  
- Confirm repair vs. replacement via damage assessment.  
- Verify abutment integrity and repair feasibility.  
- Ensure narrative details techniques (e.g., welding, polishing).  
- Assess long-term prognosis.  
**Notes:**  
- Requires detailed narrative for insurance.  
- Not for prosthesis repairs (see D6090) or screw removal (see D6096).  
- Document repair methods and limitations.  

#### Code: D6096
**Heading:** Remove broken implant retaining screw  
**When to Use:**  
- A fractured screw is removed from an implant body.  
- Use for specialized retrieval procedures.  
**What to Check:**  
- Confirm screw fracture via radiograph/clinical exam.  
- Verify retrieval technique (e.g., ultrasonic, retrieval kit).  
- Assess implant thread integrity post-removal.  
- Check fracture cause (e.g., overload, defect).  
**Notes:**  
- High-risk procedure to avoid implant damage.  
- Not for abutment repairs (see D6095).  
- Document technique, implant status, and prevention plan.  

#### Code: D6097
**Heading:** Abutment supported crown – porcelain fused to titanium and titanium alloys  
**When to Use:**  
- A porcelain-fused-to-titanium crown is placed on an implant abutment.  
- Use for single crowns, not retainers.  
**What to Check:**  
- Confirm titanium substructure via lab specs.  
- Verify abutment support, not direct implant.  
- Assess biocompatibility needs (e.g., metal allergies).  
- Check esthetic/functional outcomes.  
**Notes:**  
- Ideal for metal-sensitive patients with good esthetics.  
- Not for implant-supported crowns (see D6084) or FPDs.  
- Document material and abutment details.  

#### Code: D6098
**Heading:** Implant supported retainer – porcelain fused to predominantly base alloys  
**When to Use:**  
- A porcelain-fused-to-base-metal retainer is placed directly on an implant for a fixed partial denture (FPD).  
- Use for FPD components, not single crowns.  
**What to Check:**  
- Confirm base metal (<25% noble) via lab report.  
- Verify direct implant support, no abutment.  
- Assess FPD design and retainer role.  
- Check posterior suitability (strength-focused).  
**Notes:**  
- Economical for posterior FPDs.  
- Not for abutment-supported retainers (see D6070) or crowns.  
- Document metal type and FPD specifics.  

#### Code: D6099
**Heading:** Implant supported retainer for FPD – porcelain fused to noble alloys  
**When to Use:**  
- A porcelain-fused-to-noble-metal retainer is placed directly on an implant for an FPD.  
- Use for retainers with ≥25% noble metal.  
**What to Check:**  
- Confirm noble metal (≥25%) via lab specs.  
- Verify direct implant support and FPD context.  
- Assess biocompatibility and esthetic needs.  
- Check retainer integration with pontics.  
**Notes:**  
- Balances cost and biocompatibility.  
- Not for base metals (see D6098) or abutment-supported (see D6071).  
- Document metal composition and FPD role.  

#### Code: D6100
**Heading:** Implant removal, by report  
**When to Use:**  
- An implant is surgically removed with flap elevation.  
- Use for failed or malpositioned implants.  
**What to Check:**  
- Confirm removal reason (e.g., infection, fracture) via radiograph.  
- Verify flap surgery and debridement.  
- Ensure narrative details procedure and site management.  
- Check future treatment plans.  
**Notes:**  
- Involves osseointegration breaking and defect management.  
- Requires detailed narrative for insurance.  
- Document surgical approach and post-removal plans.  

#### Code: D6101
**Heading:** Debridement of a peri-implant defect or defects surrounding a single implant  
**When to Use:**  
- Surgical debridement is performed for peri-implantitis on one implant.  
- Use for flap access and surface cleaning, no bone work.  
**What to Check:**  
- Confirm peri-implantitis (≥5mm pockets, bone loss) via exam.  
- Verify flap surgery and implant surface detoxification.  
- Assess non-surgical failure prior.  
- Check defect extent via radiograph.  
**Notes:**  
- Aims to halt peri-implantitis progression.  
- Not for osseous work (see D6102) or grafts (see D6103).  
- Document defect details and cleaning methods.  

#### Code: D6102
**Heading:** Debridement and osseous contouring of a peri-implant defect or defects surrounding a single implant  
**When to Use:**  
- Surgical debridement with bone recontouring is performed for peri-implantitis.  
- Use for creating physiologic bone architecture.  
**What to Check:**  
- Confirm bone recontouring via surgical notes.  
- Verify peri-implantitis and flap access.  
- Assess initial vs. final bone morphology.  
- Check non-surgical failure history.  
**Notes:**  
- Enhances tissue adaptation via bone shaping.  
- Not for grafts (see D6103) or non-osseous work (see D6101).  
- Document recontouring extent and defect status.  

#### Code: D6103
**Heading:** Bone graft for repair of peri-implant defect  
**When to Use:**  
- Bone graft material is placed to repair a peri-implant defect, excluding flap access.  
- Use with D6101/D6102 for peri-implantitis.  
**What to Check:**  
- Confirm graft material (e.g., allograft, xenograft) via specs.  
- Verify defect type and size via radiograph.  
- Ensure flap access coded separately (e.g., D6101).  
- Check regenerative goals.  
**Notes:**  
- Regenerates bone around affected implants.  
- Not for simultaneous implant placement grafts (see D6104).  
- Document graft type, quantity, and defect details.  

#### Code: D6104
**Heading:** Bone graft at time of implant placement  
**When to Use:**  
- Bone graft is placed during implant surgery to address defects or augment ridge.  
- Use for socket gaps, thread coverage, etc.  
**What to Check:**  
- Confirm graft purpose (e.g., dehiscence, sinus lift) via surgery notes.  
- Verify graft material and quantity.  
- Assess defect/ridge anatomy.  
- Check simultaneous implant placement.  
**Notes:**  
- Enhances implant stability via augmentation.  
- Not for post-implant defects (see D6103).  
- Document graft specifics and implant relation.  

#### Code: D6110
**Heading:** Implant/abutment supported removable denture for edentulous arch – maxillary  
**When to Use:**  
- A removable overdenture is placed for a fully edentulous maxilla, supported by implants/abutments.  
- Use for enhanced retention over conventional dentures.  
**What to Check:**  
- Confirm full edentulism via exam.  
- Verify implant/abutment count and positions.  
- Assess attachment system (e.g., locators, bars).  
- Check patient function (e.g., chewing, phonetics).  
**Notes:**  
- Improves stability and confidence.  
- Not for partial edentulism (see D6112).  
- Document attachments and maintenance needs.  

#### Code: D6111
**Heading:** Implant/abutment supported removable denture for edentulous arch – mandibular  
**When to Use:**  
- A removable overdenture is placed for a fully edentulous mandible, supported by implants/abutments.  
- Use for significant stability improvement.  
**What to Check:**  
- Confirm mandibular edentulism.  
- Verify implant/abutment support (e.g., two-implant standard).  
- Assess attachment type and retention.  
- Check patient education on care.  
**Notes:**  
- Often a standard for mandibular edentulism.  
- Not for partial arches (see D6113).  
- Document implant count and attachment details.  

#### Code: D6112
**Heading:** Implant/abutment supported removable denture for partially edentulous arch – maxillary  
**When to Use:**  
- A removable prosthesis is placed for a partially edentulous maxilla, supported by implants/abutments and teeth.  
- Use for hybrid stability.  
**What to Check:**  
- Confirm remaining teeth and implant positions.  
- Verify force distribution design.  
- Assess attachment/clasp integration.  
- Check biomechanical balance.  
**Notes:**  
- Combines implant and tooth support.  
- Not for full edentulism (see D6110).  
- Document teeth, implants, and design specifics.  

#### Code: D6113
**Heading:** Implant/abutment supported removable denture for partially edentulous arch – mandibular  
**When to Use:**  
- A removable prosthesis is placed for a partially edentulous mandible, supported by implants/abutments and teeth.  
- Use for posterior stability.  
**What to Check:**  
- Confirm remaining teeth and implant roles.  
- Verify design for distal extension support.  
- Assess attachment integration with teeth.  
- Check stability improvements.  
**Notes:**  
- Reduces movement vs. conventional partials.  
- Not for full edentulism (see D6111).  
- Document implant/tooth support and design.  

#### Code: D6190
**Heading:** Radiographic/surgical implant index, by report  
**When to Use:**  
- A specialized appliance is created to guide implant placement relative to anatomy.  
- Use for planning or surgical precision.  
**What to Check:**  
- Confirm index purpose (radiographic/surgical) via plan.  
- Verify materials and creation process.  
- Ensure narrative details use case.  
- Check complex case needs (e.g., multi-implant).  
**Notes:**  
- Ensures accurate implant positioning.  
- Requires detailed narrative for insurance.  
- Document index role and fabrication.  

#### Code: D6197
**Heading:** Replacement of restorative material used to close an access opening of a screw-retained implant supported prosthesis, per implant  
**When to Use:**  
- Restorative material in a screw access channel is replaced, per implant.  
- Use for esthetic/functional restoration.  
**What to Check:**  
- Confirm screw-retained prosthesis via exam.  
- Verify material replacement (e.g., composite).  
- Assess color matching (anterior) and occlusion.  
- Check per-implant reporting.  
**Notes:**  
- Restores integrity of access channel.  
- Not for recementing (see D6092/D6093).  
- Document material type and esthetic needs.  

#### Code: D6198
**Heading:** Remove interim implant component  
**When to Use:**  
- A temporary implant component (e.g., healing abutment) is removed.  
- Use for planned transitional components.  
**What to Check:**  
- Confirm component type and duration via records.  
- Verify removal purpose (e.g., final prosthesis).  
- Assess tissue health post-removal.  
- Check replacement plan.  
**Notes:**  
- Distinct from second-stage surgery.  
- Not for permanent components.  
- Document component details and next steps.  

#### Code: D6199
**Heading:** Unspecified implant procedure, by report  
**When to Use:**  
- An implant-related procedure lacks a specific code.  
- Use with detailed narrative for unique cases.  
**What to Check:**  
- Confirm no other code applies via review.  
- Verify narrative covers necessity, techniques.  
- Assess medical need and payer requirements.  
- Check supporting documentation.  
**Notes:**  
- Requires manual payer review.  
- Not a default for miscoded procedures.  
- Document procedure specifics comprehensively.  

---

### Key Takeaways:
- **Diverse Services:** Covers maintenance (D6080–D6081), provisionals (D6085), repairs (D6090–D6093, D6095–D6096), restorations (D6097–D6099), surgical interventions (D6100–D6104), overdentures (D6110–D6113), and planning/miscellaneous (D6190, D6197–D6199).  
- **Specificity Matters:** Codes target precise components (e.g., screws, abutments, prostheses) and actions (e.g., repair vs. replace).  
- **Narrative Needs:** Many codes (D6090, D6095, D6100, D6190, D6199) require detailed reports for insurance.  
- **Fixed vs. Removable:** Codes distinguish fixed (e.g., D6092–D6093) vs. removable prostheses (e.g., D6110–D6113).  
- **Complication Focus:** Includes specialized codes for issues like screw fracture (D6096) or peri-implantitis (D6101–D6103).  
- **Documentation Critical:** Specify components, materials, clinical findings, and rationale for clarity and reimbursement.

Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_other_implant_services_code(self, scenario: str) -> str:
        """Extract other implant services code(s) for a given scenario."""
        try:
            print(f"Analyzing other implant services scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Other implant services extract_other_implant_services_code result: {code}")
            if code.lower() in ["none", "", "not applicable"]:
                return ""
            return code
        except Exception as e:
            print(f"Error in other implant services code extraction: {str(e)}")
            return ""
    
    def activate_other_implant_services(self, scenario: str) -> str:
        """Activate the other implant services analysis process and return results."""
        try:
            result = self.extract_other_implant_services_code(scenario)
            if not result:
                print("No other implant services code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating other implant services analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_other_implant_services(scenario)
        print(f"\n=== OTHER IMPLANT SERVICES ANALYSIS RESULT ===")
        print(f"OTHER IMPLANT SERVICES CODE: {result if result else 'None'}")

other_implant_services_service = OtherImplantServices()
# Example usage
if __name__ == "__main__":
    implant_service = OtherImplantServices()
    scenario = input("Enter an other implant services dental scenario: ")
    implant_service.run_analysis(scenario)