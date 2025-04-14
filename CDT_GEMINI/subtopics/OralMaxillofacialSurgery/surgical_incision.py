"""
Module for extracting surgical incision codes.
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
 
def create_surgical_incision_extractor(temperature=0.0):
    """
    Create a LangChain-based surgical incision code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert specializing in oral and maxillofacial surgical procedures,

## **Surgical Incision and Drainage Procedures**

### **Before picking a code, ask:**
- Is the procedure an incision and drainage, marsupialization, or removal of foreign body/non-vital bone?
- Is the incision site intraoral or extraoral?
- Is the procedure simple or complicated (involving multiple fascial spaces)?
- What is the nature of the abscess or infection (origin, extent, affected tissues)?
- Does the procedure involve removal of a foreign body? If so, from what tissue (mucosa, skin, bone, etc.)?
- Is a partial ostectomy or sequestrectomy being performed to remove non-vital bone?
- Does the procedure involve accessing the maxillary sinus for removal of a foreign body or tooth fragment?
- Is the procedure being performed to create a long-term open pocket (marsupialization)?
- Are radiographic studies involved in localizing foreign bodies or non-vital bone?
- What post-operative management is planned following the incision procedure?

---

#### **Code: D7509** – *Marsupialization of odontogenic cyst*
**Use when:** Creating a surgical window in a large odontogenic cyst to establish a permanent opening that allows for continuous drainage and gradual shrinkage of the cyst cavity over time.
**Check:** Documentation should establish the odontogenic origin of the cyst, detail the size and location, and describe the specific technique used to create the permanent opening.
**Note:** Marsupialization is typically selected for large cystic lesions where complete removal might compromise vital structures or cause significant structural damage. The procedure documentation should include the diagnostic basis for determining the cyst is odontogenic, preoperative imaging findings, the specific surgical approach to access the cyst, technique for creating the permanent opening (including dimensions of the window created), management of the cyst lining, any specimens submitted for pathological examination, packing or stenting methods used to maintain patency, and the plan for long-term follow-up. This procedure differs from simple incision and drainage in that it creates a sustained communication between the cyst and the oral cavity.

#### **Code: D7510** – *Incision and drainage of abscess - intraoral soft tissue*
**Use when:** Performing a surgical incision through oral mucosa to create a pathway for drainage of purulent material from an intraoral abscess of dental or periodontal origin.
**Check:** Documentation should specify the intraoral location of the abscess, confirm presence of purulent collection, and detail the incision and drainage technique.
**Note:** This procedure involves creating an incision through mucosa to access and drain a collection of purulent material. The documentation should include the specific location of the abscess, assessment of swelling, pain, fluctuance or other clinical indicators of abscess formation, the incision design and length, evidence of purulent drainage obtained, any cultures taken, irrigation performed, placement of drains if applicable, and instructions for post-operative care. This code is considered appropriate even when the incision is made through the gingival sulcus. Documentation should also address the suspected etiology of the infection and any concurrent or planned definitive treatment of the source (such as endodontic therapy or extraction).

#### **Code: D7511** – *Incision and drainage of abscess - intraoral soft tissue - complicated (includes drainage of multiple fascial spaces)*
**Use when:** Draining an extensive intraoral infection that involves multiple fascial spaces, requiring more complex incision and drainage techniques beyond a simple localized procedure.
**Check:** Documentation must substantiate the complicated nature by detailing involvement of multiple fascial spaces and describing the extensive approach required for adequate drainage.
**Note:** This code applies to more severe infections that have spread beyond a localized area to involve multiple anatomical spaces such as the sublingual, submandibular, buccal, canine, or masseteric spaces. The comprehensive documentation should detail the extent of the infection (often with reference to imaging studies), involvement of specific fascial spaces, the surgical approach for accessing each involved space, exploration techniques, establishment of dependent drainage, placement of drains, irrigation protocol, culture collection, and the management plan for continued drainage and resolution of infection. These cases often involve systemic manifestations that should be noted, and may require coordination with other medical specialists due to their potential severity.

#### **Code: D7520** – *Incision and drainage of abscess - extraoral soft tissue*
**Use when:** Creating a surgical incision through skin to establish drainage of an abscess or purulent collection located in the extraoral soft tissues of the face or neck.
**Check:** Documentation should confirm the extraoral location of the abscess, specify the exact anatomical site, and detail the surgical approach for drainage through the skin.
**Note:** Extraoral incision and drainage procedures require consideration of cosmetic outcomes and anatomical structures. The documentation should include the precise location and extent of the infection, any imaging studies that guided treatment, the specific incision design (often placed in natural skin creases when possible), confirmation of purulent drainage, exploration of the abscess cavity, irrigation performed, drain placement if applicable, wound management approach, and follow-up plan. These procedures often address infections that have originated from dental sources but have spread to facial or cervical spaces, requiring documentation of the suspected origin and any concurrent treatment planned to address the source.

#### **Code: D7521** – *Incision and drainage of abscess - extraoral soft tissue - complicated (includes drainage of multiple fascial spaces)*
**Use when:** Performing drainage of a complex extraoral infection involving multiple fascial spaces of the face or neck, requiring extensive surgical approaches and management.
**Check:** Documentation must specifically identify the multiple fascial spaces involved and detail the comprehensive surgical approach required for complete drainage.
**Note:** These procedures represent management of potentially serious infections that can threaten vital structures. The detailed operative report should document the extent and severity of the infection (often with reference to CT imaging), the specific facial and cervical spaces involved, surgical approaches to each space, exploration techniques, establishment of dependent drainage paths, placement of multiple drains when necessary, culture collection, irrigation protocols, and wound management. Documentation should address airway assessment and management, potential need for hospital admission, intravenous antibiotics, and coordination with other specialists (such as infectious disease or otolaryngology) often required for these cases.

