"""
Module for extracting other removable prosthetic services codes.
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
 
def create_other_removable_prosthetic_services_extractor(temperature=0.0):
    """
    Create a LangChain-based other removable prosthetic services code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert 
### **Before picking a code, ask:**
- What was the primary reason the patient came in?
- Is the procedure necessary due to wear, damage, or patient discomfort?
- Is this a complete or partial denture?
- Is the denture maxillary or mandibular?
- Does the patient require additional modifications or attachments?

## **Other Removable Prosthetic Services Codes**

### **Code: D5765**  
**Use when:** A soft liner is placed in a complete or partial removable denture using an indirect technique.  
**Check:** Ensure that the patient has soft tissue irritation or conditions that necessitate a cushioning liner.  
**Note:** This is not for direct chairside applications; it requires lab processing.

---

### **Code: D5850**  
**Use when:** The patient requires maxillary tissue conditioning to aid in ridge healing before definitive prosthetic treatment.  
**Check:** Assess the condition of the tissue and determine if a temporary liner is needed.  
**Note:** This treatment helps prepare the soft tissues for improved final denture fit.

---

### **Code: D5851**  
**Use when:** The patient requires mandibular tissue conditioning before final prosthetic placement.  
**Check:** Ensure unhealthy ridges are being treated and that conditioning materials are properly placed.  
**Note:** Follow-up evaluations may be required to monitor tissue response.

---

### **Code: D5862**  
**Use when:** A precision attachment is required as part of the prosthetic design.  
**Check:** Identify the type of attachment used and ensure proper function.  
**Note:** This code covers each pair of components used; a detailed report may be necessary.

---

### **Code: D5863**  
**Use when:** The patient requires a complete maxillary overdenture supported by implants or retained natural teeth.  
**Check:** Ensure proper stability and function with underlying support structures.  
**Note:** Overdentures provide better retention than conventional dentures but require maintenance.

---

### **Code: D5864**  
**Use when:** The patient requires a partial maxillary overdenture.  
**Check:** Confirm the presence of suitable abutments or implants for overdenture retention.  
**Note:** This option improves stability while preserving natural teeth.

---

### **Code: D5865**  
**Use when:** A complete mandibular overdenture is needed.  
**Check:** Assess occlusion and attachment function to ensure optimal fit.  
**Note:** Overdentures help in preventing bone loss and enhancing prosthetic function.

---

### **Code: D5866**  
**Use when:** The patient requires a partial mandibular overdenture.  
**Check:** Ensure the prosthesis is supported by remaining natural teeth or implant attachments.  
**Note:** This is an alternative to conventional partial dentures with improved stability.

---

### **Code: D5867**  
**Use when:** A replaceable part of a semi-precision or precision attachment needs to be replaced.  
**Check:** Identify the specific attachment component being replaced.  
**Note:** This applies per attachment and may require manufacturer-specific components.

---

### **Code: D5875**  
**Use when:** The patient has an existing removable prosthesis that requires modification after implant surgery.  
**Check:** Ensure that necessary modifications are made to accommodate implants.  
**Note:** Attachment assemblies should be billed separately.

---

### **Code: D5876**  
**Use when:** The patient requires the addition of a metal substructure to an acrylic full denture per arch.  
**Check:** Ensure the structural reinforcement is necessary for durability.  
**Note:** This can enhance strength and longevity for patients with heavy occlusal forces.

---

### **Code: D5899**  
**Use when:** A removable prosthodontic procedure is performed that does not have a specific CDT code.  
**Check:** Provide a detailed report of the procedure performed.  
**Note:** Used for unique or complex cases requiring additional documentation.

---

### **Key Takeaways:**
- **Customization:** Many of these procedures are tailored based on patient-specific needs.  
- **Attachment Types:** Precision and semi-precision attachments must be clearly documented.  
- **Healing Considerations:** Tissue conditioning and soft liners may be required before definitive prosthesis placement.  
- **Overdenture Benefits:** Overdentures provide enhanced retention and preserve natural structures when possible.  
- **Documentation:** Detailed reporting is necessary for procedures that lack specific CDT codes.



Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_other_removable_prosthetic_services_code(scenario, temperature=0.0):
    """
    Extract other removable prosthetic services code(s) for a given scenario.
    """
    try:
        chain = create_other_removable_prosthetic_services_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Other removable prosthetic services code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_other_removable_prosthetic_services_code: {str(e)}")
        return ""

def activate_other_removable_prosthetic_services(scenario):
    """
    Activate other removable prosthetic services analysis and return results.
    """
    try:
        return extract_other_removable_prosthetic_services_code(scenario)
    except Exception as e:
        print(f"Error in activate_other_removable_prosthetic_services: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient needs a soft liner for their full upper denture which will be processed in the lab."
    result = activate_other_removable_prosthetic_services(scenario)
    print(result) 