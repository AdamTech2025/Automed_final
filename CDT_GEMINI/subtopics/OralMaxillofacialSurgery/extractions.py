"""
Module for extracting extractions codes.
"""

import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from llm_services import LLMService, get_service, set_model, set_temperature

# Load environment variables
load_dotenv()

class ExtractionsServices:
    """Class to analyze and extract extractions codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing extractions scenarios."""
        from subtopics.prompt.prompt import PROMPT
        return PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert specializing in oral surgery procedures,

## **Dental Extraction and Surgical Procedures**

### **Before picking a code, ask:**
- Is the tooth primary or permanent?
- Is the tooth fully erupted, partially erupted, or completely impacted?
- If impacted, what is the level of impaction (soft tissue, partial bony, complete bony)?
- Does the extraction require removal of bone and/or sectioning of the tooth?
- Are there unusual surgical complications present (e.g., nerve proximity, sinus relation)?
- Is the procedure for removal of a tooth or of residual root tips only?
- Is a mucoperiosteal flap elevation required for the extraction?
- Is the procedure an intentional partial tooth removal (coronectomy)?
- Does the procedure involve exposure, repositioning, or transplantation of teeth?
- Has there been a complication such as oroantral fistula or sinus perforation?
- Is the procedure for biopsy, sample collection, or anchorage device placement?
- Does the procedure involve corticotomy for orthodontic purposes?

---

#### **Code: D7111** – *Extraction, coronal remnants - primary tooth*
**Use when:** Removing soft tissue-retained coronal portions of a primary tooth where the roots have significantly resorbed, requiring minimal instrumentation and typically no anesthesia.
**Check:** Documentation should specify that the tooth is primary with resorbed roots, leaving only coronal remnants retained by soft tissue.
**Note:** This procedure involves minimal instrumentation, often requiring only forceps or elevators to remove the retained coronal fragment. The documentation should include the specific primary tooth designation, clinical presentation (visible decay, mobility, etc.), confirmation of significant root resorption, technique for removal, and post-extraction management. This code should not be used for extraction of intact primary teeth with substantial root structure remaining, which would typically be coded as D7140. The procedure note should document any local anesthesia used (or lack thereof) and confirmation of complete removal of all coronal fragments.

#### **Code: D7140** – *Extraction, erupted tooth or exposed root (elevation and/or forceps removal)*
**Use when:** Removing a fully erupted tooth or exposed root using closed extraction techniques, primarily forceps and/or elevators, without the need for surgical intervention such as flap elevation or bone removal.
**Check:** Documentation should confirm the tooth was fully erupted or the root was exposed, and that extraction was completed using non-surgical techniques.
**Note:** This routine extraction procedure involves the use of elevators and/or forceps to luxate and remove the tooth or exposed root. The documentation should include the specific tooth designation, indication for extraction, anesthesia administration, use of elevators for initial luxation, forceps application technique, confirmation of complete removal including any root tips, management of the extraction socket (curettage, irrigation), hemostasis measures, and post-extraction instructions provided to the patient. Any routine smoothing of sharp bony edges and closure of the socket should be noted. This code is not appropriate when the extraction required mucoperiosteal flap elevation, bone removal, or sectioning of the tooth (which would warrant code D7210 or higher).

#### **Code: D7210** – *Extraction, erupted tooth requiring removal of bone and/or sectioning of tooth, and including elevation of mucoperiosteal flap if indicated*
**Use when:** Extracting an erupted tooth that requires surgical techniques such as mucoperiosteal flap elevation, bone removal, and/or sectioning of the tooth due to factors that prevent routine forceps extraction.
**Check:** Documentation must specifically detail the surgical approach, including flap design if created, bone removal technique if performed, and/or sectioning of the tooth if required.
**Note:** This surgical extraction of an erupted tooth is performed when routine forceps techniques are insufficient due to factors such as extensive decay, crown fracture, dense bone, divergent roots, or ankylosis. The comprehensive documentation should include the specific tooth designation, indication for surgical approach, anesthesia technique, flap design and elevation if performed, extent and method of bone removal (bur, chisel, etc.), tooth sectioning pattern if utilized, delivery of tooth or root fragments, management of the surgical site (debridement, irrigation), closure technique, and post-operative instructions. The operative record should clearly articulate why a surgical approach was necessary rather than a routine extraction (D7140), as this distinction is critical for proper code selection.

