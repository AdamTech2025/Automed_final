"""
Module for extracting excision of soft tissue lesions codes.
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
 
def create_excision_soft_tissue_extractor(temperature=0.0):
    """
    Create a LangChain-based excision of soft tissue lesions code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert specializing in oral and maxillofacial pathology,

## **Soft Tissue Lesion Excision and Management**

### **Before picking a code, ask:**
- Is the lesion benign or malignant (was tissue sent for pathology)?
- What is the size of the lesion being excised (up to 1.25 cm or greater)?
- Is the excision complicated by location, depth, or relationship to adjacent structures?
- What diagnostic measures were taken prior to excision (biopsy, imaging, etc.)?
- Is the procedure a physical or chemical destruction rather than a surgical excision?
- What type of soft tissue is involved (mucosa, gingiva, tongue, etc.)?
- Is the procedure complete excision with margins, or incisional biopsy of a portion?
- Are specialized techniques required due to the location or nature of the lesion?
- Does the patient have any complicating medical conditions that affect the approach?
- What is the primary goal of the procedure (diagnostic, therapeutic, or both)?

---

#### **Code: D7410** – *Excision of benign lesion up to 1.25 cm*
**Use when:** Performing complete surgical removal of a benign soft tissue lesion measuring up to 1.25 cm at its greatest dimension, including appropriate margins of normal-appearing tissue.
**Check:** Verify documentation includes pre-operative size measurement, clinical description of the lesion, and confirmation that the entire lesion was removed with margins of normal tissue.
**Note:** This procedure involves the complete removal of a clinically or previously diagnosed benign lesion. The excised specimen must be submitted for pathological examination. Documentation should include the precise anatomical location, clinical appearance, size measurements in all dimensions, excision technique, margin width, method of closure, and any photographs taken. The pathology report should be referenced once available to confirm the benign nature of the lesion.

#### **Code: D7411** – *Excision of benign lesion greater than 1.25 cm*
**Use when:** Removing a benign soft tissue lesion that exceeds 1.25 cm in its greatest dimension, including a margin of normal-appearing tissue.
**Check:** Documentation must clearly state the dimensions of the lesion (greater than 1.25 cm), the clinical diagnosis or suspicion of benignity, and the surgical approach used for complete removal.
**Note:** Larger benign lesions often require more complex surgical planning and execution, including considerations for primary closure, potential flap advancement, or secondary healing. The operative report should detail the challenges presented by the larger lesion, how these were addressed surgically, and the healing plan. Size documentation is critical for this code, with measurements ideally recorded both clinically and on the pathology specimen (noting that fixatives may cause shrinkage from clinical measurements).

#### **Code: D7412** – *Excision of benign lesion, complicated*
**Use when:** Excising a benign soft tissue lesion where the complexity exceeds standard removal due to anatomical location (proximity to vital structures), accessibility challenges, depth of invasion, or relation to adjacent structures requiring special techniques.
**Check:** Documentation must specifically substantiate the complicated nature of the procedure beyond size alone, detailing the specific factors that increased surgical complexity.
**Note:** The "complicated" designation requires explicit documentation of the complicating factors. These may include lesions near neurovascular bundles requiring careful dissection, lesions extending into multiple tissue planes, lesions in areas of limited access requiring specialized approaches, or cases requiring additional procedures for reconstruction. The operative note should clearly detail the technical challenges encountered and how they were managed. This code can apply to lesions of any size when significant complicating factors are present.

#### **Code: D7413** – *Excision of malignant lesion up to 1.25 cm*
**Use when:** Performing excision of a lesion clinically suspected or previously diagnosed as malignant, measuring up to 1.25 cm, with appropriate margins according to oncological principles.
**Check:** Verify that there is documentation of malignant suspicion or previous positive biopsy findings, and that margins are appropriate for the specific malignancy type.
**Note:** Excision of malignant lesions requires wider margins than benign lesions and more meticulous documentation. The operative record should include the clinical basis for malignancy suspicion, previous pathology findings if available, planned margin width, careful orientation of the specimen for pathology, and vital structure preservation considerations. Management of malignancies often involves multidisciplinary care, so documentation should reflect consultation with other specialists when appropriate. This procedure must include submission of the specimen for pathological examination.

