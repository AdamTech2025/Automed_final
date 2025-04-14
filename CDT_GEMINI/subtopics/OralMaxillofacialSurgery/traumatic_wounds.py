"""
Module for extracting traumatic wounds codes.
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
 
def create_traumatic_wounds_extractor(temperature=0.0):
    """
    Create a LangChain-based traumatic wounds code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert specializing in oral and maxillofacial trauma,

## **Traumatic Wounds and Suturing**

### **Before picking a code, ask:**
- What is the length of the wound requiring closure?
- Is this a simple or complicated suturing case?
- Are there multiple tissue layers involved in the wound?
- Are there neurovascular structures involved that require special attention?
- Is the wound recent (acute) or older (delayed closure)?
- What anatomical location is the traumatic wound (intraoral, facial, etc.)?
- Does the wound extend beyond the oral cavity into facial structures?
- Was the wound a result of trauma or is it an iatrogenic (surgical) wound?
- Are there complicating factors such as infection or foreign bodies?
- Will specialized closure techniques be required beyond simple interrupted sutures?

---

#### **Code: D7910** – *Suture of recent small wounds up to 5 cm*
**Use when:** Performing simple closure of recent traumatic wounds in or around the oral cavity that measure up to 5 cm in length.
**Check:** Verify that the injury was traumatic in nature (not a surgical incision) and required suturing as an emergency or unplanned procedure.
**Note:** This code is intended for relatively straightforward closures of recent traumatic wounds using standard suturing techniques. It typically involves single-layer closure with simple interrupted or continuous sutures. Documentation should include wound length, location, suture material used, and closure technique. Photographs are highly recommended for trauma cases to document the extent of the original injury.

#### **Code: D7911** – *Complicated suture - up to 5 cm*
**Use when:** Closing traumatic wounds up to 5 cm that involve complex tissue structures requiring layered closure, careful dissection, or specialized techniques.
**Check:** Documentation must clearly substantiate the complexity factors that distinguish this from simple suturing, such as involvement of deeper tissue layers, proximity to nerves or vessels, wounds with irregular edges, or those requiring tension-reduction techniques.
**Note:** The complexity that justifies this code over D7910 must be clearly documented. This may include debridement of necrotic tissue, management of specialized structures (salivary ducts, nerve branches), or requiring layered closure techniques. The procedure typically takes significantly longer than simple suturing due to the careful attention needed for optimal functional and aesthetic results. The operative notes should explicitly detail why standard closure techniques were insufficient for this particular wound.

#### **Code: D7912** – *Complicated suture - greater than 5 cm*
**Use when:** Performing complex wound closure for traumatic injuries exceeding 5 cm in length that involve multiple tissue layers, delicate anatomical structures, or challenging wound geography.
**Check:** The documentation must include precise wound measurements exceeding 5 cm, detailed description of the wound complexity, and specific techniques employed for closure that reflect the complicated nature of the repair.
**Note:** This code represents the highest level of traumatic wound management in the dental setting. These cases often involve extensive facial or intraoral lacerations with multiple components. The procedure typically requires significant time, specialized suture materials, and advanced closure techniques. Detailed documentation should include the total wound length (cumulative if multiple wounds), anatomical structures involved, layer-by-layer closure description, and any additional stabilization required. Post-operative care instructions and follow-up plans are particularly important for these complex cases.

---

### **Key Takeaways:**
- **Emergency Nature** - These codes are specifically for traumatic wounds requiring immediate or urgent attention, not planned surgical incisions.
- **Measurement Matters** - Accurate documentation of wound length (in centimeters) is critical for proper code selection, with 5 cm being the key threshold.
- **Complexity Factors** - Justification for "complicated" suture codes must include specific factors beyond wound length, such as depth, tissue types involved, or proximity to critical structures.
- **Photographic Documentation** - Pre-suturing photos significantly strengthen documentation and can help justify code selection, especially for complicated repairs.
- **Anatomical Considerations** - Different areas of the oral cavity and face present unique suturing challenges that may influence complexity determination.
- **Layer-by-Layer Description** - For complicated sutures, document each tissue layer closed and the specific suturing technique used for each.
- **Materials Matter** - Documentation should specify suture materials and sizes used, as these often reflect the complexity of the repair.
- **Timing Context** - Note when the injury occurred relative to the repair, as delayed closure may increase complexity.
- **Follow-up Planning** - Document the planned suture removal timing and any intermediate evaluations needed for complicated wounds.
- **Surgical vs. Traumatic** - These codes are not used for closing planned surgical incisions; they are exclusively for traumatic wounds.

Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_traumatic_wounds_code(scenario, temperature=0.0):
    """
    Extract traumatic wounds code(s) for a given scenario.
    """
    try:
        chain = create_traumatic_wounds_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Traumatic wounds code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_traumatic_wounds_code: {str(e)}")
        return ""

def activate_traumatic_wounds(scenario):
    """
    Activate traumatic wounds analysis and return results.
    """
    try:
        return extract_traumatic_wounds_code(scenario)
    except Exception as e:
        print(f"Error in activate_traumatic_wounds: {str(e)}")
        return "" 