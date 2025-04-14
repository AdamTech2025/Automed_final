"""
Module for extracting repairs to partial dentures codes.
"""

import os
import sys
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from llm_services import create_chain, invoke_chain, get_llm_service, set_model_for_file
# Add the project root to the path so we can import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.append(project_root)

from topics.prompt import PROMPT

# Load environment variables
load_dotenv()

# Get model name from environment variable, default to gpt-4o if not set
 
def create_repairs_to_partial_dentures_extractor(temperature=0.0):
    """
    Create a LangChain-based repairs to partial dentures code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert
## Prosthodontics, Removable - Repairs to Partial Dentures

### **Before picking a code, ask:**
- What is the primary issue with the partial denture?
- Is the repair related to the base, framework, clasps, or teeth?
- Will additional components need to be added to restore functionality?
- Does the patient require a temporary or permanent repair solution?

---

### **D5611 - Repair Resin Partial Denture Base (Mandibular)**
**Use when:** The mandibular resin base has fractured and requires repair.
**Check:** Ensure no other components (clasps, teeth) require repair.
**Notes:** Often needed after extended wear or accidental damage. Reinforcement may be necessary for durability.

---

### **D5612 - Repair Resin Partial Denture Base (Maxillary)**
**Use when:** The maxillary resin base has fractured and needs repair.
**Check:** Assess for additional structural weaknesses.
**Notes:** Similar to D5611 but for the upper arch. Proper fit after repair should be confirmed.

---

### **D5621 - Repair Cast Partial Framework (Mandibular)**
**Use when:** A break in the mandibular metal framework requires repair.
**Check:** Ensure no additional damage to clasps or base.
**Notes:** Requires precise adjustment to maintain fit and retention.

---

### **D5622 - Repair Cast Partial Framework (Maxillary)**
**Use when:** The maxillary metal framework has been damaged and requires repair.
**Check:** Ensure framework integrity before completing the repair.
**Notes:** Complex repairs may require new impressions for accuracy.

---

### **D5630 - Repair or Replace Broken Retentive/Clasping Materials (Per Tooth)**
**Use when:** A retentive component or clasp has broken and requires replacement.
**Check:** Confirm that other clasps and framework are intact.
**Notes:** Must match the existing material for compatibility and durability.

---

### **D5640 - Replace Broken Teeth (Per Tooth)**
**Use when:** One or more artificial teeth on a partial denture are broken or missing.
**Check:** Ensure proper occlusion and color match when replacing teeth.
**Notes:** Can be performed on both resin and cast metal frameworks.

---

### **D5650 - Add Tooth to Existing Partial Denture**
**Use when:** A new tooth is added due to an extracted natural tooth.
**Check:** Verify occlusal balance and fit within the existing framework.
**Notes:** Common for patients experiencing progressive tooth loss.

---

### **D5660 - Add Clasp to Existing Partial Denture (Per Tooth)**
**Use when:** A new clasp is required for retention improvement.
**Check:** Ensure the existing framework can support the added clasp.
**Notes:** Often necessary when additional stability is required.

---

### **D5670 - Replace All Teeth and Acrylic on Cast Metal Framework (Maxillary)**
**Use when:** All artificial teeth and acrylic need replacement on an upper partial denture.
**Check:** Assess framework for any damage before replacing components.
**Notes:** Extensive repairs may require new impressions and bite registration.

---

### **D5671 - Replace All Teeth and Acrylic on Cast Metal Framework (Mandibular)**
**Use when:** All artificial teeth and acrylic need to be replaced on a lower partial denture.
**Check:** Ensure the metal framework remains structurally sound.
**Notes:** Similar to D5670 but for the lower arch. Patients should be advised on adaptation to new teeth.

---

### **Key Takeaways:**
- **Material Considerations:** Repairs vary depending on whether the partial denture is resin or metal.
- **Extent of Damage:** Minor repairs may be quick, but extensive damage may require complete remakes.
- **Patient Comfort:** Ensure proper adjustments to prevent discomfort or bite issues.
- **Longevity:** Frequent repairs may indicate the need for a new partial denture over time.
- **Follow-Up:** Patients should return for a check-up to assess repair effectiveness and overall fit.




Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_repairs_to_partial_dentures_code(scenario, temperature=0.0):
    """
    Extract repairs to partial dentures code(s) for a given scenario.
    """
    try:
        chain = create_repairs_to_partial_dentures_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Repairs to partial dentures code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_repairs_to_partial_dentures_code: {str(e)}")
        return ""

def activate_repairs_to_partial_dentures(scenario):
    """
    Activate repairs to partial dentures analysis and return results.
    """
    try:
        return extract_repairs_to_partial_dentures_code(scenario)
    except Exception as e:
        print(f"Error in activate_repairs_to_partial_dentures: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient's maxillary partial denture has a broken clasp on tooth #3 that needs to be replaced."
    result = activate_repairs_to_partial_dentures(scenario)
    print(result) 