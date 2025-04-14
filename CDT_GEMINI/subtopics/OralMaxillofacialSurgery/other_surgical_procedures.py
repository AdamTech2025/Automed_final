"""
Module for extracting other oral and maxillofacial surgical procedures codes.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from subtopics.prompt.prompt import PROMPT
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file

# Load environment variables
try:
    load_dotenv()
except:
    pass

# Get model name from environment variable, default to gpt-4o if not set
 
def create_other_surgical_procedures_extractor(temperature=0.0):
    """
    Create a LangChain-based other surgical procedures code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    template = f"""
    You are a dental coding expert specializing in oral and maxillofacial surgery.
    
  ## **Other Surgical Procedures** 
 
### **Before picking a code, ask:** 
- What is the specific surgical procedure being performed?
- Is this a repair of a fistula, repositioning of tooth, biopsy, or other specialized procedure?
- Does the procedure involve tooth reimplantation, exposure, or mobilization?
- Is a temporary anchorage device being placed or removed, and does it require a flap?
- Is the procedure diagnostic (biopsy) or therapeutic in nature?
- Does the procedure involve bone harvesting or corticotomy?
- Are sinus or oroantral communications involved?
 
---
 
### **Sinus-Related Procedures**
 
#### **Code: D7260** – *Oroantral fistula closure* 
**Use when:** Repairing a pathological communication between the oral cavity and maxillary sinus with an advancement flap.
**Check:** Verify that a chronic fistulous tract exists between the sinus and oral cavity, not just an acute perforation.
**Note:** This procedure involves excision of the fistulous tract followed by closure via an advancement flap, typically involving reflection of mucoperiosteal tissue, removal of infected tissue, and repositioning of the flap for tension-free closure to eliminate the communication between the oral cavity and maxillary sinus.
**Procedural Distinction:** Unlike primary closure of a sinus perforation (D7261), this code specifically addresses a chronic fistula that has developed an epithelialized tract requiring excision before closure.
**Clinical Indications:** Typically performed when a communication between the oral cavity and maxillary sinus has persisted, allowing passage of oral contents into the sinus and causing chronic sinusitis or infection that fails to resolve spontaneously.
 
#### **Code: D7261** – *Primary closure of a sinus perforation* 
**Use when:** Performing immediate repair of a fresh communication between the oral cavity and maxillary sinus.
**Check:** Document that this is an acute perforation without an established fistulous tract.
**Note:** This procedure addresses acute perforations that commonly occur during extraction of maxillary posterior teeth (particularly first molars) where the roots may extend close to or into the maxillary sinus, involving careful debridement of the site, placement of an absorbable hemostatic agent if needed, and closure of soft tissue with tension-free suturing techniques to prevent development of a chronic fistula.
**Timing Considerations:** Generally performed immediately following recognition of a sinus perforation during tooth extraction or other procedures, whereas oroantral fistula closure addresses a chronic condition.
**Anatomical Factors:** Documentation should note the location and size of the perforation, as larger perforations (>3-4mm) have higher likelihood of requiring surgical intervention rather than healing spontaneously.
 
---
 
### **Tooth Reimplantation and Repositioning**
 
#### **Code: D7270** – *Tooth re-implantation and/or stabilization of accidentally evulsed or displaced tooth* 
**Use when:** Replacing an avulsed (knocked-out) tooth back into its socket or repositioning and stabilizing a tooth that has been displaced due to trauma.
**Check:** Verify that the tooth was completely out of the socket (avulsion) or significantly displaced from its normal position due to traumatic injury.
**Note:** This procedure includes cleaning the root surface while maintaining periodontal ligament viability, repositioning the tooth into its socket, splinting for stabilization, and any necessary occlusal adjustment, with the goal of maintaining tooth vitality and preventing root resorption through proper management of the periodontal ligament cells.
**Timing Considerations:** Documentation should include the time elapsed between avulsion and reimplantation, as this significantly impacts prognosis, with best outcomes achieved when reimplantation occurs within 30-60 minutes of injury.
**Follow-up Requirements:** Records should address splint type and expected duration, planned endodontic intervention if indicated based on root development stage, and monitoring protocol for potential complications including ankylosis or inflammatory resorption.
 
#### **Code: D7272** – *Tooth transplantation (includes re-implantation from one site to another and splinting and/or stabilization)* 
**Use when:** Moving a tooth from one location in the mouth to another site in the same individual.
**Check:** Document both the donor site and the recipient site for the transplanted tooth.
**Note:** This complex procedure involves atraumatic extraction of a donor tooth (often a third molar), preparation of a recipient site (such as a non-restorable first molar socket), careful transplantation with attention to maintaining periodontal ligament viability, and stabilization of the transplanted tooth with splinting techniques to allow for healing and potential pulpal revascularization.
**Case Selection:** Ideal candidates have incompletely formed roots (75-100% root formation with open apex) for better revascularization potential, though fully formed roots may be used with planned endodontic therapy.
**Procedural Documentation:** Records should detail the extraction technique for the donor tooth, any socket preparation at the recipient site, positioning considerations, stabilization method, and follow-up monitoring protocol.
 
#### **Code: D7290** – *Surgical repositioning of teeth* 
**Use when:** Surgically moving a tooth to a different position within the same socket to correct malposition.
**Check:** Verify that the tooth is being repositioned but remaining in the same general location, not extracted and reimplanted in a different site.
**Note:** This procedure involves surgical luxation of a tooth, creating space by removing bone as necessary, repositioning the tooth into a more favorable position in the dental arch, and stabilization until healing occurs, often performed to correct severe rotations or malpositions that cannot be addressed orthodontically.
**Clinical Applications:** May be used for vertically impacted teeth, severe rotations, or teeth in crossbite that cannot be moved orthodontically due to unfavorable root position or ankylosis.
**Documentation Requirements:** Records should specify the initial position, desired position, surgical technique, bone management, stabilization method, and whether additional procedures such as grafting were performed.
 
---
 
### **Impacted Tooth Management**
 
#### **Code: D7280** – *Exposure of an unerupted tooth* 
**Use when:** Surgically uncovering an impacted tooth to allow access for orthodontic attachment, not intended for extraction.
**Check:** Confirm that the procedure is aimed at facilitating eruption, not removing the tooth.
**Note:** This procedure creates surgical access to an impacted tooth through incision, flap reflection, and selective removal of overlying bone and/or soft tissue to expose the crown, allowing for subsequent orthodontic traction and guided eruption into the dental arch.
**Technique Variations:** May involve closed exposure (where the flap is repositioned after an orthodontic attachment is placed) or open exposure (where tissue is removed or repositioned to leave the crown visible), with method selection based on the tooth's position and surrounding anatomical structures.
**Coding Coordination:** Does not include placement of an orthodontic attachment (D7283), which should be reported separately when performed during the same procedure.
 
#### **Code: D7282** – *Mobilization of erupted or malpositioned tooth to aid eruption* 
**Use when:** Surgically manipulating a tooth to break ankylosis and facilitate natural eruption or orthodontic movement.
**Check:** Document that the tooth is ankylosed or severely immobile and not responding to normal orthodontic forces.
**Note:** This procedure addresses ankylosis (fusion of cementum/dentin to alveolar bone) by surgically luxating the tooth to disrupt the ankylosis while preserving the neurovascular supply, allowing renewed mobility and response to normal eruptive or orthodontic forces.
**Clinical Distinction:** Unlike surgical repositioning (D7290), this procedure does not involve establishing the tooth in a new position, but rather aims to restore normal mobility to facilitate conventional orthodontic treatment.
**Risk Assessment:** Documentation should address the potential for root fracture, damage to neurovascular supply, and the prognosis for successful mobilization based on the extent and duration of ankylosis.
 
#### **Code: D7283** – *Placement of device to facilitate eruption of impacted tooth* 
**Use when:** Attaching an orthodontic bracket, button, or chain to an impacted tooth during surgical exposure to aid in eruption.
**Check:** Verify that the surgical exposure (D7280) has been performed or is being performed concurrently.
**Note:** This procedure involves bonding an orthodontic attachment (bracket, button, or gold chain) to the exposed crown of an impacted tooth to allow application of orthodontic traction, facilitating guided eruption into proper position in the dental arch.
**Coding Requirements:** Must be reported in conjunction with D7280 (exposure of an unerupted tooth) when both procedures are performed during the same appointment.
**Documentation Specifics:** Records should detail the type of attachment placed, whether closed or open technique was used, and any immediate orthodontic forces applied.
 
---
 
### **Diagnostic Procedures**
 
#### **Code: D7285** – *Incisional biopsy of oral tissue - hard (bone, tooth)* 
**Use when:** Removing a partial sample of bone or tooth for diagnostic examination.
**Check:** Document that only a representative sample is being removed, not the entire lesion.
**Note:** This procedure involves surgical retrieval of a portion of a suspected pathological lesion in bone or tooth structure for histopathological examination, with careful attention to specimen management to preserve diagnostic features and accurate documentation of the site and clinical characteristics.
**Procedural Limitations:** This code specifically excludes apicoectomy/periradicular surgical specimens and is not used when complete excision of the lesion is performed.
**Specimen Handling:** Documentation should address fixation method, laboratory selection, clinical impression, and radiographic correlation to ensure proper processing and interpretation.
 
#### **Code: D7286** – *Incisional biopsy of oral tissue - soft* 
**Use when:** Removing a partial sample of soft tissue for diagnostic examination.
**Check:** Verify that only a representative portion of the lesion is being removed, not the entire lesion.
**Note:** This procedure involves surgical retrieval of a representative sample of soft tissue from a suspected pathological lesion for histopathological examination, with careful technique to ensure an architecturally intact specimen that preserves diagnostic features while maintaining adequate hemostasis at the donor site.
**Clinical Applications:** Appropriate for larger lesions where complete excision is not initially indicated, or when the differential diagnosis includes conditions that might require different treatment approaches pending histopathological confirmation.
**Specimen Considerations:** Documentation should include lesion location, size, clinical characteristics, reason for biopsy, and specific region sampled if the lesion has varying appearances.
 
#### **Code: D7287** – *Exfoliative cytological sample collection* 
**Use when:** Obtaining surface cells by mild scraping for cytological examination.
**Check:** Document that this is a non-transepithelial sampling technique (surface scraping only).
**Note:** This minimally invasive diagnostic procedure involves gently scraping the surface of a suspicious oral lesion to collect superficial cells for cytological examination, performed using a tongue depressor, cotton swab, or similar instrument to harvest cells that are then transferred to a slide, fixed, and submitted for pathological evaluation.
**Diagnostic Limitations:** Provides information only on exfoliated surface cells, which limits diagnostic value compared to incisional biopsy, as deeper tissues are not sampled and tissue architecture is not preserved.
**Clinical Applications:** Most appropriate for screening or monitoring of suspicious lesions where the index of suspicion for malignancy is low, or in cases where more invasive procedures are contraindicated.
 
#### **Code: D7288** – *Brush biopsy - transepithelial sample collection* 
**Use when:** Collecting oral cells via rotational brushing that samples through the full thickness of the epithelium.
**Check:** Verify that a specialized brush designed to penetrate the epithelial surface is used, not just surface scraping.
**Note:** This procedure employs a specialized stiff-bristled brush that is firmly rotated against the suspicious lesion until pinpoint bleeding occurs, indicating penetration through the epithelial layers, with collected cells then transferred to a slide or suspension medium for laboratory analysis using computer-assisted or standard cytological evaluation.
**Technical Advantages:** The specialized brush samples cells from all layers of the epithelium, including the basal cell layer where dysplastic changes often begin, providing more comprehensive sampling than surface exfoliation techniques.
**Appropriate Use:** Particularly valuable for evaluating ambiguous lesions that lack clear indications for immediate incisional biopsy, though positive or suspicious results generally require follow-up with definitive tissue biopsy for confirmation.
 
---
 
### **Fibrotomy and Anchorage Device Procedures**
 
#### **Code: D7291** – *Transseptal fiberotomy/supra crestal fiberotomy, by report* 
**Use when:** Surgically severing the gingival fibers around a tooth to reduce the tension of these fibers and decrease the potential for orthodontic relapse.
**Check:** Document that the procedure is being performed to prevent orthodontic relapse, particularly in cases of rotational movements.
**Note:** This minimally invasive procedure involves insertion of a surgical blade into the gingival sulcus to sever the supracrestal gingival fibers and transseptal fibers between teeth, creating a controlled injury that allows these fibers to reorganize during healing in a way that reduces tension and potential for orthodontic relapse.
**Procedural Extent:** A single tooth fiberotomy affects a minimum of three teeth due to the interconnected nature of the transseptal fibers, with documentation specifying which teeth were included in the procedure.
**Timing Considerations:** Typically performed near the completion of active orthodontic treatment, just before or at the time of appliance removal, to reduce relapse potential during the retention phase.
 
#### **Code: D7292** – *Placement of temporary anchorage device [screw retained plate] requiring flap* 
**Use when:** Surgically placing a bone plate anchored by screws to serve as temporary orthodontic anchorage.
**Check:** Verify that a mucoperiosteal flap is reflected for placement of a screw-retained plate.
**Note:** This procedure involves reflecting a mucoperiosteal flap, adapting a specialized bone plate to the exposed cortical bone, securing it with multiple screws, and closing the flap, creating a stable skeletal anchorage point for orthodontic forces that eliminates concerns about patient compliance or undesired reciprocal movement of anchor teeth.
**Anatomical Considerations:** Documentation should specify the location of placement (commonly the zygomatic buttress, palate, or mandibular body), plate design, number and size of screws, and planned orthodontic application.
**Duration Expectations:** These devices are intended for temporary use during specific phases of orthodontic treatment and should be removed upon completion of their purpose, with typical duration ranging from several months to 1-2 years.
 
#### **Code: D7293** – *Placement of temporary anchorage device requiring flap* 
**Use when:** Surgically placing a single implant-like device that requires flap reflection for orthodontic anchorage.
**Check:** Document that a mucoperiosteal flap is reflected for placement of the anchorage device (not a plate).
**Note:** This procedure involves creating a mucoperiosteal flap to expose the cortical bone, preparing a precise site for the temporary anchorage device, placing the implant-like device into bone, and repositioning and suturing the flap, providing absolute anchorage for orthodontic force application without depending on dental units.
**Device Specifications:** Documentation should detail the specific type of mini-implant or microscrews used, dimensions, location of placement, and planned orthodontic force application.
**Clinical Indications:** Particularly valuable for complex orthodontic movements requiring maximum anchorage, such as intrusion of posterior teeth, protraction or retraction of entire dental segments, or correction of canted occlusal planes.
 
#### **Code: D7294** – *Placement of temporary anchorage device without flap* 
**Use when:** Placing a temporary anchorage device through the gingiva without reflecting a flap.
**Check:** Verify that the procedure is performed transmucosally without a surgical flap.
**Note:** This minimally invasive procedure involves direct placement of a temporary anchorage device (mini-implant or microscrew) through the gingiva into bone using local anesthesia, requiring less surgical manipulation than flap procedures and generally allowing immediate loading with orthodontic forces.
**Technical Approach:** Performed after careful planning of insertion site, angle, and depth, typically with pilot drilling followed by device insertion to prescribed torque values, utilizing a flapless technique that minimizes patient discomfort and speeds healing.
**Anatomical Precautions:** Documentation should address proximity to vital structures (roots, nerves, blood vessels, maxillary sinus), interradicular spacing, and quality of cortical bone at the insertion site.
 
#### **Code: D7295** – *Harvest of bone for use in autogenous grafting procedure* 
**Use when:** Obtaining bone from a donor site in the patient's body for grafting purposes.
**Check:** Document both the donor site and recipient site for the harvested bone.
**Note:** This adjunctive procedure involves surgical collection of autogenous bone from a separate surgical site (commonly the mandibular ramus, symphysis, maxillary tuberosity, or tori) for use in a grafting procedure elsewhere in the mouth, including careful management of the donor site to minimize morbidity.
**Coding Specifics:** Reported in addition to the code for graft placement, as this code specifically addresses the additional procedure of harvesting bone from a separate site.
**Documentation Requirements:** Records should detail the donor site selection rationale, harvesting technique (block, particulate, or combination), quantity of bone harvested, donor site management, and any complications or postoperative instructions specific to the harvest site.
 
#### **Code: D7296** – *Corticotomy - one to three teeth or tooth spaces, per quadrant* 
**Use when:** Performing selective decortication of the alveolar bone around one to three teeth to accelerate orthodontic tooth movement.
**Check:** Document the number of teeth involved (1-3) and the specific quadrant.
**Note:** This surgical procedure to facilitate orthodontic treatment involves reflecting a full-thickness mucoperiosteal flap, creating multiple cuts or perforations in the cortical bone surrounding the teeth to be moved, while preserving the medullary bone and neurovascular bundles, initiating a regional acceleratory phenomenon that temporarily decreases bone density and accelerates tooth movement.
**Procedural Extent:** Includes flap reflection, bone surgery, and flap closure, with any grafting material or membranes used reported separately.
**Clinical Applications:** Particularly valuable for accelerating specific movements in adults with decreased cellular response to orthodontic forces, shortening treatment time, or facilitating movements that would otherwise be difficult to achieve with conventional orthodontics alone.
 
#### **Code: D7297** – *Corticotomy - four or more teeth or tooth spaces, per quadrant* 
**Use when:** Performing selective decortication of the alveolar bone around four or more teeth to accelerate orthodontic tooth movement.
**Check:** Verify that four or more teeth in the same quadrant are involved in the procedure.
**Note:** Similar to D7296 but involving a more extensive surgical field encompassing four or more teeth in a quadrant, this procedure includes flap reflection, strategic corticotomy cuts or perforations surrounding multiple teeth, and precise flap repositioning and closure, with the goal of temporarily altering regional bone physiology to accelerate orthodontic treatment.
**Biological Basis:** The surgical trauma induces a local inflammatory response that increases bone turnover rates through the regional acceleratory phenomenon, creating a window of opportunity (typically 3-4 months) during which accelerated tooth movement can occur.
**Documentation Requirements:** Records should detail the specific pattern of corticotomy cuts, depth of penetration, protection of vital structures, any additional grafting procedures performed, and coordination with the planned orthodontic force application timing.
 
#### **Code: D7298** – *Removal of temporary anchorage device [screw retained plate], requiring flap* 
**Use when:** Surgically removing a previously placed bone plate with screws that requires flap reflection.
**Check:** Document that a mucoperiosteal flap is necessary for removal of the screw-retained plate.
**Note:** This procedure involves creating a surgical access flap to expose the previously placed bone plate and associated screws, carefully removing all hardware components, managing the surgical site including any necessary bone recontouring, and closing the flap with appropriate suturing techniques.
**Clinical Considerations:** Performed after the device has served its purpose in orthodontic treatment, with timing based on treatment completion or any complications necessitating early removal.
**Documentation Specifics:** Records should address the original placement date, reason for removal (treatment completion or complications), condition of surrounding tissues, any bone defects requiring management, and post-removal instructions.
 
#### **Code: D7299** – *Removal of temporary anchorage device, requiring flap* 
**Use when:** Surgically removing a temporary anchorage device (not a plate) requiring flap reflection.
**Check:** Verify that a mucoperiosteal flap is necessary for removal of the anchorage device.
**Note:** This procedure involves creating a surgical access flap to expose a previously placed temporary anchorage device that cannot be removed with a flapless approach (due to tissue overgrowth, device fracture, or other complications), carefully removing the device with appropriate instrumentation, managing the surgical site, and closing with appropriate suturing.
**Indications for Flap:** Documentation should explain why a flap is required for removal rather than a simpler flapless approach, such as significant tissue overgrowth, osseointegration requiring osteotomy, or device fracture.
**Site Management:** Records should address how the remaining defect in the bone is managed following device removal and any recommendations for healing or follow-up.
 
#### **Code: D7300** – *Removal of temporary anchorage device without flap* 
**Use when:** Removing a temporary anchorage device without the need for flap reflection.
**Check:** Document that the device can be accessed and removed transmucosally without a surgical flap.
**Note:** This minimally invasive procedure involves direct removal of a temporary anchorage device through the existing access in the gingiva without requiring flap reflection, typically performed by reversing the insertion process using the appropriate driver to unscrew and retrieve the device.
**Patient Management:** Simpler and less invasive than flap procedures, usually requiring only topical or minimal local anesthesia, with minimal post-operative discomfort and rapid healing.
**Documentation Considerations:** Records should note the condition of the device and surrounding tissues upon removal, any difficulties encountered during retrieval, and confirmation that all components were successfully removed.
 
---
 
### **Salivary Procedures**
 
#### **Code: D7979** – *Non-surgical sialolithotomy* 
**Use when:** Removing a stone from a salivary duct without requiring surgical incision.
**Check:** Verify that the stone is accessible through the ductal opening without requiring surgical access.
**Note:** This minimally invasive procedure involves removal of a salivary stone (sialolith) from Wharton's duct (submandibular) or Stensen's duct (parotid) using non-surgical techniques such as ductal dilation, salivary stimulation, manipulation, basket retrieval, or minimally invasive intraoral procedures that do not require surgical incision into the duct.
**Procedural Distinction:** Differs from surgical sialolithotomy (D7980) which requires an incision into the duct or gland to access and remove the stone.
**Clinical Indications:** Most appropriate for anterior stones that are palpable or visible, smaller stones without significant ductal strictures, or when patient factors favor the least invasive approach.
 
---
 
### **Key Takeaways:** 
- Other surgical procedures encompass a diverse range of techniques addressing varied clinical situations from sinus communications to tooth repositioning to diagnostic procedures.
- Temporary anchorage device codes are differentiated based on whether they involve plates or single devices, and whether flap reflection is required for placement or removal.
- Corticotomy procedures are coded based on the number of teeth involved (1-3 vs. 4+) per quadrant.
- Diagnostic procedures range from minimally invasive cytological sampling to more definitive hard or soft tissue biopsies.
- Tooth repositioning procedures include reimplantation of avulsed teeth, transplantation between sites, and movement within the same socket.
- Proper documentation must specify the exact nature of the procedure, rationale, technique, materials used, and any additional procedures performed concurrently.
- When multiple related procedures are performed together (such as exposure of an impacted tooth and placement of an orthodontic attachment), each should be coded separately.
    
    SCENARIO: {{question}}
    
    {PROMPT}
    """
    
    prompt = PromptTemplate(template=template, input_variables=["question"])
    return LLMChain(llm=llm, prompt=prompt)

def extract_other_surgical_procedures_code(scenario, temperature=0.0):
    """
    Extract other surgical procedures code(s) for a given scenario.
    """
    try:
        chain = create_other_surgical_procedures_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Other surgical procedures code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_other_surgical_procedures_code: {str(e)}")
        return ""

def activate_other_surgical_procedures(scenario):
    """
    Activate other surgical procedures analysis and return results.
    """
    try:
        return extract_other_surgical_procedures_code(scenario)
    except Exception as e:
        print(f"Error in activate_other_surgical_procedures: {str(e)}")
        return "" 