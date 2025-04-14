"""
Module for extracting repairs to complete dentures codes.
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
 
def create_repairs_to_complete_dentures_extractor(temperature=0.0):
    """
    Create a LangChain-based repairs to complete dentures code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert

## Prosthodontics, Removable - Repairs to Complete Dentures

### **Before picking a code, ask:**
- What was the primary reason the patient came in?
- Is this a repair to an existing denture or a replacement of a broken/missing component?
- Does the patient need an immediate fix, or will further adjustments be required?
- Has the patient experienced frequent breakage, indicating a need for a stronger material or alternative approach?

---

### **D5511 - Repair Broken Complete Denture Base, Mandibular**
**Use when:** The mandibular (lower) complete denture base is fractured and requires repair.
**Check:** Assess the extent of the damage and determine if repair is feasible. Ensure proper bonding of repair material.
**Notes:** Not to be used for a full denture replacement. Structural reinforcement may be needed for recurrent fractures.

---

### **D5512 - Repair Broken Complete Denture Base, Maxillary**
**Use when:** The maxillary (upper) complete denture base is fractured and requires repair.
**Check:** Evaluate the fit post-repair to ensure proper occlusion and comfort.
**Notes:** Similar to D5511, but specific to the upper arch. Ensure patient follows appropriate care to prevent future fractures.

---

### **D5520 - Replace Missing or Broken Teeth — Complete Denture (Each Tooth)**
**Use when:** One or more teeth on a complete denture have broken or fallen off and need replacement.
**Check:** Verify the correct shade and size for replacement teeth. Ensure proper alignment and occlusion.
**Notes:** This code applies per missing or broken tooth. If multiple teeth need replacement, consider alternative treatment options.

---

### **Key Takeaways:**
- **Assess Damage Extent:** Minor cracks can often be repaired, but extensive fractures may require new dentures.
- **Material Considerations:** Some repairs may require stronger materials or reinforcement to prevent recurrent damage.
- **Patient Compliance:** Educate patients on proper denture care to minimize future breakage.
- **Check Fit Post-Repair:** Always verify that repaired dentures fit properly to avoid irritation or occlusal issues.



Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_repairs_to_complete_dentures_code(scenario, temperature=0.0):
    """
    Extract repairs to complete dentures code(s) for a given scenario.
    """
    try:
        chain = create_repairs_to_complete_dentures_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Repairs to complete dentures code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_repairs_to_complete_dentures_code: {str(e)}")
        return ""

def activate_repairs_to_complete_dentures(scenario):
    """
    Activate repairs to complete dentures analysis and return results.
    """
    try:
        return extract_repairs_to_complete_dentures_code(scenario)
    except Exception as e:
        print(f"Error in activate_repairs_to_complete_dentures: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient dropped their lower complete denture and it fractured in half. They need it repaired as soon as possible."
    result = activate_repairs_to_complete_dentures(scenario)
    print(result) 