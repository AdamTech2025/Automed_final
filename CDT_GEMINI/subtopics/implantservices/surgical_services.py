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

class SurgicalImplantServices:
    """Class to analyze and extract surgical implant services codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing surgical implant services."""
        return PromptTemplate(
            template=f"""
You are a dental coding expert specializing in implant services.

### Before Picking a Code, Ask:
- What type of implant is being placed? (endosteal, eposteal, transosteal, mini)
- Is this an initial surgical placement or a second stage surgery?
- Is the implant intended for a permanent prosthesis or an interim/transitional prosthesis?
- Is bone grafting or guided tissue regeneration being performed in conjunction with the implant?
- Is the procedure related to implant placement, removal, or management of peri-implant conditions?
- Are there specific anatomical or patient factors affecting the complexity of the procedure?

---

### Surgical Implant Services

#### Code: D6010
**Heading:** Surgical placement of implant body: endosteal implant  
**When to Use:**  
- An endosteal implant body is surgically placed into the jawbone to support a prosthesis.  
- Use for standard titanium implants requiring osseointegration.  
**What to Check:**  
- Confirm pre-surgical planning (e.g., CBCT, bone assessment) via records.  
- Verify implant type, size, manufacturer, and position (e.g., tooth #).  
- Assess flap creation, osteotomy, and closure details.  
- Check for complications or special conditions (e.g., bone density).  
**Notes:**  
- Covers only placement, not prosthetics or second-stage surgery.  
- Not for mini implants (see D6013) or other types (see D6040, D6050).  
- Document insertion torque, lot number, and intraoperative findings.  

#### Code: D6011
**Heading:** Surgical access to an implant body (second stage implant surgery)  
**When to Use:**  
- A submerged implant is exposed for healing abutment or prosthetic attachment.  
- Use after osseointegration for prosthetic phase transition.  
**What to Check:**  
- Confirm osseointegration via radiograph/clinical exam.  
- Verify timing since placement (e.g., 3-6 months).  
- Assess technique (e.g., punch, flap) and gingival shaping needs.  
- Check esthetic zone requirements (e.g., emergence profile).  
**Notes:**  
- Shapes peri-implant tissue for function/esthetics.  
- Not for initial placement (see D6010) or removal (see D6100).  
- Document access method, abutment type, and tissue health.  

#### Code: D6012
**Heading:** Surgical placement of interim implant body for transitional prosthesis: endosteal implant  
**When to Use:**  
- An interim endosteal implant is placed to support a temporary prosthesis.  
- Use during healing of definitive implants.  
**What to Check:**  
- Confirm temporary purpose via treatment plan.  
- Verify implant size (often smaller) and planned duration.  
- Assess loading protocol and relation to final implants.  
- Check patient understanding of interim nature.  
**Notes:**  
- Protects healing implants from premature loading.  
- Not for permanent implants (see D6010) or minis (see D6013).  
- Document interim role, removal plan, and prosthetic design.  

#### Code: D6013
**Heading:** Surgical placement of mini implant  
**When to Use:**  
- A mini implant (<3mm diameter) is placed for long-term use.  
- Use for narrow ridges, overdentures, or limited bone cases.  
**What to Check:**  
- Confirm diameter via manufacturer specs.  
- Verify clinical indication (e.g., atrophy, medical limits).  
- Assess load-bearing capacity and prosthetic plan.  
- Check occlusal management strategy.  
**Notes:**  
- Less invasive but limited strength vs. standard implants.  
- Not for standard endosteal implants (see D6010).  
- Document implant specs, site constraints, and biomechanics.  

#### Code: D6040
**Heading:** Surgical placement: eposteal implant  
**When to Use:**  
- A subperiosteal framework is placed on the jawbone surface.  
- Use for severe atrophy where endosteal implants are infeasible.  
**What to Check:**  
- Confirm bone inadequacy via CBCT or impressions.  
- Verify custom framework design and fabrication.  
- Assess two-stage process (imaging, placement).  
- Check rationale vs. grafting alternatives.  
**Notes:**  
- Rare due to modern grafting/endosteal options.  
- Not for endosteal (see D6010) or transosteal (see D6050).  
- Document framework details, surgical phases, and indications.  

#### Code: D6050
**Heading:** Surgical placement: transosteal implant  
**When to Use:**  
- A transosteal implant penetrates both mandibular cortical plates.  
- Use for extreme atrophy with no other options.  
**What to Check:**  
- Confirm penetration from inferior border to oral cavity.  
- Verify mandibular height and nerve position via CBCT.  
- Assess extraoral surgical approach.  
- Check baseplate/post design.  
**Notes:**  
- Obsolete in most cases due to endosteal success.  
- Not for endosteal (see D6010) or eposteal (see D6040).  
- Document anatomical constraints and procedural complexity.  

#### Code: D6100
**Heading:** Surgical removal of implant body  
**When to Use:**  
- An implant is surgically removed with flap elevation.  
- Use for failure, infection, fracture, or malposition.  
**What to Check:**  
- Confirm removal reason (e.g., mobility, peri-implantitis) via exam/radiograph.  
- Verify flap surgery and debridement.  
- Assess defect management and future plans.  
- Check narrative for insurance justification.  
**Notes:**  
- Involves osseointegration breaking and site repair.  
- Not for non-surgical removal (see D6105).  
- Document surgical approach, defect status, and re-treatment options.  

#### Code: D6105
**Heading:** Removal of implant body not requiring bone removal or flap elevation  
**When to Use:**  
- A mobile/failed implant is removed without surgical flaps.  
- Use for non-osseointegrated or loose implants.  
**What to Check:**  
- Confirm mobility via clinical exam.  
- Verify simple extraction (e.g., forceps) without bone work.  
- Assess site preservation post-removal.  
- Check future implant plans.  
**Notes:**  
- Less invasive than D6100, no flap needed.  
- Not for osseointegrated implants (see D6100).  
- Document ease of removal and site condition.  

#### Code: D6101
**Heading:** Debridement of a peri-implant defect or defects surrounding a single implant  
**When to Use:**  
- Surgical debridement is performed for peri-implantitis with flap access.  
- Use for ≥5mm pockets, bone loss, and non-surgical failure.  
**What to Check:**  
- Confirm peri-implantitis via radiograph/exam (e.g., bleeding, suppuration).  
- Verify flap access and implant surface detoxification.  
- Assess defect extent and non-surgical history.  
- Check no osseous work (see D6102).  
**Notes:**  
- Aims to halt infection without bone reshaping.  
- Not for grafts (see D6103) or contouring (see D6102).  
- Document defect details, cleaning methods, and tissue closure.  

#### Code: D6102
**Heading:** Debridement and osseous contouring of a peri-implant defect or defects surrounding a single implant  
**When to Use:**  
- Surgical debridement with bone recontouring is performed for peri-implantitis.  
- Use to create physiologic bone architecture.  
**What to Check:**  
- Confirm bone recontouring via surgical notes.  
- Verify peri-implantitis and flap access.  
- Assess initial vs. final bone morphology.  
- Check non-surgical failure history.  
**Notes:**  
- Enhances tissue adaptation via bone shaping.  
- Not for grafts (see D6103) or debridement alone (see D6101).  
- Document contouring extent, defect status, and flap management.  

#### Code: D6103
**Heading:** Bone graft for repair of peri-implant defect  
**When to Use:**  
- Bone graft material is placed to repair a peri-implant defect, excluding flap access.  
- Use with D6101/D6102 for peri-implantitis.  
**What to Check:**  
- Confirm graft material (e.g., allograft, xenograft) via specs.  
- Verify defect type/size via radiograph.  
- Ensure flap access coded separately (e.g., D6101).  
- Check regenerative goals.  
**Notes:**  
- Regenerates bone around affected implants.  
- Not for simultaneous implant placement grafts (see D6104).  
- Document graft type, quantity, and defect morphology.  

#### Code: D6104
**Heading:** Bone graft at time of implant placement  
**When to Use:**  
- Bone graft is placed during implant surgery to address defects or augment ridge.  
- Use for gaps, thread coverage, or ridge enhancement.  
**What to Check:**  
- Confirm graft purpose (e.g., socket gap, sinus lift) via notes.  
- Verify graft material, quantity, and defect anatomy.  
- Assess simultaneous implant placement.  
- Check esthetic/stability goals.  
**Notes:**  
- Enhances implant support and esthetics.  
- Not for post-implant defects (see D6103).  
- Document graft specifics, implant relation, and site anatomy.  

#### Code: D6106
**Heading:** Guided tissue regeneration — resorbable barrier, per implant  
**When to Use:**  
- A resorbable membrane is placed for guided tissue regeneration around an implant.  
- Use with grafts for peri-implant defects or placement.  
**What to Check:**  
- Confirm resorbable membrane (e.g., collagen) via specs.  
- Verify stabilization and defect adaptation.  
- Assess flap management to prevent exposure.  
- Check resorption timeline.  
**Notes:**  
- Prevents soft tissue ingrowth, no removal surgery needed.  
- Not for non-resorbable barriers (see D6107). 
- Document membrane type, stabilization, and defect details.  

#### Code: D6107
**Heading:** Guided tissue regeneration — non-resorbable barrier, per implant  
**When to Use:**  
- A non-resorbable membrane is placed for guided tissue regeneration.  
- Use for large defects or vertical augmentation.  
**What to Check:**  
- Confirm non-resorbable membrane (e.g., PTFE, titanium) via specs.  
- Verify planned removal surgery (4-6 months).  
- Assess space maintenance and defect complexity.  
- Check flap closure for coverage.  
**Notes:**  
- Offers superior space maintenance, requires second surgery.  
- Not for resorbable barriers (see D6106).  
- Document membrane type, defect size, and removal plan.  

---

### Key Takeaways:
- **Implant Types:** Codes differentiate endosteal (D6010–D6013), eposteal (D6040), and transosteal (D6050) implants.  
- **Procedure Stages:** Separate initial placement (D6010, D6012–D6013, D6040, D6050), second-stage (D6011), removal (D6100, D6105), and peri-implant treatments (D6101–D6104, D6106–D6107).  
- **Complexity Matters:** Removal and peri-implant codes vary by surgical extent (e.g., flap vs. no flap, bone work vs. none).  
- **Regeneration Focus:** Grafting (D6103–D6104) and membranes (D6106–D6107) address defects or augmentation.  
- **Documentation Critical:** Specify implant specs, materials, defect details, and clinical rationale for reimbursement.  
- **Rare Codes:** Eposteal (D6040) and transosteal (D6050) are nearly obsolete but included for completeness.  
- **Patient Factors:** Consider anatomy, bone quality, and prosthetic goals in code selection.

Scenario: {{scenario}}

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_surgical_services_code(self, scenario: str) -> str:
        """Extract surgical implant services code(s) for a given scenario."""
        try:
            print(f"Analyzing surgical implant scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Surgical services extract_surgical_services_code result: {code}")
            if code.lower() in ["none", "", "not applicable"]:
                return ""
            return code
        except Exception as e:
            print(f"Error in surgical services code extraction: {str(e)}")
            return ""
    
    def activate_surgical_services(self, scenario: str) -> str:
        """Activate the surgical implant services analysis process and return results."""
        try:
            result = self.extract_surgical_services_code(scenario)
            if not result:
                print("No surgical implant code returned")
                return ""
            return result
        except Exception as e:
            print(f"Error activating surgical implant analysis: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_surgical_services(scenario)
        print(f"\n=== SURGICAL IMPLANT SERVICES ANALYSIS RESULT ===")
        print(f"SURGICAL IMPLANT CODE: {result if result else 'None'}")

surgical_service = SurgicalImplantServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter a surgical implant services dental scenario: ")
    surgical_service.run_analysis(scenario)