#### **Code: D7220** – *Removal of impacted tooth - soft tissue*
**Use when:** Extracting a tooth with the occlusal surface covered by soft tissue, requiring a mucoperiosteal flap elevation for access but minimal or no bone removal.
**Check:** Documentation should confirm that the occlusal surface of the tooth was covered by soft tissue, requiring flap elevation, and describe the impaction classification.
**Note:** Soft tissue impactions involve teeth where the crown is covered by soft tissue but not bone. The detailed operative report should include the specific tooth designation, impaction classification (often with reference to radiographic findings), anesthesia technique, flap design and elevation, exposure of the tooth crown, extraction technique (which may include minimal bone removal at the cervical area or minor tooth sectioning), delivery of the tooth, management of the surgical site (debridement, irrigation), closure technique, and post-operative instructions. The distinction between this code and D7210 involves the pre-operative position of the tooth—D7220 applies to teeth that were not erupted through soft tissue prior to the procedure, whereas D7210 applies to erupted teeth requiring surgical techniques.

#### **Code: D7230** – *Removal of impacted tooth - partially bony*
**Use when:** Extracting a tooth with part of the crown covered by bone, requiring mucoperiosteal flap elevation and removal of the overlying bone for access, often with sectioning of the tooth.
**Check:** Documentation must establish that a portion of the crown was covered by bone (partial bony impaction), detail the bone removal required, and describe any tooth sectioning performed.
**Note:** Partially bony impactions present increased surgical complexity due to the bone coverage. The comprehensive operative report should include the specific tooth designation, radiographic impaction classification, anesthesia technique, flap design and elevation, extent and method of bone removal (quantifying amount and location), tooth sectioning pattern if utilized, delivery of tooth or fragments, management of the surgical site (debridement, irrigation), assessment of adjacent structures, closure technique, and detailed post-operative instructions. Documentation should clearly distinguish the partial bone coverage from complete bony impaction (where most or all of the crown is encased in bone), as this distinction determines code selection between D7230 and D7240.

#### **Code: D7240** – *Removal of impacted tooth - completely bony*
**Use when:** Extracting a tooth with the crown completely encased in bone, requiring extensive bone removal for access and typically sectioning of the tooth.
**Check:** Documentation should confirm that most or all of the crown was covered by bone (complete bony impaction), detail the extensive bone removal performed, and describe the tooth sectioning approach.
**Note:** Complete bony impactions represent high surgical complexity. The detailed operative report should include the specific tooth designation, radiographic impaction classification with evidence of complete bone coverage, anesthesia technique, flap design and elevation (often more extensive than for lesser impactions), comprehensive description of bone removal (location, extent, technique, instrumentation), tooth sectioning pattern and rationale, sequential delivery of tooth fragments, protection of adjacent vital structures, management of the surgical site (debridement, irrigation), closure technique, and comprehensive post-operative instructions. The significant difference in surgical complexity between partially and completely bony impactions should be clearly reflected in the documentation to support code selection, often with reference to preoperative imaging demonstrating the complete bone coverage.

#### **Code: D7241** – *Removal of impacted tooth - completely bony, with unusual surgical complications*
**Use when:** Extracting a completely bony impacted tooth that presents with additional unusual surgical complications such as unusual anatomic position, nerve proximity requiring dissection, or maxillary sinus involvement.
**Check:** Documentation must first establish a complete bony impaction AND then clearly identify and detail the specific unusual surgical complications that increased the procedural complexity beyond a standard complete bony impaction.
**Note:** This represents the highest complexity extraction code. The extensive operative report must document the specific tooth designation, radiographic impaction classification confirming complete bony impaction, AND the specific unusual surgical complications encountered. These might include aberrant tooth position (such as significant displacement or inverted orientation), proximity to vital structures requiring special dissection or protection (inferior alveolar nerve, lingual nerve), direct relationship to the maxillary sinus requiring separate management, significant density of surrounding bone requiring extensive osteotomy, dilacerated roots complicating delivery, or ankylosed tooth requiring extraordinary measures for removal. The documentation should detail specialized techniques employed to address these complications, protective measures for adjacent structures, any unexpected findings, management of anatomical spaces or structures, and comprehensive post-operative instructions specific to the complications encountered.

