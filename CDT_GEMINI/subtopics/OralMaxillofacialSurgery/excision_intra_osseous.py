"""
Module for extracting excision of intra-osseous lesions codes.
"""

import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from llm_services import LLMService, get_service, set_model, set_temperature

# Load environment variables
load_dotenv()

class ExcisionIntraOsseousServices:
    """Class to analyze and extract excision of intra-osseous lesions codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing excision of intra-osseous lesions scenarios."""
        from subtopics.prompt.prompt import PROMPT
        return PromptTemplate(
            template=f"""
You are a highly experienced dental coding expert specializing in oral and maxillofacial pathology,

## **Excision of Intra-Osseous Lesions**

### **Before picking a code, ask:**
- Is the lesion benign or malignant (or suspected to be malignant)?
- What is the exact size of the lesion (up to 1.25 cm or greater than 1.25 cm)?
- Is the lesion odontogenic or non-odontogenic in origin?
- What specific type of lesion is being removed (cyst, tumor, etc.)?
- Were margins of normal-appearing tissue included in the excision?
- What imaging was used to determine the extent and characteristics of the lesion?
- Has there been a previous biopsy or other diagnostic procedure?
- What surgical approach was used to access the intra-osseous lesion?
- How was the surgical defect managed following excision?
- Was reconstruction with grafting or other materials necessary?

---

#### **Code: D7440** – *Excision of malignant tumor - lesion diameter up to 1.25 cm*
**Use when:** Performing surgical removal of an intra-osseous lesion clinically suspected or confirmed to be malignant, with the lesion measuring up to 1.25 cm in its greatest dimension, including appropriate margins of normal-appearing tissue.
**Check:** Documentation should confirm malignant characteristics (through previous biopsy or strong clinical evidence), precise measurement of the lesion size (not exceeding 1.25 cm), and description of the margins of normal tissue excised.
**Note:** Excision of malignant intra-osseous lesions requires meticulous preoperative planning and assessment. The procedure documentation should include references to preoperative imaging studies (radiographs, CT, MRI), previous pathology reports if available, the surgical approach for access, method of ensuring complete excision, preservation of adjacent critical structures, and management of the resulting defect. Appropriate margin width should be explicitly documented, as should specimen orientation for the pathologist. The operative report should detail the rationale for suspecting malignancy if a definitive pre-operative diagnosis is not available.

#### **Code: D7441** – *Excision of malignant tumor - lesion diameter greater than 1.25 cm*
**Use when:** Excising an intraosseous lesion with malignant characteristics that exceeds a diameter of 1.25 cm, using appropriate oncologic principles including adequate margins of normal-appearing tissue.
**Check:** Documentation must specify the measured size exceeding 1.25 cm, confirm the malignant nature or suspicion of malignancy, and detail the extent of normal tissue margins included in the excision.
**Note:** These larger malignant lesions often present significant reconstructive challenges after excision. The comprehensive procedure note should document precise preoperative size assessment through advanced imaging, the surgeon's approach to ensuring adequate margins while preserving critical structures when possible, method of excision (instruments used), specimen handling protocol, and the reconstruction approach. Documentation should also address staging considerations, coordination with other specialists (medical oncology, radiation oncology), and the overall treatment plan. These cases often require more extensive reconstruction which should be separately documented.

#### **Code: D7450** – *Removal of benign odontogenic cyst or tumor - lesion diameter up to 1.25 cm*
**Use when:** Excising a benign intra-osseous lesion of odontogenic origin (arising from dental developmental tissues) measuring up to 1.25 cm in diameter, including a margin of normal-appearing bone.
**Check:** Documentation should establish the odontogenic nature of the lesion (through clinical and radiographic findings), confirm the benign characteristics, and record precise measurement not exceeding 1.25 cm.
**Note:** Odontogenic lesions include entities such as ameloblastomas, odontogenic keratocysts, and dentigerous cysts, among others. The operative note should document the basis for the clinical diagnosis, radiographic appearance and extent, relationship to adjacent teeth and structures, surgical approach used, technique for complete removal, management of any associated teeth (extraction or preservation), and how the surgical defect was managed. For cystic lesions, documentation should note whether the cyst was removed intact or via enucleation, and should reference submission of the specimen for pathological examination.

#### **Code: D7451** – *Removal of benign odontogenic cyst or tumor - lesion diameter greater than 1.25 cm*
**Use when:** Surgically removing a benign odontogenic cyst or tumor larger than 1.25 cm in diameter, including appropriate margins of normal-appearing tissue to ensure complete excision.
**Check:** Documentation must specifically identify the lesion as odontogenic in origin, confirm benign characteristics, and record measurements exceeding 1.25 cm in diameter.
**Note:** Larger odontogenic lesions often require more extensive surgical approaches and may present greater challenges for complete removal and reconstruction. The operative report should detail the extent of bone removal required, management of adjacent teeth and vital structures, techniques employed to ensure complete removal (particularly for lesions with high recurrence potential like keratocystic odontogenic tumors), and reconstruction or defect management approach. Documentation should address the potential impact on jaw integrity and function, particularly for lesions approaching a size that might compromise mandibular strength and increase fracture risk.

#### **Code: D7460** – *Removal of benign nonodontogenic cyst or tumor - lesion diameter up to 1.25 cm*
**Use when:** Excising a benign intra-osseous lesion of non-odontogenic origin (not arising from dental developmental tissues) measuring up to 1.25 cm in diameter, with appropriate margins of normal tissue.
**Check:** Documentation should establish the non-odontogenic nature of the lesion, confirm its benign characteristics, and record precise measurement not exceeding 1.25 cm.
**Note:** Non-odontogenic intraosseous lesions include entities such as osteomas, central giant cell granulomas, traumatic bone cysts, and fibro-osseous lesions, among others. The procedural documentation should specify the clinical and radiographic basis for the diagnosis, the surgical approach used, method of complete removal, relationship to adjacent anatomical structures (inferior alveolar nerve, maxillary sinus, etc.), and management of the resulting surgical defect. The pathological specimen handling protocol should be noted, including any special processing instructions for the pathologist based on the suspected diagnosis.

#### **Code: D7461** – *Removal of benign nonodontogenic cyst or tumor - lesion diameter greater than 1.25 cm*
**Use when:** Surgically removing a benign non-odontogenic cyst or tumor larger than 1.25 cm in diameter, including appropriate margins to ensure complete removal and minimize recurrence risk.
**Check:** Documentation must identify the lesion as non-odontogenic in origin, confirm benign characteristics, and record measurements exceeding 1.25 cm in diameter.
**Note:** Larger non-odontogenic lesions may present significant surgical challenges depending on their location and relationship to vital structures. The operative report should comprehensively document the preoperative assessment including advanced imaging when appropriate, surgical approach for access, extent of bone removal, preservation strategies for adjacent structures, complete removal verification method, and reconstruction or defect management plan. For lesions with particular biological behaviors (such as central giant cell granulomas with aggressive features), the documentation should address the specific surgical approach designed to minimize recurrence risk and any planned post-operative monitoring protocol.

---

### **Key Takeaways:**
- **Pathology Classification** - Accurate code selection depends on correctly classifying lesions as benign vs. malignant and odontogenic vs. non-odontogenic.
- **Size Determination** - Precise measurement and documentation of the lesion's greatest diameter is critical, with 1.25 cm being the key threshold between code pairs.
- **Margin Documentation** - The extent of normal tissue excised around the lesion should be documented, with wider margins typically required for malignant lesions.
- **Imaging Correlation** - Reference to preoperative imaging studies (radiographs, CT, MRI) that guided the surgical approach strengthens documentation.
- **Specimen Handling** - Documentation should include how the specimen was prepared, oriented, and submitted for pathological examination.
- **Anatomical Relationships** - The lesion's proximity to and effect on adjacent structures (teeth, nerves, sinuses) should be documented.
- **Surgical Approach** - The specific technique used to access and remove the intra-osseous lesion should be detailed.
- **Defect Management** - How the resulting surgical defect was managed (primary closure, packing, grafting) should be documented.
- **Reconstructive Planning** - For larger lesions, documentation of the reconstruction approach (immediate or delayed) is important.
- **Follow-up Protocol** - The planned approach for monitoring healing and assessing for recurrence should be included, particularly for lesions with higher recurrence potential.

Scenario:
"{{scenario}}"

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_excision_intra_osseous_code(self, scenario: str) -> str:
        """Extract excision of intra-osseous lesions code for a given scenario."""
        try:
            print(f"Analyzing excision of intra-osseous lesions scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Excision of intra-osseous lesions extract code result: {code}")
            
            # Return empty string if no code found
            if code == "None" or not code or "not applicable" in code.lower():
                return ""
                
            return code
        except Exception as e:
            print(f"Error in extract_excision_intra_osseous_code: {str(e)}")
            return ""
    
    def activate_excision_intra_osseous(self, scenario: str) -> str:
        """Activate the excision of intra-osseous lesions analysis process and return results."""
        try:
            return self.extract_excision_intra_osseous_code(scenario)
        except Exception as e:
            print(f"Error in activate_excision_intra_osseous: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_excision_intra_osseous(scenario)
        print(f"\n=== EXCISION OF INTRA-OSSEOUS LESIONS ANALYSIS RESULT ===")
        print(f"EXCISION OF INTRA-OSSEOUS LESIONS CODE: {result if result else 'None'}")


excision_intra_osseous_service = ExcisionIntraOsseousServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter an excision of intra-osseous lesions scenario: ")
    excision_intra_osseous_service.run_analysis(scenario) 