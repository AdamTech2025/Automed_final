"""
Module for extracting alveoloplasty-related procedure codes.
"""

import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from llm_services import LLMService, get_service, set_model, set_temperature

# Load environment variables
load_dotenv()

class AlveoloplastyServices:
    """Class to analyze and extract alveoloplasty-related codes based on dental scenarios."""
    
    def __init__(self, llm_service: LLMService = None):
        """Initialize with an optional LLMService instance."""
        self.llm_service = llm_service or get_service()
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create the prompt template for analyzing alveoloplasty scenarios."""
        from subtopics.prompt.prompt import PROMPT
        return PromptTemplate(
            template=f"""
You are a dental coding expert specializing in oral and maxillofacial surgery.

## **Alveoloplasty Procedures**

### **Before picking a code, ask:**
- Is the alveoloplasty being performed in conjunction with extractions or in a separate surgical session?
- How many teeth or tooth spaces are involved in the quadrant where alveoloplasty is performed?
- Is this preparation for a prosthesis (denture, partial, implant-supported restoration)?
- Which specific quadrant(s) of the mouth are involved in the alveoloplasty procedure?
- Has the surgical site already healed from previous extractions, or are extractions being performed at the same visit?
- Is the bone recontouring necessary for proper prosthesis fit, or is it being done for other therapeutic reasons?
- Is documentation clear about the distinction between the extraction procedure and the separate alveoloplasty procedure?

---

#### **Code: D7310** – *Alveoloplasty in conjunction with extractions - four or more teeth or tooth spaces, per quadrant*
**Use when:** Performing significant bone recontouring of the alveolar ridge during the same visit as multiple tooth extractions (4+ teeth/spaces) in the same quadrant, typically to prepare the ridge for a prosthesis.
**Check:** Verify that the documentation clearly distinguishes this procedure from the extractions themselves. The alveoloplasty must be substantive enough to constitute a separate billable procedure beyond routine socket shaping.
**Note:** This procedure involves more extensive bone recontouring than what would normally occur with standard extractions. It typically includes removing sharp bone edges, reducing prominent ridges, and creating a smooth contour to accommodate a future prosthesis. The clinical notes should explicitly document why the additional surgical manipulation was necessary beyond routine care of the extraction site.

#### **Code: D7311** – *Alveoloplasty in conjunction with extractions - one to three teeth or tooth spaces, per quadrant*
**Use when:** Performing alveolar ridge recontouring during the same visit as extraction of 1-3 teeth or tooth spaces in a quadrant, usually in preparation for a prosthesis.
**Check:** Documentation must demonstrate that the bone recontouring was significantly more extensive than routine socket management included in extraction codes.
**Note:** This procedure is often necessary when extracting only a few teeth but significant bone irregularities need addressing before prosthesis placement. Despite fewer teeth being involved, the complexity of the recontouring may still warrant this separate procedure code. Insurers often scrutinize this code when used with minimal extractions, so documentation of medical necessity is crucial.

#### **Code: D7320** – *Alveoloplasty not in conjunction with extractions - four or more teeth or tooth spaces, per quadrant*
**Use when:** Performing alveoloplasty in an edentulous or partially edentulous area where healing from previous extractions has already occurred, involving four or more tooth spaces in a quadrant.
**Check:** Ensure that no extractions are performed during the same surgical visit in the quadrant being treated.
**Note:** This code is appropriate when a patient presents with a healed but irregular alveolar ridge that requires surgical modification for prosthesis placement. The procedure is typically more extensive than D7310 since fibrous tissue and denser bone must be removed in a healed ridge. Documentation should detail why the existing ridge morphology is inadequate for prosthetic success.

#### **Code: D7321** – *Alveoloplasty not in conjunction with extractions - one to three teeth or tooth spaces, per quadrant*
**Use when:** Performing alveoloplasty in a healed, edentulous area involving 1-3 tooth spaces where extractions were previously performed, usually to remove irregularities preventing proper prosthesis fit.
**Check:** Confirm that the surgical site has already healed from any previous extractions and no new extractions are being performed during this visit in the quadrant being treated.
**Note:** This procedure is commonly required when localized ridge defects prevent proper prosthesis fabrication or cause patient discomfort with an existing prosthesis. The limited scope (1-3 spaces) doesn't necessarily indicate a less complex procedure, as localized defects can require precise surgical correction. Documentation should emphasize why the specific area requires surgical modification despite its limited extent.

---

### **Key Takeaways:**
- **Extraction Relationship** - The primary distinction is whether the alveoloplasty is performed in conjunction with extractions (D7310, D7311) or as a separate procedure (D7320, D7321).
- **Quadrant Specificity** - Codes are applied per quadrant, and each quadrant should be reported separately.
- **Tooth Count Matters** - The number of teeth or tooth spaces involved determines which code to use (1-3 teeth vs. 4+ teeth).
- **Surgical Nature Required** - Documentation must clearly indicate surgical recontouring beyond what would normally occur during routine extractions.
- **Purpose Documentation** - The purpose of the alveoloplasty (typically to prepare for a prosthesis) should be clearly documented.
- **Technical Details** - Documentation should include the extent of the ridge that was recontoured and the surgical techniques employed.
- **Different Day Distinction** - Alveoloplasty performed on a different day than extractions would be coded using the "not in conjunction" codes even if extractions were previously performed in the same area.
- **Benefit Limitations** - Many plans consider alveoloplasty in conjunction with extractions to be part of the extraction procedure unless there is clear documentation of significant additional surgical recontouring.
- **Anatomical Specificity** - Documentation should clearly identify the quadrant(s) where the alveoloplasty was performed.
- **Pre/Post Documentation** - Pre-operative and post-operative documentation, including radiographic evidence when available, strengthens the justification for these codes.

Scenario:
"{{scenario}}"

{PROMPT}
""",
            input_variables=["scenario"]
        )
    
    def extract_alveoloplasty_code(self, scenario: str) -> str:
        """Extract alveoloplasty code for a given scenario."""
        try:
            print(f"Analyzing alveoloplasty scenario: {scenario[:100]}...")
            result = self.llm_service.invoke_chain(self.prompt_template, {"scenario": scenario})
            code = result.strip()
            print(f"Alveoloplasty extract code result: {code}")
            
            # Return empty string if no code found
            if code == "None" or not code or "not applicable" in code.lower():
                return ""
                
            return code
        except Exception as e:
            print(f"Error in extract_alveoloplasty_code: {str(e)}")
            return ""
    
    def activate_alveoloplasty(self, scenario: str) -> str:
        """Activate the alveoloplasty analysis process and return results."""
        try:
            return self.extract_alveoloplasty_code(scenario)
        except Exception as e:
            print(f"Error in activate_alveoloplasty: {str(e)}")
            return ""
    
    def run_analysis(self, scenario: str) -> None:
        """Run the analysis and print results."""
        print(f"Using model: {self.llm_service.model} with temperature: {self.llm_service.temperature}")
        result = self.activate_alveoloplasty(scenario)
        print(f"\n=== ALVEOLOPLASTY ANALYSIS RESULT ===")
        print(f"ALVEOLOPLASTY CODE: {result if result else 'None'}")


alveoloplasty_service = AlveoloplastyServices()
# Example usage
if __name__ == "__main__":
    scenario = input("Enter an alveoloplasty scenario: ")
    alveoloplasty_service.run_analysis(scenario) 