#### **Code: D7250** – *Removal of residual tooth roots (cutting procedure)*
**Use when:** Surgically removing root structure remaining after a previous incomplete extraction or tooth fracture, requiring a mucoperiosteal flap and typically bone removal for access.
**Check:** Documentation should confirm that only root structure remained (no significant coronal portion present), specify the surgical approach with mucoperiosteal flap elevation, and detail bone removal if required.
**Note:** This procedure specifically addresses situations where roots remain after previous extraction attempts or where a tooth has fractured at the gumline. The comprehensive documentation should include the specific tooth designation and retained root portions, reason for residual root status, radiographic findings, anesthesia technique, flap design and elevation, extent and method of bone removal to access the roots, technique for delivery of the root fragments, confirmation of complete removal, management of the surgical site (debridement, irrigation), closure technique, and post-operative instructions. This code is not appropriate for removal of exposed roots visible in the oral cavity, which would typically be coded as D7140. The need for a cutting procedure (flap, bone removal) is the key distinguishing factor.

#### **Code: D7251** – *Coronectomy - intentional partial tooth removal*
**Use when:** Intentionally removing only the crown portion of a tooth while deliberately leaving the roots in place to avoid neurovascular complications, typically performed on impacted mandibular third molars with intimate relationship to the inferior alveolar nerve.
**Check:** Documentation must clearly establish that leaving the roots was a deliberate treatment decision to prevent nerve injury, not an incomplete extraction, and should reference radiographic evidence of proximity to the neurovascular bundle.
**Note:** This procedure is specifically designed to prevent nerve injury by intentionally retaining roots that are in close proximity to the neurovascular bundle. The detailed operative report should include the specific tooth designation, radiographic evidence demonstrating the intimate relationship between the roots and the nerve (often with advanced imaging such as CBCT), discussion of the treatment decision including informed consent for intentional root retention, anesthesia technique, flap design and elevation, bone removal to expose the crown, level and technique of crown sectioning (typically at the cemento-enamel junction), smoothing of the remaining root surface, verification that the retained roots are completely covered by bone, radiographic confirmation of appropriate root retention, closure technique, and specialized post-operative instructions. Long-term follow-up plans should be documented, as retained roots require monitoring.

#### **Code: D7260** – *Oroantral fistula closure*
**Use when:** Surgically closing a pathologic communication between the oral cavity and maxillary sinus that has developed an epithelialized tract, typically using a soft tissue flap advancement technique.
**Check:** Documentation should confirm the presence of an established epithelialized communication between the oral cavity and sinus (not an acute perforation), and detail the specific surgical technique for closure.
**Note:** This procedure addresses a chronic communication between the oral cavity and maxillary sinus. The comprehensive operative report should include the etiology of the fistula (often following extraction of maxillary posterior teeth), duration of the communication, symptoms reported by the patient, diagnostic findings (including possible imaging showing sinus pathology), size and location of the fistula, anesthesia technique, management of the epithelialized tract (excision or freshening of margins), specific flap design (typically buccal advancement or palatal rotation), tension-free closure technique, layered closure if performed, measures to prevent recurrence, post-operative medications (antibiotics, decongestants), and specific instructions regarding sinus precautions. This code differs from primary closure of a sinus perforation (D7261) in that it addresses a chronic, epithelialized tract rather than an acute perforation.

#### **Code: D7261** – *Primary closure of a sinus perforation*
**Use when:** Performing immediate surgical closure of an acute opening into the maxillary sinus, typically occurring during extraction of maxillary posterior teeth, using various soft tissue closure techniques.
**Check:** Documentation should establish that an acute sinus perforation occurred (typically during another procedure such as an extraction) and detail the immediate surgical management to close the communication.
**Note:** This procedure addresses an acute, iatrogenic communication with the maxillary sinus. The detailed documentation should include the circumstances of the perforation (typically during extraction or implant preparation), immediate recognition of the perforation (positive air flow, Valsalva testing), size and location of the communication, technique to verify sinus membrane status, method of soft tissue closure (advancement flap, rotational flap, buccal fat pad), suturing technique to achieve primary tension-free closure, verification of closure, immediate post-operative instructions including sinus precautions (no nose-blowing, sneezing with open mouth, avoidance of straws), and prescription of appropriate medications (antibiotics, decongestants). This code should not be used for closure of chronic oroantral fistulas with established epithelialized tracts, which would be coded as D7260.

