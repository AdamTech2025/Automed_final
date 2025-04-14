"""
Module for extracting open fractures codes.
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
 
def create_open_fractures_extractor(temperature=0.0):
    """
    Create a LangChain-based open fractures code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert specializing in oral and maxillofacial trauma management,

## **Open Fractures Treatment**

### **Before picking a code, ask:**
- Which specific anatomical structure is involved in the fracture (maxilla, mandible, malar, zygomatic arch, alveolus)?
- Is an open or closed reduction technique being used for treatment?
- Are teeth present in the fracture line that require immobilization?
- What type of fixation is being used (internal or external)?
- Is the fracture simple, comminuted, or complex?
- Are multiple surgical approaches required for adequate reduction and fixation?
- Does the fracture involve facial bones requiring special consideration?
- What imaging was used to characterize the fracture before treatment?
- Are there any neurovascular considerations in the fracture management?
- What is the plan for post-operative stabilization and monitoring?

---

#### D7710 - Maxilla - Open Reduction  
**When to Use:** Apply this code for open reduction of a maxillary open fracture, where an incision is required to access and reduce the fracture.  
**What to Check:** Confirm the fracture is open (exposed to the mouth or externally) and verify the use of an incision for reduction.  
**Notes:** This code is specific to surgical intervention; if no incision is made, use D7720. Documentation should specify the fracture's exposure and surgical approach.  

#### D7720 - Maxilla - Closed Reduction  
**When to Use:** Use for closed reduction of a maxillary open fracture, where no incision is needed to reduce the fracture.  
**What to Check:** Ensure the fracture is open but treated non-surgically, without an incision.  
**Notes:** If an incision is required, switch to D7710. This code reflects a less invasive approach despite the open fracture classification.  

#### D7730 - Mandible - Open Reduction  
**When to Use:** Select this code for open reduction of a mandibular open fracture, requiring an incision to reduce the fracture.  
**What to Check:** Verify the fracture's exposure (to the mouth or externally) and confirm the use of an incision for reduction.  
**Notes:** Distinct from D7740 (closed reduction). Documentation must detail the surgical method and fracture characteristics.  

#### D7740 - Mandible - Closed Reduction  
**When to Use:** Apply when treating a mandibular open fracture with closed reduction, without an incision.  
**What to Check:** Confirm the fracture is open but managed non-surgically, with no incision involved.  
**Notes:** Use D7730 if an incision is made. This code focuses on a simpler reduction method for an open fracture.  

#### D7750 - Malar and/or Zygomatic Arch - Open Reduction  
**When to Use:** Use this code for open reduction of an open fracture in the malar (cheekbone) or zygomatic arch, requiring an incision.  
**What to Check:** Ensure the fracture is open and verify that an incision was made to reduce it in the malar or zygomatic region.  
**Notes:** Teeth are not typically involved. Documentation should highlight the surgical approach and fracture exposure.  

#### D7760 - Malar and/or Zygomatic Arch - Closed Reduction  
**When to Use:** Select for closed reduction of an open fracture in the malar or zygomatic arch, where no incision is required.  
**What to Check:** Confirm the fracture is open but treated non-surgically, without an incision.  
**Notes:** If an incision is used, switch to D7750. This code emphasizes a non-invasive reduction for an open fracture.  

#### D7770 - Alveolus - Open Reduction Stabilization of Teeth  
**When to Use:** Apply this code for open reduction of an alveolar open fracture, requiring an incision, with stabilization of teeth.  
**What to Check:** Verify the fracture is exposed (to the mouth or externally), an incision is made, and teeth are stabilized (e.g., wiring, banding, splinting).  
**Notes:** This differs from D7771 due to the surgical approach. Documentation must support tooth stabilization and the open fracture's nature.  

#### D7771 - Alveolus - Closed Reduction Stabilization of Teeth  
**When to Use:** Use for closed reduction of an alveolar open fracture, with stabilization of teeth, without an incision.  
**What to Check:** Confirm the fracture is open (exposed to the mouth or externally) and teeth are stabilized, with no incision required.  
**Notes:** If an incision is involved, use D7770. Focus is on non-surgical reduction with tooth stabilization as needed.  

#### D7780 - Facial Bones - Complicated Reduction with Fixation and Multiple Approaches  
**When to Use:** Select this code for complex open fractures of facial bones (e.g., jaws, cheeks, orbital bones) requiring complicated reduction, fixation, and multiple surgical approaches.  
**What to Check:** Verify involvement of multiple facial bones, the need for extensive fixation, and the use of multiple incisions or approaches for an open fracture.  
**Notes:** This code is for highly complex cases. Detailed narrative documentation is essential to justify the procedure's scope and complexity.  


---

### **Key Takeaways:**
- **Open vs. Closed Technique** - The primary distinction between code pairs is whether direct surgical exposure of the fracture site was performed (open) or whether treatment was accomplished without visualizing the fracture line (closed).
- **Anatomical Specificity** - Proper code selection requires identifying the exact anatomical structure(s) involved (maxilla, mandible, malar, zygomatic arch, alveolus).
- **Tooth Involvement** - When teeth are present in the fracture line, documentation should address their management and role in stabilization.
- **Fixation Method** - The type of fixation used (plates, screws, wires, arch bars, intermaxillary fixation) should be specifically documented.
- **Occlusal Verification** - For fractures affecting tooth-bearing areas, documentation should confirm restoration of proper occlusal relationships.
- **Multiple Approaches** - For code D7680, documentation must support the need for multiple surgical approaches to address the complex fracture pattern.
- **Radiographic Correlation** - References to pre- and post-operative imaging that guided treatment and confirmed reduction strengthen documentation.
- **Functional Assessment** - Post-reduction evaluation of function (occlusion, mandibular movement, sensation) should be included in documentation.
- **Healing Plan** - Documentation should address the stabilization period, follow-up protocol, and plan for hardware or fixation removal.
- **Complication Management** - For complex cases, documentation should address potential complications and monitoring strategy.

Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_open_fractures_code(scenario, temperature=0.0):
    """
    Extract open fractures code(s) for a given scenario.
    """
    try:
        chain = create_open_fractures_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Open fractures code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_open_fractures_code: {str(e)}")
        return ""

def activate_open_fractures(scenario):
    """
    Activate open fractures analysis and return results.
    """
    try:
        return extract_open_fractures_code(scenario)
    except Exception as e:
        print(f"Error in activate_open_fractures: {str(e)}")
        return "" 