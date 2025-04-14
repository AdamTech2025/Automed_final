"""
Module for extracting other repair procedures codes.
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
 
def create_other_repair_procedures_extractor(temperature=0.0):
    """
    Create a LangChain-based other repair procedures code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert specializing in oral and maxillofacial surgical procedures.

## **Other Oral Surgery Repair Procedures**

### **Before picking a code, ask:**
- What type of tissue is being repaired (soft tissue, bone, nerve)?
- Is this a primary repair or secondary revision?
- What is the location and extent of the defect or damage?
- Is this repair related to a pathological condition or trauma?
- Does the procedure involve grafting materials (autogenous, allogeneic, xenogeneic)?
- What specific technique is being used for the repair?
- Is the procedure addressing a functional deficit or is it for cosmetic purposes?
- Are there any complicating factors such as infection or anatomical complexity?
- What is the size of the defect being repaired?
- Is hardware placement or removal involved?
- Is a biopsy or excision being performed in conjunction with the repair?
- Does the repair involve adjacent anatomical structures?

---

#### **Code: D7340** – *Vestibuloplasty - ridge extension (second epithelialization)*
**Use when:** Performing a surgical procedure to deepen the vestibular fornix or increase the height of the denture-bearing area through secondary epithelialization, typically for pre-prosthetic preparation.
**Check:** Documentation should specify the surgical approach for ridge extension, confirm that healing will occur through secondary epithelialization (without grafts), and detail the area(s) involved.
**Note:** This procedure increases the relative height of the alveolar ridge through muscle attachment modification. The comprehensive documentation should include the specific arch and area being treated, indication for the procedure (often pre-prosthetic), preoperative assessment of vestibular depth and ridge height, anesthesia technique, incision design, submucosal dissection approach, management of muscle attachments, method of securing the repositioned tissue (suturing to periosteum), packing or stent placement if utilized, verification of increased vestibular depth, post-operative instructions including stent management, and plan for prosthetic follow-up. This code specifically involves secondary epithelialization without grafts, distinguishing it from the more complex D7350. Documentation should include measurements of vestibular depth before and after the procedure.

#### **Code: D7350** – *Vestibuloplasty - ridge extension (including soft tissue grafts, muscle reattachment, revision of soft tissue attachment and management of hypertrophied and hyperplastic tissue)*
**Use when:** Performing a complex vestibuloplasty involving soft tissue grafts and/or muscle reattachment to increase the height of the denture-bearing area, typically for cases requiring greater augmentation than can be achieved with secondary epithelialization alone.
**Check:** Documentation should detail the use of soft tissue grafts and/or muscle reattachment techniques, specify the donor site if grafts were used, and describe management of any hyperplastic tissue.
**Note:** This procedure represents a more complex vestibuloplasty than D7340. The detailed operative report should include the specific arch and area being treated, comprehensive preoperative evaluation including limitations of existing ridge, anesthesia technique, incision design, submucosal dissection extent, specific management of muscle attachments (release, repositioning, reattachment), excision of hyperplastic tissue if present, graft harvesting technique and donor site management if applicable, graft placement and stabilization method, use of splints or stents, closure technique, post-operative management protocol including stent adjustment schedule, and plan for prosthetic rehabilitation. Documentation should include detailed measurements of vestibular depth before and after the procedure and specific description of the grafting materials or techniques used.