#### **Code: D7270** – *Tooth reimplantation and/or stabilization of accidentally evulsed or displaced tooth*
**Use when:** Reinserting and stabilizing a tooth that has been completely or partially avulsed from its socket due to trauma, or repositioning and stabilizing a tooth that has been significantly displaced from its normal position.
**Check:** Documentation should verify the traumatic nature of the tooth displacement or avulsion, and detail the reimplantation technique and stabilization method used.
**Note:** This procedure addresses dental trauma resulting in tooth avulsion or significant displacement. The comprehensive documentation should include the circumstances of the injury, time elapsed since avulsion (critical for prognosis), storage medium if the tooth was completely avulsed, assessment of socket integrity, cleaning and preparation of the root surface (avoiding damage to the periodontal ligament), technique for reinsertion, radiographic verification of proper positioning, specific method of splinting or stabilization (type of splint, materials used), occlusal adjustment if needed, prescriptions provided (antibiotics, analgesics), and detailed post-operative instructions. The documentation should also address the planned duration of splinting and the follow-up protocol for monitoring pulpal and periodontal healing. This code includes both the reimplantation and the stabilization components.

#### **Code: D7272** – *Tooth transplantation (includes reimplantation from one site to another)*
**Use when:** Surgically moving a tooth from one location in the mouth to another, typically to replace a missing tooth or to reposition a malpositioned tooth that cannot be moved orthodontically.
**Check:** Documentation should specify both the donor site and recipient site, detail the surgical technique for removal and transplantation, and describe the method of stabilization.
**Note:** This complex procedure involves moving a tooth from one socket to another within the same patient. The detailed operative report should document the indication for transplantation, preoperative assessment of donor tooth suitability (root formation stage, size compatibility), preparation of the recipient site, atraumatic extraction technique at the donor site, time management to minimize extra-oral exposure, preparation of the tooth if needed (endodontic consideration, root-end preparation), insertion technique, adjustments for fit, stabilization method, occlusal adjustment, radiographic verification of positioning, post-operative medications, and comprehensive follow-up protocol. The documentation should address both the donor site management and the recipient site preparation. This code includes both the transplantation procedure and the required stabilization.

#### **Code: D7280** – *Exposure of an unerupted tooth*
**Use when:** Surgically exposing the crown of an impacted tooth that is not intended for extraction, typically to facilitate orthodontic eruption.
**Check:** Documentation should confirm the tooth is unerupted/impacted, verify it is not being extracted, and detail the surgical approach for exposure.
**Note:** This procedure creates surgical access to an unerupted tooth for orthodontic purposes. The comprehensive documentation should include the specific tooth designation, preoperative radiographic assessment of tooth position and surrounding structures, consultation with the orthodontist regarding the desired approach (open vs. closed exposure), anesthesia technique, incision design, flap elevation, removal of overlying bone and/or soft tissue, methods to control hemorrhage, management of the surgical site (apical positioning of the flap for open technique or placement of orthodontic attachment and flap replacement for closed technique), and post-operative instructions. If an orthodontic attachment is placed during the procedure, code D7283 should be reported separately. The documentation should clearly distinguish this procedure from an extraction, emphasizing the preservation of the tooth for future orthodontic movement.

#### **Code: D7282** – *Mobilization of erupted or malpositioned tooth to aid eruption*
**Use when:** Using dental or surgical procedures to loosen a tooth that is erupted or malpositioned but mechanically impeded, to facilitate its movement into proper position.
**Check:** Documentation should verify that the tooth is partially erupted or malpositioned (not fully impacted), and detail the specific techniques used to mobilize the tooth without extraction.
**Note:** This procedure addresses teeth that are mechanically impeded from normal eruption or movement, often due to dense bone, fibrotic tissue, or ankylosis. The detailed documentation should include the specific tooth designation, diagnosis of the impediment to normal eruption, radiographic findings, anesthesia technique, surgical approach if utilized (incision, flap design), management of obstructing tissues or bone, specific mobilization technique (luxation with elevators, surgical uprighting, circumferential fibrotomy), verification of increased mobility, management of the surgical site, and post-operative instructions. This procedure is not used in conjunction with an extraction and is typically performed to aid orthodontic treatment or to facilitate natural eruption of a tooth. The documentation should address coordination with planned orthodontic therapy if applicable.

