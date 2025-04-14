"""
Module for extracting denture rebase procedures codes.
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
 
def create_denture_rebase_procedures_extractor(temperature=0.0):
    """
    Create a LangChain-based denture rebase procedures code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert

C
## Prosthodontics, Removable - Denture Rebase Procedures

### **Before picking a code, ask:**
- What was the primary reason the patient came in?
- Is the existing denture causing discomfort, poor fit, or instability?
- Is this a routine maintenance procedure or due to significant wear or damage?
- Does the patient require a full denture or partial denture rebase?
- Is the denture hybrid, requiring special base material replacement?

---

### **D5710 - Rebase Complete Maxillary Denture**
**Use when:** The base of a complete maxillary denture requires replacement while retaining the existing denture teeth.
**Check:** Ensure that the teeth are in good condition and can be retained.
**Notes:** This procedure is done when the base material has deteriorated, causing poor fit or irritation.

---

### **D5711 - Rebase Complete Mandibular Denture**
**Use when:** The patient needs a new base for their complete mandibular denture.
**Check:** Confirm stability and occlusion; evaluate the condition of remaining alveolar ridges.
**Notes:** Necessary when the base material is compromised due to resorption or wear, leading to instability.

---

### **D5720 - Rebase Maxillary Partial Denture**
**Use when:** The acrylic base of a maxillary partial denture requires full replacement.
**Check:** Assess framework and teeth to ensure they can be retained.
**Notes:** Often needed due to long-term wear or significant adaptation changes in the oral tissues.

---

### **D5721 - Rebase Mandibular Partial Denture**
**Use when:** The patient needs a new base for their mandibular partial denture while keeping existing teeth and framework.
**Check:** Ensure proper adaptation of the new base to the remaining structures.
**Notes:** Essential when the existing base has lost integrity, affecting retention and stability.

---

### **D5725 - Rebase Hybrid Prosthesis**
**Use when:** The base material of a hybrid prosthesis (implant-supported denture) needs replacement.
**Check:** Evaluate implant stability and ensure framework compatibility with new base material.
**Notes:** This procedure is used when the original base material deteriorates, leading to fit issues or patient discomfort.

---

### **Key Takeaways:**
- **Rebasing replaces the entire denture base while retaining existing teeth.**
- **Use when denture fit is compromised due to material degradation, tissue changes, or resorption.**
- **Ensure the teeth and framework are stable and functional before rebasing.**
- **Rebasing differs from relining, which only adds material to the existing base rather than replacing it.**
- **Hybrid prosthesis rebasing involves implant-supported restorations, requiring careful assessment.**




Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_denture_rebase_procedures_code(scenario, temperature=0.0):
    """
    Extract denture rebase procedures code(s) for a given scenario.
    """
    try:
        chain = create_denture_rebase_procedures_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Denture rebase procedures code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_denture_rebase_procedures_code: {str(e)}")
        return ""

def activate_denture_rebase_procedures(scenario):
    """
    Activate denture rebase procedures analysis and return results.
    """
    try:
        return extract_denture_rebase_procedures_code(scenario)
    except Exception as e:
        print(f"Error in activate_denture_rebase_procedures: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient's upper complete denture needs a complete rebase due to significant ridge resorption over the past year."
    result = activate_denture_rebase_procedures(scenario)
    print(result) 