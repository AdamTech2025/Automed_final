import os
import sys
from langchain.prompts import PromptTemplate
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file
from subtopics.prompt.prompt import PROMPT



def create_drugs_extractor():
    """
    Creates a LangChain-based extractor for drugs codes.
    """
    template = f"""
    You are a dental coding expert
    
    
### **Before picking a code, ask:** 
- Is the drug being administered via injection (parenteral) or dispensed for home use? 
- Is it a single or multiple administrations of different medications? 
- Is the drug being used for pain control, infection, or inflammation? 
- Is the drug being administered for sedation, anesthesia, or reversal? (If so, do not use these codes.) 
- Is the medication infiltrated for sustained-release pain management? 
 
---
 
### **Detailed Coding Guidelines for Drug Administration & Dispensing** 
 
#### **Code: D9610** – *Therapeutic Parenteral Drug, Single Administration* 
**Use when:** A single administration of a therapeutic drug (antibiotic, steroid, anti-inflammatory, etc.) via injection. 
**Check:** Ensure the drug is not a sedative, anesthetic, or reversal agent. 
**Note:** This applies to in-office drug administration but does not include dispensing for home use. 
 
#### **Code: D9612** – *Therapeutic Parenteral Drugs, Two or More Administrations, Different Medications* 
**Use when:** Two or more different medications are administered via injection in a single visit. 
**Check:** Confirm that multiple distinct drugs (such as an antibiotic and an anti-inflammatory) are used. 
**Note:** This code is used instead of D9610 when multiple drugs are necessary on the same date. 
 
#### **Code: D9613** – *Infiltration of Sustained-Release Therapeutic Drug, Per Quadrant* 
**Use when:** A long-acting pharmacologic agent is infiltrated into the surgical site for prolonged pain relief. 
**Check:** Ensure that this is for sustained-release pain management, not local anesthesia. 
**Note:** Typically used for post-surgical pain control, reducing the need for systemic analgesics. 
 
#### **Code: D9630** – *Drugs or Medicaments Dispensed in the Office for Home Use* 
**Use when:** A dentist provides medications (such as antibiotics, analgesics, or topical fluoride) for patient home use. 
**Check:** Ensure that the medication is dispensed directly in the office and not just prescribed. 
**Note:** Does not apply to written prescriptions—only to physical drugs given to the patient. 
 
---
 
### **Key Takeaways:** 
- **D9610 & D9612** cover in-office parenteral administration, with D9612 used for multiple drugs. 
- **D9613** is specifically for infiltration of a long-acting drug for pain management. 
- **D9630** is used when dispensing medications for home use, not for prescribing. 
- **Proper documentation** should include the drug type, purpose, and administration method. 
 
Correct use of these codes ensures proper billing and compliance when administering or dispensing drugs in a dental setting.

    SCENARIO: {{scenario}}
    
    {PROMPT}
    """
    
    prompt = PromptTemplate(template=template, input_variables=["scenario"])
    return create_chain(prompt)

def extract_drugs_code(scenario):
    """
    Extracts drugs code(s) for a given scenario.
    """
    try:
        extractor = create_drugs_extractor()
        result = invoke_chain(extractor, {"scenario": scenario})
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Error in drugs code extraction: {str(e)}")
        return None

def activate_drugs(scenario):
    """
    Activates the drugs analysis process and returns results.
    """
    try:
        result = extract_drugs_code(scenario)
        return result
    except Exception as e:
        print(f"Error activating drugs analysis: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Print the current Gemini model and temperature being used
    llm_service = get_llm_service()
    print(f"Using Gemini model: {llm_service.gemini_model} with temperature: {llm_service.temperature}")
    
    scenario = "Patient received an in-office injection of antibiotics after a complicated extraction procedure."
    result = activate_drugs(scenario)
    print(result) 