#### **Code: D7283** – *Placement of device to facilitate eruption of impacted tooth*
**Use when:** Attaching an orthodontic bracket, band, button, or chain to an unerupted tooth during its surgical exposure to aid in guided eruption.
**Check:** Documentation should confirm that an orthodontic attachment device was placed on the impacted tooth during the exposure procedure, and specify the type of device used.
**Note:** This procedure is performed in conjunction with surgical exposure of an impacted tooth (D7280), which should be reported separately. The detailed documentation should include the specific tooth designation, type of orthodontic attachment placed (bracket, button, gold chain), technique for bonding or securing the attachment, verification of secure placement, management of any traction devices or ligatures extending into the oral cavity, coordination with the orthodontist regarding desired direction of traction, and specific post-operative instructions related to the eruption device. The technique for maintaining access to the attachment (packing, stent) should be documented, as should any immediate traction applied. This code represents only the device placement component; the surgical exposure should be coded separately as D7280.

#### **Code: D7285** – *Incisional biopsy of oral tissue - hard (bone, tooth)*
**Use when:** Surgically removing a representative portion of bone or tooth tissue for histopathological examination, without removing the entire lesion.
**Check:** Documentation should specify that the biopsy involves hard tissue (bone or tooth), confirm that only a portion of the lesion was removed for diagnostic purposes, and detail the biopsy technique.
**Note:** This diagnostic procedure obtains a tissue sample of bone or tooth structure for pathological analysis. The comprehensive documentation should include the location and clinical characteristics of the lesion, suspected differential diagnosis, anesthesia technique, surgical approach for access, specific technique for obtaining the specimen (type of bur or instrument used), size and depth of the tissue sample, management of bleeding, handling of the specimen (fixation, labeling), closure technique, post-operative instructions, and the plan for follow-up once the pathology report is received. This code is used only for partial removal of a lesion for diagnostic purposes; it is not appropriate for apicoectomy procedures or complete lesion removal. Documentation should address the chain of custody for the specimen and confirm submission for pathological examination.

#### **Code: D7286** – *Incisional biopsy of oral tissue - soft*
**Use when:** Surgically removing a representative portion of soft tissue for histopathological examination, without removing the entire lesion.
**Check:** Documentation should specify that the biopsy involves soft oral tissue, confirm that only a portion of the lesion was removed for diagnostic purposes, and detail the biopsy technique.
**Note:** This procedure obtains a tissue sample from a soft tissue lesion for pathological analysis. The detailed documentation should include the specific location and clinical characteristics of the lesion (size, color, texture, borders), suspected differential diagnosis, anesthesia technique, incision design (wedge, punch, elliptical), technique for tissue retrieval, specimen dimensions, hemostasis management, closure method if needed, handling of the specimen (fixation, labeling), post-operative instructions, and the plan for follow-up once the pathology report is received. This code is used only for partial removal of a lesion for diagnostic purposes; it is not appropriate for complete excision or for apicoectomy/periradicular curettage. Documentation should confirm that the specimen was submitted for pathological examination and address the chain of custody.

#### **Code: D7287** – *Exfoliative cytological sample collection*
**Use when:** Collecting cells from the surface of oral mucosa using a mild scraping technique for cytological examination, typically for screening or monitoring of suspicious areas.
**Check:** Documentation should specify the collection was non-transepithelial (surface scraping only), identify the specific site sampled, and detail the collection technique.
**Note:** This minimally invasive diagnostic procedure collects surface cells without penetrating the epithelium. The documentation should include the location and clinical appearance of the area being sampled, reason for collection (screening, monitoring of previously identified lesion), specific collection technique (wooden spatula, brush without transepithelial capabilities), handling of the sample (fixation, smearing onto slide), labeling protocol, and plan for follow-up once results are available. This technique differs from the more invasive brush biopsy (D7288) in that it collects only surface cells without penetrating the basement membrane. The documentation should address patient education regarding the purpose and limitations of exfoliative cytology compared to tissue biopsy, and confirm that the sample was submitted for cytological examination.