#### **Code: D7530** – *Removal of foreign body from mucosa, skin, or subcutaneous alveolar tissue*
**Use when:** Surgically removing foreign material that has become embedded or lodged in the oral mucosa, facial skin, or subcutaneous tissues of the alveolar region.
**Check:** Documentation should identify the specific foreign body being removed, its location in soft tissues (not bone), and the surgical technique employed for removal.
**Note:** This procedure involves the removal of reaction-producing foreign objects such as splinters, metal fragments, glass, or other materials from soft tissues. The documentation should include the history of how the foreign body was introduced, its composition if known, the exact location, any diagnostic imaging used to localize it, the surgical approach for access, technique for removal, wound management following extraction of the foreign body, and verification of complete removal. If the foreign body is embedded in bone rather than soft tissue, code D7540 would be more appropriate. Documentation of any specimens or removed materials sent for pathological or laboratory examination strengthens the record.

#### **Code: D7540** – *Removal of reaction-producing foreign bodies, musculoskeletal system*
**Use when:** Surgically extracting foreign material embedded within bone or muscle tissue that is causing a tissue reaction or symptoms.
**Check:** Documentation should specify that the foreign body is located within the musculoskeletal system (bone or muscle, not soft tissue), describe the reaction it has produced, and detail the surgical approach for removal.
**Note:** This procedure typically requires more extensive surgical intervention than soft tissue foreign body removal. The comprehensive documentation should include the foreign body's composition if known, how it was introduced, the specific location within bone or muscle, imaging studies used for localization (often 3D imaging for precise location), the surgical approach including any osteotomies required for access, technique for isolation and removal, management of the reactive tissue surrounding the foreign body, verification of complete removal (often through post-operative imaging), and the approach to wound closure and healing. Any specimens submitted for pathological examination should be noted, along with post-operative management plans.

#### **Code: D7550** – *Partial ostectomy/sequestrectomy for removal of non-vital bone*
**Use when:** Surgically removing segments of dead or infected bone that have separated from healthy bone as a result of infection, trauma, or compromised blood supply.
**Check:** Documentation should establish the presence of non-vital bone (sequestrum), detail the surgical approach for removal, and describe the extent of bone requiring removal.
**Note:** This procedure involves the removal of loose, sloughed, or non-vital bone fragments that have separated from the surrounding healthy bone. The clinical documentation should include the etiology of the bone necrosis (infection, radiation, medication-related osteonecrosis, trauma), imaging studies confirming the presence and extent of non-vital bone, the surgical approach for access, technique for identifying the interface between vital and non-vital bone, method of sequestrum removal, management of any associated soft tissue, irrigation protocols, and the approach to promoting healing of the affected site. If the procedure is performed for medication-related osteonecrosis, specific documentation regarding medication history and consultation with prescribing physicians strengthens the record.

#### **Code: D7560** – *Maxillary sinusotomy for removal of tooth fragment or foreign body*
**Use when:** Creating a surgical opening into the maxillary sinus specifically to retrieve a tooth fragment or foreign object that has been displaced or introduced into the sinus cavity.
**Check:** Documentation should confirm the presence of a tooth fragment or foreign body within the maxillary sinus (typically through imaging), and detail the surgical approach used to access the sinus and retrieve the object.
**Note:** This procedure typically results from complications during extraction of maxillary posterior teeth or from traumatic injuries. The comprehensive documentation should include preoperative imaging that confirms the presence and precise location of the foreign body or tooth fragment within the sinus, the specific surgical approach used for sinus access (often through a Caldwell-Luc approach or from an existing extraction site), visualization technique, method of retrieving the foreign material, verification of complete removal, management of the sinus membrane, closure technique, post-operative instructions regarding sinus precautions, and follow-up protocol. Any cultures obtained or antibiotics prescribed should be documented, particularly if signs of sinusitis are present.

---

### **Key Takeaways:**
- **Anatomical Location** - Documentation must clearly specify whether the procedure was performed intraorally or extraorally, as this is a primary determinant in code selection.
- **Complexity Assessment** - Justification for "complicated" codes (D7511, D7521) requires specific documentation of multiple fascial space involvement and the extensive nature of the infection.
- **Infection Source** - The suspected origin of the infection should be documented, particularly for dental or periodontal sources, along with plans to address the primary cause.
- **Foreign Body Characterization** - For foreign body removal, documentation should specify the material's composition, location (soft tissue vs. musculoskeletal), and the reaction it has produced.
- **Imaging Correlation** - Reference to radiographic or advanced imaging studies that guided diagnosis and treatment significantly strengthens documentation.
- **Drainage Verification** - For incision and drainage procedures, documentation should confirm that purulent material was encountered and drained.
- **Specimen Management** - Any materials sent for pathological examination, culture, or other testing should be documented.
- **Post-Procedure Protocol** - Documentation should address drain placement (if applicable), wound management, and follow-up instructions.
- **Marsupialization Distinction** - Code D7509 specifically involves creating a permanent opening for long-term decompression of odontogenic cysts, differentiating it from simple incision and drainage.
- **Sinus Precautions** - For maxillary sinusotomy procedures, documentation should include specific post-operative instructions regarding sinus precautions.

Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_surgical_incision_code(scenario, temperature=0.0):
    """
    Extract surgical incision code(s) for a given scenario.
    """
    try:
        chain = create_surgical_incision_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Surgical incision code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_surgical_incision_code: {str(e)}")
        return ""

def activate_surgical_incision(scenario):
    """
    Activate surgical incision analysis and return results.
    """
    try:
        return extract_surgical_incision_code(scenario)
    except Exception as e:
        print(f"Error in activate_surgical_incision: {str(e)}")
        return "" 