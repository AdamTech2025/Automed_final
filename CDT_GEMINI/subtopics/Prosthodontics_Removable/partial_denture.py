"""
Module for extracting partial denture codes.
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
 
def create_partial_denture_extractor(temperature=0.0):
    """
    Create a LangChain-based partial denture code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert 

## Prosthodontics, Removable - Partial Denture Routine Delivery Care

### **Before picking a code, ask:**
- What was the primary reason the patient came in?
- Is this an initial placement or a follow-up?
- What type of material is being used (resin, cast metal, flexible base)?
- Is this a standard or immediate partial denture?
- Are there specific anatomical challenges affecting the choice of material?
- Has the patient experienced previous denture failures or discomfort with a particular type?

---

### **D5211 - Maxillary Partial Denture (Resin Base)**
**Use when:** The patient requires a removable maxillary partial denture with a resin base.
**Check:** Ensure proper fit, retention, and clasp placement. Verify occlusion with remaining teeth.
**Notes:** Includes clasps, rests, and teeth. Resin-based dentures may require relining over time due to resorption. Patient education is important for maintenance and longevity.

---

### **D5212 - Mandibular Partial Denture (Resin Base)**
**Use when:** The patient requires a removable mandibular partial denture with a resin base.
**Check:** Confirm that the denture provides adequate support without excessive pressure on soft tissues.
**Notes:** Similar to D5211, resin-based partials may require future adjustments. Regular follow-ups are recommended to assess tissue adaptation and occlusal wear.

---

### **D5213 - Maxillary Partial Denture (Cast Metal Framework with Resin Base)**
**Use when:** A stronger and more durable maxillary partial denture is needed.
**Check:** Ensure appropriate framework design, clasping, and support for stability.
**Notes:** Cast metal frameworks provide better longevity and strength compared to resin-only bases. Less bulky than resin-only dentures, improving comfort and speech.

---

### **D5214 - Mandibular Partial Denture (Cast Metal Framework with Resin Base)**
**Use when:** A mandibular partial denture with additional durability is needed.
**Check:** Evaluate retention and fit to prevent irritation or excess movement.
**Notes:** More rigid than resin-based partials; preferred for long-term wear. Proper oral hygiene is essential to prevent irritation under metal components.

---

### **D5225 - Maxillary Partial Denture (Flexible Base)**
**Use when:** A more flexible and aesthetic option is desired.
**Check:** Ensure flexibility does not compromise support or retention.
**Notes:** May not be as durable as metal frameworks but offers enhanced comfort. Patients with allergy concerns to metal or rigid acrylic may benefit from this option.

---

### **D5226 - Mandibular Partial Denture (Flexible Base)**
**Use when:** A mandibular flexible partial denture is needed.
**Check:** Assess for adequate retention and patient tolerance.
**Notes:** Provides a lightweight, comfortable alternative to metal. More prone to deformation over time and may require earlier replacement.

---

### **D5221 - Immediate Maxillary Partial Denture (Resin Base)**
**Use when:** A maxillary partial denture is placed immediately after extractions.
**Check:** Ensure fit post-extraction; expect adjustments as healing occurs.
**Notes:** Includes limited follow-up care; rebasing or relining not included. Patients should be advised about expected changes in fit as the healing process progresses.

---

### **D5222 - Immediate Mandibular Partial Denture (Resin Base)**
**Use when:** A mandibular partial denture is placed immediately after extractions.
**Check:** Verify adaptation to the healing ridge.
**Notes:** Follow-up care is limited; additional modifications require separate codes. Patients should be educated on soft diet recommendations and possible pressure points.

---

### **D5223 - Immediate Maxillary Partial Denture (Cast Metal Framework with Resin Base)**
**Use when:** An immediate maxillary denture with a cast metal framework is required.
**Check:** Ensure sufficient retention and adjust for post-extraction changes.
**Notes:** Stronger than resin-only immediate dentures but requires follow-ups. Requires precise initial impressions to minimize the need for extensive adjustments.

---

### **D5224 - Immediate Mandibular Partial Denture (Cast Metal Framework with Resin Base)**
**Use when:** An immediate mandibular partial denture with added durability is needed.
**Check:** Assess fit carefully post-extraction.
**Notes:** Like D5223, this provides a long-term solution with minimal follow-up care. Early patient adaptation and speech training may be necessary.

---

### **D5227 - Immediate Maxillary Partial Denture (Flexible Base)**
**Use when:** A flexible immediate denture is preferred.
**Check:** Confirm retention and adaptation as healing progresses.
**Notes:** Provides improved aesthetics and comfort but requires monitoring. Risk of warping over time; may require replacement sooner than other materials.

---

### **D5228 - Immediate Mandibular Partial Denture (Flexible Base)**
**Use when:** A flexible mandibular partial denture is placed immediately after extractions.
**Check:** Ensure occlusion is not disrupted by the flexible nature.
**Notes:** Healing may require future rebasing or relining. Patients may require frequent minor adjustments due to rapid gum tissue changes post-extraction.

---

### **D5282 - Removable Unilateral Partial Denture (One-Piece Cast Metal, Maxillary)**
**Use when:** A single-sided (unilateral) partial denture is needed for the upper arch.
**Check:** Verify retention and stability.
**Notes:** Includes clasps, rests, and teeth in a single-piece design. Ideal for patients with limited edentulous areas but requiring stability.

---

### **D5283 - Removable Unilateral Partial Denture (One-Piece Cast Metal, Mandibular)**
**Use when:** A single-sided mandibular partial denture is required.
**Check:** Assess occlusion and fit.
**Notes:** More durable than resin or flexible alternatives. Provides better longevity but may require adaptation for comfort.

---

### **D5284 - Removable Unilateral Partial Denture (One-Piece Flexible Base, Per Quadrant)**
**Use when:** A single-sided partial denture with a flexible base is needed.
**Check:** Ensure comfort and function in the affected quadrant.
**Notes:** More aesthetic and comfortable than metal but may lack rigidity. Beneficial for patients with tissue sensitivities or concerns about metal restorations.

---

### **D5286 - Removable Unilateral Partial Denture (One-Piece Resin, Per Quadrant)**
**Use when:** A single-sided partial denture with a resin base is required.
**Check:** Fit and retention should be optimized.
**Notes:** A cost-effective alternative to metal or flexible bases. May require reinforcement in cases of significant occlusal forces.

---

### **Key Takeaways:**
- **Material Matters:** Choose resin for cost-effectiveness, metal for durability, and flexible bases for aesthetics and comfort.
- **Immediate vs. Standard:** Immediate dentures require more adjustments but provide post-extraction support.
- **Unilateral vs. Bilateral:** Unilateral dentures are used for single-quadrant edentulism, whereas bilateral options restore larger areas.
- **Future Adjustments:** Most partial dentures will require relining, rebasing, or repairs over time.
- **Patient Education:** Ensure patients understand maintenance, follow-up needs, and expected adaptation challenges.

Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_partial_denture_code(scenario, temperature=0.0):
    """
    Extract partial denture code(s) for a given scenario.
    """
    try:
        chain = create_partial_denture_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Partial denture code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_partial_denture_code: {str(e)}")
        return ""

def activate_partial_denture(scenario):
    """
    Activate partial denture analysis and return results.
    """
    try:
        return extract_partial_denture_code(scenario)
    except Exception as e:
        print(f"Error in activate_partial_denture: {str(e)}")
        return ""

# Example usage
if __name__ == "__main__":
    scenario = "Patient needs a maxillary partial denture with a cast metal framework to replace missing teeth #3, 4, 5, and 12."
    result = activate_partial_denture(scenario)
    print(result) 