#### **Code: D7288** – *Brush biopsy - transepithelial sample collection*
**Use when:** Collecting oral epithelial cells using a specialized brush that penetrates the full thickness of the epithelium, providing a sample for computer-assisted analysis.
**Check:** Documentation should specify that a specialized transepithelial collection brush was used (not just surface scraping), identify the specific site sampled, and detail the collection technique.
**Note:** This procedure collects a full-thickness epithelial sample through specialized brushing technique. The detailed documentation should include the location and clinical characteristics of the area sampled, reason for brush biopsy selection over incisional biopsy, specific brush device used (brand name if applicable), technique for applying proper pressure to ensure transepithelial sampling (often evidenced by pinpoint bleeding), number of rotations or strokes, method of transferring the sample to slide or collection medium, fixation protocol, submission process (particularly if using a specialized analysis service such as OralCDx), and the plan for follow-up once results are received. The documentation should distinguish this from simple exfoliative cytology by noting the penetration of the full epithelial thickness, and should address the criteria for selecting brush biopsy versus conventional tissue biopsy based on the clinical presentation.

#### **Code: D7290** – *Surgical repositioning of teeth*
**Use when:** Surgically repositioning a tooth or teeth within the alveolar process to a more favorable position when orthodontic movement alone is not feasible.
**Check:** Documentation should detail the surgical approach for mobilization and repositioning, specify the tooth or teeth involved, and explain why conventional orthodontic movement was not appropriate.
**Note:** This procedure involves surgical movement of a tooth into a new position within the alveolar bone. The comprehensive documentation should include the specific tooth designation, indication for surgical rather than orthodontic repositioning, preoperative radiographic assessment, anesthesia technique, flap design and elevation, bone removal approach to create space for repositioning, technique for mobilizing the tooth (often with forceps or elevators), method of stabilization in the new position, radiographic verification of positioning, occlusal adjustment if needed, closure technique, and post-operative instructions. If grafting procedures are performed in conjunction with the repositioning, they should be reported separately. The documentation should address coordination with orthodontic treatment, if applicable, and the planned timeline for any subsequent therapy following healing.

#### **Code: D7291** – *Transseptal fiberotomy/supra crestal fiberotomy, by report*
**Use when:** Surgically severing the gingival fibers around a tooth to reduce the tension of these fibers, typically performed to reduce the potential for orthodontic relapse.
**Check:** Documentation should describe the specific surgical technique for fiber separation, identify the teeth involved, and explain the relationship to orthodontic treatment.
**Note:** This procedure addresses the transseptal and supracrestal fibers that can contribute to orthodontic relapse. The detailed "by report" documentation should include the specific teeth involved (a single transseptal fiberotomy typically involves a minimum of three teeth), timing in relation to orthodontic treatment (often performed near the completion of active treatment), anesthesia technique, specific surgical approach (knife, laser), depth and extent of the incision, confirmation that the incision remained within the gingival sulcus without exposing the root surface, verification of complete fiber separation, hemostasis management, any dressing or packing placed, and post-operative instructions. The documentation should explain the rationale for performing the procedure, typically to reduce the potential for rotational relapse or space reopening following orthodontic treatment, and address coordination with the orthodontic treatment plan.

#### **Code: D7292** – *Placement of temporary anchorage device [screw retained plate] requiring flap; includes device removal*
**Use when:** Surgically placing a temporary skeletal anchorage plate that requires a full-thickness flap for access, to provide orthodontic anchorage.
**Check:** Documentation should confirm that a screw-retained plate (not just a single screw) was placed, verify that a full-thickness flap was elevated, and detail both the placement and planned removal.
**Note:** This procedure involves placement of a more complex anchorage device requiring surgical flap access. The comprehensive documentation should include the specific indication for skeletal anchorage, device selection rationale, planned orthodontic force application, anesthesia technique, incision design, flap elevation approach, preparation of the bone for plate placement, specific device used (dimensions, material, number of screws), verification of stability, radiographic confirmation of placement if obtained, closure technique, post-operative instructions, and the planned timeline for orthodontic force application and eventual device removal. The timing and technique for device removal should be addressed in the treatment plan. This code includes both the placement and the eventual removal of the device, which distinguishes it from implant placement codes. The documentation should address coordination with the orthodontic treatment plan and the specific biomechanical purpose of the anchorage device.

