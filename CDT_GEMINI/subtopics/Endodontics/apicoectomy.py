import os
import sys
from langchain.prompts import PromptTemplate
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file
from subtopics.prompt.prompt import PROMPT



def create_apicoectomy_extractor():
    """
    Create a LangChain-based Apicoectomy/Periradicular Services code extractor.
    """
    prompt_template = f"""
You are a highly experienced dental coding expert

### Before Picking a Code, Ask:
- What was the primary reason the patient came in? Was it for a specific issue (e.g., persistent infection, root resorption) requiring surgical intervention, or was it identified during a routine visit?
- Which tooth and root(s) are involved? Is it an anterior, premolar, or molar tooth, and how many roots are being treated?
- Is the procedure an apicoectomy, root resection, repair of resorption, or another periradicular service?
- Are diagnostic findings (e.g., radiographs, clinical exams) confirming the need for surgery (e.g., periapical pathology, resorption)?
- Does the procedure include additional steps like retrograde filling, bone grafting, or tissue regeneration?

---

### Apicoectomy/Periradicular Services

#### Code: D3410
**Heading:** Apicoectomy — anterior  
**Description:** For surgery on root of anterior tooth. Does not include placement of retrograde filling material.  
**When to Use:**  
- The patient has a permanent anterior tooth with a periapical lesion or failed root canal requiring surgical root-end resection.  
- Involves removing the root tip and sealing the canal surgically, excluding retrograde filling.  
**What to Check:**  
- Confirm the tooth is an anterior (incisor/canine) via radiograph or exam.  
- Assess periapical pathology (e.g., abscess, granuloma) and prior endodontic treatment.  
- Check if retrograde filling is planned (code separately as D3430).  
- Verify tooth restorability post-surgery.  
**Notes:**  
- Use D3430 for retrograde filling if performed—D3410 covers surgery only.  
- Not for premolars or molars (see D3421, D3425).  
- Narrative and X-rays often required for insurance.  

#### Code: D3421
**Heading:** Apicoectomy — premolar (first root)  
**Description:** For surgery on one root of a premolar. Does not include placement of retrograde filling material. If more than one root is treated, see D3426.  
**When to Use:**  
- The patient has a premolar with a periapical issue on one root requiring surgical resection.  
- Use for the first root only; additional roots use D3426.  
**What to Check:**  
- Confirm the tooth is a premolar and only one root is treated via radiograph.  
- Assess the need for surgery (e.g., persistent infection) and canal status.  
- Check if additional roots require treatment (use D3426 if so).  
- Verify no retrograde filling is included (code D3430 separately).  
**Notes:**  
- Limited to one root—multi-root premolars may need D3426 for additional roots.  
- Excludes retrograde filling—document separately.  
- Requires evidence of pathology for insurance.  

#### Code: D3425
**Heading:** Apicoectomy — molar (first root)  
**Description:** For surgery on one root of a molar tooth. Does not include placement of retrograde filling material. If more than one root is treated, see D3426.  
**When to Use:**  
- The patient has a molar with a periapical lesion on one root requiring surgical resection.  
- Use for the first root only; additional roots use D3426.  
**What to Check:**  
- Confirm the tooth is a molar and only one root is treated via radiograph.  
- Assess the root-specific pathology and prior endodontic history.  
- Check if additional roots are involved (use D3426 if applicable).  
- Verify retrograde filling isn't included (code D3430 separately).  
**Notes:**  
- Limited to one root—multi-root molars may need D3426.  
- Excludes retrograde filling—code separately.  
- Detailed documentation needed due to molar complexity.  

#### Code: D3426
**Heading:** Apicoectomy (each additional root)  
**Description:** Typically used for premolar and molar surgeries when more than one root is treated during the same procedure. This does not include retrograde filling material placement.  
**When to Use:**  
- The patient has a premolar or molar with multiple roots requiring apicoectomy on additional roots beyond the first (D3421 or D3425).  
- Use per additional root in the same surgical session.  
**What to Check:**  
- Confirm multiple roots are treated in one procedure via radiograph.  
- Assess each root's condition and surgical necessity.  
- Check if used with D3421 or D3425 for the first root.  
- Verify no retrograde filling is included (use D3430).  
**Notes:**  
- Not a standalone code—pairs with D3421 or D3425.  
- Excludes retrograde filling—code separately.  
- Specify root count in documentation for insurance.  

#### Code: D3471
**Heading:** Surgical repair of root resorption — anterior  
**Description:** For surgery on root of anterior tooth. Does not include placement of restoration.  
**When to Use:**  
- The patient has an anterior tooth with root resorption (external/internal) requiring surgical repair.  
- Involves accessing and repairing the resorbed area surgically.  
**What to Check:**  
- Confirm resorption on an anterior tooth via radiograph or exam.  
- Assess resorption extent and location (e.g., cervical, apical).  
- Check if restoration is needed post-repair (code separately).  
- Verify no apicoectomy is performed (use D3410 if so).  
**Notes:**  
- Excludes restoration—code separately (e.g., D2950).  
- Not for premolars or molars (see D3472, D3473).  
- Narrative required to justify surgical need.  

#### Code: D3472
**Heading:** Surgical repair of root resorption — premolar  
**Description:** For surgery on root of premolar tooth. Does not include placement of restoration.  
**When to Use:**  
- The patient has a premolar with root resorption requiring surgical intervention.  
- Use for repairing resorption without restoration.  
**What to Check:**  
- Confirm resorption on a premolar via radiograph.  
- Assess resorption severity and surgical feasibility.  
- Check if restoration follows (code separately).  
- Verify no apicoectomy is involved (use D3421 if so).  
**Notes:**  
- Excludes restoration—code separately.  
- Not for anterior or molars (see D3471, D3473).  
- Documentation of resorption critical for insurance.  

#### Code: D3473
**Heading:** Surgical repair of root resorption — molar  
**Description:** For surgery on root of molar tooth. Does not include placement of restoration.  
**When to Use:**  
- The patient has a molar with root resorption needing surgical repair.  
- Use for surgical correction of resorption only.  
**What to Check:**  
- Confirm resorption on a molar via radiograph.  
- Assess resorption location and impact on tooth stability.  
- Check if restoration is planned (code separately).  
- Verify no apicoectomy is performed (use D3425 if so).  
**Notes:**  
- Excludes restoration—code separately.  
- Not for anterior or premolars (see D3471, D3472).  
- Requires detailed narrative for insurance.  

#### Code: D3501
**Heading:** Surgical exposure of root surface without apicoectomy or repair of root resorption — anterior  
**Description:** Exposure of root surface followed by observation and surgical closure of the exposed area. Not to be used for or in conjunction with apicoectomy or repair of root resorption.  
**When to Use:**  
- The patient has an anterior tooth requiring root surface exposure for observation (e.g., diagnostic purposes) without resection or repair.  
- Involves surgical access and closure only.  
**What to Check:**  
- Confirm the tooth is anterior and no apicoectomy/resorption repair is needed.  
- Assess the purpose (e.g., diagnostic, minor pathology) via radiograph.  
- Check if combined with other procedures (not allowed with D3410, D3471).  
- Verify patient condition supports surgical exposure.  
**Notes:**  
- Standalone code—not for use with apicoectomy or resorption repair.  
- Narrative needed to explain purpose (e.g., diagnostic intent).  
- Not for premolars or molars (see D3502, D3503).  

#### Code: D3502
**Heading:** Surgical exposure of root surface without apicoectomy or repair of root resorption — premolar  
**Description:** Exposure of root surface followed by observation and surgical closure of the exposed area. Not to be used for or in conjunction with apicoectomy or repair of root resorption.  
**When to Use:**  
- The patient has a premolar requiring root surface exposure for observation without further surgical treatment.  
- Use for surgical access and closure only.  
**What to Check:**  
- Confirm the tooth is a premolar and no apicoectomy/resorption repair is planned.  
- Assess the clinical need for exposure via radiograph or exam.  
- Check if paired with other codes (not allowed with D3421, D3472).  
- Verify patient suitability for procedure.  
**Notes:**  
- Not combinable with apicoectomy or resorption repair codes.  
- Requires justification in documentation.  
- Not for anterior or molars (see D3501, D3503).  

#### Code: D3503
**Heading:** Surgical exposure of root surface without apicoectomy or repair of root resorption — molar  
**Description:** Exposure of root surface followed by observation and surgical closure of the exposed area. Not to be used for or in conjunction with apicoectomy or repair of root resorption.  
**When to Use:**  
- The patient has a molar requiring root surface exposure for observation without resection or repair.  
- Use for surgical access and closure only.  
**What to Check:**  
- Confirm the tooth is a molar and no apicoectomy/resorption repair is involved.  
- Assess the purpose of exposure (e.g., diagnostic) via radiograph.  
- Check if combined with other procedures (not allowed with D3425, D3473).  
- Verify patient condition supports surgery.  
**Notes:**  
- Standalone code—not for use with apicoectomy or resorption repair.  
- Narrative required to explain intent.  
- Not for anterior or premolars (see D3501, D3502).  

#### Code: D3428
**Heading:** Bone graft in conjunction with periradicular surgery — per tooth, single site  
**Description:** Includes non-autogenous graft material.  
**When to Use:**  
- The patient requires a bone graft at a single site during periradicular surgery (e.g., apicoectomy).  
- Use for one tooth with non-autogenous material to support healing.  
**What to Check:**  
- Confirm periradicular surgery (e.g., D3410) is performed on the same tooth.  
- Assess bone defect size and need for grafting via radiograph.  
- Check if only one site is treated (use D3429 for additional sites).  
- Verify material is non-autogenous (e.g., synthetic, allograft).  
**Notes:**  
- Pairs with apicoectomy codes (e.g., D3410, D3421).  
- Narrative and X-rays needed for insurance.  
- Not for autogenous grafts (use D7950 if applicable).  

#### Code: D3429
**Heading:** Bone graft in conjunction with periradicular surgery — each additional contiguous tooth in the same surgical site  
**Description:** Includes non-autogenous graft material.  
**When to Use:**  
- The patient has additional contiguous teeth in the same surgical site requiring bone grafting during periradicular surgery.  
- Use per extra tooth beyond the first (D3428).  
**What to Check:**  
- Confirm D3428 is used for the first tooth and additional teeth are contiguous.  
- Assess bone loss across multiple teeth via radiograph.  
- Check if surgery spans multiple teeth in one site.  
- Verify non-autogenous material is used.  
**Notes:**  
- Not standalone—requires D3428 for the first tooth.  
- Specify tooth count in documentation.  
- Insurance may scrutinize multi-tooth grafting.  

#### Code: D3430
**Heading:** Retrograde filling — per root  
**Description:** For placement of retrograde filling material during periradicular surgery procedures. If more than one filling is placed in one root, report as D3999 and describe.  
**When to Use:**  
- The patient has a root requiring retrograde filling (e.g., amalgam, MTA) during periradicular surgery.  
- Use per root treated with filling material.  
**What to Check:**  
- Confirm periradicular surgery (e.g., D3410) is performed.  
- Assess the number of roots filled (one code per root).  
- Check if multiple fillings in one root occur (use D3999 instead).  
- Verify material type and placement success.  
**Notes:**  
- Pairs with apicoectomy codes (e.g., D3410, D3426).  
- Use D3999 with description for multiple fillings in one root.  
- Documentation of material and placement required.  

#### Code: D3431
**Heading:** Biologic materials to aid in soft and osseous tissue regeneration in conjunction with periradicular surgery  
**When to Use:**  
- The patient requires biologic materials (e.g., growth factors) to enhance tissue regeneration during periradicular surgery.  
- Use to support soft and bone healing beyond standard grafting.  
**What to Check:**  
- Confirm periradicular surgery is performed (e.g., D3410).  
- Assess the need for biologic enhancement via clinical findings.  
- Check material type and application method.  
- Verify not overlapping with D3428/D3429 (bone grafts).  
**Notes:**  
- Distinct from bone grafts—focuses on biologic agents.  
- Narrative required to specify materials and purpose.  
- Insurance may require justification for use.  

#### Code: D3432
**Heading:** Guided tissue regeneration, resorbable barrier, per site, in conjunction with periradicular surgery  
**When to Use:**  
- The patient requires a resorbable barrier for guided tissue regeneration during periradicular surgery.  
- Use per surgical site to promote selective tissue growth.  
**What to Check:**  
- Confirm periradicular surgery is performed (e.g., D3425).  
- Assess defect size and need for GTR via radiograph.  
- Check if barrier is resorbable (non-resorbable uses different coding).  
- Verify site-specific application.  
**Notes:**  
- Pairs with apicoectomy or related codes.  
- Narrative and X-rays needed for insurance.  
- Not for non-resorbable barriers.  

#### Code: D3450
**Heading:** Root amputation — per root  
**Description:** Root resection of a multi-rooted tooth while leaving the crown. If the crown is sectioned, see D3920.  
**When to Use:**  
- The patient has a multi-rooted tooth (e.g., molar) with one root requiring removal while preserving the crown.  
- Use per root amputated.  
**What to Check:**  
- Confirm the tooth is multi-rooted and crown is retained via radiograph.  
- Assess the root's condition (e.g., fracture, resorption).  
- Check if crown sectioning occurs (use D3920 instead).  
- Verify restorability post-amputation.  
**Notes:**  
- Not for crown sectioning (see D3920).  
- Specify root in documentation.  
- Often followed by restorative coding.  

#### Code: D3460
**Heading:** Endodontic endosseous implant  
**Description:** Placement of implant material, which extends from a pulpal space into the bone beyond the end of the root.  
**When to Use:**  
- The patient requires an endodontic implant extending from the canal into periapical bone for stabilization.  
- Use for rare cases of root reinforcement.  
**What to Check:**  
- Confirm the tooth and bone condition support implantation via radiograph.  
- Assess prior endodontic status and implant feasibility.  
- Check material type and placement depth.  
- Verify patient consent for experimental procedure.  
**Notes:**  
- Rarely used—requires extensive justification.  
- Narrative and imaging critical for insurance.  
- Not a standard endodontic procedure.  

#### Code: D3470
**Heading:** Intentional re-implantation (including necessary splinting)  
**Description:** For the intentional removal, inspection, and treatment of the root and replacement of a tooth into its own socket. This does not include necessary retrograde filling material placement.  
**When to Use:**  
- The patient has a tooth intentionally extracted, treated (e.g., root-end resection), and re-implanted into its socket.  
- Includes splinting for stabilization.  
**What to Check:**  
- Confirm the tooth is viable for re-implantation via exam and radiograph.  
- Assess the procedure steps (extraction, treatment, reinsertion).  
- Check if retrograde filling is needed (code D3430 separately).  
- Verify splinting is performed and effective.  
**Notes:**  
- Excludes retrograde filling—code separately.  
- Requires detailed narrative and X-rays for insurance.  
- High-risk procedure—document patient consent.  

---

### Key Takeaways:
- **Tooth and Root Specificity:** Codes vary by tooth type (anterior, premolar, molar) and root count—accuracy is essential.  
- **Surgical Scope:** Codes reflect specific procedures (e.g., apicoectomy, resorption repair)—don't assume volume equals complexity.  
- **Add-Ons Separate:** Retrograde fillings, grafts, and restorations require additional coding—don't bundle.  
- **Documentation Heavy:** Insurance often demands narratives, X-rays, and clinical justification for surgical codes.  
- **Procedure Limits:** Some codes (e.g., D3501-D3503) exclude combination with others—check compatibility.




### **Scenario:**
"{{scenario}}"

{PROMPT}
"""
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["scenario"])
    return create_chain(prompt)

def extract_apicoectomy_code(scenario):
    """
    Extract Apicoectomy/Periradicular Services code(s) for a given scenario.
    """
    try:
        extractor = create_apicoectomy_extractor()
        result = invoke_chain(extractor, {"scenario": scenario})
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Error in apicoectomy code extraction: {str(e)}")
        return None

def activate_apicoectomy(scenario):
    """
    Activate Apicoectomy/Periradicular Services analysis and return results.
    """
    try:
        result = extract_apicoectomy_code(scenario)
        return result
    except Exception as e:
        print(f"Error activating apicoectomy analysis: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = "A patient has persistent pain in tooth #8 (maxillary right central incisor) despite having a root canal two years ago. Radiographs show a periapical lesion. The dentist performs an apicoectomy, removing the root tip and surgically sealing the canal. No retrograde filling material is placed."
    result = activate_apicoectomy(scenario)
    print(result) 