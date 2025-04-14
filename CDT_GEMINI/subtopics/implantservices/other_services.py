"""
Module for extracting other implant services codes.
"""

import os
import sys
from langchain.prompts import PromptTemplate
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file
from subtopics.prompt.prompt import PROMPT



def create_other_implant_services_extractor():
    """
    Creates a LangChain-based extractor for other implant services codes.
    """
    template = f"""
    You are a dental coding expert specializing in implant services.
    
  ## **Other Implant Services** 
 
### **Before picking a code, ask:** 
- What type of service is being performed? (maintenance, repair, replacement, etc.)
- Is the procedure related to an existing implant, abutment, or implant-supported prosthesis?
- Is the procedure addressing a complication or part of routine maintenance?
- Is this a replacement of a component or repair of an existing component?
- Is the procedure for a removable or fixed prosthesis?
- Does the procedure involve specific components like retaining screws or semi-precision attachments?
 
---
 
### **Implant Maintenance**
 
#### **Code: D6080** – *Implant maintenance procedures when prostheses are removed and reinserted, including cleansing of prostheses and abutments* 
**Use when:** Performing professional maintenance of an implant-supported fixed prosthesis that requires removal, cleaning, and reinsertion.
**Check:** Verify that the prosthesis was actually removed for cleaning and then reinserted rather than simply cleaned in place.
**Note:** This comprehensive maintenance procedure involves the careful removal of a fixed implant-supported prosthesis (not a procedure for removable overdentures), thorough cleansing of both the prosthesis and the supporting abutments, inspection of all components for wear or damage, evaluation of peri-implant tissues, and precise reinsertion with verification of proper seating and, if applicable, retightening of screws to recommended torque values.
**Frequency Considerations:** The appropriate interval for this procedure varies based on patient-specific factors including oral hygiene, restoration design, accessibility for home care, peri-implant tissue health, and risk factors for peri-implantitis, but typically may be performed every 3-6 months for high-risk patients and annually for lower-risk patients.
**Documentation Requirements:** Records should specify the type of prosthesis maintained, cleaning methods employed, condition of components, any issues identified requiring further attention, and home care instructions provided to the patient.
 
#### **Code: D6081** – *Scaling and debridement in the presence of inflammation or mucositis of a single implant* 
**Use when:** Performing non-surgical periodontal maintenance specifically focused on an implant showing signs of peri-implant mucositis.
**Check:** Document the presence of inflammation or mucositis around the implant being treated.
**Note:** This focused procedure addresses early peri-implant inflammation (mucositis) through careful instrumentation to remove biofilm and calculus from a single implant using specialized instruments designed not to damage implant surfaces (such as plastic, carbon fiber, or titanium instruments), irrigation with antimicrobial solutions, and site-specific home care instructions.
**Clinical Distinction:** This code is specific to a single implant showing signs of inflammation without bone loss and cannot be reported in conjunction with D1110, D4910, or D4346 in the same visit.
**Treatment Goal:** The objective is to arrest inflammation before it progresses to peri-implantitis with bone loss, focusing on biofilm disruption, decontamination of the implant surface, and establishing an environment conducive to tissue healing.
 
---
 
### **Provisional Components**
 
#### **Code: D6085** – *Provisional implant crown* 
**Use when:** Placing a temporary crown on an implant during the healing phase before the final prosthesis.
**Check:** Document the purpose of the provisional crown and its expected duration of service.
**Note:** This temporary restoration serves multiple critical functions beyond simple space maintenance, including development of optimal emergence profile and gingival architecture, assessment of esthetic outcomes before final restoration commitment, protection of the implant from unwanted loading vectors, and evaluation of occlusal function.
**Treatment Planning:** The provisional may be used to gradually shape soft tissues through controlled pressure, evaluate phonetics, confirm patient satisfaction with esthetics, and guide the laboratory in creating the definitive prosthesis.
**Material Selection:** Documentation should specify the material used (typically acrylic, composite, or polymer), whether the provisional is screw-retained or cement-retained, and any modifications made during the provisionalization period.
 
---
 
### **Repairs and Modifications**
 
#### **Code: D6090** – *Repair implant supported prosthesis, by report* 
**Use when:** Performing repairs to an implant-supported prosthesis that cannot be removed by the patient.
**Check:** Provide a narrative report detailing the nature of the damage and the specific repairs performed.
**Note:** This procedure encompasses a wide range of potential repairs to fixed implant-supported prostheses, including but not limited to repair of fractured porcelain or acrylic, replacement of artificial teeth on the prosthesis, repair of framework components, and addressing issues with retentive elements or coatings.
**Procedural Complexity:** The specific techniques and materials used vary significantly based on the nature of the damage, the prosthesis design, and the materials involved, which must be clearly documented in the accompanying narrative report.
**Documentation Requirements:** A detailed narrative should specify the type of prosthesis, the nature and extent of damage, repair materials and techniques utilized, and any limitations or durability concerns regarding the repairs performed.
 
#### **Code: D6091** – *Replacement of replaceable part of semi-precision or precision attachment of implant/abutment supported prosthesis, per attachment* 
**Use when:** Replacing a worn component of an attachment system used with an implant-supported prosthesis.
**Check:** Identify the specific attachment being replaced and confirm it is a replaceable part of a semi-precision or precision attachment.
**Note:** This procedure focuses on the replacement of worn or damaged components within a precision or semi-precision attachment system—such as nylon inserts, rubber O-rings, clips, or other retentive elements—that connect a removable prosthesis to implant abutments, restoring optimal retention and function of the prosthetic device.
**Component Specificity:** The code is reported per attachment component replaced, with clear documentation of the specific type, brand, and position of each attachment serviced.
**Maintenance Protocol:** These replaceable components typically require periodic replacement due to normal wear and loss of retention, with frequency depending on factors such as attachment design, patient habits, and biomechanical forces.
 
#### **Code: D6092** – *Re-cement or re-bond implant/abutment supported crown* 
**Use when:** Re-cementing a crown that has become loose from an implant abutment.
**Check:** Document that the original crown is intact and suitable for re-cementation rather than replacement.
**Note:** This procedure involves the careful removal of residual cement from both the crown and abutment, assessment of crown integrity, thorough cleaning and preparation of surfaces, application of appropriate cement, precise reseating of the crown, removal of excess cement (especially in subgingival areas), and verification of proper fit, contacts, and occlusion.
**Clinical Considerations:** The choice of cement for re-cementation is critical, with factors including margin depth, retrievability requirements, and retention needs dictating whether a temporary or permanent luting agent is most appropriate.
**Root Cause Analysis:** Documentation should address potential causes of the initial cement failure (such as inadequate retention form, improper cement selection, or occlusal factors) and any modifications made to prevent recurrence.
 
#### **Code: D6093** – *Re-cement or re-bond implant/abutment supported fixed partial denture* 
**Use when:** Re-cementing a fixed partial denture (bridge) that has become loose from implant abutments.
**Check:** Verify that the prosthesis is intact and suitable for re-cementation rather than replacement.
**Note:** Similar to D6092 but involving a multi-unit fixed prosthesis, this procedure requires careful assessment of fit at multiple abutments, thorough cleaning of all components, appropriate cement selection, precise seating with special attention to complete adaptation at all abutment interfaces, and verification of proper contacts and occlusion along the entire prosthesis.
**Technical Challenges:** Re-cementing a multi-unit prosthesis presents additional challenges in ensuring complete seating, managing excess cement at multiple interfaces, and addressing potential distortion that may have occurred when the prosthesis became dislodged.
**Preventive Measures:** Documentation should address factors that may have contributed to cement failure and any modifications to cement type, prosthesis design, or occlusal adjustments made to prevent recurrence.
 
#### **Code: D6095** – *Repair implant abutment, by report* 
**Use when:** Repairing a damaged implant abutment rather than replacing it.
**Check:** Provide a detailed narrative describing the damage and specific repair procedures performed.
**Note:** This procedure involves addressing damage to an implant abutment through various repair methods rather than complete replacement, which might include re-contouring damaged areas, thread repair, repairing fractures or fissures, addressing connection issues, or modifying the emergence profile for better tissue adaptation.
**Technical Assessment:** Documentation should include evaluation of whether repair is appropriate versus replacement, considering the location and extent of damage, the structural integrity of the abutment, and the long-term prognosis for the repaired component.
**Repair Methods:** The narrative should specify exactly what was repaired, the techniques and materials used, and any limitations that may affect the longevity or function of the repaired abutment.
 
#### **Code: D6096** – *Remove broken implant retaining screw* 
**Use when:** Removing a fractured screw from within an implant body.
**Check:** Document the location of the broken screw and the technique used for removal.
**Note:** This technically demanding procedure addresses a serious complication when a screw fractures within the implant body, using specialized instrumentation and techniques for retrieval without damaging the internal implant connection—such as screw retrieval kits, ultrasonic instruments, modified burs, or reverse torque devices—followed by inspection of the implant threads and internal connection for damage before placement of a new screw.
**Complication Risk:** Attempts at removal carry risk of further damage to the implant's internal connection, which could render the implant unusable for conventional restoration, potentially necessitating the use of alternative components or implant removal.
**Clinical Decision-Making:** Documentation should address the cause of screw fracture when identifiable (such as occlusal overload, improper torque, fatigue, or manufacturing defect) and preventive measures to reduce risk of recurrence.
 
---
 
### **Abutment and Implant Supported Prosthetic Components**
 
#### **Code: D6097** – *Abutment supported crown – porcelain fused to titanium and titanium alloys* 
**Use when:** Placing a porcelain-fused-to-titanium crown on an implant abutment.
**Check:** Verify that the restoration is specifically a crown supported by an abutment and involves porcelain fused to titanium.
**Note:** This crown combines the esthetic benefits of porcelain with the excellent biocompatibility and strength of titanium, providing an optimal solution for patients with metal sensitivities while delivering excellent esthetics and durability.
**Material Properties:** The titanium substructure offers superior strength-to-weight ratio compared to other metal options, with excellent tissue compatibility, while supporting a porcelain veneer that provides natural appearance.
**Clinical Applications:** Particularly valuable in cases where biocompatibility is a primary concern, this restoration is suitable for both anterior and posterior locations with good esthetic outcomes.
 
#### **Code: D6098** – *Implant supported retainer – porcelain fused to predominantly base alloys* 
**Use when:** Placing a porcelain-fused-to-base-metal retainer directly on an implant as part of a fixed partial denture.
**Check:** Confirm that this is a retainer for a fixed partial denture (not a single crown) attached directly to an implant without an intermediate abutment.
**Note:** This retainer utilizes predominantly base metal alloys (containing <25% noble metal) as its substructure, providing economical strength while supporting a porcelain veneer for improved esthetics.
**Material Selection:** Base alloys offer cost advantages while maintaining adequate strength for posterior applications where occlusal forces are significant, though they may have less optimal biocompatibility compared to noble metal options.
**Documentation Specifics:** Records should clearly distinguish this code from single crown codes, noting that it specifically applies to a component of a fixed partial denture directly supported by an implant.
 
#### **Code: D6099** – *Implant supported retainer for FPD – porcelain fused to noble alloys* 
**Use when:** Placing a porcelain-fused-to-noble-metal retainer directly on an implant as part of a fixed partial denture.
**Check:** Verify that this is a retainer for a fixed partial denture attached directly to an implant and uses noble metal alloys.
**Note:** This retainer incorporates noble metal alloys (containing ≥25% noble metal) in its substructure, balancing moderate cost with good biocompatibility, corrosion resistance, and adequate strength to support a porcelain veneer in a multi-unit fixed prosthesis.
**Clinical Considerations:** Noble alloys offer better biocompatibility than base metals but at higher cost, suitable for patients with moderate metal sensitivity concerns or when optimal tissue response is desired without the premium cost of high noble metals.
**Technical Specifics:** Documentation should specify that this is a component of a multi-unit fixed prosthesis directly attached to an implant rather than utilizing an intermediate abutment.
 
---
 
### **Implant Removal and Peri-Implant Treatments**
 
#### **Code: D6100** – *Implant removal, by report* 
**Use when:** Surgically removing a previously placed implant that requires a surgical approach with flap elevation.
**Check:** Document the reason for implant removal (failure, infection, malposition, etc.) and provide a detailed narrative of the procedure.
**Note:** This surgical procedure involves creating a flap to access the implant site, removing bone as necessary to expose the implant, using specialized instruments to break osseointegration, extracting the implant, debriding the site, managing the remaining defect, and suturing the flap closed.
**Clinical Indications:** Removal may be necessary due to implant failure (mobility, infection, persistent pain), peri-implantitis that hasn't responded to treatment, implant fracture, or malposition that cannot be managed prosthetically.
**Documentation Requirements:** The narrative report should detail the original implant placement date if known, reason for removal, surgical approach, instrumentation used, site management after removal, and plans for potential future implant placement or alternative prosthesis.
 
#### **Code: D6101** – *Debridement of a peri-implant defect or defects surrounding a single implant* 
**Use when:** Performing surgical debridement of infected tissue around an implant, including flap access and surface cleaning.
**Check:** Document the presence of a peri-implant defect requiring surgical intervention.
**Note:** This procedure addresses peri-implantitis by creating a surgical flap to access the defect, removing granulation and infected tissue, detoxifying the implant surface using mechanical and/or chemical means, and repositioning and suturing the flap to facilitate healing.
**Procedural Details:** Includes flap entry and closure as well as surface cleaning of exposed implant surfaces, but does not include osseous recontouring or regenerative procedures.
**Clinical Context:** Appropriate for peri-implantitis cases showing pocket depths ≥5mm, bleeding/suppuration on probing, and radiographic evidence of bone loss, where non-surgical approaches have failed.
 
#### **Code: D6102** – *Debridement and osseous contouring of a peri-implant defect or defects surrounding a single implant* 
**Use when:** Performing surgical debridement with additional bone recontouring around an affected implant.
**Check:** Verify that the procedure includes both soft tissue debridement and osseous recontouring.
**Note:** This comprehensive procedure builds upon D6101 by adding osseous recontouring to establish a more physiologic bone architecture around the implant, potentially removing sharp edges, creating positive architecture, or eliminating bony defects to create a more cleansable environment.
**Surgical Objectives:** The goal is to eliminate the infectious process, create favorable architecture for soft tissue adaptation to the implant, and establish conditions conducive to long-term health.
**Anatomical Considerations:** Documentation should detail the initial bone defect morphology, the extent of recontouring performed, and the final bone architecture achieved.
 
#### **Code: D6103** – *Bone graft for repair of peri-implant defect* 
**Use when:** Placing bone graft material to repair a defect around an implant, not including flap entry and closure.
**Check:** Document the type of bone graft material used and specify that this code does not include flap access.
**Note:** This procedure focuses on placement of bone replacement grafts to regenerate lost bone support around an implant affected by peri-implantitis or other defects, typically used in conjunction with D6101 or D6102 (which include the flap access).
**Material Selection:** Documentation should specify the type, brand, and quantity of graft material used, whether autogenous, allograft, xenograft, or synthetic, and any additives or biologics incorporated.
**Procedural Context:** This code is typically reported together with other codes that provide the surgical access, as it specifically excludes flap entry and closure.
 
#### **Code: D6104** – *Bone graft at time of implant placement* 
**Use when:** Placing bone graft material simultaneously with implant placement to address defects or augment ridge dimensions.
**Check:** Document the reason for simultaneous bone grafting and its relationship to the implant placement.
**Note:** This procedure involves the placement of bone replacement materials during the same surgical appointment as implant placement, addressing situations such as jumping gaps between implant and socket walls, covering exposed implant threads, or enhancing ridge dimensions.
**Clinical Applications:** Common uses include immediate implant placement with socket grafting, simultaneous sinus augmentation, guided bone regeneration for dehiscence or fenestration defects, and horizontal ridge augmentation concurrent with implant placement.
**Material Documentation:** Records should specify the type and amount of graft material used, the defect being addressed, and the relationship between the graft and the implant placement.
 
---
 
### **Implant/Abutment Supported Removable Dentures**
 
#### **Code: D6110** – *Implant/abutment supported removable denture for edentulous arch – maxillary* 
**Use when:** Creating a removable prosthesis for a completely edentulous upper arch that is supported by implants or abutments.
**Check:** Verify that the upper arch is fully edentulous and document the number and position of supporting implants or abutments.
**Note:** This prosthesis (often called an overdenture) provides significantly improved stability, retention and function compared to conventional dentures while allowing removal for hygiene and maintenance.
**Attachment Systems:** Documentation should specify the type of attachment system used (such as locator attachments, ball attachments, or bar-clip systems) and the number of implants supporting the denture.
**Patient Benefits:** This restoration provides enhanced chewing efficiency, improved phonetics, and greater patient confidence compared to conventional removable prostheses.
 
#### **Code: D6111** – *Implant/abutment supported removable denture for edentulous arch – mandibular* 
**Use when:** Creating a removable prosthesis for a completely edentulous lower arch that is supported by implants or abutments.
**Check:** Confirm the lower arch is completely without teeth and document the supporting implants or abutments.
**Note:** Lower implant-supported overdentures offer particularly significant quality-of-life improvements due to the inherent instability of conventional mandibular dentures, with even two implants providing substantial enhancement in retention and stability.
**Clinical Standard:** The mandibular two-implant overdenture is often considered a standard of care for the edentulous mandible, providing dramatic improvement with minimal implant support.
**Maintenance Considerations:** Documentation should address attachment selection, maintenance requirements, and patient education regarding home care and periodic professional maintenance.
 
#### **Code: D6112** – *Implant/abutment supported removable denture for partially edentulous arch – maxillary* 
**Use when:** Creating a removable prosthesis for a partially edentulous upper arch that is supported by both implants/abutments and natural teeth.
**Check:** Document which natural teeth remain and the position of supporting implants or abutments.
**Note:** This hybrid prosthesis combines the stability of implant support with the proprioception of natural teeth, allowing for strategic implant placement to overcome limitations of conventional partial dentures.
**Design Considerations:** The prosthesis requires careful planning for force distribution between implants and natural teeth, with specialized attachment systems to accommodate different support types.
**Biomechanical Factors:** Documentation should address how the design accommodates the differential support provided by rigid implants versus the periodontal ligament-supported natural teeth.
 
#### **Code: D6113** – *Implant/abutment supported removable denture for partially edentulous arch – mandibular* 
**Use when:** Creating a removable prosthesis for a partially edentulous lower arch that is supported by both implants/abutments and natural teeth.
**Check:** Specify which natural teeth remain and how the implants are integrated into the support system.
**Note:** This prosthesis significantly improves stability compared to conventional removable partial dentures, particularly in distal extension cases where posterior implant support eliminates the common problems of movement and food entrapment.
**Strategic Implant Placement:** Documentation should detail the strategic positioning of implants, often placed in posterior edentulous areas to eliminate movement and provide cross-arch stabilization.
**Attachment Selection:** For partially edentulous cases, attachment selection must consider integration with any clasps or other retention elements engaging the natural teeth.
 
---
 
### **Surgical Index and Component Management**
 
#### **Code: D6190** – *Radiographic/surgical implant index, by report* 
**Use when:** Creating a specialized appliance designed to relate osteotomy or fixture position to existing anatomic structures.
**Check:** Document the purpose of the index and provide a detailed narrative report.
**Note:** This specialized appliance serves as a precise guide for implant placement, ensuring optimal positioning relative to critical anatomic structures and prosthetic considerations.
**Clinical Applications:** Used during radiographic assessment for treatment planning and/or during surgery for precise implant placement, particularly valuable for complex cases involving multiple implants or proximity to vital structures.
**Documentation Specifics:** The narrative should detail how the index was created, what materials were used, and how it will be utilized during treatment planning or surgical phases.
 
#### **Code: D6197** – *Replacement of restorative material used to close an access opening of a screw-retained implant supported prosthesis, per implant* 
**Use when:** Replacing the filling material that covers a screw access channel in a screw-retained implant restoration.
**Check:** Document that this specifically involves replacing the access opening material, not recementing or replacing the entire prosthesis.
**Note:** This procedure restores the integrity and esthetics of a screw-retained implant prosthesis by replacing deteriorated or missing restorative material used to seal the screw access channel.
**Technical Considerations:** Proper execution involves color matching for anterior restorations, ensuring adequate bulk of restorative material, establishing appropriate occlusal contours, and preserving access to the underlying screw.
**Reporting Specifics:** This code is reported per implant, requiring separate reporting for each access opening replaced within a multi-unit prosthesis.
 
#### **Code: D6198** – *Remove interim implant component* 
**Use when:** Removing a temporary implant component that was placed for a specific clinical purpose.
**Check:** Document the type of interim component being removed and the reason for its removal.
**Note:** This procedure involves removing a temporary component (such as a healing abutment or provisional crown) that was placed for tissue management, space maintenance, or esthetic purposes during treatment.
**Procedural Context:** Unlike second stage surgery, this applies to the removal of interim components placed for a planned duration as part of the treatment sequence.
**Documentation Requirements:** Records should specify what component is being removed, how long it has been in place, and what will replace it.
 
---
 
### **Unspecified Procedures**
 
#### **Code: D6199** – *Unspecified implant procedure, by report* 
**Use when:** Performing an implant-related procedure that doesn't fit into any existing code description.
**Check:** Provide a comprehensive narrative describing the procedure, including indications, technique, and materials.
**Note:** This code serves as a mechanism for reporting legitimate implant-related procedures not accurately described by any other specific code, requiring a detailed narrative report explaining the nature, extent, and necessity of the service.
**Documentation Essentials:** The narrative must clearly establish medical necessity, detail techniques and materials used, and explain why existing codes are inadequate.
**Approval Considerations:** This code typically requires manual review by payers and may need additional supporting documentation.
 
---
 
### **Key Takeaways:** 
- The implant services category includes a wide range of procedures from maintenance to component replacement to management of complications.
- Proper code selection requires careful consideration of what specific component is being addressed and what exact service is being performed.
- Many codes in this category require "by report" documentation with detailed narratives explaining the specific circumstances and procedures.
- Repair codes (D6090, D6095) and replacement codes (D6091, D6197) address different components of the implant system and require clear documentation.
- Several codes represent specialized procedures addressing specific complications, such as broken screw removal (D6096).
- Maintenance procedures distinguish between comprehensive prosthesis removal/cleaning (D6080) and focused management of inflammation (D6081).
- Removable prosthesis codes (D6110-D6113) are differentiated based on whether the arch is fully or partially edentulous and whether it's maxillary or mandibular.
- For any procedure not covered by specific codes, the unspecified procedure code (D6199) can be used with appropriate narrative documentation.
    
    SCENARIO: {{scenario}}
    
    {PROMPT}
    """
    
    prompt = PromptTemplate(template=template, input_variables=["scenario"])
    return create_chain(prompt)

def extract_other_implant_services_code(scenario):
    """
    Extracts other implant services code(s) for a given scenario.
    """
    try:
        extractor = create_other_implant_services_extractor()
        result = invoke_chain(extractor, {"scenario": scenario})
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Error in other implant services code extraction: {str(e)}")
        return None

def activate_other_implant_services(scenario):
    """
    Analyze a dental scenario to determine other implant services code.
    
    Args:
        scenario (str): The dental scenario to analyze.
        
    Returns:
        str: The identified other implant services code or empty string if none found.
    """
    try:
        result = extract_other_implant_services_code(scenario)
        
        # Return empty string if no code found
        if result == "None" or not result or "not applicable" in result.lower():
            return ""
            
        return result
    except Exception as e:
        print(f"Error in activate_other_implant_services: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = "A patient with a four-unit implant-supported bridge in the maxillary arch presents with loosened composite filling material in one of the screw access channels. The dentist needs to replace this material to ensure proper function and esthetics."
    result = activate_other_implant_services(scenario)
    print(result)