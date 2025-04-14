"""
Module for extracting alveoloplasty codes.
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
 
def activate_alveoloplasty(scenario):
    """
    Analyze a dental scenario to determine alveoloplasty code.
    
    Args:
        scenario (str): The dental scenario to analyze.
        
    Returns:
        str: The identified alveoloplasty code or empty string if none found.
    """
    try:
        llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=0.0)        
        template = f"""
You are a dental coding expert specializing in oral surgery procedures,

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
- **Procedure vs. Extraction Distinction** - Alveoloplasty must be a distinct surgical procedure from routine extractions, with separate documentation justifying the additional surgical manipulation beyond what would normally occur during extractions.
- **Timing Matters** - The "in conjunction with extractions" codes (D7310, D7311) are used when extractions are performed at the same visit, while "not in conjunction" codes (D7320, D7321) apply to surgical modification of already-healed ridges.
- **Tooth Count is Per Quadrant** - The distinction between codes is based on the number of teeth or tooth spaces in the specific quadrant being treated, not the total number in the mouth.
- **Prosthetic Purpose** - Most alveoloplasties are performed to facilitate prosthesis placement, and this purpose should be clearly documented in the patient record.
- **Medical Necessity** - Documentation must establish why the existing or anticipated ridge form would be inadequate without surgical modification.
- **One Code Per Quadrant** - When performing alveoloplasty in multiple quadrants, each quadrant should be coded separately with the appropriate code.
- **Documentation Specificity** - Detail the extent of bone removal, the recontouring technique, and the specific anatomical landmarks addressed.
- **Radiographic Evidence** - Pre and post-operative radiographs are valuable for justifying the necessity of the procedure, especially for insurance submissions.

Scenario:
"{{scenario}}"

{PROMPT}
"""
        
        prompt = PromptTemplate(template=template, input_variables=["scenario"])
        chain = LLMChain(llm=llm, prompt=prompt)
        
        result = invoke_chain(chain, {"scenario": scenario}).strip()
        
        # Return empty string if no code found
        if result == "None" or not result or "not applicable" in result.lower():
            return ""
            
        return result
    except Exception as e:
        print(f"Error in activate_alveoloplasty: {str(e)}")
        return "" 