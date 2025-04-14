"""
Module for extracting interim prosthesis codes.
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
 
def create_interim_prosthesis_extractor(temperature=0.0):
    """
    Create a LangChain-based interim prosthesis code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert
### **Before picking a code, ask:**
- What was the primary reason the patient came in?
- Is the interim prosthesis needed for healing, aesthetics, or function?
- Is this a complete or partial denture?
- Is the denture maxillary or mandibular?
- Will the patient require a definitive prosthesis later?

#### Code: D5810  
**Heading:** Interim complete denture (maxillary)  
**When to Use:**  
- The patient requires a **temporary full upper denture** during the healing phase after extractions or surgery.  
- Planned use is **prior to delivery of a final maxillary complete denture**.  
- Useful when immediate esthetics, function, or tissue conditioning is needed before definitive treatment.  
**What to Check:**  
- Ensure the denture is truly **interim**, not final.  
- Verify extractions or surgeries have recently occurred or are planned.  
- Check the patient’s healing progress and estimated timeline for final prosthesis.  
- Document the treatment plan including final prosthesis intent.  
**Notes:**  
- This is typically **not covered** as a “final prosthesis” by insurance — emphasize it is **transitional**.  
- May require a narrative stating the **reason for interim use** (e.g., surgical healing, bone remodeling).  
- Final denture fabrication should be coded separately (e.g., D5110).

---

#### Code: D5811  
**Heading:** Interim complete denture (mandibular)  
**When to Use:**  
- The patient needs a **temporary full lower denture** for use during the healing phase before receiving a definitive mandibular prosthesis.  
- Often used after full arch extractions or for tissue conditioning.  
**What to Check:**  
- Confirm the denture is **not the final prosthesis**.  
- Ensure a treatment plan exists for a final denture (e.g., D5120).  
- Evaluate healing needs or surgical conditions (e.g., bone grafting, implant planning).  
**Notes:**  
- This interim code helps with function and esthetics **during soft tissue or bony healing**.  
- A clear **transition plan to a permanent solution** should be documented.  
- Like D5810, insurance may request a narrative or deny duplicate prosthesis codes.

---

#### Code: D5820  
**Heading:** Interim partial denture (maxillary)  
**When to Use:**  
- Use when the patient needs a **temporary upper partial denture** to replace missing teeth during the healing phase.  
- Often used post-extraction, post-trauma, or during implant healing to maintain function/esthetics.  
**What to Check:**  
- Confirm it is **interim** and not definitive (D5213 is the definitive counterpart).  
- Verify extractions, implants, or ridge healing is part of the overall treatment plan.  
- Evaluate the need for immediate replacement of anterior teeth for appearance/social function.  
**Notes:**  
- Insurance plans often **limit coverage** to one prosthesis every 5+ years—narrative needed for interim approval.  
- Useful for temporary occlusal support, esthetics, or space maintenance during complex treatment.

---

#### Code: D5821  
**Heading:** Interim partial denture (mandibular)  
**When to Use:**  
- Applied when the patient requires a **temporary lower partial denture** during a healing or transition phase.  
- Common in cases of recent extractions, trauma, or implant preparation.  
**What to Check:**  
- Ensure the patient is **not receiving a final prosthesis** yet.  
- Confirm that tooth/arch condition is in transition (e.g., bone graft healing, socket healing, etc.).  
- Identify and document which teeth are being temporarily replaced.  
**Notes:**  
- This is **not a definitive partial denture**—plan and document for final prosthetic restoration.  
- Reimbursement may require documentation showing why the patient can’t receive final treatment immediately.
### **Key Takeaways:**
- **Temporary Solution:** Interim prostheses are not meant for long-term use but aid in function, aesthetics, and healing.  
- **Patient Education:** Clearly explain that adjustments may be required as the tissues heal.  
- **Retention & Stability:** Check for proper retention and occlusion to minimize patient discomfort.  
- **Transition to Definitive Prosthesis:** Ensure a plan is in place for the final prosthetic solution once healing is complete.  


Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_interim_prosthesis_code(scenario, temperature=0.0):
    """
    Extract interim prosthesis code(s) for a given scenario.
    """
    try:
        chain = create_interim_prosthesis_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Interim prosthesis code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_interim_prosthesis_code: {str(e)}")
        return ""

def activate_interim_prosthesis(scenario):
    """
    Activate interim prosthesis analysis and return results.
    """
    try:
        return extract_interim_prosthesis_code(scenario)
    except Exception as e:
        print(f"Error in activate_interim_prosthesis: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient needs a temporary upper partial denture while implants are healing for a fixed prosthesis."
    result = activate_interim_prosthesis(scenario)
    print(result) 