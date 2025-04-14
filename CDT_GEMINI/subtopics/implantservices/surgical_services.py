"""
Module for extracting surgical implant services codes.
"""

import os
import sys
from langchain.prompts import PromptTemplate
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file
from subtopics.prompt.prompt import PROMPT



def create_surgical_services_extractor():
    """
    Creates a LangChain-based extractor for surgical implant services codes.
    """
    template = f"""
    You are a dental coding expert specializing in implant services.
    
  ## **Surgical Implant Services** 
 
### **Before picking a code, ask:** 
- What type of implant is being placed? (endosteal, eposteal, transosteal, mini)
- Is this an initial surgical placement or a second stage surgery?
- Is the implant intended for a permanent prosthesis or an interim/transitional prosthesis?
- Is bone grafting or guided tissue regeneration being performed in conjunction with the implant?
- Is the procedure related to implant placement, removal, or management of peri-implant conditions?
- Are there specific anatomical or patient factors affecting the complexity of the procedure?
 
---
 
### **Implant Placement**
 
#### **Code: D6010** – *Surgical placement of implant body: endosteal implant* 
**Use when:** Surgically placing an implant body into the jawbone that will eventually support a prosthetic device.
**Check:** Verify that proper pre-surgical planning, including radiographs and assessment of bone quality and quantity, has been completed and documented.
**Note:** Endosteal implants are the most common type used in modern dentistry, typically made of titanium and designed to integrate with the bone through osseointegration, with various designs (threaded, press-fit, etc.) available to accommodate different clinical situations, bone densities, and prosthetic requirements.
**Procedure Specifics:** This code covers the surgical placement only, including flap creation, osteotomy preparation, implant insertion, and primary closure; it does not include any prosthetic components, second-stage surgery, or associated procedures such as bone grafting or tissue regeneration.
**Documentation Requirements:** Records should specify implant type, size, manufacturer, lot number, location (tooth position), insertion torque if applicable, and any intraoperative findings or complications that may affect integration or subsequent treatment.
 
#### **Code: D6011** – *Surgical access to an implant body (second stage implant surgery)* 
**Use when:** Performing the second-stage surgery to expose a previously placed implant for attachment of a healing abutment or other fixture.
**Check:** Document the timing since initial implant placement and clinical/radiographic evidence of successful osseointegration.
**Note:** This procedure involves creating access to a submerged implant by removing overlying soft tissue, allowing for the placement of healing abutments that help shape the peri-implant gingival architecture or for the attachment of permanent abutments or prosthetic components.
**Technique Variations:** The approach may involve a simple punch technique for ideally positioned implants with adequate keratinized tissue, or more complex flap procedures for implants requiring soft tissue modification, especially in esthetic zones where emergence profile management is critical.
**Clinical Significance:** This stage marks the transition from the osseointegration phase to the prosthetic phase of implant treatment and presents an opportunity to evaluate osseointegration and modify peri-implant soft tissues to optimize functional and esthetic outcomes.
 
#### **Code: D6012** – *Surgical placement of interim implant body for transitional prosthesis: endosteal implant* 
**Use when:** Placing an implant specifically intended to support a temporary prosthesis during healing or treatment phases.
**Check:** Clarify the interim nature of the implant and its role in the overall treatment plan.
**Note:** Interim implants provide temporary support for prostheses during the osseointegration period of definitive implants, allowing immediate function and esthetics while protecting healing implants from premature loading; they are typically smaller in diameter and may be designed for eventual removal.
**Treatment Planning:** Document the planned duration of use, loading protocol, and relationship to definitive implants in the overall treatment sequence.
**Patient Education:** Records should indicate that the patient understands the temporary nature of these implants and the subsequent treatment phases required.
 
#### **Code: D6013** – *Surgical placement of mini implant* 
**Use when:** Placing a mini implant (typically less than 3mm in diameter) designed for long-term use.
**Check:** Verify that the implant diameter qualifies as a mini implant according to manufacturer specifications.
**Note:** Mini implants serve specific clinical situations such as severely atrophic ridges with inadequate width for standard implants, transitional support during comprehensive treatment, or stabilization of removable prostheses in patients with medical or anatomical contraindications to extensive surgical procedures.
**Clinical Applications:** These smaller-diameter implants are particularly useful for narrow edentulous spaces, overdenture stabilization with minimal available bone, and for patients who cannot tolerate more invasive surgical procedures, though they have limitations regarding load-bearing capacity compared to standard implants.
**Biomechanical Considerations:** Documentation should address how the treatment plan accounts for the reduced surface area and structural strength of mini implants, including prosthetic design modifications and occlusal management strategies.
 
#### **Code: D6040** – *Surgical placement: eposteal implant* 
**Use when:** Placing a subperiosteal framework on the surface of the jawbone.
**Check:** Document the reason for selecting an eposteal implant rather than an endosteal option.
**Note:** Eposteal (subperiosteal) implants rest upon the bone surface beneath the periosteum rather than within the bone, using a custom-fabricated framework designed from CT scans or direct bone impressions, with permucosal extensions that protrude through the gingiva to support prostheses.
**Clinical Indications:** These implants are rarely used in modern implantology but may be considered in cases of severe bone atrophy where endosteal implants cannot be placed and the patient cannot or will not undergo extensive bone grafting procedures.
**Procedural Complexity:** This is typically a two-stage procedure requiring an initial surgery for bone impression or advanced imaging, followed by framework fabrication and a second surgery for placement; the code includes both surgical phases when performed.
 
#### **Code: D6050** – *Surgical placement: transosteal implant* 
**Use when:** Placing an implant that penetrates both cortical plates of the mandible.
**Check:** Verify that the implant design penetrates completely through the mandible, from the inferior border to the oral cavity.
**Note:** Transosteal implants consist of a baseplate attached to the inferior border of the mandible with threaded posts that pass completely through the bone into the oral cavity, providing support for fixed or removable prostheses in the severely atrophic mandible.
**Historical Context:** These implants are now rarely used due to the development of advanced bone grafting techniques and the success of endosteal implants, but may still be documented in older cases or in extremely specific clinical scenarios where other options have failed.
**Anatomical Considerations:** Documentation should include assessment of mandibular height, vital structure location (particularly the inferior alveolar nerve), and access considerations for the extraoral surgical approach typically required.
 
---
 
### **Implant Removal**
 
#### **Code: D6100** – *Surgical removal of implant body* 
**Use when:** Surgically removing a previously placed implant body that requires a surgical approach with flap elevation.
**Check:** Document the reason for implant removal (failure, infection, malposition, etc.) and that the procedure involves surgical access.
**Note:** This procedure involves creating a surgical flap, possibly removing bone to access the implant, using specialized instrumentation to break the osseointegration, extracting the implant, debriding the site, and managing the resulting defect, which may require grafting in preparation for future implant placement.
**Clinical Indications:** Removal may be necessary due to implant failure (mobility, persistent infection, unresolvable peri-implantitis), prosthetic complications, implant fracture, or malposition that cannot be corrected prosthetically.
**Treatment Planning:** Documentation should address site management after removal and future treatment options, including the potential for immediate or delayed replacement implant placement.
 
#### **Code: D6105** – *Removal of implant body not requiring bone removal or flap elevation* 
**Use when:** Removing a failed or mobile implant that can be extracted without creating a surgical flap or removing bone.
**Check:** Verify that the implant can be removed without significant surgical intervention due to mobility or lack of osseointegration.
**Note:** This less invasive procedure is appropriate when an implant has failed to integrate or has lost integration and exhibits mobility, allowing for simple removal with forceps or other basic instrumentation without the need for extensive surgical access.
**Procedural Distinction:** The key differential factor from D6100 is the lack of need for surgical flap elevation or bone removal to access and retrieve the implant.
**Post-Procedure Considerations:** Documentation should address site preservation measures, healing expectations, and plans for potential future implant placement at the site.
 
---
 
### **Peri-Implant Treatments**
 
#### **Code: D6101** – *Debridement of a peri-implant defect or defects surrounding a single implant* 
**Use when:** Performing surgical debridement of infected tissue around an implant, including flap access and surface cleaning.
**Check:** Document the presence of a peri-implant defect requiring surgical intervention beyond non-surgical therapy.
**Note:** This procedure involves creating a surgical flap to access the peri-implant defect, removing granulation and infected tissue, detoxifying the implant surface using mechanical and/or chemical means, and repositioning and suturing the flap to facilitate healing and potential reattachment of soft tissues to the implant.
**Clinical Indications:** Appropriate for peri-implantitis cases with pocket depths ≥5mm, bleeding/suppuration on probing, and radiographic evidence of bone loss, where non-surgical approaches have failed to resolve the infection and inflammation.
**Procedural Extent:** This code specifically includes flap entry and closure along with thorough debridement and implant surface decontamination, but does not include osseous recontouring or regenerative procedures.
 
#### **Code: D6102** – *Debridement and osseous contouring of a peri-implant defect or defects surrounding a single implant* 
**Use when:** Performing surgical debridement of an infected area around an implant that also includes reshaping of the surrounding bone.
**Check:** Document the need for bone recontouring in addition to soft tissue debridement around the affected implant.
**Note:** This more comprehensive procedure includes all elements of D6101 plus osseous recontouring to establish a more physiologic bone architecture around the implant, potentially removing sharp edges, creating positive architecture, or removing infected bone to create a more cleansable and maintainable environment.
**Surgical Objectives:** The goal is to eliminate the infectious process, create favorable architecture for soft tissue adaptation to the implant, and establish conditions conducive to long-term implant health and maintenance.
**Procedural Complexity:** This procedure requires careful evaluation of remaining bone support, strategic contouring to maintain sufficient osseous support while eliminating defects, and meticulous soft tissue management for optimal healing.
 
#### **Code: D6103** – *Bone graft for repair of peri-implant defect* 
**Use when:** Placing bone graft material to repair a defect around an implant, not including flap entry and closure.
**Check:** Document the type of bone graft material used and the nature of the peri-implant defect being treated.
**Note:** This procedure focuses specifically on the placement of bone replacement grafts to regenerate lost bone support around an implant affected by peri-implantitis or other defects, employing materials such as autogenous bone, allografts, xenografts, or synthetic materials to stimulate new bone formation.
**Combined Procedures:** This code is typically reported in conjunction with D6101 or D6102 (which include the flap access) and may be used with D6106 or D6107 if barrier membranes are also employed as part of a guided tissue regeneration approach.
**Documentation Requirements:** Records should specify the type, brand, and quantity of graft material used, any additives or biologics incorporated (such as growth factors), and the specific defect morphology being treated.
 
#### **Code: D6104** – *Bone graft at time of implant placement* 
**Use when:** Placing bone graft material simultaneously with implant placement to address defects or augment ridge dimensions.
**Check:** Document the reason for simultaneous bone grafting and the relationship to the implant placement.
**Note:** This procedure involves the placement of bone replacement materials during the same surgical appointment as implant placement, addressing situations such as jumping gaps between implant and socket walls, covering exposed implant threads, or enhancing ridge dimensions to improve implant support and esthetic outcomes.
**Clinical Scenarios:** Common applications include immediate implant placement with socket grafting, simultaneous sinus augmentation with lateral window or crestal approaches, guided bone regeneration for dehiscence or fenestration defects, and horizontal ridge augmentation concurrent with implant placement.
**Material Selection:** Documentation should specify the graft materials selected based on the specific defect characteristics, healing timeline, and regenerative objectives of the case.
 
#### **Code: D6106** – *Guided tissue regeneration — resorbable barrier, per implant* 
**Use when:** Placing a resorbable membrane as part of guided tissue regeneration for a peri-implant defect or during implant placement.
**Check:** Verify the use of a resorbable barrier membrane and document the type of membrane used.
**Note:** This procedure involves the strategic placement of a biodegradable membrane (made of materials such as collagen, polylactic acid, or polyglycolic acid) to prevent soft tissue ingrowth into bone defects around implants, creating a protected space for bone regeneration while eliminating the need for a second surgery for membrane removal.
**Barrier Function:** The membrane serves to exclude epithelial and connective tissue cells from the healing site while allowing space for slower-migrating osteogenic cells to populate the defect, enhancing the predictability of bone regeneration when used in conjunction with bone grafting materials.
**Technique Considerations:** Documentation should address membrane stabilization methods, adaptation to the defect and implant, flap management to avoid membrane exposure, and expected resorption timeline of the specific barrier material selected.
 
#### **Code: D6107** – *Guided tissue regeneration — non-resorbable barrier, per implant* 
**Use when:** Placing a non-resorbable membrane as part of guided tissue regeneration for a peri-implant defect.
**Check:** Document the use of a non-resorbable barrier requiring subsequent removal and specify the membrane type.
**Note:** This procedure employs a synthetic non-resorbable membrane (typically expanded polytetrafluoroethylene, titanium-reinforced PTFE, or titanium mesh) to exclude unwanted cell types from a healing site while maintaining space for bone regeneration, offering advantages of superior space maintenance and longer barrier function for challenging regenerative scenarios.
**Two-Stage Protocol:** This approach necessitates a second surgical procedure for membrane removal after sufficient healing (typically 4-6 months), which should be planned and documented as part of the treatment sequence.
**Case Selection:** Non-resorbable barriers are particularly valuable for large defects requiring significant space maintenance, vertical augmentation attempts, or situations where the predictable barrier function duration is critical to treatment success.
 
---
 
### **Key Takeaways:** 
- Proper code selection requires clear differentiation between the various types of implants (endosteal, eposteal, transosteal, mini) and understanding their distinct clinical applications.
- Second-stage surgery (D6011) is distinctly coded from initial implant placement and focuses on accessing the implant for prosthetic phases.
- Implant removal codes (D6100, D6105) are differentiated by the surgical complexity and need for flap elevation or bone removal.
- Peri-implant treatments are coded based on the specific procedures performed: debridement alone (D6101), debridement with osseous recontouring (D6102), or with bone grafting (D6103).
- Bone grafting may be performed at implant placement (D6104) or as a separate procedure for peri-implant defects (D6103).
- Guided tissue regeneration procedures are coded based on barrier type (resorbable D6106, non-resorbable D6107) and are reported per implant site.
- Detailed documentation of clinical rationale, specific materials used, and procedural details is essential for accurate coding and treatment planning.
    
    SCENARIO: {{scenario}}
    
    {PROMPT}
    """
    
    prompt = PromptTemplate(template=template, input_variables=["scenario"])
    return create_chain(prompt)

def extract_surgical_services_code(scenario):
    """
    Extracts surgical implant services code(s) for a given scenario.
    """
    try:
        extractor = create_surgical_services_extractor()
        result = invoke_chain(extractor, {"scenario": scenario})
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Error in surgical services code extraction: {str(e)}")
        return None

def activate_surgical_services(scenario):
    """
    Analyze a dental scenario to determine surgical implant services code.
    
    Args:
        scenario (str): The dental scenario to analyze.
        
    Returns:
        str: The identified surgical services code or empty string if none found.
    """
    try:
        result = extract_surgical_services_code(scenario)
        
        # Return empty string if no code found
        if result == "None" or not result or "not applicable" in result.lower():
            return ""
            
        return result
    except Exception as e:
        print(f"Error in activate_surgical_services: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = "A patient requires placement of an endosteal dental implant in position #19 (lower left first molar) to replace a missing tooth. The procedure involves flap elevation, osteotomy preparation, and implant insertion with primary closure. All necessary pre-surgical planning has been completed including CBCT and bone quality assessment."
    result = activate_surgical_services(scenario)
    print(result) 