#### **Code: D7414** – *Excision of malignant lesion greater than 1.25 cm*
**Use when:** Removing a clinically suspected or confirmed malignant lesion exceeding 1.25 cm in its greatest dimension, with oncologically appropriate margins.
**Check:** Documentation must include clear measurements confirming size greater than 1.25 cm, the basis for malignancy suspicion or diagnosis, and the surgical approach including margin planning.
**Note:** Larger malignant lesions present significant surgical challenges, including ensuring adequate margins while preserving function and aesthetics. The operative report should detail the extent of the lesion, any preoperative imaging used for surgical planning, the specific technique for ensuring clear margins, management of surrounding tissues, and the reconstruction or healing plan. Often, coordination with oncology, pathology, and reconstructive specialists should be documented. Staging information should be included when available.

#### **Code: D7415** – *Excision of malignant lesion, complicated*
**Use when:** Excising a malignant lesion with significant complications due to size, location, depth of invasion, proximity to vital structures, or need for complex reconstruction.
**Check:** Documentation must specifically detail the complicating factors beyond routine malignancy management that justify this higher-level code.
**Note:** This code represents the most complex oral soft tissue malignancy excisions. These cases often involve extensive preoperative planning, potentially including advanced imaging, multidisciplinary consultation, and consideration of staged procedures. Complicating factors might include lesions invading deep structures, wrapped around neurovascular bundles, involving multiple anatomical spaces, or requiring extensive reconstruction. Detailed operative documentation should include each challenge encountered, steps taken to overcome these challenges, and specific techniques employed to maintain oncologic principles while preserving function and anatomy where possible.

#### **Code: D7465** – *Destruction of lesion(s) by physical or chemical method, by report*
**Use when:** Using physical methods (laser, electrosurgery, cryosurgery) or chemical agents to destroy oral lesions rather than surgically excising them.
**Check:** Documentation must specify the destruction method used, clinical justification for this approach rather than excision, and detailed description of the lesion(s) being treated.
**Note:** This approach is typically used for superficial or multiple lesions where excision might be unnecessarily invasive or create functional/aesthetic concerns. Common applications include viral papillomas, superficial vascular lesions, and certain premalignant conditions. The report should detail the specific destruction method (e.g., laser type and settings, cryosurgery protocol, chemical agent used), the number and location of lesions treated, pre-treatment photographs when available, expected healing course, and follow-up plan. Since tissue is not submitted for pathological examination, strong justification for the clinical diagnosis is critical.

---

### **Key Takeaways:**
- **Size Determination** - Accurate measurement and documentation of lesion size is crucial for proper code selection, with 1.25 cm being the key threshold.
- **Benign vs. Malignant** - Different codes apply based on the pathological nature of the lesion; preliminary clinical assessment or previous biopsy results guide initial code selection.
- **Complexity Factors** - "Complicated" designations require specific documentation of factors beyond size alone that increased surgical difficulty.
- **Margin Requirements** - Benign lesions typically require smaller margins than malignant lesions; margin width should be documented.
- **Pathological Submission** - All excised specimens should be submitted for pathological examination (except D7465) with proper orientation and identification.
- **Photographic Documentation** - Clinical photographs significantly strengthen documentation and can help justify code selection.
- **Destruction vs. Excision** - D7465 specifically applies to lesion destruction rather than excision and requires detailed reporting of the method used.
- **Complete vs. Partial Removal** - These codes are for complete lesion removal; for diagnostic sampling, use biopsy codes (D7285, D7286) instead.
- **Documenting Reconstruction** - For larger or complicated excisions, document how the resulting defect was managed.
- **Follow-up Planning** - Include plans for wound management, healing assessment, and pathology result review.

Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_excision_soft_tissue_code(scenario, temperature=0.0):
    """
    Extract excision of soft tissue lesions code(s) for a given scenario.
    """
    try:
        chain = create_excision_soft_tissue_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Excision of soft tissue lesions code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_excision_soft_tissue_code: {str(e)}")
        return ""

def activate_excision_soft_tissue(scenario):
    """
    Activate excision of soft tissue lesions analysis and return results.
    """
    try:
        return extract_excision_soft_tissue_code(scenario)
    except Exception as e:
        print(f"Error in activate_excision_soft_tissue: {str(e)}")
        return "" 