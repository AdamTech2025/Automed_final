"""
Module for extracting adjustments to dentures codes.
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
 
def create_adjustments_to_dentures_extractor(temperature=0.0):
    """
    Create a LangChain-based adjustments to dentures code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert

## Prosthodontics, Removable - Adjustments to Dentures

### **Before picking a code, ask:**
- What was the primary reason the patient came in?
- Is this a new denture or an existing one needing adjustments?
- What specific issue is the patient experiencing (fit, function, breakage)?
- Is the adjustment related to occlusion, pressure sores, or retention issues?
- Does the denture require repair, replacement of components, or a complete remake?

---

### **D5410 - Adjust Complete Denture (Maxillary)**
**Use when:** A maxillary complete denture requires adjustment for fit, occlusion, or patient comfort.
**Check:** Look for pressure points, overextensions, and occlusal discrepancies.
**Notes:** Often needed after initial denture placement or due to tissue changes. Minor adjustments can greatly improve comfort and function.

---

### **D5411 - Adjust Complete Denture (Mandibular)**
**Use when:** A mandibular complete denture requires adjustment.
**Check:** Evaluate for areas of irritation, overextensions, or improper occlusion.
**Notes:** Mandibular dentures often require more frequent adjustments due to lower stability compared to maxillary dentures.

---

### **D5421 - Adjust Partial Denture (Maxillary)**
**Use when:** A maxillary partial denture needs minor adjustments for comfort or function.
**Check:** Inspect clasps, rests, and base extensions for proper fit.
**Notes:** Adjustments may involve relieving pressure points, improving retention, or modifying occlusion.

---

### **D5422 - Adjust Partial Denture (Mandibular)**
**Use when:** A mandibular partial denture requires fit or occlusal adjustments.
**Check:** Ensure clasps are not causing irritation, and check occlusion.
**Notes:** Adjustments may be necessary if the patient experiences discomfort due to shifting or pressure points.

---

### **D5511 - Repair Broken Complete Denture Base (Mandibular)**
**Use when:** A mandibular complete denture has a fractured base that needs repair.
**Check:** Confirm the extent of the damage and whether repair is feasible.
**Notes:** Repairs should restore function without compromising denture integrity. Consider relining if structural support is weakened.

---

### **D5512 - Repair Broken Complete Denture Base (Maxillary)**
**Use when:** A maxillary complete denture has a broken base that needs repair.
**Check:** Assess whether the breakage is due to poor fit, stress points, or patient mishandling.
**Notes:** If repeated breakages occur, a new denture may be needed rather than continued repairs.

---

### **D5520 - Replace Missing or Broken Teeth (Complete Denture, Each Tooth)**
**Use when:** One or more teeth on a complete denture are missing or fractured and need replacement.
**Check:** Ensure proper occlusion and fit after replacement.
**Notes:** If multiple teeth are missing or recurrent fractures occur, a new denture or reinforcement may be required.

---

### **Key Takeaways:**
- **Adjustments vs. Repairs:** Adjustments focus on fit and comfort, while repairs restore function after damage.
- **Denture Base vs. Teeth:** Repairing the base (D5511, D5512) differs from replacing teeth (D5520), which should be coded separately.
- **Assessment is Crucial:** Always determine the underlying cause of discomfort or breakage to provide long-term solutions.
- **Patient Education:** Educate patients on proper care and handling to minimize future issues.


Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_adjustments_to_dentures_code(scenario, temperature=0.0):
    """
    Extract adjustments to dentures code(s) for a given scenario.
    """
    try:
        chain = create_adjustments_to_dentures_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Adjustments to dentures code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_adjustments_to_dentures_code: {str(e)}")
        return ""

def activate_adjustments_to_dentures(scenario):
    """
    Activate adjustments to dentures analysis and return results.
    """
    try:
        return extract_adjustments_to_dentures_code(scenario)
    except Exception as e:
        print(f"Error in activate_adjustments_to_dentures: {str(e)}")
        return ""

# # Example usage
# if __name__ == "__main__":
#     scenario = "Patient has developed a sore spot on the upper ridge from their complete maxillary denture and needs an adjustment."
#     result = activate_adjustments_to_dentures(scenario)
#     print(result) 