#### **Code: D7293** – *Placement of temporary anchorage device requiring flap; includes device removal*
**Use when:** Surgically placing a temporary skeletal anchorage device (other than a screw-retained plate) that requires a full-thickness flap for access, to provide orthodontic anchorage.
**Check:** Documentation should specify the type of anchorage device placed (not a plate), verify that a full-thickness flap was elevated, and detail both the placement and planned removal.
**Note:** This procedure addresses placement of temporary skeletal anchorage devices requiring flap elevation, such as certain mini-implants or specialized pins. The detailed documentation should include the specific orthodontic indication for skeletal anchorage, type and dimensions of the device, planned force application, anesthesia technique, incision design, flap elevation approach, site preparation, device insertion technique, verification of primary stability, radiographic confirmation if obtained, closure technique, post-operative instructions, and the timeline for orthodontic loading and eventual removal. The procedure note should specifically distinguish this from code D7292 by confirming that the device is not a screw-retained plate, and from code D7294 by documenting that flap elevation was required for placement. This code includes both placement and removal, which should be addressed in the documentation. Coordination with the orthodontic treatment plan should be documented, including the biomechanical rationale for the specific placement location.

#### **Code: D7294** – *Placement of temporary anchorage device without flap; includes device removal*
**Use when:** Placing a temporary skeletal anchorage device through a flapless approach (transmucosal), typically a mini-screw or mini-implant, to provide orthodontic anchorage.
**Check:** Documentation should confirm that no surgical flap was elevated for placement, specify the type of device used, and detail both the placement and planned removal.
**Note:** This procedure involves transmucosal placement of skeletal anchorage devices, typically orthodontic mini-screws. The comprehensive documentation should include the specific indication for temporary skeletal anchorage, device selection (type, dimensions, material), site selection rationale, anesthesia technique, soft tissue preparation (often just topical anesthetic and tissue punch), insertion technique including angulation, torque application method, verification of stability, radiographic confirmation if obtained, immediate post-placement assessment, and instructions for hygiene and maintenance. The documentation should specifically confirm that no flap was elevated, distinguishing this code from D7293. The planned timeline for orthodontic force application and the eventual removal protocol should be addressed. This code includes both placement and removal of the device. Coordination with the orthodontic treatment plan should be documented, including the specific biomechanical purpose of the anchorage.

#### **Code: D7295** – *Harvest of bone for use in autogenous grafting procedure*
**Use when:** Surgically collecting bone from one site to use as graft material at another site, when this harvesting is not included in the code for the primary grafting procedure.
**Check:** Documentation should detail the harvest site, technique for bone collection, quantity obtained, and confirm this was for an autogenous grafting procedure.
**Note:** This procedure addresses the donor site portion of autogenous bone grafting. The detailed documentation should include the specific indication for autogenous bone (rather than allograft or xenograft materials), selection rationale for the donor site (often based on bone quality, quantity, and access), anesthesia technique, incision design and flap elevation at the donor site, specific bone harvesting technique (block, particulate, scraping, filtering), instrumentation used (burs, chisels, bone scrapers, collection devices), volume or dimensions of bone harvested, management of the donor site (hemostasis, placement of hemostatic agents, membrane coverage if indicated), closure technique, and donor site post-operative instructions. This code is reported in addition to the grafting procedure code for the recipient site. The documentation should address the chain of custody for the harvested material and confirm its use in the grafting procedure.

#### **Code: D7296** – *Corticotomy - one to three teeth or tooth spaces, per quadrant*
**Use when:** Creating surgical cuts in the alveolar cortical bone around one to three teeth or tooth spaces in a quadrant, to facilitate accelerated orthodontic tooth movement.
**Check:** Documentation should specify the exact teeth or tooth spaces involved (between one and three), confirm the procedure was limited to a single quadrant, and detail the specific corticotomy technique.
**Note:** This procedure creates controlled surgical injury to cortical bone to induce a regional acceleratory phenomenon for enhanced orthodontic tooth movement. The comprehensive documentation should include the specific teeth involved (confirming no more than three teeth or tooth spaces in the quadrant), coordination with orthodontic treatment plan, timing of the procedure relative to orthodontic force application, anesthesia technique, flap design and elevation, specific pattern of cortical cuts or perforations (vertical, horizontal, or both), instrumentation used (piezosurgery, rotary, or hand instruments), depth of cuts (ensuring they remain in cortical bone without penetrating medullary bone), any additional augmentation materials placed (graft material, membranes), closure technique, immediate post-operative assessment, and instructions for post-surgical care. The documentation should address the planned orthodontic force application timeline following the procedure. If graft material or membranes are used, this should be noted but is included in this procedure code.