#### **Code: D7410** – *Excision of benign lesion up to 1.25 cm*
**Use when:** Surgically removing a benign soft tissue lesion measuring up to 1.25 cm in its greatest dimension, with the specimen submitted for pathological examination.
**Check:** Documentation should specify the lesion size (confirming it's ≤ 1.25 cm), establish that it was benign based on clinical assessment or previous biopsy, and confirm specimen submission for pathological examination.
**Note:** This procedure involves complete removal of a benign soft tissue lesion for therapeutic purposes. The comprehensive documentation should include the specific location and clinical characteristics of the lesion (size, appearance, texture, borders), suspected clinical diagnosis, relation to adjacent structures, anesthesia technique, surgical approach (incision design, margin width), technique for complete removal, management of the surgical defect, hemostasis methods, closure technique, handling of the specimen (fixation, labeling), and post-operative instructions. The documentation must specifically state the measured size of the lesion (≤ 1.25 cm in greatest dimension) as this determines code selection. Confirmation that the specimen was submitted for pathological examination should be included, along with the plan for follow-up once the pathology report is received.

#### **Code: D7411** – *Excision of benign lesion greater than 1.25 cm*
**Use when:** Surgically removing a benign soft tissue lesion measuring greater than 1.25 cm in its greatest dimension, with the specimen submitted for pathological examination.
**Check:** Documentation should specify the lesion size (confirming it's > 1.25 cm), establish that it was benign based on clinical assessment or previous biopsy, and confirm specimen submission for pathological examination.
**Note:** This procedure addresses larger benign soft tissue lesions requiring more extensive surgical management. The detailed operative report should include the specific location and comprehensive clinical characteristics of the lesion (size with precise measurements, appearance, texture, borders, depth), suspected clinical diagnosis, proximity to vital structures, anesthesia technique, surgical approach with consideration for the larger defect, technique for complete removal with appropriate margins, management of the more extensive surgical defect, hemostasis methods, closure technique (which may be more complex for larger defects), handling of the specimen, and detailed post-operative instructions. The documentation must specifically state the measured size of the lesion (> 1.25 cm in greatest dimension) as this is the key determinant between codes D7410 and D7411. Confirmation of pathology submission and the follow-up plan should be included.

#### **Code: D7412** – *Excision of benign lesion, complicated*
**Use when:** Removing a benign soft tissue lesion that presents unusual surgical complications due to factors such as size, location, depth, adjacent vital structures, or required reconstruction technique.
**Check:** Documentation must first establish that the lesion was benign AND then clearly identify the specific surgical complications that increased procedural complexity beyond a standard excision.
**Note:** This procedure addresses benign lesions with complicating factors requiring advanced surgical management. The comprehensive documentation should include the specific location and clinical characteristics of the lesion, AND explicit description of the complicating factors encountered. These might include proximity to vital structures requiring special dissection or protection, deep extension into underlying tissues, location in an anatomically difficult area (floor of mouth, retromolar pad, maxillary tuberosity), involvement of multiple tissue planes, extensive size requiring complex reconstruction, unusual adherence to surrounding structures, or excessive vascularity requiring advanced hemostatic measures. The operative report should detail the specific techniques employed to address these complications, any modified surgical approaches required, the management of adjacent structures, complexity of the closure or reconstruction, and specialized post-operative instructions. The documentation must clearly articulate why the procedure was more complicated than a standard excision of similar-sized lesion.

#### **Code: D7413** – *Excision of malignant lesion up to 1.25 cm*
**Use when:** Surgically removing a soft tissue lesion clinically suspected or previously diagnosed as malignant, measuring up to 1.25 cm in its greatest dimension, with wider margins than would be used for benign lesions.
**Check:** Documentation should specify the lesion size (confirming it's ≤ 1.25 cm), establish the basis for malignancy suspicion or diagnosis, detail the margin width, and confirm specimen submission for pathological examination.
**Note:** This procedure involves the excision of a malignant lesion requiring wider surgical margins. The detailed documentation should include the specific location and clinical characteristics of the lesion (size, appearance, borders), basis for malignancy suspicion (previous biopsy, clinical features), anesthesia technique, planned margin width appropriate for malignancy, incision design accounting for these wider margins, surgical approach with particular attention to complete removal, technique for ensuring clear margins, management of the surgical defect (which may be larger due to wider margins), closure technique or basis for leaving wound open if appropriate, detailed handling of the specimen including orientation marking if utilized, and comprehensive post-operative instructions. The documentation must specifically state the measured size of the lesion (≤ 1.25 cm in greatest dimension) and clearly indicate why a malignant lesion code was selected rather than a benign lesion code. Coordination with oncology specialists and plans for follow-up should be addressed.

#### **Code: D7414** – *Excision of malignant lesion greater than 1.25 cm*
**Use when:** Surgically removing a soft tissue lesion clinically suspected or previously diagnosed as malignant, measuring greater than 1.25 cm in its greatest dimension, with wider margins than would be used for benign lesions.
**Check:** Documentation should specify the lesion size (confirming it's > 1.25 cm), establish the basis for malignancy suspicion or diagnosis, detail the margin width, and confirm specimen submission for pathological examination.
**Note:** This procedure addresses larger malignant lesions requiring more extensive surgical management with wide margins. The comprehensive operative report should include the specific location and detailed clinical characteristics of the lesion (size with precise measurements, appearance, borders, invasion pattern), basis for malignancy suspicion or diagnosis (previous biopsy, clinical features), preoperative imaging findings if obtained, anesthesia technique, planned margin width appropriate for the type of malignancy and location, extensive surgical approach to ensure complete removal with adequate margins, technique for ensuring clear margins (which may include frozen sections), management of the more extensive surgical defect, reconstruction approach if required, closure technique, detailed specimen handling protocol including orientation marking, and comprehensive post-operative instructions. The documentation must specifically state the measured size of the lesion (> 1.25 cm in greatest dimension) and clearly justify the use of a malignant lesion code. The plan for oncologic follow-up, adjunctive therapies, and coordination with other specialists should be addressed.

#### **Code: D7415** – *Excision of malignant lesion, complicated*
**Use when:** Removing a malignant soft tissue lesion that presents unusual surgical complications due to factors such as size, location, depth, invasion pattern, proximity to vital structures, or required reconstruction technique.
**Check:** Documentation must first establish that the lesion was malignant AND then clearly identify the specific surgical complications that increased procedural complexity beyond a standard malignant lesion excision.
**Note:** This procedure addresses malignant lesions with significant complicating factors requiring advanced surgical management. The extensive documentation should include the specific location and clinical characteristics of the lesion, confirmation of malignancy status, AND explicit description of the complicating factors encountered. These might include invasion of deep tissues or bone, encroachment on vital neurovascular structures requiring special dissection techniques, location in an anatomically complex region, involvement of multiple tissue planes or anatomical spaces, need for neck dissection or other extended procedures, requirements for complex reconstruction with local or regional flaps, excessive bleeding requiring advanced hemostatic measures, or prior treatment effects complicating the surgery. The detailed operative report should document the specific techniques employed to address these complications, the approach to securing clear margins despite the complications, management of invaded or adjacent structures, complexity of the reconstruction if performed, and comprehensive specialized post-operative instructions. The documentation must clearly articulate why the procedure was more complicated than a standard excision of a similar-sized malignant lesion.

#### **Code: D7440** – *Excision of malignant tumor - lesion diameter up to 1.25 cm*
**Use when:** Surgically removing a malignant neoplasm involving both soft tissue and underlying structures such as bone, measuring up to 1.25 cm in its greatest dimension.
**Check:** Documentation should specify the tumor size (confirming it's ≤ 1.25 cm), verify involvement of both soft tissue and underlying structures, establish the basis for malignancy diagnosis, and confirm specimen submission for pathological examination.
**Note:** This procedure addresses malignant tumors involving deeper structures beyond just the soft tissue. The comprehensive documentation should include the specific location and clinical characteristics of the tumor, imaging findings demonstrating involvement of underlying structures (radiographs, CT, MRI), basis for malignancy diagnosis (previous biopsy, clinical features), anesthesia technique, surgical approach considering both soft tissue and underlying structure involvement, extent of resection including both soft and hard tissues, margin management appropriate for malignancy, reconstruction approach if performed, closure technique, specimen handling protocol, and detailed post-operative instructions. The documentation must specifically state the measured size of the tumor (≤ 1.25 cm in greatest dimension) and clearly distinguish this procedure from a soft tissue malignant lesion excision (D7413) by documenting the involvement of underlying structures. The coordination with oncology specialists, plans for prosthetic rehabilitation if applicable, and follow-up protocol should be addressed.

#### **Code: D7441** – *Excision of malignant tumor - lesion diameter greater than 1.25 cm*
**Use when:** Surgically removing a malignant neoplasm involving both soft tissue and underlying structures such as bone, measuring greater than 1.25 cm in its greatest dimension.
**Check:** Documentation should specify the tumor size (confirming it's > 1.25 cm), verify involvement of both soft tissue and underlying structures, establish the basis for malignancy diagnosis, and confirm specimen submission for pathological examination.
**Note:** This procedure addresses larger malignant tumors with more extensive involvement of deeper structures. The detailed operative report should include the specific location and comprehensive clinical characteristics of the tumor, advanced imaging findings demonstrating extent of involvement in underlying structures (CT, MRI, possibly PET), basis for malignancy diagnosis, preoperative multidisciplinary planning if conducted, anesthesia technique, extensive surgical approach to address both soft tissue and underlying structure involvement, careful margin management appropriate for the type and extent of malignancy, management of vital structures within the surgical field, reconstruction approach for the complex defect, closure technique, detailed specimen handling protocol including orientation marking, and comprehensive post-operative instructions. The documentation must specifically state the measured size of the tumor (> 1.25 cm in greatest dimension) and clearly document the involvement of underlying structures beyond soft tissue. The extensive post-surgical management plan should be addressed, including coordination with oncology, radiation therapy if planned, nutritional management if applicable, and rehabilitation strategy.

#### **Code: D7460** – *Removal of benign nonodontogenic cyst or tumor - lesion diameter up to 1.25 cm*
**Use when:** Surgically removing a benign nonodontogenic cyst or tumor (not derived from tooth-forming tissues) measuring up to 1.25 cm in its greatest dimension.
**Check:** Documentation should specify the lesion size (confirming it's ≤ 1.25 cm), establish its nonodontogenic origin, verify its benign nature based on clinical assessment or previous biopsy, and confirm specimen submission for pathological examination.
**Note:** This procedure addresses benign lesions of non-dental tissue origin. The comprehensive documentation should include the specific location and clinical characteristics of the cyst or tumor, radiographic or other imaging findings, suspected diagnosis identifying the nonodontogenic nature (e.g., nasopalatine duct cyst, dermoid cyst, salivary gland tumor), basis for benign assessment, anesthesia technique, surgical approach appropriate for the specific type of lesion, technique for complete removal, management of the surgical defect, verification of lesion integrity during removal if encapsulated, handling of the specimen, closure technique, and post-operative instructions. The documentation must specifically state the measured size of the lesion (≤ 1.25 cm in greatest dimension) and clearly establish its nonodontogenic nature, distinguishing it from odontogenic cysts or tumors which would be coded differently. The plan for follow-up once the pathology report is received should be included, with attention to the possibility of recurrence based on the specific diagnosis.

#### **Code: D7461** – *Removal of benign nonodontogenic cyst or tumor - lesion diameter greater than 1.25 cm*
**Use when:** Surgically removing a benign nonodontogenic cyst or tumor (not derived from tooth-forming tissues) measuring greater than 1.25 cm in its greatest dimension.
**Check:** Documentation should specify the lesion size (confirming it's > 1.25 cm), establish its nonodontogenic origin, verify its benign nature based on clinical assessment or previous biopsy, and confirm specimen submission for pathological examination.
**Note:** This procedure addresses larger benign lesions of non-dental tissue origin requiring more extensive management. The detailed operative report should include the specific location and comprehensive clinical characteristics of the cyst or tumor, radiographic or other imaging findings demonstrating extent, suspected specific diagnosis identifying the nonodontogenic nature, basis for benign assessment, anesthesia technique, more extensive surgical approach necessitated by the larger size, technique for complete removal, management of adjacent vital structures, approach to the more significant surgical defect, reconstruction if required, verification of lesion integrity during removal if encapsulated, handling of the specimen, closure technique, and detailed post-operative instructions. The documentation must specifically state the measured size of the lesion (> 1.25 cm in greatest dimension) and clearly establish its nonodontogenic nature. The plan for follow-up should be comprehensive, addressing possible functional or cosmetic consequences of the more extensive surgery, as well as monitoring for recurrence based on the specific pathological diagnosis.

#### **Code: D7465** – *Destruction of lesion(s) by physical or chemical method, by report*
**Use when:** Eliminating oral lesions using physical methods (cryotherapy, electrosurgery, laser ablation) or chemical methods (chemocautery), rather than surgical excision.
**Check:** Documentation should specify the destruction method used (physical or chemical), identify the lesion type and location, and explain why this approach was selected over surgical excision.
**Note:** This procedure eliminates lesions without excision for pathological examination. The detailed "by report" documentation should include the specific location and clinical characteristics of the lesion(s), suspected clinical diagnosis, justification for destruction rather than biopsy/excision (often because the diagnosis is clinically evident, the lesion is recurrent with known pathology, or the patient's condition contraindicates excision), specific method of destruction used (cryotherapy with spray or probe technique, electrosurgery with specific settings, laser ablation with type of laser and parameters, chemical agent used for chemocautery), number of applications or treatment sessions, depth and lateral extent of destruction, immediate post-treatment assessment, management of the treated site, and detailed post-treatment instructions. If the diagnosis was previously established by biopsy, this should be referenced in the documentation. The "by report" format requires comprehensive justification for the procedure and technique, including why a non-excisional approach was appropriate for this specific clinical situation.

#### **Code: D7471** – *Removal of lateral exostosis (maxilla or mandible)*
**Use when:** Surgically removing a benign bony growth (exostosis) from the buccal or lingual aspect of the maxilla or mandible, typically for prosthetic or functional purposes.
**Check:** Documentation should specify the location as a lateral (buccal or lingual) exostosis of the maxilla or mandible, not a torus, and detail the surgical approach for removal.
**Note:** This procedure addresses localized bony overgrowths on the lateral aspects of the jaws. The comprehensive documentation should include the specific location of the exostosis (buccal or lingual aspect of maxilla or mandible, with area specified), size and extent of the bony prominence, reason for removal (prosthetic interference, chronic irritation, aesthetic concerns), anesthesia technique, incision design and flap elevation, technique for bone removal (bur, chisel, bone file), extent of bone removed, management of the surgical site including bone smoothing and recontouring, irrigation protocol, closure technique, verification of adequate reduction of the prominence, post-operative instructions, and plan for prosthetic follow-up if applicable. The documentation should clearly distinguish this procedure from removal of tori (D7472, D7473) by specifying the lateral nature of the exostosis. If multiple exostoses are removed, each site should be documented separately and may be reported with multiple units of this code as appropriate.

#### **Code: D7472** – *Removal of torus palatinus*
**Use when:** Surgically removing a benign bony growth (torus) from the midline of the hard palate, typically for prosthetic or functional purposes.
**Check:** Documentation should specify the location as the midline of the hard palate (torus palatinus), detail the size and morphology of the torus, and describe the surgical approach for removal.
**Note:** This procedure addresses the removal of a developmental bony growth from the palatal midline. The detailed documentation should include the size, shape, and extent of the torus palatinus (broad-based vs. pedunculated, single vs. multilobular), reason for removal (typically prosthetic interference, but sometimes chronic ulceration or speech concerns), anesthesia technique including specific palatal blocks, incision design (often Y-shaped or midline with lateral releases), flap elevation technique, method of bone removal (sectioning technique for larger tori, use of burs, chisels, or mallets), consideration of vascular structures especially the greater palatine arteries, management of the sharp edges, irrigation protocol, closure technique including consideration of the increased tissue required to cover the defect, verification of complete removal, post-operative instructions addressing the unique healing challenges of palatal surgery, and plan for prosthetic follow-up if applicable. The documentation should note any unusual anatomical variations or surgical challenges encountered, such as particularly thin overlying mucosa or exceptionally large or multilobular tori requiring staged sectioning.

#### **Code: D7473** – *Removal of torus mandibularis*
**Use when:** Surgically removing a benign bony growth (torus) from the lingual aspect of the mandible in the premolar region, typically for prosthetic or functional purposes.
**Check:** Documentation should specify the location as the lingual aspect of the mandible (torus mandibularis), note whether unilateral or bilateral, detail the size and morphology, and describe the surgical approach for removal.
**Note:** This procedure addresses the removal of developmental bony growths from the lingual aspect of the mandible. The comprehensive documentation should include the specific location (lingual aspect of mandible, noting whether unilateral or bilateral), size, shape, and extent of the tori (broad-based vs. pedunculated, single vs. multilobular), reason for removal (typically prosthetic interference, but sometimes chronic irritation or food trapping), anesthesia technique including lingual nerve blocks, incision design, flap elevation with particular attention to protecting the lingual nerve, method of bone removal (sectioning technique, use of burs, chisels, or mallets), management of the sharp edges, irrigation protocol, closure technique, verification of complete removal, post-operative instructions addressing the unique considerations of the lingual aspect (tongue management, speech, swallowing), and plan for prosthetic follow-up if applicable. If bilateral tori are removed in the same operative session, this should be clearly documented, and the code may be reported twice to reflect both sides. The relationship of the tori to lingual nerve path should be noted, as this presents a particular risk during this procedure.

#### **Code: D7485** – *Reduction of osseous tuberosity*
**Use when:** Surgically reducing an enlarged maxillary tuberosity (posterior lateral aspect of the maxilla), typically for prosthetic purposes or to address functional limitations.
**Check:** Documentation should specify the location as the maxillary tuberosity, establish the enlargement as osseous (bony) rather than fibrous, and detail the surgical approach for reduction.
**Note:** This procedure addresses an enlarged bony prominence at the posterior maxilla. The detailed documentation should include the specific side(s) affected, extent and nature of the enlargement (differentiating osseous from fibrous enlargement), reason for reduction (typically prosthetic interference or cheek biting), anesthesia technique, incision design, flap elevation with consideration of the greater palatine neurovascular bundle, technique for bone removal, extent of reduction performed, management of any maxillary sinus proximity or exposure, irrigation protocol, closure technique, verification of adequate reduction, post-operative instructions with particular attention to possible sinus precautions, and plan for prosthetic follow-up. If the removal includes significant soft tissue reduction, this should be noted but is included in the procedure. If bilateral tuberosity reductions are performed, each side should be documented separately and may be reported with multiple units of this code as appropriate. The documentation should clearly establish that the reduced tissue was primarily osseous in nature to distinguish this from soft tissue procedures.

#### **Code: D7490** – *Radical resection of maxilla or mandible*
**Use when:** Performing an extensive surgical removal of a portion of the maxilla or mandible, typically for aggressive benign or malignant lesions, involving resection beyond the alveolar process to include portions of the basal bone.
**Check:** Documentation should establish the extent of resection (going beyond just the alveolar process), specify whether maxilla or mandible, detail the pathological indication requiring radical approach, and describe reconstruction if performed.
**Note:** This procedure represents major oral surgery involving extensive resection of jawbone. The comprehensive documentation should include the specific diagnosis necessitating radical resection, preoperative imaging findings demonstrating extent of disease, multidisciplinary planning if conducted, anesthesia technique (typically general anesthesia), surgical approach including external incisions if utilized, extent of bone resection with anatomical boundaries clearly defined, management of vital structures (nerves, vessels, adjacent organs), margins assessment, specimen handling protocol, immediate reconstruction approach if performed, fixation methods if utilized, closure techniques for both intraoral and extraoral components if applicable, surgical drain placement if used, immediate postoperative assessment, and detailed post-operative management plan. This code is distinguished from less extensive procedures by the scope of the resection (beyond just the alveolar process) and often involving discontinuity of the jaw. The coordination with other specialists for comprehensive rehabilitation should be documented, including plans for prosthetic reconstruction, additional surgical procedures, and management of form and function.

---

### **Key Takeaways:**
- **Size-Based Code Selection** - For excisional procedures, precise measurement and documentation of lesion size (≤ 1.25 cm vs. > 1.25 cm) is critical for proper code selection.
- **Tissue Origin Differentiation** - Clear documentation must distinguish between odontogenic and nonodontogenic lesions, soft tissue lesions vs. tumors involving deeper structures, and benign vs. malignant pathology.
- **Complexity Factors** - For "complicated" procedure codes (D7412, D7415), documentation must first establish the primary diagnosis AND then clearly articulate the specific complications that increased surgical difficulty.
- **Margin Documentation** - For malignant lesion excisions, documentation of planned margin width is essential and should reflect appropriate oncologic principles.
- **Complete Excision vs. Destruction** - For destruction procedures (D7465), documentation should justify why a non-excisional approach was selected over biopsy or complete excision.
- **Anatomical Specificity for Exostoses/Tori** - Precise anatomical location documentation distinguishes between lateral exostoses (D7471), torus palatinus (D7472), and torus mandibularis (D7473).
- **Vestibuloplasty Technique** - Documentation must clearly differentiate between secondary epithelialization techniques (D7340) and the more complex procedures involving grafts and muscle reattachment (D7350).
- **Reconstruction Documentation** - When reconstruction is performed following excision or resection, the specific technique and materials should be documented, though they may be included in the primary procedure code.
- **Pathology Submission** - For excisional procedures, documentation should confirm that specimens were submitted for pathological examination and address the plan for follow-up once results are received.
- **Radical vs. Local Procedures** - For radical resection (D7490), documentation must clearly establish the extent of resection beyond the alveolar process, distinguishing it from more localized procedures.

Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_other_repair_procedures_code(scenario, temperature=0.0):
    """
    Extract other repair procedures code(s) for a given scenario.
    """
    try:
        chain = create_other_repair_procedures_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Other repair procedures code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_other_repair_procedures_code: {str(e)}")
        return ""

def activate_other_repair_procedures(scenario):
    """
    Activate other repair procedures analysis and return results.
    """
    try:
        return extract_other_repair_procedures_code(scenario)
    except Exception as e:
        print(f"Error in activate_other_repair_procedures: {str(e)}")
        return "" 