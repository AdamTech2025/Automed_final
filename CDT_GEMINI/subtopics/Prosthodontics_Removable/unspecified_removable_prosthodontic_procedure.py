"""
Module for extracting unspecified removable prosthodontic procedure codes.
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
 
def create_unspecified_removable_prosthodontic_procedure_extractor(temperature=0.0):
    """
    Create a LangChain-based unspecified removable prosthodontic procedure code extractor.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro-exp-03-25", temperature=temperature)
    
    prompt_template = PromptTemplate(
        template=f"""
You are a highly experienced dental coding expert

### **Before Picking a Code, Ask:**
- Is the procedure truly **not described** by any existing CDT code?
- Have you reviewed all related prosthodontic, implant, and adjunctive codes?
- Can you provide a **detailed narrative** describing the procedure, materials, and clinical rationale?
- Is there supporting documentation (e.g., radiographs, lab invoice, photos)?
- Is this a one-time or temporary solution, or part of a larger treatment plan?

---

#### **Code: D5899**  
**Heading:** Unspecified removable prosthodontic procedure, by report  
**When to Use:**  
- Used only when a **removable prosthodontic service** doesn’t match any existing CDT code.  
- Common scenarios include **custom modifications**, **digital workflows**, or **novel techniques** not covered under standard codes.  
**What to Check:**  
- Confirm that no appropriate CDT code exists (D5110–D5876 range).  
- Prepare a detailed report: procedure description, materials used, treatment purpose, and patient benefit.  
- Include clinical photos, diagnostic evidence, and lab documentation if available.  
**Notes:**  
- **"By report" is mandatory** — claim submission must include a thorough narrative.  
- Use sparingly and only when no other code appropriately applies.  
- Often subject to **insurance review or denial** without sufficient justification.

---

### **Key Takeaways:**
- **Narrative is Essential**: Claims without detailed explanation are likely to be denied.
- **Use When No Other Code Fits**: This is a fallback for true exceptions, not a substitute for existing CDT codes.
- **Attach Documentation**: Support claims with photos, models, invoices, or clinical records.
- **Billing May Be Delayed**: Be prepared for payer follow-up or prior authorization requests.


Scenario:
"{{question}}"

{PROMPT}
""",
        input_variables=["question"]
    )
    
    return LLMChain(llm=llm, prompt=prompt_template)

def extract_unspecified_removable_prosthodontic_procedure_code(scenario, temperature=0.0):
    """
    Extract unspecified removable prosthodontic procedure code(s) for a given scenario.
    """
    try:
        chain = create_unspecified_removable_prosthodontic_procedure_extractor(temperature)
        result = invoke_chain(chain, {"question": scenario})
        print(f"Unspecified removable prosthodontic procedure code result: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in extract_unspecified_removable_prosthodontic_procedure_code: {str(e)}")
        return ""

def activate_unspecified_removable_prosthodontic_procedure(scenario):
    """
    Activate unspecified removable prosthodontic procedure analysis and return results.
    """
    try:
        return extract_unspecified_removable_prosthodontic_procedure_code(scenario)
    except Exception as e:
        print(f"Error in activate_unspecified_removable_prosthodontic_procedure: {str(e)}")
        return "" 