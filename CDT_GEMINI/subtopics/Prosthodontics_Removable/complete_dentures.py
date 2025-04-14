"""
Module for extracting complete dentures codes.
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
 
def create_complete_dentures_extractor(temperature=0.0):
    """
    Create a LangChain-based complete dentures code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert

## Prosthodontics, Removable - Complete Dentures & Routine Post-Delivery Care

### **Before picking a code, ask:**
- What was the primary reason the patient came in?
- Is this an initial placement or a follow-up?
- Does the code cover future procedures like rebasing or relining?
- Is the patient receiving the denture immediately after extractions or after healing?
- Are there any complicating factors such as residual ridge resorption or anatomical challenges?

---

### **Code: D5110 - Complete Denture (Maxillary)**
**Use when:** The patient is receiving a complete maxillary denture for the first time.
**Check:** Ensure the treatment includes a full upper denture covering the maxillary arch.
**Notes:** This code includes the fabrication and placement of the denture, but does not cover additional procedures like relining or rebasing later. Patient expectations regarding fit, comfort, and adjustment period should be managed.

---

### **Code: D5120 - Complete Denture (Mandibular)**
**Use when:** The patient is receiving a complete mandibular denture for the first time.
**Check:** Verify that the denture is a full prosthesis for the lower arch.
**Notes:** Covers the creation and fitting of the denture but does not include future modifications such as relining or rebasing. Mandibular dentures often require additional considerations due to lower ridge resorption and stability concerns.

---

### **Code: D5130 - Immediate Denture (Maxillary)**
**Use when:** The patient is receiving an immediate maxillary denture following extractions.
**Check:** Ensure the denture is placed immediately after extractions for proper healing support.
**Notes:** Includes limited follow-up care but **does not** cover future rebasing or relining procedures. Immediate dentures may require significant adjustments as healing progresses and should be relined or replaced within a few months.

---

### **Code: D5140 - Immediate Denture (Mandibular)**
**Use when:** The patient is receiving an immediate mandibular denture following extractions.
**Check:** Verify that the denture is placed right after the removal of teeth.
**Notes:** Includes limited follow-up care but **does not** include future rebasing or relining. Patients should be advised that healing may cause changes in fit and function, requiring additional procedures later.

---

### **Additional Considerations for Denture Patients:**
- **Adjustment Period:** Patients need time to adapt to new dentures, and multiple adjustments may be required.
- **Occlusion and Fit:** Proper occlusion must be assessed to avoid discomfort and TMJ issues.
- **Oral Hygiene:** Patients should be instructed on proper cleaning techniques to avoid infections like denture stomatitis.
- **Follow-Up Care:** Regular follow-ups are essential to monitor fit and function, particularly for immediate dentures.
- **Long-Term Maintenance:** Relining or rebasing is often necessary within a few years due to bone resorption.
- **Patient Expectations:** Clear communication about the limitations and adaptation process can improve satisfaction and compliance.

---

### **Key Takeaways:**
- **Complete dentures (D5110, D5120)** are for fully edentulous arches and do not include future adjustments.
- **Immediate dentures (D5130, D5140)** are placed right after extractions and include only **limited** follow-up care.
- **Future modifications like relining/rebasing** require additional codes and are **not** included under these codes.
- **Patient education and realistic expectations** play a crucial role in successful prosthodontic treatment.




Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_complete_dentures_code(scenario, temperature=0.0):
    """
    Extract complete dentures code(s) for a given scenario.
    """
    try:
        chain = create_complete_dentures_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Complete dentures code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_complete_dentures_code: {str(e)}")
        return ""

def activate_complete_dentures(scenario):
    """
    Activate complete dentures analysis and return results.
    """
    try:
        return extract_complete_dentures_code(scenario)
    except Exception as e:
        print(f"Error in activate_complete_dentures: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "65-year-old patient needs a complete maxillary denture after all remaining upper teeth were extracted 3 months ago."
    result = activate_complete_dentures(scenario)
    print(result) 