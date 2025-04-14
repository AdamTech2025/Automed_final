"""
Module for extracting excision of bone tissue codes.
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
 
def create_excision_bone_tissue_extractor(temperature=0.0):
    """
    Create a LangChain-based excision of bone tissue code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert specializing in oral and maxillofacial osseous procedures,

## **Excision of Bone Tissue**

### **Before picking a code, ask:**
- What specific type of bony growth or abnormality is being removed (exostosis, torus, etc.)?
- What is the anatomical location of the bone tissue being excised (maxilla, mandible, palate)?
- Is the procedure a removal of a localized growth or a more extensive resection?
- What is the clinical indication for removal of the bone tissue?
- Is the procedure being performed for prosthetic considerations or due to pathology?
- Does the excision involve cutting of adjacent soft tissue and reflection of a flap?
- How extensive is the bone removal procedure (partial or complete resection)?
- Will the procedure require reconstruction or grafting to restore form and function?
- Are there any unusual anatomical considerations that increase case complexity?
- How will the surgical site be managed following excision (primary closure, secondary healing)?

---

#### **Code: D7471** – *Removal of lateral exostosis (maxilla or mandible)*
**Use when:** Excising a benign, localized outgrowth or protuberance of bone from the lateral aspect of the maxilla or mandible, typically performed to eliminate tissue interference with a prosthetic appliance or to address soft tissue irritation.
**Check:** Documentation should specify the exact location of the exostosis (buccal or labial aspect of maxilla or mandible), dimensions of the bony growth, and the surgical approach for removal.
**Note:** This procedure typically involves raising a mucoperiosteal flap, exposing the bony outgrowth, using rotary and/or hand instruments to remove the excess bone, smoothing the remaining bone surface, and repositioning and suturing the flap. The operative report should detail the incision design, extent of bone removal, management of the surgical site, and the clinical rationale for the procedure. Photographs or diagrams can be particularly helpful in documenting the location and extent of the exostosis.

#### **Code: D7472** – *Removal of torus palatinus*
**Use when:** Surgically removing a benign bony growth or protuberance from the hard palate (midline of the maxilla), typically performed for prosthetic reasons or due to chronic irritation or ulceration of the overlying mucosa.
**Check:** Documentation should confirm the midline palatal location of the torus, describe its size and morphology (discrete nodule, multilobular, etc.), and detail the surgical technique for removal.
**Note:** Torus palatinus procedures often present unique challenges due to the thin overlying mucosa, proximity to the greater palatine vessels, and difficulty in achieving primary closure in some cases. The operative report should document the incision design (often Y-shaped or elliptical), method of bone removal (rotary instruments, bone files, mallets and chisels), management of the wound (primary closure or surgical packing), and any special considerations due to size or vascularity. Post-operative instructions regarding palatal coverage appliances are often included in the documentation.

#### **Code: D7473** – *Removal of torus mandibularis*
**Use when:** Excising a benign bony growth or protuberance from the lingual aspect of the mandible, in the premolar region above the mylohyoid line, typically performed to facilitate prosthetic treatment or address mucosal trauma.
**Check:** Documentation should specify the unilateral or bilateral nature of the tori, their dimensions, and the detailed surgical approach for removal.
**Note:** The lingual location of mandibular tori creates specific surgical challenges, including difficult access, proximity to the lingual nerve, and management of the lingual flap. The operative report should detail precautions taken to protect the lingual nerve, the method of bone removal, how the surgical site was managed, and the rationale for removal. If bilateral tori are removed in a single session, this should be clearly documented with specific details for each side. Particular attention to hemostasis and flap management is often noted due to the tendency for hematoma formation in this area.

#### **Code: D7485** – *Surgical reduction of osseous tuberosity*
**Use when:** Reducing an enlarged bony prominence on the maxillary tuberosity region (posterior to the last molar), typically performed to eliminate tissue interference with a prosthetic appliance or to correct functional issues.
**Check:** Documentation should describe the extent of the tuberosity enlargement, confirm the location posterior to the last molar, and detail the surgical approach for reduction.
**Note:** Tuberosity reduction requires special consideration due to proximity to the maxillary sinus, greater palatine vessels, and pterygoid plates. The operative note should document assessment of the maxillary sinus relationship (radiographic evaluation), the technique for bone removal, measures taken to prevent sinus perforation, management of the soft tissue envelope (which is often excessive following reduction), and verification of hemostasis. If performed in conjunction with extraction of posterior teeth, both procedures should be separately documented and justified.

#### **Code: D7490** – *Radical resection of maxilla or mandible*
**Use when:** Performing an extensive surgical removal of a portion or the entirety of the maxilla or mandible, typically due to pathology such as aggressive benign tumors or malignancies requiring wide surgical margins.
**Check:** Documentation must substantiate the extensive nature of the resection, including detailed description of the extent of bone removal and the pathological indication requiring this aggressive approach.
**Note:** This represents the most extensive bone removal procedure in this section and often requires multidisciplinary planning. The comprehensive operative report should document preoperative imaging studies and planning, the specific approach for accessing the surgical site, extent of bone and soft tissue removal, margin status, preservation or sacrifice of adjacent structures, method of reconstruction (if performed), and planned rehabilitation. This procedure often involves coordinated care with other specialists including oral surgeons, head and neck surgeons, prosthodontists, and oncologists. Appropriate staging information and pre/post-operative images should be included in the documentation.

---

### **Key Takeaways:**
- **Anatomical Precision** - Documentation must precisely identify the specific location of the bony abnormality being removed (lateral exostosis, palatal torus, mandibular torus, tuberosity).
- **Procedural Rationale** - The clinical indication for bone removal should be clearly documented, whether for prosthetic purposes, due to pathology, or to address functional issues.
- **Dimensional Documentation** - The size and extent of the bony growth or area to be resected should be recorded in the documentation.
- **Surgical Technique** - The method of bone removal (rotary instruments, chisels, saws, etc.) should be specified in the operative note.
- **Anatomical Considerations** - Documentation should address management of and precautions taken for critical adjacent structures (nerves, vessels, sinus).
- **Flap Design** - The surgical approach, including incision design and flap management, should be detailed in the documentation.
- **Wound Management** - The method of closure or management of the surgical site following bone removal should be documented.
- **Prosthetic Planning** - When performed for prosthetic reasons, documentation should include how the procedure relates to the planned prosthetic rehabilitation.
- **Complexity Factors** - Any unusual anatomical variations or procedural difficulties should be noted in the documentation.
- **Imaging Correlation** - Reference to pre-operative radiographs or other imaging that guided the surgical approach adds value to the documentation.

Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_excision_bone_tissue_code(scenario, temperature=0.0):
    """
    Extract excision of bone tissue code(s) for a given scenario.
    """
    try:
        chain = create_excision_bone_tissue_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Excision of bone tissue code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_excision_bone_tissue_code: {str(e)}")
        return ""

def activate_excision_bone_tissue(scenario):
    """
    Activate excision of bone tissue analysis and return results.
    """
    try:
        return extract_excision_bone_tissue_code(scenario)
    except Exception as e:
        print(f"Error in activate_excision_bone_tissue: {str(e)}")
        return "" 