#### **Code: D7297** – *Corticotomy - four or more teeth or tooth spaces, per quadrant*
**Use when:** Creating surgical cuts in the alveolar cortical bone around four or more teeth or tooth spaces in a quadrant, to facilitate accelerated orthodontic tooth movement.
**Check:** Documentation should specify the exact teeth or tooth spaces involved (four or more), confirm the procedure was limited to a single quadrant, and detail the specific corticotomy technique.
**Note:** This procedure is similar to D7296 but addresses a more extensive surgical field involving four or more teeth or tooth spaces within a quadrant. The detailed documentation should include the specific teeth involved (confirming four or more teeth or tooth spaces in the quadrant), coordination with the orthodontic treatment plan, timing relative to orthodontic force application, anesthesia technique, flap design and elevation (typically more extensive than for D7296), pattern and extent of cortical cuts or perforations, instrumentation used, depth control methodology, management of any anatomical structures (mental foramen, maxillary sinus), any augmentation materials placed, closure technique, post-operative assessment, and comprehensive instructions for post-surgical care and orthodontic follow-up. The documentation should address the biomechanical rationale for including the specific teeth in the procedure and the expected acceleration of tooth movement. As with D7296, any graft material or membranes used are included in this procedure code.

---

### **Key Takeaways:**
- **Extraction Complexity Hierarchy** - Documentation should clearly establish the specific factors that determine code selection within the extraction hierarchy, from simple forceps extraction to complicated impaction removal.
- **Surgical Technique Documentation** - For surgical extractions (D7210 and higher), the documentation must specifically detail each surgical component—flap design, bone removal method and extent, tooth sectioning pattern.
- **Impaction Classification** - Documentation for impacted tooth removal should include the specific impaction classification (soft tissue, partial bony, complete bony) with reference to radiographic findings.
- **Unusual Complications** - For code D7241, documentation must first establish a complete bony impaction AND then clearly identify specific unusual complications beyond standard complete bony impactions.
- **Intentional vs. Incomplete** - Coronectomy (D7251) documentation must clearly establish that root retention was intentional to prevent nerve injury, not an incomplete extraction.
- **Sinus Communications** - Clear distinction between acute perforation (D7261) and chronic fistula (D7260) must be established in the documentation.
- **Device Placement Specificity** - For anchorage device placement (D7292-D7294), documentation must distinguish between flap vs. flapless approaches and plate vs. non-plate devices.
- **Exposure vs. Extraction** - Documentation for procedures like D7280 should clearly distinguish exposure for orthodontic purposes from extraction procedures.
- **Corticotomy Extent** - The number of teeth or tooth spaces involved in corticotomy procedures determines code selection (D7296 vs. D7297) and must be clearly documented.
- **Procedure Bundling** - Documentation should address which components are included in procedure codes (such as device placement AND removal for D7292-D7294) and which require separate coding.

Scenario:
"{{scenario}}"

{PROMPT}
""",
            input_variables=["scenario"]
    )

    def extract_extractions_code(self, scenario: str) -> str:
        """Extract extractions code for a given scenario."""
        try:
            print(f"Analyzing extractions scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Extractions extract code result: {code}")
            
            # Return empty string if no code found
            if code == "None" or not code or "not applicable" in code.lower():
                return ""
                
            return code
        except Exception as e:
            print(f"Error in extract_extractions_code: {str(e)}")
            return ""

    def activate_extractions(self, scenario: str) -> str:
        """Activate the extractions analysis process and return results."""
        try:
            return self.extract_extractions_code(scenario)
        except Exception as e:
            print(f"Error in activate_extractions: {str(e)}")
            return ""

    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_extractions(scenario)
        print(f"\n=== EXTRACTIONS ANALYSIS RESULT ===")
        print(f"EXTRACTIONS CODE: {result if result else 'None'}")


extractions_service = ExtractionsServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter an extractions scenario: ")
    extractions_service.run_analysis(scenario) 